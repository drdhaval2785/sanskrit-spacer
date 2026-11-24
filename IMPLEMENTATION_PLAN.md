# Sanskrit Spacer — Implementation Plan

You are the implementing agent. Follow this document top to bottom. Do exactly what it says; where it gives a constant, a regex, a file name or a command, use it verbatim. Do not substitute your own design. If a `GATE` check fails, stop and report the numbers you saw; do not improvise a workaround.

Project root (all relative paths below start here):
`/Users/Shared/drdhaval2785/lexicon_manuscripts/sanskrit_spacer`

---

## 1. What we are building

Sanskrit manuscripts are written without spaces between words. Printed books need spaces. We train a model that takes a line of Sanskrit with no spaces and returns the same line with spaces inserted.

The model never changes, adds or removes a letter. Its only decision is, for each gap between two adjacent letters, "space here: yes or no". So this is a **binary tagging problem over letters**, not a text-generation problem. Do not build a sequence-to-sequence model.

The experiment: train the same model on 1 MB, 5 MB, 10 MB and 20 MB of text, and report precision, recall and F1 on a fixed test set for each, to see how quality grows with data.

### What "done" means

All of these exist and are consistent with each other:

1. `data/splits/` with `test.jsonl`, `val.jsonl`, `train_1mb.jsonl`, `train_5mb.jsonl`, `train_10mb.jsonl`, `train_20mb.jsonl`.
2. `runs/1mb_s1/`, `runs/5mb_s1/`, `runs/10mb_s1/`, `runs/20mb_s1/`, each with `best.pt`, `log.jsonl`, `threshold.json`, `metrics_test.json`.
3. `reports/results.md` with the results table, and `reports/learning_curve.png`.
4. `space.py`, a command-line tool that spaces a Devanagari text file using a trained model.
5. `pytest tests/` passes.

---

## 2. Decisions already made (do not revisit)

**D1. Internal alphabet is SLP1.** All text is converted to SLP1 before anything else. In SLP1 every Sanskrit sound is exactly one ASCII character, so "remove the spaces" produces exactly what a manuscript line contains. This does not hold in Devanagari: removing the space from `तम् उवाच` gives `तम्उवाच`, but a manuscript writes `तमुवाच`. In SLP1 both are `tamuvAca`. Devanagari appears only at the very edges (measuring file size, the final command-line tool, human-readable reports).

**D2. One data source for this version: the Pramāṇa open data release**, downloaded as Parquet files from Hugging Face. Do not call the indike.org API in a loop: its `robots.txt` disallows automated use of `/pramana/api/export`, and the Hugging Face release is the publisher's intended bulk route. Other sources are listed in section 12 for the record; do not download them.

**D3. Target spacing convention = the convention of Devanagari printed editions**, exactly as found in the selected documents. Sources differ: Devanagari-derived editions write `dharmyamākhyānamuttamam` joined, while romanised scholarly editions split it as `dharmyam ākhyānam uttamam`. Mixing the two gives the model contradictory answers for the same letters. We keep only documents that follow the Devanagari convention; the document audit in Phase 3 removes the others automatically.

**D4. "1 MB" means 1,000,000 bytes of the spaced sentences written in Devanagari, UTF-8, one sentence per line.** Devanagari is what the end user's files look like, so that is the unit. (SLP1 uses about 2.7 times fewer bytes for the same text; the report also gives letter and word counts so nothing is hidden.)

**D5. Train, validation and test never share a work.** All recensions of and commentaries on a work go to the same split as the work. Otherwise the test set would contain verses the model saw in training and the scores would be inflated.

**D6. One model architecture, one random seed per size.** A small character-level Transformer encoder. Hyperparameters are fixed in section 8 and are identical for all four sizes.

---

## 3. Directory layout

Create exactly this. Scripts live in `src/`; nothing downloaded is ever placed in `src/`.

```
sanskrit_spacer/
  IMPLEMENTATION_PLAN.md        (this file)
  requirements.txt
  config.py
  space.py
  src/
    __init__.py                 (empty)
    translit.py
    segment.py
    metrics.py
    model.py
    s01_download.py
    s02_extract.py
    s03_audit.py
    s04_split.py
    s05_train.py
    s06_evaluate.py
    s07_report.py
  tests/
    test_translit.py
    test_segment.py
    test_metrics.py
  data/
    raw/pramana/                (downloaded Parquet files)
    interim/                    (sentences_raw.jsonl, doc_audit.tsv, sentences.jsonl, *.stats.json)
    splits/
  runs/
  reports/
```

Run every script from the project root as a module, for example `.venv/bin/python -m src.s02_extract`. Every script must be safe to re-run: it overwrites its own outputs and nothing else.

---

## 4. `config.py` — every constant in one place

Create `config.py` with exactly these values. All scripts import from it; no script may hard-code any of them.

