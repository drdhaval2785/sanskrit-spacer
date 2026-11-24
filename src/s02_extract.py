import glob
import json
import re
from collections import Counter

import pyarrow.parquet as pq

from config import ALLOWED_REPOS, ALLOWED_KINDS
from src.segment import segment, clean

cat = pq.read_table("data/raw/pramana/catalogue.parquet",
                    columns=["path", "lang", "script", "words", "text_in_release", "source_repos"]).to_pylist()
sel = {}
for r in cat:
    repos = r["source_repos"]
    if (r["lang"] == "sa" and r["script"] == "Latn" and r["text_in_release"] and (r["words"] or 0) > 0
            and repos and all(x in ALLOWED_REPOS for x in repos)):
        sel[r["path"]] = "+".join(sorted(repos))
print("selected documents", len(sel))
assert 700 <= len(sel) <= 800, len(sel)

rows = []
for f in sorted(glob.glob("data/raw/pramana/passages/*.parquet")):
    pf = pq.ParquetFile(f)
    for b in pf.iter_batches(batch_size=50_000, columns=["path", "loc", "ord", "kind", "text"]):
        for r in b.to_pylist():
            if r["path"] in sel and r["text"] is not None and r["kind"] in ALLOWED_KINDS:
                rows.append((r["path"], r["ord"], r["loc"], r["kind"], r["text"]))
    print(f, len(rows), flush=True)
rows.sort(key=lambda x: (x[0], x[1]))

stats = Counter()
seen = set()
with open("data/interim/sentences_raw.jsonl", "w", encoding="utf-8") as out:
    for path, _, loc, kind, text in rows:
        stats["passages_read"] += 1
        k = 0
        for seg in segment(text):
            stats["segments_seen"] += 1
            sents, reason = clean(seg)
            if reason:
                stats["reject_" + reason] += 1
            for slp in sents:
                letters = slp.replace(" ", "")
                if letters in seen:
                    stats["reject_duplicate"] += 1
                    continue
                seen.add(letters)
                out.write(json.dumps({
                    "id": f"{path}@{loc}#{k}", "path": path, "group": re.sub(r"[*!~].*$", "", path),
                    "repo": sel[path], "kind": kind, "slp": slp, "n": len(letters)}, ensure_ascii=False) + "\n")
                k += 1
                stats["sentences_written"] += 1
stats["documents"] = len(sel)
json.dump(dict(stats), open("data/interim/extract.stats.json", "w"), indent=1)
print(dict(stats))
rej = stats["reject_non_iast"] + stats["reject_hiatus"]
assert stats["sentences_written"] >= 500_000, stats["sentences_written"]
assert rej < 0.15 * stats["segments_seen"], (rej, stats["segments_seen"])
print("GATE 2 OK")
