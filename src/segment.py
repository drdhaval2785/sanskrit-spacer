import re
import unicodedata

from config import MIN_LETTERS, MAX_LETTERS, VOWELS, CONSONANTS
from src.translit import iast_to_slp1

_BRACKETS = re.compile(r"\([^()]*\)|\[[^\[\]]*\]|\{[^{}]*\}|<[^<>]*>|##[^#]*##")
_AVAGRAHA = re.compile(r"(?<=[eoā]) *'(?=[kgṅcjñṭḍṇtdnpbmyrlvśṣsh])")
_SEG = re.compile(r"[a-zāīūṛṝḷḹḻṅñṭḍṇśṣṃḥ~' ]+")
_HIATUS = re.compile("[%s]{2}" % VOWELS)
_REPEAT = re.compile(r"(.)\1{3,}")


def segment(text):
    text = unicodedata.normalize("NFC", text).lower()
    for a, b in [("r̥̄", "ṝ"), ("r̥", "ṛ"), ("l̥̄", "ḹ"), ("l̥", "ḷ"),
                 ("ē", "e"), ("ō", "o"), ("ṁ", "ṃ"), ("m̐", "~"),
                 ("’", "'"), ("ʼ", "'"), ("‘", "\n"), ("`", "\n")]:
        text = text.replace(a, b)
    for _ in range(3):
        text = _BRACKETS.sub("\n", text)
    text = re.sub(r"'{2,}", "'", text)
    text = _AVAGRAHA.sub("\x01", text)
    text = text.replace("'", "\n").replace("\x01", "'")
    out = []
    for seg in _SEG.findall(text):
        seg = re.sub(" +", " ", seg).strip(" ")
        if seg:
            out.append(seg)
    return out


def clean(seg):
    slp = iast_to_slp1(seg)
    if slp is None:
        return [], "non_iast"
    if _HIATUS.search(slp):
        return [], "hiatus"
    letters = slp.replace(" ", "")
    if _REPEAT.search(letters):
        return [], "repeat"
    if len(letters) > MAX_LETTERS:
        chunks, cur, cur_n = [], [], 0
        for w in slp.split(" "):
            if len(w) > MAX_LETTERS:
                if cur:
                    chunks.append(cur)
                cur, cur_n = [], 0
                continue
            if cur and cur_n + len(w) > MAX_LETTERS:
                chunks.append(cur)
                cur, cur_n = [], 0
            cur.append(w)
            cur_n += len(w)
        if cur:
            chunks.append(cur)
        res = [" ".join(c) for c in chunks if sum(len(w) for w in c) >= MIN_LETTERS]
        return res, (None if res else "too_short")
    if len(letters) < MIN_LETTERS:
        return [], "too_short"
    return [slp], None