```python
SEED = 20261123

# --- data source ---
HF_REPO = "srajma/pramana"
HF_REVISION = "76b82194cd64ec912b06545337e355a342af26c3"
ALLOWED_REPOS = {"sa.wikisource", "sarit", "ambuda"}
ALLOWED_KINDS = {"verse", "prose", "line", "bhāṣya"}

# --- alphabet (SLP1) ---
VOWELS = "aAiIuUfFxXeEoO"
CONSONANTS = "kKgGNcCjJYwWqQRtTdDnpPbBmyrlvSzshL"
OTHERS = "MH'~"            # anusvara, visarga, avagraha, candrabindu
ALPHABET = VOWELS + "MH" + CONSONANTS + "'~"   # 52 symbols, this exact order
PAD_ID = 0
UNK_ID = 1                 # symbol i of ALPHABET has id i + 2; vocabulary size = 54

# --- sentence filters ---
MIN_LETTERS = 12
MAX_LETTERS = 240

# --- document audit ---
MAX_ANALYTIC_RATE = 0.03
MIN_SPACE_RATE = 0.04
MAX_SPACE_RATE = 0.25
MIN_DOC_LETTERS = 1000

# --- splits (bytes of Devanagari UTF-8, see D4) ---
TEST_BYTES = 2_500_000
VAL_BYTES = 2_500_000
GROUP_CAP_BYTES = 100_000
TIERS_MB = [1, 5, 10, 20]

# --- model ---
MAX_LEN = 256
D_MODEL = 256
N_HEAD = 4
N_LAYERS = 4
D_FF = 1024
DROPOUT = 0.1

# --- training ---
BATCH_SIZE = 128
PEAK_LR = 5e-4
MIN_LR = 5e-5
WARMUP_STEPS = 1000
MAX_STEPS = 20000
EVAL_EVERY = 500
PATIENCE_EVALS = 8
WEIGHT_DECAY = 0.01
GRAD_CLIP = 1.0
```

---

## 5. Phase 0 — Environment

The machine is an Apple M2 Pro, 16 GB RAM, macOS, with Homebrew Python 3.14 at `/opt/homebrew/bin/python3`. There is no conda and no uv. These exact package versions were installed and tested on this machine on 2026-11-23: torch 2.15.0 (Apple GPU backend "mps" available), pyarrow 26.0.1.

```bash
cd /Users/Shared/drdhaval2785/lexicon_manuscripts/sanskrit_spacer
/opt/homebrew/bin/python3 -m venv .venv
.venv/bin/pip install --upgrade pip
.venv/bin/pip install torch numpy pyarrow huggingface_hub indic-transliteration matplotlib pytest
.venv/bin/pip freeze > requirements.txt
.venv/bin/python -c "import torch; print(torch.__version__, torch.backends.mps.is_available())"
```

`GATE 0`: the last command prints a version and `True`. If it prints `False`, continue anyway; training will use the CPU and be several times slower.

Always use `.venv/bin/python`. Never use the system `python3` to run project code.

---

## 6. Phase 1 — Download (`src/s01_download.py`)

```python
from huggingface_hub import snapshot_download
snapshot_download(
    repo_id=HF_REPO, repo_type="dataset", revision=HF_REVISION,
    local_dir="data/raw/pramana",
    allow_patterns=["catalogue.parquet", "passages/*.parquet", "README.md", "LICENCES.md", "stats.json"],
)
```

Total download is about 545 MB: `catalogue.parquet` (15 MB) and four files `passages/part-0000.parquet` … `part-0003.parquet` (104, 154, 100, 171 MB).

What the two tables contain:

| table | columns you need | meaning |
|---|---|---|
| `catalogue.parquet` | `path`, `lang`, `script`, `words`, `text_in_release`, `source_repos` (list of strings) | one row per document |
| `passages/*.parquet` | `path`, `loc`, `ord`, `kind`, `text` | one row per verse or paragraph; `text` is in IAST romanisation; `text` can be null |

`path` joins the two tables. A path looks like `in.lit.ramayana.valmiki*gitapress`. The characters `*`, `!` and `~` inside a path introduce a recension, a commentary and a translation respectively.

`GATE 1`: all five Parquet files exist, and `pyarrow.parquet.read_metadata` reports 299,705 rows for the catalogue and 3,819,508 rows summed over the four passage files.

---

## 7. Phases 2–4 — Building the dataset

### 7.1 `src/translit.py`

Implement these four functions. Do not use a library for `iast_to_slp1`: the `indic-transliteration` library silently turns the IAST letters `oṃ` into `AUM`, which corrupts the data.

**`iast_to_slp1(s: str) -> str | None`**

Input is lowercase, NFC-normalised IAST containing only letters, spaces, `'` and `~`. Scan left to right. At each position try the two-character entries first, then the one-character entries. If nothing matches, return `None`.

Two-character entries:

| IAST | SLP1 | IAST | SLP1 |
|---|---|---|---|
| `ai` | `E` | `au` | `O` |
| `kh` | `K` | `gh` | `G` |
| `ch` | `C` | `jh` | `J` |
| `ṭh` | `W` | `ḍh` | `Q` |
| `th` | `T` | `dh` | `D` |
| `ph` | `P` | `bh` | `B` |

