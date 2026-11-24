import torch
import torch.nn as nn

from config import (ALPHABET, PAD_ID, UNK_ID, MAX_LEN, D_MODEL, N_HEAD, N_LAYERS, D_FF, DROPOUT)
from src.metrics import encode

_IDX = {c: i + 2 for i, c in enumerate(ALPHABET)}


class Spacer(nn.Module):
    def __init__(self, d_model=D_MODEL, n_head=N_HEAD, n_layers=N_LAYERS, d_ff=D_FF,
                 dropout=DROPOUT, max_len=MAX_LEN):
        super().__init__()
        self.cfg = {"MAX_LEN": max_len, "D_MODEL": d_model, "N_HEAD": n_head,
                    "N_LAYERS": n_layers, "D_FF": d_ff, "DROPOUT": dropout}
        self.tok = nn.Embedding(len(ALPHABET) + 2, d_model, padding_idx=PAD_ID)
        self.pos = nn.Embedding(max_len, d_model)
        self.drop = nn.Dropout(dropout)
        layer = nn.TransformerEncoderLayer(d_model, n_head, d_ff, dropout,
                                           activation="gelu", batch_first=True, norm_first=True)
        self.enc = nn.TransformerEncoder(layer, n_layers, norm=nn.LayerNorm(d_model),
                                         enable_nested_tensor=False)
        self.out = nn.Linear(d_model, 1)

    def forward(self, ids):
        pad = ids.eq(PAD_ID)
        pos = torch.arange(ids.size(1), device=ids.device).unsqueeze(0)
        x = self.drop(self.tok(ids) + self.pos(pos))
        x = self.enc(x, src_key_padding_mask=pad)
        return self.out(x).squeeze(-1)


def ids_of(letters):
    return [_IDX.get(c, UNK_ID) for c in letters]


def make_batch(slps, device):
    """slps: list of spaced SLP1 strings -> ids, labels, mask (valid positions)."""
    enc = [encode(s) for s in slps]
    L = max(len(l) for l, _ in enc)
    ids = torch.zeros(len(enc), L, dtype=torch.long)
    lab = torch.zeros(len(enc), L)
    mask = torch.zeros(len(enc), L, dtype=torch.bool)
    for i, (l, y) in enumerate(enc):
        ids[i, :len(l)] = torch.tensor(ids_of(l))
        lab[i, :len(l)] = torch.tensor(y, dtype=torch.float)
        mask[i, :len(l) - 1] = True
    return ids.to(device), lab.to(device), mask.to(device)


def load_model(run_dir, device):
    ck = torch.load(f"{run_dir}/best.pt", map_location="cpu")
    c = ck.get("config", {})
    m = Spacer(d_model=c.get("D_MODEL", D_MODEL), n_head=c.get("N_HEAD", N_HEAD),
               n_layers=c.get("N_LAYERS", N_LAYERS), d_ff=c.get("D_FF", D_FF),
               dropout=c.get("DROPOUT", DROPOUT), max_len=c.get("MAX_LEN", MAX_LEN))
    m.load_state_dict(ck["model"])
    return m.to(device).eval()


@torch.no_grad()
def predict_probs(model, letters_list, device, batch=256):
    """letters_list: list of letter strings (each <= MAX_LEN). Returns list of prob lists."""
    order = sorted(range(len(letters_list)), key=lambda i: len(letters_list[i]))
    res = [None] * len(letters_list)
    for s in range(0, len(order), batch):
        idx = order[s:s + batch]
        L = max(len(letters_list[i]) for i in idx)
        ids = torch.zeros(len(idx), L, dtype=torch.long)
        for j, i in enumerate(idx):
            ids[j, :len(letters_list[i])] = torch.tensor(ids_of(letters_list[i]))
        p = torch.sigmoid(model(ids.to(device))).cpu()
        for j, i in enumerate(idx):
            res[i] = p[j, :len(letters_list[i])].tolist()
    return res
