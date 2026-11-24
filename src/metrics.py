def encode(slp):
    """Return (letters, labels). labels[i]=1 if a space follows letter i."""
    letters, labels = [], []
    for ch in slp:
        if ch == " ":
            if labels:
                labels[-1] = 1
        else:
            letters.append(ch)
            labels.append(0)
    return "".join(letters), labels


def positions(slp):
    letters, labels = encode(slp)
    return {i for i, l in enumerate(labels[:-1]) if l}


def words(pos, n):
    cuts = [0] + sorted(p + 1 for p in pos) + [n]
    return {(a, b) for a, b in zip(cuts, cuts[1:]) if b > a}


class Meter:
    def __init__(self):
        self.tp = self.fp = self.fn = 0
        self.wc = self.wp = self.wg = 0
        self.sent = self.exact = 0
        self.gaps = 0

    def add(self, gold_pos, pred_pos, n):
        self.tp += len(gold_pos & pred_pos)
        self.fp += len(pred_pos - gold_pos)
        self.fn += len(gold_pos - pred_pos)
        gw, pw = words(gold_pos, n), words(pred_pos, n)
        self.wc += len(gw & pw)
        self.wp += len(pw)
        self.wg += len(gw)
        self.sent += 1
        self.exact += gold_pos == pred_pos
        self.gaps += max(n - 1, 0)

    @staticmethod
    def _prf(c, p, g):
        pr = c / p if p else 0.0
        rc = c / g if g else 0.0
        f = 2 * pr * rc / (pr + rc) if pr + rc else 0.0
        return pr, rc, f

    def result(self):
        bp, br, bf = self._prf(self.tp, self.tp + self.fp, self.tp + self.fn)
        wp, wr, wf = self._prf(self.wc, self.wp, self.wg)
        return {"sentences": self.sent, "gaps": self.gaps, "tp": self.tp, "fp": self.fp, "fn": self.fn,
                "boundary_p": bp, "boundary_r": br, "boundary_f1": bf,
                "word_p": wp, "word_r": wr, "word_f1": wf,
                "sentence_acc": self.exact / self.sent if self.sent else 0.0}