One-character entries:

| IAST | SLP1 | IAST | SLP1 | IAST | SLP1 | IAST | SLP1 |
|---|---|---|---|---|---|---|---|
| `a` | `a` | `ā` | `A` | `i` | `i` | `ī` | `I` |
| `u` | `u` | `ū` | `U` | `ṛ` | `f` | `ṝ` | `F` |
| `ḷ` | `x` | `ḹ` | `X` | `e` | `e` | `o` | `o` |
| `ṃ` | `M` | `ḥ` | `H` | `k` | `k` | `g` | `g` |
| `ṅ` | `N` | `c` | `c` | `j` | `j` | `ñ` | `Y` |
| `ṭ` | `w` | `ḍ` | `q` | `ṇ` | `R` | `t` | `t` |
| `d` | `d` | `n` | `n` | `p` | `p` | `b` | `b` |
| `m` | `m` | `y` | `y` | `r` | `r` | `l` | `l` |
| `v` | `v` | `ś` | `S` | `ṣ` | `z` | `s` | `s` |
| `h` | `h` | `ḻ` | `L` | `'` | `'` | `~` | `~` |
| (space) | (space) | | | | | | |

The Latin letters `f q w x z` are deliberately absent: they never occur in IAST Sanskrit, so a segment containing them is not Sanskrit and gets rejected by the `None`.

**`slp1_to_deva(s: str) -> str`** — `indic_transliteration.sanscript.transliterate(s, sanscript.SLP1, sanscript.DEVANAGARI)`.

**`deva_to_slp1(s: str) -> str`** — the same call with the two schemes swapped.

**`deva_bytes(slp: str) -> int`** — `len(slp1_to_deva(slp).encode("utf-8")) + 1` (the `+ 1` is the newline).

### 7.2 `src/segment.py`

**`segment(text: str) -> list[str]`** turns the IAST text of one passage into a list of clean IAST segments. A segment is our "sentence". The source uses many marks to end sentences and verses: `।`, `॥`, `|`, `||`, `/`, `//`, `.`, `..`, digits, and line breaks. The rule that covers all of them: **a segment is a maximal run of letters, spaces and avagrahas; every other character ends the segment.**

Apply these steps in this order:

1. `text = unicodedata.normalize("NFC", text).lower()`
2. Fixed replacements, in this order:
   - `"r̥̄"` → `ṝ`, `"r̥"` → `ṛ`, `"l̥̄"` → `ḹ`, `"l̥"` → `ḷ`
   - `ē` → `e`, `ō` → `o`, `ṁ` → `ṃ`
   - `"m̐"` → `~`
   - `’` → `'`, `ʼ` → `'`
   - `‘` → newline, `` ` `` → newline
3. Remove bracketed material (references, editorial notes, glosses). Run this substitution three times in a row, replacing each match with a newline:
   `\([^()]*\)|\[[^\[\]]*\]|\{[^{}]*\}|<[^<>]*>|##[^#]*##`
4. Collapse repeated apostrophes: `re.sub(r"'{2,}", "'", text)`.
5. Decide which apostrophes are avagrahas. An apostrophe is an avagraha only when the last letter before it is `e`, `o` or `ā` (spaces between are allowed) and the character right after it is a consonant. Every other apostrophe is a quotation mark. Code:
   ```python
   text = re.sub(r"(?<=[eoā]) *'(?=[kgṅcjñṭḍṇtdnpbmyrlvśṣsh])", "\x01", text)
   text = text.replace("'", "\n").replace("\x01", "'")
   ```
   This also deletes any space in front of an avagraha, so `kṛto 'tra` becomes `kṛto'tra`, matching Devanagari `कृतोऽत्र`.
6. Extract segments: `re.findall(r"[a-zāīūṛṝḷḹḻṅñṭḍṇśṣṃḥ~' ]+", text)`.
7. For each segment: replace runs of spaces by one space, strip leading and trailing spaces, drop it if empty.

**`clean(segment_iast: str) -> tuple[list[str], str | None]`** converts one segment to SLP1 and filters it. It returns `(list_of_slp1_sentences, reject_reason)`. Let `letters` mean the SLP1 string with spaces removed. Apply in this order; the first rule that fires decides:

| order | condition | result |
|---|---|---|
| 1 | `iast_to_slp1` returns `None` | reject, reason `non_iast` |
| 2 | `re.search(r"[aAiIuUfFxXeEoO]{2}", slp)` matches (two vowels touching inside a word: Prakrit, English or noise) | reject, reason `hiatus` |
| 3 | `re.search(r"(.)\1{3,}", letters)` matches | reject, reason `repeat` |
| 4 | `len(letters) > MAX_LETTERS` | split into chunks (below), then apply rule 5 to each chunk |
| 5 | `len(letters) < MIN_LETTERS` | reject, reason `too_short` |
| 6 | otherwise | accept |

