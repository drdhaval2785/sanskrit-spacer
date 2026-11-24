"""Insert word spaces into the unspaced (#ocr) pages of a Manuscribe TEI transcription.

Usage:
  .venv/bin/python segment_xml.py --run auto FILE.xml [MORE.xml ...]      # in place, keeps FILE.xml.orig once
  .venv/bin/python segment_xml.py --run runs/full_e10_s1 --out OUT.xml FILE.xml

What it does, per <pb .../> whose level is "#ocr":
  * the page text is read straight through every tag inside the page: <lb/> line breaks (with or without
    break="no"), <unclear>, <add> and anything else are kept exactly where they are, and words flow across
    them, so a word split over two lines is spaced as one word. Only <p> and </p> are hard word boundaries
    (and the page break itself);
  * spaces are inserted inside runs of Devanagari letters, and one space is put on each side of every
    danda, double danda and number, as in printed editions (--no-punct-spacing to skip); Latin text and
    all tags are untouched and no letter is altered (checked). A boundary that falls exactly at a tag is written
    as a space after a closing tag or before any other tag, e.g. "word \n<lb n="2" break="no"/>next";
  * the page's level is changed to "#segmented", so a second pass finds nothing to do: running the script
    again on its own output changes nothing. Pages at any other level are not touched at all.
A <change xml:id="segmented"> entry is added once to the header's <listChange> (skip with --no-header).
"""
import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"
import argparse
import glob
import json
import re
import sys

import torch

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from config import MAX_LEN
from src.model import load_model, predict_probs
from src.translit import deva_to_slp1
from space import _CH, _RUN, _ALPHA, window_probs, space_punctuation

TAG = re.compile(r"<[^>]+>")
PB = re.compile(r"<pb\b[^>]*>")
LEVEL_OCR = re.compile(r'''\blevel=(["'])#ocr\1''')
BREAK_NO = re.compile(r'''\s+break=(["'])no\1''')
WS_BETWEEN = re.compile(r"(?<=%s)[ \t]+(?=%s)" % (_CH, _CH))
HEADER_CHANGE = ('<change xml:id="segmented" type="segmentation">Word spaces inserted automatically by the '
                 'sanskrit_spacer model; letters not yet proofread</change>')


def tag_name(tag):
    m = re.match(r"</?\s*([A-Za-z_][\w:.-]*)", tag)
    return m.group(1) if m else ""


def best_run():
    """The run with the best boundary F1 on the clean test set (validated Wikisource pages) if any run has been
    scored on it, else on the original test set."""
    for name in ("metrics_test_wsv.json", "metrics_test.json"):
        best, best_f1 = None, -1.0
        for mt in glob.glob(f"runs/*/{name}"):
            d = os.path.dirname(mt)
            if not (os.path.exists(f"{d}/best.pt") and os.path.exists(f"{d}/threshold.json")):
                continue
            f1 = json.load(open(mt))["test"]["boundary_f1"]
            if f1 > best_f1:
                best, best_f1 = d, f1
        if best:
            return best
    sys.exit("no evaluated run found under runs/")

CONSONANT = set(chr(c) for c in range(0x0915, 0x093A)) | set(chr(c) for c in range(0x0958, 0x0960))
MATRA = set(chr(c) for c in range(0x093E, 0x094D)) | {"\u0962", "\u0963", "\u0955", "\u0956", "\u0957"}
VIRAMA, NUKTA = "\u094d", "\u093c"
MODIFIER = {"\u0901", "\u0902", "\u0903"}  # candrabindu, anusvara, visarga: stay with their syllable


