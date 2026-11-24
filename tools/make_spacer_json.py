"""Build spacer.json: the spacer's shared parameters and the Devanagari -> SLP1 tables for letter units, derived once from
indic_transliteration and checked against it on every possible unit, so that the reference (spacer_reference.py) and
its JavaScript port need no transliteration library.

    .venv/bin/python tools/make_spacer_json.py [run]     # default: segment_xml.best_run()
"""
import itertools, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from config import ALPHABET, MAX_LEN, PAD_ID, UNK_ID
from src.translit import deva_to_slp1
import segment_xml as X

VIRAMA, NUKTA = "्", "़"
RUN_RANGES = [(0x0900, 0x094F), (0x0951, 0x0963), (0x0970, 0x097F)]
chars = [chr(c) for a, b in RUN_RANGES for c in range(a, b + 1)]
cons = sorted(X.CONSONANT)
signs = sorted(X.MATRA)
mods = sorted(X.MODIFIER)
other = [c for c in chars if c not in X.CONSONANT and c not in X.MATRA and c not in X.MODIFIER and c not in (VIRAMA, NUKTA)]
# tables
cons_base = {c: deva_to_slp1(c + VIRAMA) for c in cons}
cons_nukta = {c: deva_to_slp1(c + NUKTA + VIRAMA) for c in cons}
k = deva_to_slp1("क" + VIRAMA)
sign = {s: deva_to_slp1("क" + s)[len(k):] for s in signs}
a = deva_to_slp1("अ")
mod = {m: deva_to_slp1("अ" + m)[len(a):] for m in mods}
oth = {c: deva_to_slp1(c) for c in chars if c not in X.CONSONANT}   # every non-consonant on its own (a stray sign too)
inherent = deva_to_slp1("क")[len(k):]

def slp(unit):
    c = unit[0]
    i = 1
    if c in cons_base:
        base = cons_base[c]
        if i < len(unit) and unit[i] == NUKTA:
            base = cons_nukta[c]; i += 1
        if i < len(unit) and unit[i] == VIRAMA:
            vow = ""; i += 1
        elif i < len(unit) and unit[i] in sign:
            vow = sign[unit[i]]; i += 1
        else:
            vow = inherent
        return base + vow + "".join(mod[m] for m in unit[i:])
    return oth[c] + "".join(mod[m] for m in unit[1:])
# every unit units_of can form
units = []
for c in cons:
    for nk in ("", NUKTA):
        for v in [""] + [VIRAMA] + signs:
            for ms in itertools.chain([()], ((m,) for m in mods), itertools.product(mods, repeat=2)):
                units.append(c + nk + v + "".join(ms))
for c in other:
    for ms in itertools.chain([()], ((m,) for m in mods), itertools.product(mods, repeat=2)):
        units.append(c + "".join(ms))
alpha = set(ALPHABET)
inside = lambda s: all(ch in alpha for ch in s)
# what matters is every decision: where the library's SLP1 lies in the alphabet ours must be the same string, and
# where it does not ours must not either (the run is then left unspaced); nukta forms differ only outside it
bad = [u for u in units if (inside(deva_to_slp1(u)) or inside(slp(u))) and slp(u) != deva_to_slp1(u)]
same = sum(slp(u) == deva_to_slp1(u) for u in units)
print(f"{len(units)} possible units: the same SLP1 as the library for {same}; the same decision for {len(units) - len(bad)}" + (f"; differ: {bad[:5]}" if bad else ""))
n_inside = sum(inside(slp(u)) for u in units)
run = sys.argv[1] if len(sys.argv) > 1 else X.best_run()
th = json.load(open(os.path.join(run, "threshold.json")))["threshold"]
spec = {
    "version": 1,
    "about": "Parameters shared by the spacer's Python reference (spacer_reference.py) and its JavaScript port. Built by tools/make_spacer_json.py from indic_transliteration and checked against it on every possible letter unit.",
    "run": os.path.basename(run.rstrip("/")), "threshold": th,
    "alphabet": ALPHABET, "pad_id": PAD_ID, "unk_id": UNK_ID, "max_len": MAX_LEN, "window_step": 128, "window_keep": [64, 192],
    "run_ranges": [[a, b] for a, b in RUN_RANGES],
    "virama": VIRAMA, "nukta": NUKTA,
    "consonant_base": cons_base, "consonant_nukta": cons_nukta, "vowel_sign": sign, "inherent": inherent,
    "modifier": mod, "other": oth,
    "punctuation": {"dandas": "।॥", "digits": "०१२३४५६७८९0123456789"},
}
json.dump(spec, open("spacer.json", "w", encoding="utf-8"), ensure_ascii=False, indent=1)
print(f"spacer.json written: run {spec['run']}, threshold {th}; {n_inside} of {len(units)} units fall inside the alphabet")
assert not bad