Chunking for rule 4: walk through the words; keep adding words to the current chunk while the chunk's letter count stays ≤ `MAX_LETTERS`; when the next word would exceed it, close the chunk and start a new one with that word. A single word longer than `MAX_LETTERS` is discarded (reason `long_word`) and closes the current chunk.

### 7.3 Phase 2 — `src/s02_extract.py`

1. Read `catalogue.parquet`. Select documents where all of these hold: `lang == "sa"`, `script == "Latn"`, `text_in_release` is true, `words > 0`, `source_repos` is a non-empty list and every element is in `ALLOWED_REPOS`.
   `GATE 2a`: between 700 and 800 documents are selected (758 expected).
2. For each selected document compute `group = re.sub(r"[*!~].*$", "", path)` and `repo = "+".join(sorted(source_repos))`.
3. Read the passage files one at a time with `pyarrow.parquet.ParquetFile(...).iter_batches(batch_size=50_000, columns=["path","loc","ord","kind","text"])`. Never load a whole passage file into memory. Keep rows where `path` is selected, `text` is not null and `kind` is in `ALLOWED_KINDS`.
4. Collect the kept rows, sort them by `(path, ord)`, then for each row run `segment` and `clean`. For the k-th accepted sentence of a passage (k starting at 0) write one JSON line to `data/interim/sentences_raw.jsonl`:
   ```json
   {"id": "<path>@<loc>#<k>", "path": "...", "group": "...", "repo": "...", "kind": "...", "slp": "tO rAjaputrO kArtsnyena DarmyamAKyAnamuttamam", "n": 39}
   ```
   `slp` is the spaced SLP1 sentence (the training target). `n` is the letter count without spaces. Write JSON with `ensure_ascii=False`.
5. Exact de-duplication while writing: keep a set of `letters` strings already written; skip a sentence whose `letters` is already in the set (reason `duplicate`).
6. Write `data/interim/extract.stats.json`: number of documents, passages read, segments seen, sentences written, and the count for each reject reason.

The `kind` column is not fully reliable (some prose commentaries are labelled `verse`). Use it only for the filter in step 3 and for the breakdown in the report; never branch on it elsewhere.

`GATE 2b`: at least 500,000 sentences written, and `non_iast` + `hiatus` rejections together are under 15% of segments seen.

### 7.4 Phase 3 — `src/s03_audit.py`

This removes documents that use the wrong spacing convention (see D3) or are not really spaced text.

For each `path`, over its sentences in `sentences_raw.jsonl`, compute:

- `letters` = sum of `n`
- `spaces` = total number of space characters in `slp`
- `cv` = total matches of the regex `[CONSONANTS] [VOWELS]` (a consonant, one space, a vowel), built from the two config strings
- `space_rate = spaces / letters`
- `analytic_rate = cv / spaces` (0 if `spaces == 0`)

A document is **dropped** if any of these is true, checked in this order, recording the first reason:

| reason | condition |
|---|---|
| `tiny` | `letters < MIN_DOC_LETTERS` |
| `analytic` | `analytic_rate > MAX_ANALYTIC_RATE` |
| `underspaced` | `space_rate < MIN_SPACE_RATE` |
| `overspaced` | `space_rate > MAX_SPACE_RATE` |

Why `analytic_rate` works: a Devanagari edition almost never puts a space between a word ending in a consonant and a word beginning with a vowel (it writes them as one cluster), while a romanised scholarly edition does so in roughly one space out of ten.

Outputs:

- `data/interim/doc_audit.tsv` with columns `path, group, repo, sentences, letters, spaces, cv, space_rate, analytic_rate, decision` (`keep` or the drop reason), sorted by `path`.
- `data/interim/sentences.jsonl`: the sentences of kept documents, same format and order as the input.
- `data/interim/audit.stats.json`: documents and letters kept and dropped per reason and per repo, and `kept_deva_bytes_estimate = round(2.7 * kept_letters)`.

What to expect: a preliminary check on the raw passage text (before cleaning, so your numbers will differ slightly) found 20 of the 757 documents above the 3% limit — for example Sāyaṇa's Atharvaveda commentary at 6.2% and Vācaspati's Yogasūtra sub-commentary at 17.3% — and about 91 of 97 million characters in documents under the limit. Almost all kept documents had a space rate between 0.05 and 0.14, and about 700 distinct groups remained. If you see most documents being dropped, the bug is in your code, not in the data.

`GATE 3`: `kept_deva_bytes_estimate` ≥ 60,000,000, and the kept sentences span at least 300 distinct `group` values.

### 7.5 Phase 4 — `src/s04_split.py`

Define `h(x) = hashlib.sha1(f"{SEED}:{x}".encode("utf-8")).hexdigest()`. All ordering below is by this hash, so the split is identical on every run.