def units_of(run):
    """Split a Devanagari run into orthographic units [(devanagari, slp1), ...] such that the SLP1 pieces
    concatenate to deva_to_slp1(run). Spaces may only be inserted between units. None if unsupported."""
    units = []
    i = 0
    while i < len(run):
        c = run[i]
        if c in CONSONANT:
            j = i + 1
            if j < len(run) and run[j] == NUKTA:
                j += 1
            if j < len(run) and (run[j] == VIRAMA or run[j] in MATRA):
                j += 1
            while j < len(run) and run[j] in MODIFIER:
                j += 1
            units.append(run[i:j])
            i = j
        else:
            j = i + 1
            while j < len(run) and run[j] in MODIFIER:
                j += 1
            units.append(run[i:j])
            i = j
    out = [(u, deva_to_slp1(u)) for u in units]
    s = "".join(x for _, x in out)
    if s != deva_to_slp1(run) or not s or any(ch not in _ALPHA for ch in s):
        return None
    return out


def space_texts(model, texts, th, device, stats=None):
    """Insert spaces into Devanagari runs of each text. Returns one string per input; only spaces are added,
    and only between orthographic units of the original text (it is never re-transliterated)."""
    runs = {}
    for t in texts:
        for m in _RUN.finditer(t):
            r = m.group()
            if r not in runs:
                runs[r] = units_of(r)
    slp = {r: "".join(x for _, x in u) for r, u in runs.items() if u is not None}
    if stats is not None:
        stats["runs"] = stats.get("runs", 0) + len(runs)
        stats["unsupported"] = stats.get("unsupported", 0) + sum(u is None for u in runs.values())
    short = [r for r, s in slp.items() if len(s) <= MAX_LEN]
    probs = dict(zip(short, predict_probs(model, [slp[r] for r in short], device))) if short else {}
    spaced = {}
    for r, u in runs.items():
        if u is None:
            spaced[r] = r
            continue
        p = probs[r] if r in probs else window_probs(model, slp[r], device)
        out, pos = [], 0
        for k, (d, x) in enumerate(u):
            out.append(d)
            pos += len(x)
            if k < len(u) - 1 and p[pos - 1] >= th:
                out.append(" ")
        spaced[r] = "".join(out)
    return [_RUN.sub(lambda m: spaced[m.group()], t) for t in texts]


def tokenize(span):
    """Split a page span into text pieces and tags. Whitespace touching a tag is attached to the tag."""
    toks = []
    pos = 0
    for m in TAG.finditer(span):
        toks.append(["text", span[pos:m.start()]])
        toks.append(["tag", m.group()])
        pos = m.end()
    toks.append(["text", span[pos:]])
    out = []
    for i, (kind, s) in enumerate(toks):
        if kind == "text":
            if i > 0:
                lead = len(s) - len(s.lstrip())
                out[-1][1] += s[:lead]
                s = s[lead:]
            if i + 1 < len(toks):
                trail = len(s) - len(s.rstrip())
                toks[i + 1][1] = s[len(s) - trail:] + toks[i + 1][1]
                s = s[:len(s) - trail]
            if s:
                out.append(["text", s])
        else:
            out.append(["tag", s])
    return out


def segment_page(span, model, th, device, stats, punct=True):
    """Return the re-spaced page span. Only <p>/</p> split the text; every other tag is transparent."""
    toks = tokenize(span)
    segments, cur, hard = [], {"stream": "", "tags": []}, []
    for kind, t in toks:
        if kind == "text":
            cur["stream"] += WS_BETWEEN.sub("", t)
        elif tag_name(t.strip()) == "p":
            segments.append(cur)
            hard.append(t)
            cur = {"stream": "", "tags": []}
        else:
            cur["tags"].append((len(cur["stream"]), t))
    segments.append(cur)
    spaced = space_texts(model, [seg["stream"] for seg in segments], th, device, stats)
    if punct:
        spaced = [space_punctuation(sp) for sp in spaced]
    out = []
    for k, (seg, sp) in enumerate(zip(segments, spaced)):
        stream, tags = seg["stream"], seg["tags"]
        assert sp.replace(" ", "") == stream.replace(" ", ""), "model changed letters"
        j, ti = 0, 0
        for i in range(len(stream) + 1):
            boundary = j < len(sp) and sp[j] == " " and (i == len(stream) or stream[i] != " ")
            due = []
            while ti < len(tags) and tags[ti][0] == i:
                due.append(tags[ti][1])
                ti += 1
            if boundary:
                j += 1
                if due:
                    # space after leading closing tags, before the rest; skip it if whitespace is already there
                    n = 0
                    while n < len(due) and due[n].lstrip().startswith("</"):
                        n += 1
                    # whitespace attached outside the tags: after the last closing tag, before the next tag
                    after_close = due[n - 1][due[n - 1].rfind(">") + 1:] if n else ""
                    before_next = due[n][:due[n].find("<")] if n < len(due) else ""
                    out.extend(due[:n])
                    if not re.search(r"[ \t]", after_close + before_next):
                        out.append(" ")
                    out.extend(due[n:])
                    due = []
                else:
                    out.append(" ")
            out.extend(due)
            if i < len(stream):
                assert sp[j] == stream[i]
                out.append(stream[i])
                j += 1
        if k < len(hard):
            out.append(hard[k])
    return "".join(out)


