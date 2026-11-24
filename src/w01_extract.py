"""Extract sentences from the validated scan pages of Sanskrit Wikisource (Page namespace, quality 4)."""
import bz2
import html
import json
import re
import unicodedata
import xml.etree.ElementTree as ET
from collections import Counter

from config import WSV_DUMP, WSV_LEVELS, WSV_PAGE_HINDI_RATE, VOWELS, MIN_LETTERS, MAX_LETTERS, ALPHABET
from src.translit import deva_to_slp1

XNS = "{http://www.mediawiki.org/xml/export-0.11/}"
QUAL = re.compile(r'<pagequality\s+level="(\d)"')
# Words that are Hindi or Marathi and never a Sanskrit word on their own.
STRICT_VERNACULAR = set("है हैं में नहीं और यह थी थे था किया गया लिए होता होती होते जाता जाती करते करता करती "
                        "अपने अपनी इस उस साथ बाद आहे आणि नाही केले होते".split())
BROAD_VERNACULAR = STRICT_VERNACULAR | set("का की के को से वह".split())
ALPHA = set(ALPHABET) | {" "}
HIATUS = re.compile("[%s]{2}" % VOWELS)
REPEAT = re.compile(r"(.)\1{3,}")
SEG = re.compile(r"[ऀ-ॏ॑-ॣॱ-ॿ ]+")  # letters, signs, avagraha; not ॐ, dandas, digits, ॰


def unwrap_templates(t):
    """{{name|..|text}} -> text when the last positional parameter has Devanagari, else a line break."""
    def rep(m):
        parts = [p for p in m.group(1).split("|")[1:] if "=" not in p.split("ऽ")[0][:20]]
        last = parts[-1] if parts else ""
        return last if re.search(r"[ऀ-ॿ]", last) else "\n"
    for _ in range(6):
        t2 = re.sub(r"\{\{([^{}]*)\}\}", rep, t)
        if t2 == t:
            break
        t = t2
    return t


def clean_wikitext(t):
    t = re.sub(r"<noinclude>.*?</noinclude>", "", t, flags=re.S)
    t = re.sub(r"<!--.*?-->", "", t, flags=re.S)
    t = re.sub(r"<ref[^>]*/>", "", t)
    t = re.sub(r"<ref[^>]*>.*?</ref>", "\n", t, flags=re.S | re.I)
    t = re.sub(r"<(sup|sub|math|score|syntaxhighlight|references)\b[^>]*>.*?</\1>", "\n", t, flags=re.S | re.I)
    t = re.sub(r"<br\s*/?>", "\n", t, flags=re.I)
    t = unwrap_templates(t)
    # tables: drop the syntax, keep the cells' text
    lines = []
    for line in t.split("\n"):
        s = line.strip()
        if s.startswith(("{|", "|}", "|-")):
            continue
        if s.startswith(("|", "!")):
            s = s[1:]
            for cell in re.split(r"\|\||!!", s):
                if "|" in cell and "=" in cell.split("|", 1)[0]:
                    cell = cell.split("|", 1)[1]
                lines.append(cell)
            continue
        lines.append(line)
    t = "\n".join(lines)
    t = re.sub(r"\[\[(?:[^\]|]*:)[^\]]*\]\]", "", t)            # files, categories, interwiki
    t = re.sub(r"\[\[[^\]|]*\|([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[\[([^\]]*)\]\]", r"\1", t)
    t = re.sub(r"\[(?:https?:)?//\S+\s*([^\]]*)\]", r"\1", t)
    t = re.sub(r"</?[A-Za-z][^>]*>", "", t)                     # remaining tags: keep their text
    t = t.replace("'''", "").replace("''", "")
    t = re.sub(r"^=+|=+$", "", t, flags=re.M)
    t = re.sub(r"__[A-Z]+__", "", t)
    return html.unescape(t)


def segment_deva(text):
    text = unicodedata.normalize("NFC", text)
    text = re.sub("[​‌‍­﻿]", "", text)
    for _ in range(3):
        text = re.sub(r"\([^()]*\)|\[[^\[\]]*\]|\{[^{}]*\}|<[^<>]*>", "\n", text)
    text = re.sub(r"[ \t]+ऽ", "ऽ", text)                       # कृतो ऽत्र -> कृतोऽत्र
    out = []
    for seg in SEG.findall(text):
        seg = re.sub(" +", " ", seg).strip(" ")
        if seg:
            out.append(seg)
    return out