1. Load `sentences.jsonl`. Compute `b = deva_bytes(slp)` for each sentence when it is first needed and cache it.
2. Sort the distinct groups by `h(group)`. Call this the group queue.
3. **Test set.** Take groups from the front of the queue one at a time. For each group, sort its sentences by `h(id)` and add them to the test set one by one until the group has contributed ≥ `GROUP_CAP_BYTES` or has no sentences left. The group's remaining sentences are discarded (they are used nowhere). Stop taking groups as soon as the test set's total bytes ≥ `TEST_BYTES`.
4. **Validation set.** Continue from the same queue position, same procedure, until total bytes ≥ `VAL_BYTES`.
5. **Training pool.** All sentences of all remaining groups, sorted by `h(id)`.
6. **Training tiers.** For each `T` in `TIERS_MB`, `train_{T}mb` is the shortest prefix of the training pool whose total bytes ≥ `T * 1_000_000`. Because they are prefixes of one list, each tier contains the one before it.
7. Write `data/splits/test.jsonl`, `val.jsonl`, `train_1mb.jsonl`, `train_5mb.jsonl`, `train_10mb.jsonl`, `train_20mb.jsonl` (same JSON format as before, plus field `"b"`), and `data/splits/split.stats.json` giving, for each file: sentences, letters, words (space-separated tokens), Devanagari bytes, number of groups, number of spaces, and `base_rate = spaces / (letters - sentences)`.

The group cap exists so the test set covers at least 25 different works instead of being one large purāṇa.

`GATE 4` (assert all of these in the script):
- No `group` appears in more than one of test, val, training pool.
- No `letters` string appears in more than one of test, val, `train_20mb`.
- Training pool total bytes ≥ 20,500,000.
- Test and val each contain ≥ 25 groups.
- `train_1mb` ⊂ `train_5mb` ⊂ `train_10mb` ⊂ `train_20mb` (compare `id` sets).

---

## 8. Phase 5 — Model and training

### 8.1 Encoding an example

From a sentence's spaced SLP1 string `slp`:

- `letters` = `slp` with spaces removed. This is the model input.
- `labels[i] = 1` if, in `slp`, a space follows the i-th letter; otherwise `0`.
- The last letter never has a space after it. It is excluded from the loss and from all metrics.

Worked example: `slp = "tam uvAca"` → `letters = "tamuvAca"`, `labels = [0,0,1,0,0,0,0,0]`; positions 0–6 count, position 7 (the last) is excluded.

Token id of a letter = its index in `ALPHABET` + 2. Unknown character → `UNK_ID`. Padding → `PAD_ID`.

### 8.2 `src/model.py`

```python
class Spacer(nn.Module):
    def __init__(self):
        super().__init__()
        self.tok = nn.Embedding(54, D_MODEL, padding_idx=PAD_ID)
        self.pos = nn.Embedding(MAX_LEN, D_MODEL)
        self.drop = nn.Dropout(DROPOUT)
        layer = nn.TransformerEncoderLayer(D_MODEL, N_HEAD, D_FF, DROPOUT,
                                           activation="gelu", batch_first=True, norm_first=True)
        self.enc = nn.TransformerEncoder(layer, N_LAYERS, norm=nn.LayerNorm(D_MODEL),
                                         enable_nested_tensor=False)
        self.out = nn.Linear(D_MODEL, 1)

    def forward(self, ids):                      # ids: (batch, length) int64
        pad = ids.eq(PAD_ID)
        pos = torch.arange(ids.size(1), device=ids.device).unsqueeze(0)
        x = self.drop(self.tok(ids) + self.pos(pos))
        x = self.enc(x, src_key_padding_mask=pad)
        return self.out(x).squeeze(-1)           # (batch, length) logits
```

About 3.2 million parameters. A logit above 0 means "space after this letter".

### 8.3 `src/s05_train.py`

Command line: `.venv/bin/python -m src.s05_train --tier 5 --seed 1`. Output directory: `runs/{tier}mb_s{seed}/`.

