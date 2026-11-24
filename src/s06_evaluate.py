import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import argparse
import json
from collections import defaultdict

import torch

from src.model import load_model, predict_probs
from src.metrics import encode, positions, Meter


def spaced(letters, pos):
    return "".join(c + (" " if i in pos else "") for i, c in enumerate(letters)).rstrip(" ")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--data", default="data/splits", help="directory with test.jsonl")
    ap.add_argument("--tag", default="", help="output name suffix, e.g. wsv -> metrics_test_wsv.json")
    a = ap.parse_args()
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = load_model(a.run, device)
    th = json.load(open(f"{a.run}/threshold.json"))
    data = [json.loads(l) for l in open(f"{a.data}/test.jsonl", encoding="utf-8")]
    suffix = f"_{a.tag}" if a.tag else ""
    letters = [encode(d["slp"])[0] for d in data]
    probs = predict_probs(model, letters, device)
    tot, by_repo, by_kind = Meter(), defaultdict(Meter), defaultdict(Meter)
    with open(f"{a.run}/predictions_test{suffix}.jsonl", "w", encoding="utf-8") as out:
        for d, L, p in zip(data, letters, probs):
            pred = {i for i in range(len(L) - 1) if p[i] >= th["threshold"]}
            gold = positions(d["slp"])
            for m in (tot, by_repo[d["repo"]], by_kind[d["kind"]]):
                m.add(gold, pred, len(L))
            out.write(json.dumps({"id": d["id"], "gold": d["slp"], "pred": spaced(L, pred)}, ensure_ascii=False) + "\n")
    res = {"run": os.path.basename(a.run), "threshold": th["threshold"], "best_step": th["best_step"],
           "test": tot.result(),
           "by_repo": {k: v.result() for k, v in by_repo.items()},
           "by_kind": {k: v.result() for k, v in by_kind.items()}}
    res["test_data"] = a.data
    json.dump(res, open(f"{a.run}/metrics_test{suffix}.json", "w"), indent=1)
    print(a.run, a.data, {k: round(v, 4) for k, v in res["test"].items() if isinstance(v, float)})


if __name__ == "__main__":
    main()