def process(text, model, th, device, add_header, stats, punct=True):
    pbs = list(PB.finditer(text))
    out, pos, done = [], 0, 0
    for k, m in enumerate(pbs):
        if not LEVEL_OCR.search(m.group()):
            continue
        end = pbs[k + 1].start() if k + 1 < len(pbs) else len(text)
        new = segment_page(text[m.end():end], model, th, device, stats, punct)
        out.append(text[pos:m.start()])
        out.append(LEVEL_OCR.sub(lambda mm: f"level={mm.group(1)}#segmented{mm.group(1)}", m.group()))
        out.append(new)
        pos = end
        done += 1
    out.append(text[pos:])
    result = "".join(out)
    if add_header and done and 'xml:id="segmented"' not in result and "<listChange" in result:
        # Place it after the "ocr" change if there is one (the list is ordered), else first in the list.
        ocr = re.search(r'<change\b[^>]*xml:id="ocr"[^>]*>.*?</change>', result, flags=re.S)
        if ocr:
            indent = re.search(r"\n([ \t]*)$", result[:ocr.start()])
            result = result[:ocr.end()] + "\n" + (indent.group(1) if indent else "") + HEADER_CHANGE + result[ocr.end():]
        else:
            result = re.sub(r"(<listChange\b[^>]*>)(\s*)",
                            lambda mm: mm.group(1) + mm.group(2) + HEADER_CHANGE + mm.group(2), result, count=1)
    return result, done


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("files", nargs="+")
    ap.add_argument("--run", default="auto", help='run directory with best.pt, or "auto" for the best test F1')
    ap.add_argument("--out", help="write here instead of in place (single input file only)")
    ap.add_argument("--no-header", action="store_true", help="do not add the <change xml:id=\"segmented\"> entry")
    ap.add_argument("--no-punct-spacing", action="store_true", help="do not add spaces around dandas and numbers")
    a = ap.parse_args()
    if a.out and len(a.files) != 1:
        sys.exit("--out needs exactly one input file")
    device = "mps" if torch.backends.mps.is_available() else "cpu"
    run = best_run() if a.run == "auto" else a.run
    model = load_model(run, device)
    th = json.load(open(f"{run}/threshold.json"))["threshold"]
    print(f"model {run} (threshold {th}) on {device}")
    for f in a.files:
        text = open(f, encoding="utf-8", newline="").read()
        stats = {}
        result, done = process(text, model, th, device, not a.no_header, stats, not a.no_punct_spacing)
        if stats.get("unsupported"):
            print(f"  {stats['unsupported']} of {stats['runs']} letter runs left unspaced (characters outside the model's alphabet)")
        target = a.out or f
        if result == text:
            print(f"{f}: nothing to do (no #ocr pages)" if not done else f"{f}: unchanged")
            if a.out:
                open(target, "w", encoding="utf-8", newline="").write(result)
            continue
        if not a.out and not os.path.exists(f + ".orig"):
            open(f + ".orig", "w", encoding="utf-8", newline="").write(text)
        tmp = target + ".tmp"
        open(tmp, "w", encoding="utf-8", newline="").write(result)
        os.replace(tmp, target)
        print(f"{f}: {done} pages segmented -> {target}")


if __name__ == "__main__":
    main()
