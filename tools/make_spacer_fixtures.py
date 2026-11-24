"""Write the fixture set that the JavaScript port of the spacer's reference (Manuscribe's app/js/recogspace.js) is held
to by Manuscribe's tests/t-recog-spacer.js: texts in Devanagari, and what spacer_reference.py makes of each with the
ONNX spacer of a model pack.

    ../manuscript_ocr/.venv-onnx/bin/python tools/make_spacer_fixtures.py [--pack DIR] [--out DIR]

It runs where onnxruntime is (manuscript_ocr's .venv-onnx); the test sentences are put into Devanagari by the spacer's
own slp1_to_deva (indic_transliteration), run in this folder's .venv. Every text is drawn deterministically:
  sentence   200 sentences of data/splits/test.jsonl, evenly spread, their spaces taken out first (scriptio continua,
             as space.py feeds them: slp1_to_deva(slp.replace(" ", "")))
  long       consecutive test sentences run together and cut to 255-3,000 letters: runs that need windows, at and
             around the window boundaries (256, 384, 512, ...); two with dandas and numbers between long runs
  mixed      sentences with dandas, numbers, Latin, ॐ, joiners, other scripts and whitespace of many kinds put in at
             random places (space_punctuation, WS_BETWEEN and str.isspace)
  refused    sentences with letters outside the 52-letter alphabet put in (nukta forms, Vedic accents, candra vowels,
             ...), so that units() is None for some runs and they are left as they are
  soup       random strings of the alphabet's letters, signs and marks, and of anything in U+0900-097F
  edge       short cases written by hand (empty text, a stray virama at the start of a run, ...)
  page       the box texts of the pipeline fixtures' pages (09_text.json, a box's lines joined as msocr/fixtures.py
             joins them); their spaced text is checked here against 10_spaced.json

-> <out>/<pack>/index.json   {spacer_version, pack, threshold, made, texts, kinds, format}
   <out>/<pack>/texts.json   [{id, kind, text, runs, spaced}]: runs are the runs space_text spaces (RUN on the text after
                             WS_BETWEEN), each {run, units: [[devanagari, slp1], ...] or null, p: the probability of every
                             letter (float64, the sigmoid space_run compares with the threshold) or null}; spaced is
                             space_text(text, network, threshold)
The set lies a folder below <out> (default manuscript_ocr/data/fixtures/spacer, git-ignored there): an index.json in
data/fixtures/spacer itself would be taken for a pipeline fixture set by Manuscribe's t-recog-conformance.js.
"""
import argparse
import json
import os
import random
import subprocess
import sys
import time

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
import spacer_reference as SR

OCR = os.path.abspath(os.path.join(HERE, "..", "manuscript_ocr"))
SPACER_PY = os.path.join(HERE, ".venv", "bin", "python")

# put into the mixed texts: punctuation, numbers, Latin, ॐ, joiners, other scripts (one outside the BMP), and
# whitespace that Python's str.isspace and JavaScript's \s see differently (U+001C-001F, U+0085; U+FEFF)
MIXED = [" ", "\t", "  ", " \t ", "\n", "\r\n", "।", "॥", "।।", "॥ १ ॥", "॥१॥", "१२", "12", "0", "३।", "abc", "Latin text",
         "ॐ", "\u200c", "\u200d", "\u00a0", "\u3000", "\u2028", "\x1c", "\x1f", "\x85", "\ufeff", "\U0001f600", "\U00011013",
         "-", ",", ".", "?", "(", ")", "॰", "ऽ", "ং", "ਕ"]
# letters outside the alphabet: nukta forms (single and decomposed), Vedic accents and marks, candra vowels, ...
REFUSED = ["\u0958", "\u095b", "\u095c", "\u095d", "\u095e", "\u095f", "ऩ", "ऱ", "ऴ", "क\u093c", "ड\u093c", "ग\u093cा", "\u093c",
           "\u0951", "\u0952",
           "ॅ", "ॉ", "ऍ", "ऑ", "ॲ", "ॆ", "ऎ", "ऄ", "ऀ", "ॎ", "ॏ", "॰", "ॱ", "ॽ", "ॿ", "ॕ", "ॖ", "ॗ", "ऺ", "ऻ"]