- Set `os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"` before importing torch. Device: `"mps"` if `torch.backends.mps.is_available()` else `"cpu"`.
- Seed `random` and `torch` with `SEED + seed`.
- Training data: `data/splits/train_{tier}mb.jsonl`. Validation data: `data/splits/val.jsonl`. **The training script never opens `test.jsonl`.**
- Batching, repeated every epoch: shuffle all example indices; cut the list into blocks of `BATCH_SIZE * 100`; sort each block by letter count; cut each block into batches of `BATCH_SIZE`; shuffle the order of the batches. Pad each batch to its longest example.
- Loss: `torch.nn.functional.binary_cross_entropy_with_logits` on the positions that are neither padding nor the last letter of their sentence, averaged over those positions. No class weights.
- Optimiser: `torch.optim.AdamW(model.parameters(), lr=PEAK_LR, weight_decay=WEIGHT_DECAY)`. Clip the gradient norm to `GRAD_CLIP` before each step.
- Learning rate at step `s` (first step is `s = 1`): if `s ≤ WARMUP_STEPS`, `PEAK_LR * s / WARMUP_STEPS`; otherwise `MIN_LR + 0.5 * (PEAK_LR - MIN_LR) * (1 + cos(pi * (s - WARMUP_STEPS) / (MAX_STEPS - WARMUP_STEPS)))`.
- Every `EVAL_EVERY` steps: switch to `model.eval()`, run the whole validation set under `torch.no_grad()`, predict "space" where `sigmoid(logit) ≥ 0.5`, compute boundary precision, recall and F1 (section 9), switch back to `model.train()`. Append one line to `log.jsonl`: `{"step", "train_loss" (mean since last eval), "val_loss", "val_p", "val_r", "val_f1", "lr", "elapsed_s"}`.
- If `val_f1` is the best so far, save `best.pt` containing `{"model": state_dict, "step": step, "val_f1": val_f1, "config": {all model constants}, "alphabet": ALPHABET}`.
- Stop when `step == MAX_STEPS`, or when `PATIENCE_EVALS` evaluations in a row have not improved the best `val_f1`.
- After stopping: load `best.pt`, compute validation-set probabilities once, then for each threshold `t` in `0.10, 0.15, …, 0.90` compute boundary F1. Pick the `t` with the highest F1; on a tie pick the one closest to 0.50. Write `threshold.json`: `{"threshold": t, "val_f1_at_threshold": ..., "val_f1_at_0.5": ..., "best_step": ...}`.

Run the four sizes one after another, smallest first:

```bash
for t in 1 5 10 20; do .venv/bin/python -m src.s05_train --tier $t --seed 1; done
```

Expected time on this machine: up to about one hour per run, usually less because early stopping ends the small tiers sooner.

`GATE 5` (after the 1 MB run, before starting the others): `val_f1_at_threshold` ≥ 0.60 and training loss in `log.jsonl` decreased between the first and the last evaluation. A value near `base_rate` or near 0 means a bug in label alignment or masking; fix it before training the rest.

---

## 9. Phase 6 — Evaluation

### 9.1 `src/metrics.py`

All metrics compare, for one sentence, the gold set of space positions with the predicted set. A position is the index of the letter the space follows. Both are computed over the same `letters` string.

**Boundary metrics (the headline numbers).** Summed over all sentences of the set:

- TP = positions in both gold and predicted
- FP = positions in predicted only
- FN = positions in gold only
- precision = TP / (TP + FP), recall = TP / (TP + FN), F1 = 2·P·R / (P + R). Any division by zero gives 0.

**Word metrics.** A word is a span `[start, end)` of letter indices between consecutive boundaries. A predicted word is correct when the identical span is a gold word. Word precision = correct / predicted words, word recall = correct / gold words, word F1 as above. Summed over all sentences.

**Sentence accuracy.** Fraction of sentences whose predicted set equals the gold set.

Worked example to use as a unit test — gold `tam uvAca tataH`, predicted `tamuvAca ta taH`:

- letters `tamuvAcatataH` (13 letters); gold positions `{2, 7}`; predicted positions `{7, 9}`
- TP = 1, FP = 1, FN = 1 → boundary precision 0.5, recall 0.5, F1 0.5
- gold words `[0,3) [3,8) [8,13)`; predicted words `[0,8) [8,10) [10,13)`; none identical → word precision 0, recall 0, F1 0
- sentence accuracy 0

### 9.2 `src/s06_evaluate.py`

Command line: `.venv/bin/python -m src.s06_evaluate --run runs/5mb_s1`.

Load `best.pt` and `threshold.json`. Predict on `data/splits/test.jsonl` with that threshold. Write `metrics_test.json` in the run directory:

```json
{
  "run": "5mb_s1", "threshold": 0.45, "best_step": 6500,
  "test": {"sentences": 0, "gaps": 0, "tp": 0, "fp": 0, "fn": 0,
           "boundary_p": 0.0, "boundary_r": 0.0, "boundary_f1": 0.0,
           "word_p": 0.0, "word_r": 0.0, "word_f1": 0.0, "sentence_acc": 0.0},
  "by_repo": {"sa.wikisource": {"...same fields...": 0}},
  "by_kind": {"verse": {"...same fields...": 0}}
}
```

Also write `predictions_test.jsonl` in the run directory: `{"id", "gold", "pred"}` with both as spaced SLP1.

Evaluate each run exactly once, after its training has finished. Never use test results to change a constant, a threshold or a filter.

---

## 10. Phase 7 — Report (`src/s07_report.py`)

Write `reports/results.md` containing, in this order:

1. One paragraph: what was trained, on what data, and the definition of "MB" from D4.
2. Dataset table from `split.stats.json`: one row per split file with sentences, letters, words, Devanagari MB, groups, base rate.
3. Results table, one row per tier:

   | Train size | Sentences | Best step | Threshold | Boundary P | Boundary R | Boundary F1 | Word F1 | Sentence acc. |
   |---|---|---|---|---|---|---|---|---|

   Percentages with two decimals.
