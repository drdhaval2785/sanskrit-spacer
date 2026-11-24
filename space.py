import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import argparse
import json
import re

import torch

from config import ALPHABET, MAX_LEN
from src.model import load_model, predict_probs
from src.translit import deva_to_slp1, slp1_to_deva

_CH = r"[ऀ-ॏ॑-ॣ॰-ॿ]"  # Sanskrit-run char: excludes ॐ । ॥ and digits U+0966-096F
_RUN = re.compile(_CH + "+")
_ALPHA = set(ALPHABET)
# Printing convention: dandas and numbers are set off by spaces ("... युयुत्सवः ॥ १ ॥ मामकाः ...").
_PUNCT_TOKENS = re.compile(r"[।॥]+|[०-९0-9]+|[^।॥०-९0-9]+")


def space_punctuation(s):
    """Put exactly one space on each side of every run of dandas or digits, except where whitespace is
    already there and at the very start or end of the string. Only spaces are added."""
    toks = _PUNCT_TOKENS.findall(s)
    out = []
    for k, t in enumerate(toks):
        if k and (t[0] in "।॥०१२३४५६७८९0123456789" or toks[k - 1][-1] in "।॥०१२३४५६७८९0123456789") \
                and not t[0].isspace() and not toks[k - 1][-1].isspace():
            out.append(" ")
        out.append(t)
    return "".join(out)


def window_probs(model, s, device):
    n = len(s)
    if n <= MAX_LEN:
        return predict_probs(model, [s], device)[0]
    starts = list(range(0, n - MAX_LEN + 1, 128))
    last = n - MAX_LEN
    wins = [(st, st + MAX_LEN) for st in starts] + [(last, n)]
    ps = predict_probs(model, [s[a:b] for a, b in wins], device)
    out = [None] * n
    for k, ((a, b), p) in enumerate(zip(wins, ps)):
        if k == len(wins) - 1:
            lo, hi = 64, MAX_LEN
        elif k == 0:
            lo, hi = 0, 192
        else:
            lo, hi = 64, 192
        for i in range(lo, min(hi, len(p))):
            if out[a + i] is None:
                out[a + i] = p[i]
    return out


def space_run(model, run_text, th, device):
    s = deva_to_slp1(run_text)
    if not s or any(c not in _ALPHA for c in s):
        return run_text
    p = window_probs(model, s, device)
    res = "".join(c + (" " if i < len(s) - 1 and p[i] >= th else "") for i, c in enumerate(s))
    return slp1_to_deva(res)


def space_line(model, line, th, device, punct=True):
    # whitespace-only separators between Sanskrit runs are deleted and the runs joined
    line = re.sub(r"(?<=%s)[ \t]+(?=%s)" % (_CH, _CH), "", line)
    out, last = [], 0
    for m in _RUN.finditer(line):
        out.append(line[last:m.start()])
        out.append(space_run(model, m.group(), th, device))
        last = m.end()
    out.append(line[last:])
    text = "".join(out)
    return space_punctuation(text) if punct else text


def selftest(run, model, th, device):
    preds = {}
    for l in open(f"{run}/predictions_test.jsonl", encoding="utf-8"):
        d = json.loads(l)
        preds[d["id"]] = d["pred"]
    test = [json.loads(l) for l in open("data/splits/test.jsonl", encoding="utf-8")][:200]
    ok = 0
    for d in test:
        inp = slp1_to_deva(d["slp"].replace(" ", ""))
        ok += space_line(model, inp, th, device) == slp1_to_deva(preds[d["id"]])
    print(f"selftest identical: {ok}/200")
    assert ok >= 198, ok
    print("GATE 8 OK")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--run", required=True)
    ap.add_argument("--in", dest="inp")
    ap.add_argument("--out")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--no-punct-spacing", action="store_true", help="do not add spaces around dandas and numbers")
    a = ap.parse_args()
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    model = load_model(a.run, device)
    th = json.load(open(f"{a.run}/threshold.json"))["threshold"]
    if a.selftest:
        return selftest(a.run, model, th, device)
    with open(a.inp, encoding="utf-8") as f, open(a.out, "w", encoding="utf-8") as g:
        for line in f:
            g.write(space_line(model, line.rstrip("\n"), th, device, punct=not a.no_punct_spacing) + "\n")


if __name__ == "__main__":
    main()