EDGE = ["", " ", "\t", "\n", "क", "कं", "ं", "ःक", "ऽ", "अ", "्", "्क", "्कमलम्", "क्", "क्ष्", "क््", "का्म", "रामः्वनं",
        "राम ्वनं", "्क्", "।", "॥", "॥१॥", "१२३", "abc", "a।b", "क ख", "क\tख", "क \t ख", "क\nख", "क\u00a0ख", "क\u3000ख",
        "क१ख", "क।ख", " । ", "॥ ।", "।॥।", "\x1c।\x1c", "\x85।\x85", "\ufeff।\ufeff", "\u2028।", "\U0001f600।\U0001f600",
        "राम\U0001f600।", "ॐ", "ॐनमः", "नमः।।१।।", " रामः ", "रामः\t", "\tरामः", "रामः १ ", "रामो राघवः ।", "\u093c", "\u0958ख",
        "कख\u093cग", "ऩ", "ॠ", "ॡ", "ऌ", "कॢ", "कॣ", "ळ", "कँ", "कँं", "कं्", "इ्"]


def deva(slps):
    """slp1_to_deva of the spacer's own src/translit.py (indic_transliteration), in its .venv."""
    code = ("import json, sys; sys.path.insert(0, '.'); from src.translit import slp1_to_deva; "
            "print(json.dumps([slp1_to_deva(s) for s in json.load(sys.stdin)], ensure_ascii=True))")
    r = subprocess.run([SPACER_PY, "-c", code], input=json.dumps(slps), capture_output=True, text=True, cwd=HERE, check=True)
    return json.loads(r.stdout)


def slp_of(text):
    """The letters the spacer sees of a text of one run, or None."""
    u = SR.units(text)
    return None if u is None else "".join(x for _, x in u)