def clean_deva(seg):
    """-> (list of spaced SLP1 sentences, reject reason or None)"""
    if any(w in STRICT_VERNACULAR for w in seg.split(" ")):
        return [], "vernacular"
    slp = deva_to_slp1(seg)
    if not slp or any(c not in ALPHA for c in slp):
        return [], "non_alpha"
    if HIATUS.search(slp):
        return [], "hiatus"
    letters = slp.replace(" ", "")
    if REPEAT.search(letters):
        return [], "repeat"
    if len(letters) > MAX_LETTERS:
        chunks, cur, n = [], [], 0
        for w in slp.split(" "):
            if len(w) > MAX_LETTERS:
                if cur:
                    chunks.append(cur)
                cur, n = [], 0
                continue
            if cur and n + len(w) > MAX_LETTERS:
                chunks.append(cur)
                cur, n = [], 0
            cur.append(w)
            n += len(w)
        if cur:
            chunks.append(cur)
        res = [" ".join(c) for c in chunks if sum(map(len, c)) >= MIN_LETTERS]
        return res, (None if res else "too_short")
    if len(letters) < MIN_LETTERS:
        return [], "too_short"
    return [slp], None


def book_of(title):
    name = title.split(":", 1)[-1].rsplit("/", 1)[0]
    return name


def group_of(book):
    """The work a scanned book belongs to: its name up to the first bracket, dash or number, so that volumes,
    parts and editions of one work fall together (they must never be split between training and test)."""
    g = re.sub(r"\.(pdf|djvu|tif|tiff)$", "", book, flags=re.I)
    g = re.split(r"\s*[(\[]|\s+[-–]\s+|[0-9०-९]", g)[0]
    g = re.sub(r"[\s_\-–,.]*((भागः|भाग|खण्डः|खण्ड|खंडः|खंड|vol\.?|volume|part)[\s_\-.]*)?$", "", g, flags=re.I)
    return g.strip() or book


def main():
    stats = Counter()
    seen = set()
    rows = []
    for _, el in ET.iterparse(bz2.open(WSV_DUMP), events=("end",)):
        if el.tag != XNS + "page":
            continue
        if el.findtext(XNS + "ns") == "104":
            raw = el.findtext(f"{XNS}revision/{XNS}text") or ""
            m = QUAL.search(raw)
            if m and m.group(1) in WSV_LEVELS:
                title = el.findtext(XNS + "title") or ""
                rows.append((title, raw))
        el.clear()
    stats["validated_pages"] = len(rows)

    def pkey(r):
        book = book_of(r[0])
        p = r[0].rsplit("/", 1)[-1]
        return (book, int(p) if p.isdigit() else 10**9, p)
    rows.sort(key=pkey)
    with open("data/wsv/interim/sentences_raw.jsonl", "w", encoding="utf-8") as out:
        for title, raw in rows:
            text = clean_wikitext(raw)
            words = re.findall(r"[ऀ-ॿ]+", text)
            if words and sum(w in BROAD_VERNACULAR for w in words) / len(words) > WSV_PAGE_HINDI_RATE and len(words) > 20:
                stats["pages_dropped_vernacular"] += 1
                continue
            stats["pages_used"] += 1
            book = book_of(title)
            page = title.rsplit("/", 1)[-1]
            k = 0
            for seg in segment_deva(text):
                stats["segments_seen"] += 1
                sents, why = clean_deva(seg)
                if why:
                    stats["reject_" + why] += 1
                for slp in sents:
                    letters = slp.replace(" ", "")
                    if letters in seen:
                        stats["reject_duplicate"] += 1
                        continue
                    seen.add(letters)
                    out.write(json.dumps({"id": f"{book}/{page}#{k}", "path": book, "group": group_of(book),
                                          "repo": "sa.wikisource-validated", "kind": "page", "slp": slp,
                                          "n": len(letters)}, ensure_ascii=False) + "\n")
                    k += 1
                    stats["sentences_written"] += 1
    stats["books"] = len({book_of(t) for t, _ in rows})
    json.dump(dict(stats), open("data/wsv/interim/extract.stats.json", "w"), indent=1)
    print(json.dumps(dict(stats), indent=1))


if __name__ == "__main__":
    main()
