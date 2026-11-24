import hashlib
import json
import os

import torch

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from config import SEED, TIERS_MB, HF_REVISION
from src.translit import slp1_to_deva

pc = lambda x: f"{100 * x:.2f}%"
h = lambda x: hashlib.sha1(f"{SEED}:{x}".encode("utf-8")).hexdigest()
split = json.load(open("data/splits/split.stats.json"))
ext = json.load(open("data/interim/extract.stats.json"))
aud = json.load(open("data/interim/audit.stats.json"))
TIERS = list(TIERS_MB) + ["full"]
rdir = lambda T: "full_s1" if T == "full" else f"{T}mb_s1"
sname = lambda T: "train_full" if T == "full" else f"train_{T}mb"
label = lambda T: f"Full ({split['train_full']['deva_bytes'] / 1e6:.0f} MB)" if T == "full" else f"{T} MB"
runs = {T: json.load(open(f"runs/{rdir(T)}/metrics_test.json")) for T in TIERS}

L = []
L.append("# Sanskrit spacer: results\n")
L.append("A small character-level Transformer (about 3.2 M parameters) was trained to decide, for every gap between "
         "two letters of unspaced Sanskrit, whether a space belongs there. The same model and hyperparameters were "
         "trained on 1, 5, 10 and 20 MB of text and on the full cleaned training pool (all 20,000 steps, identical settings) and scored on one fixed test set. \"MB\" means 1,000,000 bytes of the "
         "spaced sentences written in Devanagari (UTF-8, one sentence per line).\n")
L.append("## Dataset\n")
L.append("| split | sentences | letters | words | Devanagari MB | groups | base rate |\n|---|---|---|---|---|---|---|")
for k, v in split.items():
    L.append(f"| {k} | {v['sentences']:,} | {v['letters']:,} | {v['words']:,} | {v['deva_bytes'] / 1e6:.2f} | "
             f"{v['groups']} | {pc(v['base_rate'])} |")
L.append("\n## Results on the test set\n")
L.append("| Train size | Sentences | Best step | Threshold | Boundary P | Boundary R | Boundary F1 | Word F1 | Sentence acc. |\n"
         "|---|---|---|---|---|---|---|---|---|")
for T in TIERS:
    r, t = runs[T], runs[T]["test"]
    L.append(f"| {label(T)} | {split[sname(T)]['sentences']:,} | {r['best_step']} | {r['threshold']} | "
             f"{pc(t['boundary_p'])} | {pc(t['boundary_r'])} | {pc(t['boundary_f1'])} | {pc(t['word_f1'])} | "
             f"{pc(t['sentence_acc'])} |")
EXTRA = [("full_e10_s1", "Full, 10 passes, base model (4 layers, 256 wide)"),
         ("full_e10_L_s1", "Full, 10 passes, larger model (6 layers, 384 wide)")]
extra = [(d, lab) for d, lab in EXTRA if os.path.exists(f"runs/{d}/metrics_test.json")]
if extra:
    L.append("\n## Multi-pass runs on the full data\n")
    L.append("Same data as the full-data row above, but an effective batch of 256 and a budget of up to 10 passes with early "
             "stopping (patience 12 evaluations of 1,000 updates). Not part of the learning curve: the training budget "
             "differs from the comparable tiers.\n")
    L.append("| Run | Params | Passes done | Best step | Threshold | Boundary P | Boundary R | Boundary F1 | Word F1 | Sentence acc. |\n"
             "|---|---|---|---|---|---|---|---|---|---|")
    for d, lab in extra:
        r = json.load(open(f"runs/{d}/metrics_test.json"))
        t = r["test"]
        lg = [json.loads(l) for l in open(f"runs/{d}/log.jsonl", encoding="utf-8")]
        c = torch.load(f"runs/{d}/best.pt", map_location="cpu")
        params = sum(v.numel() for v in c["model"].values())
        L.append(f"| {lab} | {params / 1e6:.1f} M | {lg[-1]['epoch']:.2f} | {r['best_step']} | {r['threshold']} | "
                 f"{pc(t['boundary_p'])} | {pc(t['boundary_r'])} | {pc(t['boundary_f1'])} | {pc(t['word_f1'])} | "
                 f"{pc(t['sentence_acc'])} |")
for title, key in (("source repository", "by_repo"), ("passage kind", "by_kind")):
    L.append(f"\n## Full-data run by {title}\n")
    L.append("| | Sentences | Boundary P | Boundary R | Boundary F1 | Word F1 |\n|---|---|---|---|---|---|")
    for k, t in runs["full"][key].items():
        L.append(f"| {k} | {t['sentences']:,} | {pc(t['boundary_p'])} | {pc(t['boundary_r'])} | "
                 f"{pc(t['boundary_f1'])} | {pc(t['word_f1'])} |")
L.append("\n## Error examples (full-data run)\n")
errs = [json.loads(l) for l in open("runs/full_s1/predictions_test.jsonl", encoding="utf-8")]
errs = sorted((e for e in errs if e["pred"] != e["gold"]), key=lambda e: h(e["id"]))[:20]
for e in errs:
    L.append(f"- gold: {slp1_to_deva(e['gold'])}  \n  pred: {slp1_to_deva(e['pred'])}")
L.append("\n## Data provenance\n")
L.append(f"Pramāṇa open data release (Hugging Face `srajma/pramana`, revision `{HF_REVISION}`, "
         "https://doi.org/10.5281/zenodo.24408373). Source repositories used: Sanskrit Wikisource (CC BY-SA 4.0), "
         "SARIT (CC BY-SA 3.0), Ambuda (CC0). Wikisource and SARIT texts are CC BY-SA: any redistributed derivative "
         "of the dataset must carry the same licence and credit the sources.\n")
L.append("## Pipeline counts\n")
L.append("| stage | count |\n|---|---|")
for k, v in ext.items():
    L.append(f"| extract: {k} | {v:,} |")
for k in ("kept_letters", "kept_groups", "kept_deva_bytes_estimate"):
    L.append(f"| audit: {k} | {aud[k]:,} |")
for k, v in aud["docs"].items():
    L.append(f"| audit: documents {k} | {v:,} |")
open("reports/results.md", "w", encoding="utf-8").write("\n".join(L) + "\n")

fig, ax = plt.subplots(figsize=(6, 4))
xs = [split[sname(T)]["deva_bytes"] / 1e6 for T in TIERS]
ax.plot(xs, [100 * runs[T]["test"]["boundary_f1"] for T in TIERS], "o-", label="Boundary F1")
ax.plot(xs, [100 * runs[T]["test"]["word_f1"] for T in TIERS], "s-", label="Word F1")
ax.set_xscale("log")
ax.set_xticks(xs)
ax.set_xticklabels([f"{x:.0f}" for x in xs])
ax.minorticks_off()
ax.set_xlabel("Training size (MB, Devanagari UTF-8)")
ax.set_ylabel("Test score (%)")
ax.legend()
ax.grid(alpha=0.3)
fig.tight_layout()
fig.savefig("reports/learning_curve.png", dpi=150)
print("report written")
