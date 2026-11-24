import hashlib
import json
from collections import defaultdict

from config import SEED, TEST_BYTES, VAL_BYTES, GROUP_CAP_BYTES, TIERS_MB
from src.translit import deva_bytes


def h(x):
    return hashlib.sha1(f"{SEED}:{x}".encode("utf-8")).hexdigest()


by_group = defaultdict(list)
for line in open("data/interim/sentences.jsonl", encoding="utf-8"):
    s = json.loads(line)
    s["b"] = deva_bytes(s["slp"])
    by_group[s["group"]].append(s)

queue = sorted(by_group, key=h)
pos = 0


def take(limit):
    global pos
    out, total = [], 0
    while total < limit and pos < len(queue):
        g = queue[pos]
        pos += 1
        gb = 0
        for s in sorted(by_group[g], key=lambda x: h(x["id"])):
            if gb >= GROUP_CAP_BYTES:
                break
            out.append(s)
            gb += s["b"]
        total += gb
    return out


test = take(TEST_BYTES)
val = take(VAL_BYTES)
pool = sorted((s for g in queue[pos:] for s in by_group[g]), key=lambda x: h(x["id"]))

tiers = {}
for T in TIERS_MB:
    tot, n = 0, 0
    for s in pool:
        tot += s["b"]
        n += 1
        if tot >= T * 1_000_000:
            break
    tiers[T] = pool[:n]

files = {"test": test, "val": val}
for T in TIERS_MB:
    files[f"train_{T}mb"] = tiers[T]
files["train_full"] = pool
stats = {}
for name, data in files.items():
    with open(f"data/splits/{name}.jsonl", "w", encoding="utf-8") as f:
        for s in data:
            f.write(json.dumps(s, ensure_ascii=False) + "\n")
    letters = sum(s["n"] for s in data)
    spaces = sum(s["slp"].count(" ") for s in data)
    stats[name] = {"sentences": len(data), "letters": letters,
                   "words": sum(len(s["slp"].split(" ")) for s in data),
                   "deva_bytes": sum(s["b"] for s in data),
                   "groups": len({s["group"] for s in data}),
                   "spaces": spaces,
                   "base_rate": spaces / (letters - len(data))}
json.dump(stats, open("data/splits/split.stats.json", "w"), indent=1)
print(json.dumps(stats, indent=1))

# ---- GATE 4 ----
g_test, g_val = {s["group"] for s in test}, {s["group"] for s in val}
g_pool = {s["group"] for s in pool}
assert not (g_test & g_val) and not (g_test & g_pool) and not (g_val & g_pool), "group leak"
let = lambda d: {s["slp"].replace(" ", "") for s in d}
lt, lv, l20 = let(test), let(val), let(tiers[20])
assert not (lt & lv) and not (lt & l20) and not (lv & l20), "letters leak"
assert sum(s["b"] for s in pool) >= 20_500_000, sum(s["b"] for s in pool)
assert len(g_test) >= 25 and len(g_val) >= 25, (len(g_test), len(g_val))
ids = {T: {s["id"] for s in tiers[T]} for T in TIERS_MB}
assert ids[1] <= ids[5] <= ids[10] <= ids[20]
print("GATE 4 OK")
