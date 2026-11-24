"""Compare models on the clean test set (validated Wikisource pages) and on the original Pramāṇa test set."""
import json
import os

import torch

RUNS = [("full_e10_s1", "Pramāṇa pool (163 MB), 10 passes"),
        ("full_e10_L_s1", "Pramāṇa pool (163 MB), stopped by hand after 4.4 of 10 passes"),
        ("wsv_base_s1", "Validated Wikisource (30 MB), 10 passes"),
        ("wsv_L_s1", "Validated Wikisource (30 MB), 10 passes")]
pc = lambda x: f"{100 * x:.2f}%"
split = json.load(open("data/wsv/splits/split.stats.json"))
L = ["# Clean-test comparison\n",
     f"The clean test set is {split['test']['sentences']:,} sentences ({split['test']['deva_bytes'] / 1e6:.2f} MB of "
     f"Devanagari) from {split['test']['groups']} works whose scan pages were validated by a second proofreader on "
     "Sanskrit Wikisource. None of its sentences occurs in the Pramāṇa training pool, so all models are scored on text "
     "they have not seen. The original test set is the noisier one from the Pramāṇa pool.\n",
     "| Model | Size | Trained on | Clean test: P | R | Boundary F1 | Word F1 | Sentence acc. | Original test: Boundary F1 |",
     "|---|---|---|---|---|---|---|---|---|"]
for run, data in RUNS:
    d = f"runs/{run}"
    if not os.path.exists(f"{d}/metrics_test_wsv.json"):
        continue
    w = json.load(open(f"{d}/metrics_test_wsv.json"))["test"]
    o = json.load(open(f"{d}/metrics_test.json"))["test"]["boundary_f1"] if os.path.exists(f"{d}/metrics_test.json") else None
    ck = torch.load(f"{d}/best.pt", map_location="cpu")
    c = ck.get("config", {})
    size = f"{c.get('N_LAYERS', 4)}×{c.get('D_MODEL', 256)}, {sum(v.numel() for v in ck['model'].values()) / 1e6:.1f} M"
    L.append(f"| `{run}` | {size} | {data} | {pc(w['boundary_p'])} | {pc(w['boundary_r'])} | **{pc(w['boundary_f1'])}** | "
             f"{pc(w['word_f1'])} | {pc(w['sentence_acc'])} | {pc(o) if o is not None else '–'} |")
L.append("\nTest works: " + ", ".join(split["test_groups"]) + ".\n")
os.makedirs("reports", exist_ok=True)
open("reports/wsv_comparison.md", "w", encoding="utf-8").write("\n".join(L) + "\n")
print("\n".join(L))