def texts(rows, pages):
    out = []
    add = lambda kind, i, text: out.append({"id": f"{kind}/{i}", "kind": kind, "text": text})
    # sentences, evenly spread; checked to come back as their letters
    picks = [rows[i * len(rows) // 200] for i in range(200)]
    for r, d in zip(picks, deva([r["slp"].replace(" ", "") for r in picks])):
        assert slp_of(d) == r["slp"].replace(" ", ""), (r["id"], d)
        add("sentence", r["id"], d)
    # long runs: consecutive sentences, cut to so many letters
    targets = [255, 256, 257, 300, 383, 384, 385, 400, 511, 512, 513, 600, 640, 641, 767, 768, 769, 1000, 1024, 1345,
               1500, 2048, 3000]
    longs = []
    for k, t in enumerate(targets):
        i, s = (k * 997) % len(rows), ""
        while len(s) < t:
            s += rows[i]["slp"].replace(" ", "")
            i = (i + 1) % len(rows)
        longs.append(s[:t])
    for k, (s, d) in enumerate(zip(longs, deva(longs))):
        assert slp_of(d) == s, (k, d)
        add("long", f"{len(s)}", d)
    a, b, c = deva([longs[19], longs[17], longs[12]])
    add("long", "1345+1000", a + " ॥ १ ॥ " + b)
    add("long", "600+600+1000", c + "।" + c + "\n" + b + "॥२॥")
    # mixed
    rng = random.Random(20261124)
    picks = [rows[(i * 7919 + 13) % len(rows)] for i in range(60)]
    for r, d in zip(picks, deva([r["slp"].replace(" ", "") for r in picks])):
        cs = list(d)
        for _ in range(rng.randint(1, 6)):
            cs.insert(rng.randint(0, len(cs)), rng.choice(MIXED))
        add("mixed", r["id"], "".join(cs))
    # refused: one letter or more outside the alphabet in some runs
    rng = random.Random(97)
    picks = [rows[(i * 4099 + 5) % len(rows)] for i in range(40)]
    for r, d in zip(picks, deva([r["slp"].replace(" ", "") for r in picks])):
        cs = list(d)
        for _ in range(rng.randint(1, 3)):
            cs.insert(rng.randint(0, len(cs)), rng.choice(REFUSED))
        if rng.random() < 0.5:
            cs.insert(rng.randint(0, len(cs)), rng.choice(["।", " ॥ ", "१", " "]))
        add("refused", r["id"], "".join(cs))
    # soup: random strings of the run characters
    S = SR.S
    letters = ([c for c in S["consonant_base"] if all(x in SR._ALPHA for x in S["consonant_base"][c])]
               + [c for c, x in S["vowel_sign"].items() if x in SR._ALPHA] + list(S["modifier"]) + [S["virama"]]
               + [c for c, x in S["other"].items() if x and all(y in SR._ALPHA for y in x) and c not in S["vowel_sign"]])
    anything = [chr(c) for a, b in S["run_ranges"] for c in range(a, b + 1)] + list("।॥०१९ \t॒ॐ")
    rng = random.Random(4242)
    for i in range(60):
        pool = letters if i < 40 else anything
        extra = [S["nukta"], "।", "१", " "] if i % 4 == 3 else []
        add("soup", i, "".join(rng.choice(pool + extra) for _ in range(rng.randint(1, 80))))
    for i, t in enumerate(EDGE):
        add("edge", i, t)
    for page, boxes in pages:
        for box, lines in boxes.items():
            add("page", f"{page}/{box}", "".join(l["text"] for l in lines))
    return out


def main():
    ap = argparse.ArgumentParser()
    packs = os.path.join(OCR, "data", "model_pack")
    newest = sorted(p for p in os.listdir(packs) if os.path.exists(os.path.join(packs, p, "spacer.onnx")))[-1]
    ap.add_argument("--pack", default=os.path.join(packs, newest))
    ap.add_argument("--out", default=os.path.join(OCR, "data", "fixtures", "spacer"))
    a = ap.parse_args()
    pack = os.path.abspath(a.pack)
    manifest = json.load(open(os.path.join(pack, "manifest.json"), encoding="utf-8"))
    assert json.load(open(os.path.join(pack, "spacer.json"), encoding="utf-8")) == SR.S, "the pack's spacer.json is not this one"
    assert manifest["spacer_version"] == SR.VERSION
    threshold = manifest["models"]["spacer"]["threshold"]
    net = SR.onnx_network(os.path.join(pack, "spacer.onnx"))
    rows = [json.loads(l) for l in open(os.path.join(HERE, "data", "splits", "test.jsonl"), encoding="utf-8")]
    # the pipeline fixtures' pages of this pack, with their spaced text to check against
    fx = os.path.join(OCR, "data", "fixtures", manifest["pack"])
    pages = []
    if os.path.exists(os.path.join(fx, "index.json")):
        for pg in json.load(open(os.path.join(fx, "index.json"), encoding="utf-8"))["pages"]:
            d = os.path.join(fx, pg["dir"])
            pages.append((pg["page"], json.load(open(os.path.join(d, "09_text.json"), encoding="utf-8"))))
            ref = json.load(open(os.path.join(d, "10_spaced.json"), encoding="utf-8"))
            for box, lines in pages[-1][1].items():
                assert SR.space_text("".join(l["text"] for l in lines), net, threshold) == ref[box], (pg["page"], box)
    items = texts(rows, pages)
    t0 = time.time()
    for it in items:
        runs = []
        for m in SR.RUN.finditer(SR.WS_BETWEEN.sub("", it["text"])):
            u = SR.units(m.group())
            p = None if u is None else [float(v) for v in SR.probabilities("".join(x for _, x in u), net)]
            runs.append({"run": m.group(), "units": None if u is None else [list(x) for x in u], "p": p})
        it["runs"] = runs
        it["spaced"] = SR.space_text(it["text"], net, threshold)
    root = os.path.join(a.out, manifest["pack"])
    os.makedirs(root, exist_ok=True)
    json.dump(items, open(os.path.join(root, "texts.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=0)
    kinds = {}
    for it in items:
        kinds[it["kind"]] = kinds.get(it["kind"], 0) + 1
    nruns = sum(len(it["runs"]) for it in items)
    refused = sum(r["units"] is None for it in items for r in it["runs"])
    letters = sum(len(r["p"]) for it in items for r in it["runs"] if r["p"])
    json.dump({"spacer_version": SR.VERSION, "pack": manifest["pack"], "threshold": threshold,
               "made": time.strftime("%Y-%m-%dT%H:%M:%S"), "texts": len(items), "kinds": kinds, "runs": nruns,
               "refused_runs": refused, "letters": letters,
               "format": "texts.json: [{id, kind, text, runs: [{run, units: [[devanagari, slp1], ...] | null, p: [float64 "
                         "sigmoid of each letter's logit] | null}], spaced: space_text(text, network, threshold)}]; runs as "
                         "space_text finds them (RUN on the text after WS_BETWEEN); network: spacer.onnx of the pack "
                         "(onnx_network, CPU)"},
              open(os.path.join(root, "index.json"), "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print(f"[spacer fixtures] {len(items)} texts ({', '.join(f'{v} {k}' for k, v in kinds.items())}); {nruns} runs, "
          f"{refused} refused, {letters} letters; {time.time() - t0:.1f} s: {root}")


if __name__ == "__main__":
    main()
