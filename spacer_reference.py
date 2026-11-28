"""The spacer's reference pipeline: word spaces put into Devanagari text, as pure functions, with no transliteration
library. It is what the JavaScript port in Manuscribe copies and is checked against. Its parameters and its
Devanagari -> SLP1 tables are in spacer.json (built by tools/make_spacer_json.py, checked against indic_transliteration
on every possible letter unit); the network is passed in as a function from letter ids (int64, 1 x L) to logits (1 x L).

  space_text(text, network)          whitespace between Sanskrit runs removed; each run spaced; dandas and numbers
                                     set off by one space
    runs: maximal stretches of the run characters (U+0900-094F, 0951-0963, 0970-097F: not ॐ, dandas or digits)
    units(run) -> [(devanagari, slp1)]   orthographic units: a consonant with its nukta, virama or vowel sign and any
                                     candrabindu, anusvāra, visarga; or any other character with those marks.
                                     None (run left as it is) if a unit's SLP1 leaves the 52-letter alphabet
    probabilities(slp1, network)     sigmoid of the network for every letter; runs longer than max_len in windows of
                                     max_len every window_step letters, each letter from the middle of a window
    a space after unit k where the probability at its last letter reaches the threshold (not after the last unit)
"""
import json
import re
from pathlib import Path

import numpy as np

S = json.loads(Path(__file__).with_name("spacer.json").read_text(encoding="utf-8"))
VERSION = S["version"]            # spacer.json's format version (what Manuscribe checks a pack against)
__version__ = "0.13.4"               # this software's: Manuscribe and its companions carry the same one
_CLASS = "".join(f"{chr(a)}-{chr(b)}" for a, b in S["run_ranges"])
RUN = re.compile(f"[{_CLASS}]+")
WS_BETWEEN = re.compile(f"(?<=[{_CLASS}])[ \t]+(?=[{_CLASS}])")
_ALPHA = set(S["alphabet"])
_IDX = {c: i + 2 for i, c in enumerate(S["alphabet"])}
_PUNCT = S["punctuation"]["dandas"] + S["punctuation"]["digits"]
_TOKENS = re.compile(r"[।॥]+|[०-९0-9]+|[^।॥०-९0-9]+")


def units(run):
    out, i, n = [], 0, len(run)
    cons, sign, mod = S["consonant_base"], S["vowel_sign"], S["modifier"]
    while i < n:
        c = run[i]
        j = i + 1
        if c in cons:
            base = cons[c]
            if j < n and run[j] == S["nukta"]:
                base = S["consonant_nukta"][c]
                j += 1
            if j < n and run[j] == S["virama"]:
                vow = ""
                j += 1
            elif j < n and run[j] in sign:
                vow = sign[run[j]]
                j += 1
            else:
                vow = S["inherent"]
            x = base + vow
        else:
            x = S["other"][c]
        while j < n and run[j] in mod:
            x += mod[run[j]]
            j += 1
        out.append((run[i:j], x))
        i = j
    s = "".join(x for _, x in out)
    if not s or any(ch not in _ALPHA for ch in s):
        return None
    return out


def letter_ids(slp):
    return np.array([[_IDX.get(c, S["unk_id"]) for c in slp]], dtype=np.int64)


def probabilities(slp, network):
    n, L = len(slp), S["max_len"]
    sig = lambda z: 1.0 / (1.0 + np.exp(-np.asarray(z, dtype=np.float64)))
    if n <= L:
        return sig(network(letter_ids(slp))[0])
    step, (keep0, keep1) = S["window_step"], S["window_keep"]
    wins = [(a, a + L) for a in range(0, n - L + 1, step)] + [(n - L, n)]
    out = [None] * n
    for k, (a, b) in enumerate(wins):
        p = sig(network(letter_ids(slp[a:b]))[0])
        lo, hi = (0, keep1) if k == 0 else ((keep0, L) if k == len(wins) - 1 else (keep0, keep1))
        for i in range(lo, min(hi, len(p))):
            if out[a + i] is None:
                out[a + i] = p[i]
    return np.array(out)


def space_run(run, network, threshold):
    u = units(run)
    if u is None:
        return run
    p = probabilities("".join(x for _, x in u), network)
    out, pos = [], 0
    for k, (d, x) in enumerate(u):
        out.append(d)
        pos += len(x)
        if k < len(u) - 1 and p[pos - 1] >= threshold:
            out.append(" ")
    return "".join(out)


def space_punctuation(s):
    """One space on each side of every run of dandas or digits, where there is none and not at the ends."""
    toks = _TOKENS.findall(s)
    out = []
    for k, t in enumerate(toks):
        if k and (t[0] in _PUNCT or toks[k - 1][-1] in _PUNCT) and not t[0].isspace() and not toks[k - 1][-1].isspace():
            out.append(" ")
        out.append(t)
    return "".join(out)


def space_text(text, network, threshold=S["threshold"], punct=True):
    text = WS_BETWEEN.sub("", text)
    text = RUN.sub(lambda m: space_run(m.group(), network, threshold), text)
    return space_punctuation(text) if punct else text


def torch_network(model):
    import torch
    model = model.eval()

    def f(ids):
        with torch.no_grad():
            return model(torch.from_numpy(ids)).numpy()
    return f


def onnx_network(path):
    """The exported spacer. One exported at a fixed length (the first packs: max_len) is given ids padded with pad_id
    to that length, the outputs cut back; one exported with a free length is given the letters as they are."""
    import onnxruntime as ort
    s = ort.InferenceSession(str(path), providers=["CPUExecutionProvider"])
    name, fixed = s.get_inputs()[0].name, s.get_inputs()[0].shape[1]

    def f(ids):
        if not isinstance(fixed, int):
            return s.run(None, {name: ids})[0]
        x = np.full((ids.shape[0], fixed), S["pad_id"], dtype=np.int64)
        x[:, :ids.shape[1]] = ids
        return s.run(None, {name: x})[0][:, :ids.shape[1]]
    return f