4. The breakdown by `repo` and by `kind` for the 20 MB run.
5. Twenty error examples from the 20 MB run: the first twenty sentences of `predictions_test.jsonl`, ordered by `h(id)`, where `pred != gold`. Show gold and predicted in Devanagari (`slp1_to_deva`), one above the other.
6. Data provenance: Pramāṇa open release, revision hash, the three source repositories, and the note that Wikisource and SARIT texts are CC BY-SA (any redistributed derivative of the dataset must carry the same licence and credit), Ambuda texts CC0.
7. The contents of `extract.stats.json` and `audit.stats.json` as a short table of counts.

Write `reports/learning_curve.png` with matplotlib: x-axis = training size in MB on a log scale with ticks at 1, 5, 10, 20; y-axis = test score in percent; two lines with point markers, "Boundary F1" and "Word F1"; axis labels and a legend; 150 dpi.

---

## 11. Phase 8 — Command-line tool (`space.py`)

Usage: `.venv/bin/python space.py --run runs/20mb_s1 --in input.txt --out output.txt`

Input is UTF-8 Devanagari, one line of manuscript text per line. For each line:

1. Split the line into alternating **Sanskrit runs** and **separators**. A Sanskrit run is a maximal sequence of characters in the range U+0900–U+097F excluding U+0950 (ॐ), U+0964 (।), U+0965 (॥) and U+0966–U+096F (digits). Everything else is a separator.
2. If a separator consists only of whitespace, delete it and join the two runs around it into one (the model decides afresh where spaces go).
3. For each run: `s = deva_to_slp1(run)`. If `s` contains a character outside `ALPHABET`, copy the run to the output unchanged.
4. Otherwise get a probability for each letter of `s`:
   - If `len(s) ≤ MAX_LEN`: one forward pass.
   - If longer: take windows of `MAX_LEN` letters starting at letter 0, 128, 256, … for as long as the window fits entirely inside the run, then add one final window covering exactly the last `MAX_LEN` letters. From the first window use its positions 0–191; from each later window use its positions 64–191; from the final window use everything from its position 64 to its end. Every letter gets its probability from exactly one window; if two windows both cover a letter under these rules, use the earlier window.
5. Insert a space after each letter whose probability ≥ the run's threshold from `threshold.json`, except after the last letter.
6. Convert back with `slp1_to_deva` and write it. Copy non-whitespace separators through unchanged.

`GATE 8` (round-trip check, put it in `tests/` or a `--selftest` flag): for the first 200 sentences of `test.jsonl`, build the manuscript-style input `slp1_to_deva(letters)`, run it through the tool, and compare with `slp1_to_deva(pred)` for the same sentence from `predictions_test.jsonl`. At least 198 of 200 must be identical.

---

## 12. Unit tests (write these before Phase 2 and keep them passing)

`tests/test_translit.py`

| call | expected |
|---|---|
| `iast_to_slp1("tau rājaputrau kārtsnyena dharmyamākhyānamuttamam")` | `"tO rAjaputrO kArtsnyena DarmyamAKyAnamuttamam"` |
| `iast_to_slp1("oṃ namaḥ śivāya")` | `"oM namaH SivAya"` |
| `iast_to_slp1("so'pi kṛto'tra")` | `"so'pi kfto'tra"` |
| `iast_to_slp1("the quick fox")` | `None` |
| `slp1_to_deva("tam uvAca")` | `"तम् उवाच"` |
| `slp1_to_deva("tamuvAca")` | `"तमुवाच"` |
| `deva_to_slp1("तमुवाच धर्मक्षेत्रे")` | `"tamuvAca Darmakzetre"` |
| `deva_bytes("tam uvAca")` | `23` |

`tests/test_segment.py`

| input to `segment` | expected list |
|---|---|
| `"tau rājaputrau kārtsnyena dharmyamākhyānamuttamam .\nvācovidheyaṃ tatsarvaṃ kṛtvā kāvyamaninditau ..1-4-12.."` | `["tau rājaputrau kārtsnyena dharmyamākhyānamuttamam", "vācovidheyaṃ tatsarvaṃ kṛtvā kāvyamaninditau"]` |
| `"kṛto 'tra bhinnaliṅgānām || 8 ||"` | `["kṛto'tra bhinnaliṅgānām"]` |
| ``"`caraṇaśabda' ityādinā sūtrasya viṣayaṃ darśayati."`` | `["caraṇaśabda", "ityādinā sūtrasya viṣayaṃ darśayati"]` |
| `"kṣudir sampevaṇe (dhā.pā.1443) kṣudyata iti kṣudraḥ"` | `["kṣudir sampevaṇe", "kṣudyata iti kṣudraḥ"]` |
| `"Dharmakṣetre Kurukṣetre"` | `["dharmakṣetre kurukṣetre"]` |

`clean` cases:

| input to `clean` | expected |
|---|---|
| `"ahaṃ vijaā kiṃ karīadu"` | `([], "hiatus")` |
| `"iti"` | `([], "too_short")` |
| `"dharmakṣetre kurukṣetre"` | `(["Darmakzetre kurukzetre"], None)` |

