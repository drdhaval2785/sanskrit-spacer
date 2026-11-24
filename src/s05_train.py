import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import argparse
import json
import math
import random
import time

import torch
import torch.nn.functional as F

from config import *
from src.model import Spacer, make_batch


def load(path):
    return [json.loads(l)["slp"] for l in open(path, encoding="utf-8")]


def batches(data, rng, bs):
    idx = list(range(len(data)))
    rng.shuffle(idx)
    out = []
    blk = bs * 100
    for s in range(0, len(idx), blk):
        b = sorted(idx[s:s + blk], key=lambda i: len(data[i]))
        out += [b[j:j + bs] for j in range(0, len(b), bs)]
    rng.shuffle(out)
    return out


def lr_at(s, max_steps):
    if s <= WARMUP_STEPS:
        return PEAK_LR * s / WARMUP_STEPS
    return MIN_LR + 0.5 * (PEAK_LR - MIN_LR) * (1 + math.cos(math.pi * (s - WARMUP_STEPS) / (max_steps - WARMUP_STEPS)))


@torch.no_grad()
def val_probs(model, val, device):
    """Return probabilities and gold labels over all valid positions, and the mean loss."""
    model.eval()
    order = sorted(range(len(val)), key=lambda i: len(val[i]))
    probs, golds = {}, {}
    tot, cnt = 0.0, 0
    for s in range(0, len(order), 256):
        idx = order[s:s + 256]
        ids, lab, mask = make_batch([val[i] for i in idx], device)
        lg = model(ids)
        tot += F.binary_cross_entropy_with_logits(lg[mask], lab[mask], reduction="sum").item()
        cnt += mask.sum().item()
        p = torch.sigmoid(lg).cpu()
        m = mask.cpu()
        l = lab.cpu()
        for j, i in enumerate(idx):
            probs[i] = p[j][m[j]]
            golds[i] = l[j][m[j]]
    model.train()
    P = torch.cat([probs[i] for i in range(len(val))])
    G = torch.cat([golds[i] for i in range(len(val))])
    return P, G, tot / cnt


