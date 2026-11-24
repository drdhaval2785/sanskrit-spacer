"""Split the validated Wikisource sentences into test / val / train by work. Test and val take whole works that
are small and (almost) absent from the old training pool (data/splits/train_full.jsonl); any sentence of theirs
that is in the old pool is removed, so the old models can be scored on the same test set without having seen it."""
import hashlib
import json
from collections import defaultdict

from config import SEED, WSV_TEST_BYTES, WSV_VAL_BYTES, WSV_EVAL_GROUP_MAX, WSV_MAX_OLD_OVERLAP
from src.translit import deva_bytes


def h(x):
    return hashlib.sha1(f"{SEED}:{x}".encode("utf-8")).hexdigest()


old = set()
for line in open("data/splits/train_full.jsonl", encoding="utf-8"):
    old.add(json.loads(line)["slp"].replace(" ", ""))

by_group = defaultdict(list)
for line in open("data/wsv/interim/sentences.jsonl", encoding="utf-8"):
    s = json.loads(line)
    s["b"] = deva_bytes(s["slp"])
    s["in_old"] = s["slp"].replace(" ", "") in old
    by_group[s["group"]].append(s)

info = {}
for g, ss in by_group.items():
    info[g] = {"sentences": len(ss), "bytes": sum(s["b"] for s in ss),
               "old_overlap": sum(s["in_old"] for s in ss) / len(ss)}
eligible = [g for g in sorted(by_group, key=h)
            if info[g]["bytes"] <= WSV_EVAL_GROUP_MAX and info[g]["old_overlap"] <= WSV_MAX_OLD_OVERLAP]

pos = 0


def take(limit):
    global pos
    out, gs, total = [], [], 0
    while total < limit and pos < len(eligible):
        g = eligible[pos]
        pos += 1
        ss = [s for s in sorted(by_group[g], key=lambda x: h(x["id"])) if not s["in_old"]]
        out += ss
        gs.append(g)
        total += sum(s["b"] for s in ss)
    return out, gs


test, test_groups = take(WSV_TEST_BYTES)
val, val_groups = take(WSV_VAL_BYTES)
eval_groups = set(test_groups) | set(val_groups)
train = sorted((s for g in by_group if g not in eval_groups for s in by_group[g]), key=lambda x: h(x["id"]))

stats = {}
for name, data in {"test": test, "val": val, "train_full": train}.items():
    with open(f"data/wsv/splits/{name}.jsonl", "w", encoding="utf-8") as f:
        for s in data:
            f.write(json.dumps({k: v for k, v in s.items() if k != "in_old"}, ensure_ascii=False) + "\n")
    letters = sum(s["n"] for s in data)
    spaces = sum(s["slp"].count(" ") for s in data)
    stats[name] = {"sentences": len(data), "letters": letters, "words": sum(len(s["slp"].split(" ")) for s in data),
                   "deva_bytes": sum(s["b"] for s in data), "groups": len({s["group"] for s in data}),
                   "spaces": spaces, "base_rate": spaces / max(1, letters - len(data)),
                   "in_old_training_pool": sum(s["in_old"] for s in data)}
stats["eligible_groups"] = len(eligible)
stats["test_groups"] = {g: info[g] for g in test_groups}
stats["val_groups"] = {g: info[g] for g in val_groups}
json.dump(stats, open("data/wsv/splits/split.stats.json", "w"), indent=1, ensure_ascii=False)
for k in ("test", "val", "train_full"):
    print(k, json.dumps(stats[k]))
print("eligible works:", len(eligible), "of", len(by_group))
for k in ("test_groups", "val_groups"):
    print(k)
    for g, x in stats[k].items():
        print(f"   {x['bytes']/1e6:5.2f} MB  overlap {x['old_overlap']:.3f}  {g}")

# ---- checks ----
gt, gv, gr = {s["group"] for s in test}, {s["group"] for s in val}, {s["group"] for s in train}
assert not (gt & gv) and not (gt & gr) and not (gv & gr), "a work is in two splits"
L = lambda d: {s["slp"].replace(" ", "") for s in d}
lt, lv, lr = L(test), L(val), L(train)
assert not (lt & lv) and not (lt & lr) and not (lv & lr), "a sentence is in two splits"
assert not ((lt | lv) & old), "a val/test sentence is in the old training pool"
assert stats["test"]["groups"] >= 5 and stats["val"]["groups"] >= 5, "too few works in val/test"
print("SPLIT CHECKS OK")
