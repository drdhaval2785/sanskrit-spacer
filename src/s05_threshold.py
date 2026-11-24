"""Pick the decision threshold for a run stopped before the end of training: the same validation-set search
that s05_train does after its last step, written to <run>/threshold.json.

    python -m src.s05_threshold --run runs/full_e10_L_s1 [--data data/splits]
"""
import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import argparse
import json

import torch

from src.model import load_model
from src.s05_train import load, prf, val_probs


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--data", default="data/splits", help="directory with the val.jsonl the run was trained against")
    a = ap.parse_args()
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = load_model(a.run, device)
    ck = torch.load(f"{a.run}/best.pt", map_location="cpu")
    P, G, _ = val_probs(model, load(f"{a.data}/val.jsonl"), device)
    ts = [round(0.10 + 0.05 * i, 2) for i in range(17)]
    scored = [(prf(P, G, t)[2], t) for t in ts]
    top = max(s for s, _ in scored)
    bt = min((t for s, t in scored if s == top), key=lambda t: abs(t - 0.5))
    json.dump({"threshold": bt, "val_f1_at_threshold": top, "val_f1_at_0.5": prf(P, G, 0.5)[2],
               "best_step": ck["step"], "stopped_early_by_hand": True}, open(f"{a.run}/threshold.json", "w"), indent=1)
    print("threshold", bt, "f1", top, "best_step", ck["step"])


if __name__ == "__main__":
    main()