def prf(P, G, t):
    pred = P >= t
    gold = G > 0.5
    tp = (pred & gold).sum().item()
    fp = (pred & ~gold).sum().item()
    fn = (~pred & gold).sum().item()
    p = tp / (tp + fp) if tp + fp else 0.0
    r = tp / (tp + fn) if tp + fn else 0.0
    return p, r, (2 * p * r / (p + r) if p + r else 0.0)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--tier", required=True, help='integer MB, or "full" for the whole training pool')
    ap.add_argument("--seed", type=int, default=1)
    ap.add_argument("--device", default=None)
    # Epoch mode. Without --epochs the run is the original fixed budget of MAX_STEPS steps.
    ap.add_argument("--epochs", type=float, default=None, help="passes over the training file; sets the step budget")
    ap.add_argument("--batch", type=int, default=BATCH_SIZE, help="effective batch size (sentences per update)")
    ap.add_argument("--accum", type=int, default=1,
                    help="split each batch into this many micro-batches to save memory; the update is unchanged")
    ap.add_argument("--eval-every", type=int, default=EVAL_EVERY)
    ap.add_argument("--patience", type=int, default=PATIENCE_EVALS, help="evaluations without improvement before stopping")
    ap.add_argument("--name", default=None, help="run directory name under runs/ (default: <tier>_s<seed>)")
    ap.add_argument("--data", default="data/splits", help="directory with train_<tier>.jsonl and val.jsonl")
    # Model size. Defaults are the config.py values used by all the comparable tiers.
    ap.add_argument("--layers", type=int, default=N_LAYERS)
    ap.add_argument("--d-model", type=int, default=D_MODEL)
    ap.add_argument("--heads", type=int, default=N_HEAD)
    ap.add_argument("--d-ff", type=int, default=D_FF)
    a = ap.parse_args()
    device = a.device or ("mps" if torch.backends.mps.is_available() else "cpu")
    tier_name = "full" if a.tier == "full" else f"{a.tier}mb"
    run = f"runs/{a.name or f'{tier_name}_s{a.seed}'}"
    os.makedirs(run, exist_ok=True)
    random.seed(SEED + a.seed)
    torch.manual_seed(SEED + a.seed)
    rng = random.Random(SEED + a.seed)
    train = load(f"{a.data}/train_{tier_name}.jsonl")
    val = load(f"{a.data}/val.jsonl")
    steps_per_epoch = math.ceil(len(train) / a.batch)
    max_steps = round(a.epochs * steps_per_epoch) if a.epochs else MAX_STEPS
    print(f"device {device} train {len(train)} val {len(val)} batch {a.batch} "
          f"accum {a.accum} steps/epoch {steps_per_epoch} max_steps {max_steps} eval_every {a.eval_every} patience {a.patience}", flush=True)

    model = Spacer(d_model=a.d_model, n_head=a.heads, n_layers=a.layers, d_ff=a.d_ff).to(device)
    print(f"model layers {a.layers} d_model {a.d_model} heads {a.heads} d_ff {a.d_ff} "
          f"params {sum(p.numel() for p in model.parameters()):,}", flush=True)
    opt = torch.optim.AdamW(model.parameters(), lr=PEAK_LR, weight_decay=WEIGHT_DECAY)
    log = open(f"{run}/log.jsonl", "w")
    step, best, bad, run_loss, run_n = 0, -1.0, 0, 0.0, 0
    t0 = time.time()
    model.train()
    done = False
    while not done:
        for b in batches(train, rng, a.batch):
            step += 1
            for g in opt.param_groups:
                g["lr"] = lr_at(step, max_steps)
            opt.zero_grad()
            if a.accum == 1:
                ids, lab, mask = make_batch([train[i] for i in b], device)
                loss = F.binary_cross_entropy_with_logits(model(ids)[mask], lab[mask])
                loss.backward()
                loss_val = loss.item()
            else:
                # Same mean-over-positions loss as a single batch, computed in micro-batches.
                n = math.ceil(len(b) / a.accum)
                parts = [make_batch([train[i] for i in b[k:k + n]], device) for k in range(0, len(b), n)]
                total = sum(m.sum().item() for _, _, m in parts)
                loss_val = 0.0
                for ids, lab, mask in parts:
                    loss = F.binary_cross_entropy_with_logits(model(ids)[mask], lab[mask], reduction="sum") / total
                    loss.backward()
                    loss_val += loss.item()
            torch.nn.utils.clip_grad_norm_(model.parameters(), GRAD_CLIP)
            opt.step()
            run_loss += loss_val
            run_n += 1
            if step % a.eval_every == 0:
                P, G, vl = val_probs(model, val, device)
                p, r, f1 = prf(P, G, 0.5)
                rec = {"step": step, "epoch": round(step / steps_per_epoch, 3), "train_loss": run_loss / run_n,
                       "val_loss": vl, "val_p": p, "val_r": r, "val_f1": f1, "lr": lr_at(step, max_steps),
                       "elapsed_s": time.time() - t0}
                log.write(json.dumps(rec) + "\n")
                log.flush()
                print(rec, flush=True)
                run_loss, run_n = 0.0, 0
                if f1 > best:
                    best, bad = f1, 0
                    torch.save({"model": model.state_dict(), "step": step, "val_f1": f1,
                                "config": {**model.cfg, "batch": a.batch, "accum": a.accum, "epochs": a.epochs, "max_steps": max_steps, "data": a.data},
                                "alphabet": ALPHABET}, f"{run}/best.pt")
                else:
                    bad += 1
                if bad >= a.patience:
                    print(f"early stop at step {step}: no improvement in {a.patience} evaluations", flush=True)
                    done = True
                    break
            if step >= max_steps:
                done = True
                break
    log.close()

    ck = torch.load(f"{run}/best.pt", map_location="cpu")
    model.load_state_dict(ck["model"])
    P, G, _ = val_probs(model, val, device)
    ts = [round(0.10 + 0.05 * i, 2) for i in range(17)]
    scored = [(prf(P, G, t)[2], t) for t in ts]
    top = max(s for s, _ in scored)
    bt = min((t for s, t in scored if s == top), key=lambda t: abs(t - 0.5))
    json.dump({"threshold": bt, "val_f1_at_threshold": top, "val_f1_at_0.5": prf(P, G, 0.5)[2],
               "best_step": ck["step"]}, open(f"{run}/threshold.json", "w"), indent=1)
    print("threshold", bt, "f1", top, "best_step", ck["step"])


if __name__ == "__main__":
    main()