`tests/test_metrics.py`: the worked example in section 9.1, plus the encoding example in section 8.1.

Run with `.venv/bin/python -m pytest tests/ -q`.

---

## 13. Order of work

| step | action | gate to pass before moving on |
|---|---|---|
| 1 | Phase 0: environment | GATE 0 |
| 2 | Write `config.py`, `src/translit.py`, `src/segment.py`, `src/metrics.py` and all tests | all tests pass |
| 3 | Phase 1: download | GATE 1 |
| 4 | Phase 2: extract | GATE 2a, 2b |
| 5 | Phase 3: audit | GATE 3 |
| 6 | Phase 4: split | GATE 4 |
| 7 | Look at 30 random lines of `train_20mb.jsonl` converted with `slp1_to_deva`; they must read as normal spaced Sanskrit | by eye; report anything odd |
| 8 | Phase 5: train 1 MB | GATE 5 |
| 9 | Phase 5: train 5, 10, 20 MB | each run has `best.pt` and `threshold.json` |
| 10 | Phase 6: evaluate all four runs | four `metrics_test.json` files |
| 11 | Phase 7: report | `results.md` and `learning_curve.png` exist |
| 12 | Phase 8: `space.py` | GATE 8 |

When finished, report: the results table, the path to `reports/results.md`, any gate that needed attention, and anything you saw in step 7 that looked wrong.

---

## 14. Rules that apply throughout

- Do not change any value in `config.py`. If you believe one is wrong, stop and say why.
- Do not open `test.jsonl` from any script except `s04_split.py` (which writes it), `s06_evaluate.py` and the `space.py` self-test.
- Do not download anything other than what Phase 1 specifies. Do not call `indike.org` endpoints.
- Do not add data augmentation, pretrained models, extra features, class weights or a different architecture.
- Do not delete `data/raw/`. Everything else under `data/`, `runs/` and `reports/` can be regenerated.
- If a script crashes, fix the script; never hand-edit a data file to get past an error.
- If the Apple GPU backend raises an "operation not implemented" error even with the fallback variable set, re-run that training with `--device cpu` (add this flag to `s05_train.py`) and note it in the final report.

---

## 15. Source registry (for reference; only the first row is used)

Checked on 2026-11-23. "Convention" is the spacing convention discussed in D3.

| source | where | format and script | convention | licence | status |
|---|---|---|---|---|---|
| Pramāṇa open release | Hugging Face dataset `srajma/pramana`; also Zenodo DOI 10.5281/zenodo.24408373 | Parquet; IAST | per document; mostly Devanagari-style | per text: CC0, CC BY, CC BY-SA, public domain | **used** — 758 Sanskrit documents, about 8.5 million words, from Sanskrit Wikisource (503 documents), Ambuda (218), SARIT (15) and mixed (22) |
| Pramāṇa live API | `https://indike.org/pramana/api/docs`; text of any work at `/pramana/api/v1/nodes/{path}/content?format=txt` | JSON, Markdown, text; IAST | per document | includes non-commercial texts (GRETIL etc.) | not used: bulk export is disallowed for automated clients in `robots.txt` |
| GRETIL | `https://gretil.sub.uni-goettingen.de/gretil/1_sanskr.zip` (296 MB) | HTML and text; IAST | mostly analytic (`kim akurvata`) | mostly CC BY-NC-SA | not used: wrong convention for this target |
| Sanskrit Wikisource dump | `https://dumps.wikimedia.org/sawikisource/latest/sawikisource-latest-pages-articles.xml.bz2` (234 MB) | MediaWiki XML; Devanagari | Devanagari-style | CC BY-SA | not used: its cleaned content is already in the Pramāṇa release; first choice if more data is needed later |
| Itihāsa | Hugging Face dataset `rahular/itihasa`, files `train.sn.csv`, `dev.sn.csv`, `test.sn.csv` | CSV; Devanagari | Devanagari-style | Apache-2.0 | not used: Rāmāyaṇa and Mahābhārata only, overlaps with the above |
| SARIT | `https://github.com/sarit/SARIT-corpus` | TEI XML; mixed scripts | per document | CC BY-SA | partly included through Pramāṇa |
| Digital Corpus of Sanskrit | `https://github.com/OliverHellwig/sanskrit` | CoNLL-U; IAST | words are stored with sandhi undone | see repository | not suitable: the text is not in its written form |
| sanskrit/raw_etexts | `https://github.com/sanskrit/raw_etexts` (3.7 GB) | mixed | mixed | none stated | not used: no licence, heterogeneous |
| sanskritdocuments.org | website | ITX and Devanagari | Devanagari-style | none stated | not used: no licence |

---

## 16. Not part of this plan

Do none of these unless separately asked: more random seeds; a tier above 20 MB; adding GRETIL after converting its spacing; comparing other architectures; handling OCR errors in the input; splitting sandhi (turning `tamuvāca` into `tam uvāca`), which is a different and harder task.
