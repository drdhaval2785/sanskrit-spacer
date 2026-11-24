"""Per-book audit of the validated Wikisource sentences: the same checks as s03_audit (romanised-style spacing,
implausible space rates, tiny books), plus the optional halanta-convention filter WSV_MIN_SEP_RATE."""
import csv
import json
import re
from collections import defaultdict, Counter

from config import (CONSONANTS, VOWELS, MAX_ANALYTIC_RATE, MIN_SPACE_RATE, MAX_SPACE_RATE, MIN_DOC_LETTERS,
                    WSV_MIN_SEP_RATE)

CV = re.compile("[%s] [%s]" % (CONSONANTS, VOWELS))
CC = re.compile("[%s] [%s]" % (CONSONANTS, CONSONANTS))
IN, OUT = "data/wsv/interim/sentences_raw.jsonl", "data/wsv/interim/sentences.jsonl"

docs = defaultdict(lambda: {"group": "", "sentences": 0, "letters": 0, "spaces": 0, "cv": 0, "cc": 0})
for line in open(IN, encoding="utf-8"):
    s = json.loads(line)
    d = docs[s["path"]]
    d["group"] = s["group"]
    d["sentences"] += 1
    d["letters"] += s["n"]
    d["spaces"] += s["slp"].count(" ")
    d["cv"] += len(CV.findall(s["slp"]))
    d["cc"] += len(CC.findall(s["slp"]))

decision = {}
for p, d in docs.items():
    d["space_rate"] = d["spaces"] / d["letters"]
    d["analytic_rate"] = d["cv"] / d["spaces"] if d["spaces"] else 0.0
    d["sep_rate"] = d["cc"] / d["spaces"] if d["spaces"] else 0.0
    if d["letters"] < MIN_DOC_LETTERS:
        dec = "tiny"
    elif d["analytic_rate"] > MAX_ANALYTIC_RATE:
        dec = "analytic"
    elif d["space_rate"] < MIN_SPACE_RATE:
        dec = "underspaced"
    elif d["space_rate"] > MAX_SPACE_RATE:
        dec = "overspaced"
    elif WSV_MIN_SEP_RATE is not None and d["sep_rate"] < WSV_MIN_SEP_RATE:
        dec = "joins_halanta"
    else:
        dec = "keep"
    decision[p] = dec

cols = ["path", "group", "sentences", "letters", "spaces", "cv", "cc", "space_rate", "analytic_rate", "sep_rate", "decision"]
with open("data/wsv/interim/doc_audit.tsv", "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f, delimiter="\t")
    w.writerow(cols)
    for p in sorted(docs):
        d = docs[p]
        w.writerow([p, d["group"], d["sentences"], d["letters"], d["spaces"], d["cv"], d["cc"],
                    round(d["space_rate"], 4), round(d["analytic_rate"], 4), round(d["sep_rate"], 4), decision[p]])

kept, groups = 0, set()
with open(OUT, "w", encoding="utf-8") as out:
    for line in open(IN, encoding="utf-8"):
        s = json.loads(line)
        if decision[s["path"]] == "keep":
            out.write(line)
            kept += s["n"]
            groups.add(s["group"])
stats = {"docs": dict(Counter(decision.values())),
         "letters": {k: sum(d["letters"] for p, d in docs.items() if decision[p] == k) for k in set(decision.values())},
         "kept_letters": kept, "kept_groups": len(groups), "kept_deva_bytes_estimate": round(2.9 * kept)}
json.dump(stats, open("data/wsv/interim/audit.stats.json", "w"), indent=1)
print(json.dumps(stats, indent=1, ensure_ascii=False))
for p, d in sorted(docs.items(), key=lambda kv: -kv[1]["letters"]):
    if decision[p] != "keep" and d["letters"] >= MIN_DOC_LETTERS:
        print(f"  dropped ({decision[p]}): {p[:60]}  letters={d['letters']} analytic={d['analytic_rate']:.3f} space={d['space_rate']:.3f}")
