import csv
import json
import re
from collections import defaultdict, Counter

from config import (CONSONANTS, VOWELS, MAX_ANALYTIC_RATE, MIN_SPACE_RATE, MAX_SPACE_RATE, MIN_DOC_LETTERS)

CV = re.compile("[%s] [%s]" % (CONSONANTS, VOWELS))
docs = defaultdict(lambda: {"group": "", "repo": "", "sentences": 0, "letters": 0, "spaces": 0, "cv": 0})
for line in open("data/interim/sentences_raw.jsonl", encoding="utf-8"):
    s = json.loads(line)
    d = docs[s["path"]]
    d["group"], d["repo"] = s["group"], s["repo"]
    d["sentences"] += 1
    d["letters"] += s["n"]
    d["spaces"] += s["slp"].count(" ")
    d["cv"] += len(CV.findall(s["slp"]))

decision = {}
for p, d in docs.items():
    d["space_rate"] = d["spaces"] / d["letters"]
    d["analytic_rate"] = d["cv"] / d["spaces"] if d["spaces"] else 0.0
    if d["letters"] < MIN_DOC_LETTERS:
        dec = "tiny"
    elif d["analytic_rate"] > MAX_ANALYTIC_RATE:
        dec = "analytic"
    elif d["space_rate"] < MIN_SPACE_RATE:
        dec = "underspaced"
    elif d["space_rate"] > MAX_SPACE_RATE:
        dec = "overspaced"
    else:
        dec = "keep"
    decision[p] = dec

cols = ["path", "group", "repo", "sentences", "letters", "spaces", "cv", "space_rate", "analytic_rate", "decision"]
with open("data/interim/doc_audit.tsv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(cols)
    for p in sorted(docs):
        d = docs[p]
        w.writerow([p, d["group"], d["repo"], d["sentences"], d["letters"], d["spaces"], d["cv"],
                    round(d["space_rate"], 4), round(d["analytic_rate"], 4), decision[p]])

kept_letters = 0
groups = set()
stats = {"docs": Counter(), "letters": Counter(), "by_repo_kept_letters": Counter()}
with open("data/interim/sentences.jsonl", "w", encoding="utf-8") as out:
    for line in open("data/interim/sentences_raw.jsonl", encoding="utf-8"):
        s = json.loads(line)
        if decision[s["path"]] == "keep":
            out.write(line)
            kept_letters += s["n"]
            groups.add(s["group"])
            stats["by_repo_kept_letters"][s["repo"]] += s["n"]
for p, d in docs.items():
    stats["docs"][decision[p]] += 1
    stats["letters"][decision[p]] += d["letters"]
stats = {k: dict(v) for k, v in stats.items()}
stats["kept_letters"] = kept_letters
stats["kept_groups"] = len(groups)
stats["kept_deva_bytes_estimate"] = round(2.7 * kept_letters)
json.dump(stats, open("data/interim/audit.stats.json", "w"), indent=1)
print(json.dumps(stats, indent=1))
assert stats["kept_deva_bytes_estimate"] >= 60_000_000, stats["kept_deva_bytes_estimate"]
assert len(groups) >= 300, len(groups)
print("GATE 3 OK")
