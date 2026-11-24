from indic_transliteration import sanscript

_TWO = {
    "ai": "E", "au": "O", "kh": "K", "gh": "G", "ch": "C", "jh": "J",
    "ṭh": "W", "ḍh": "Q", "th": "T", "dh": "D", "ph": "P", "bh": "B",
}
_ONE = {
    "a": "a", "ā": "A", "i": "i", "ī": "I", "u": "u", "ū": "U", "ṛ": "f", "ṝ": "F",
    "ḷ": "x", "ḹ": "X", "e": "e", "o": "o", "ṃ": "M", "ḥ": "H", "k": "k", "g": "g",
    "ṅ": "N", "c": "c", "j": "j", "ñ": "Y", "ṭ": "w", "ḍ": "q", "ṇ": "R", "t": "t",
    "d": "d", "n": "n", "p": "p", "b": "b", "m": "m", "y": "y", "r": "r", "l": "l",
    "v": "v", "ś": "S", "ṣ": "z", "s": "s", "h": "h", "ḻ": "L", "'": "'", "~": "~",
    " ": " ",
}


def iast_to_slp1(s):
    out = []
    i = 0
    n = len(s)
    while i < n:
        two = s[i:i + 2]
        if two in _TWO:
            out.append(_TWO[two])
            i += 2
        elif s[i] in _ONE:
            out.append(_ONE[s[i]])
            i += 1
        else:
            return None
    return "".join(out)


def slp1_to_deva(s):
    return sanscript.transliterate(s, sanscript.SLP1, sanscript.DEVANAGARI)


def deva_to_slp1(s):
    return sanscript.transliterate(s, sanscript.DEVANAGARI, sanscript.SLP1)


def deva_bytes(slp):
    return len(slp1_to_deva(slp).encode("utf-8")) + 1
