# Sanskrit Spacer

Version 0.13.2 (26 November 2026; `spacer_reference.__version__`), released with Manuscribe 0.13.2 (whose companions
all carry the same version number), which runs its
model in the browser. `spacer.json`'s own `version` (1) is the version of its format, which Manuscribe checks a pack
against, and does not follow this one.

Repository: https://github.com/drdhaval2785/sanskrit-spacer (the folder is called `sanskrit_spacer` on the developer's
computer, beside `manuscript_ocr`). The code is under the GNU General Public License v3 ([LICENSE](LICENSE)), as
Manuscribe's is; the trained weights are published in Manuscribe's recognition packs under CC BY-SA 4.0, as the texts
they learned from are; the corpus is not kept here but downloaded and built again (`src/s01_download.py` ...).

Sanskrit manuscripts are written without spaces between words; modern printed editions need them. This project trains a small neural model that takes a line of unspaced Devanagari Sanskrit and puts the spaces back.

The model never adds, removes or changes a letter. For every gap between two adjacent letters it answers one question: *space here, yes or no?* The output is therefore always the input text with spaces inserted.

```
input : धर्मक्षेत्रेकुरुक्षेत्रेसमवेतायुयुत्सवः
output: धर्मक्षेत्रे कुरुक्षेत्रे समवेता युयुत्सवः
```

(Illustrative; actual output depends on the trained model.)

## What it does not do

- It does **not split sandhi**. It inserts spaces only where a printed Devanagari edition would, so `तमुवाच` stays joined while `तम् उवाच` is not produced. The spacing convention is that of Devanagari editions, not romanised scholarly editions (see *Spacing convention* below).
- It does **not correct OCR errors**. Characters outside the Sanskrit alphabet pass through untouched.
- It only handles Devanagari input.

## Results

Trained and tested on the same split, same model, same settings (20,000 updates of 128 sentences, seed 1). The test set is 23,782 sentences from 74 works that never appear in training.

| Train size | Boundary P | Boundary R | Boundary F1 | Word F1 | Sentence accuracy |
|---|---|---|---|---|---|
| 1 MB | 79.85% | 67.63% | 73.23% | 55.40% | 30.98% |
| 5 MB | 87.77% | 78.62% | 82.94% | 69.29% | 46.12% |
| 10 MB | 89.46% | 82.05% | 85.60% | 73.53% | 51.70% |
| 20 MB | 90.66% | 83.46% | 86.91% | 75.82% | 55.38% |
| Full (163 MB) | 92.27% | 83.83% | 87.85% | 77.46% | 57.72% |
| Full, 10 passes | 93.08% | 88.02% | **90.48%** | **81.84%** | **64.35%** |

"MB" is megabytes of the spaced training sentences in Devanagari UTF-8. "Full" is the whole cleaned training pool (1.46 million sentences); in the same 20,000 updates it saw only about 1.75 passes over the data. The last row trains the same model on the same data for 10 full passes (57,180 updates of 256 sentences, with early stopping that never triggered): the extra passes add 2.6 points of boundary F1 and 6.6 points of sentence accuracy, and the validation score was still improving slightly at the end. That row is not on the learning curve because its training budget differs from the others. Details and the breakdown by source are in [reports/results.md](reports/results.md); the learning curve is [reports/learning_curve.png](reports/learning_curve.png).

Metric definitions:
- **Boundary P / R / F1**: over all gaps, how many of the model's spaces are correct (precision), how many true spaces it found (recall).
- **Word F1**: a predicted word counts only if both its edges match a true word exactly.
- **Sentence accuracy**: the fraction of sentences with every space correct.

All numbers come from a single training run per size, so differences of about a point are not firmly established. Part of the remaining error is label noise: the training texts contain typos and editors who space differently.

## Quick start

Developed and tested only on macOS (Apple M2 Pro) with Python 3.14; `requirements.txt` pins the exact versions used. On Apple Silicon the GPU (MPS) is used automatically; otherwise the CPU.

```bash
python3 -m venv .venv
.venv/bin/pip install -r requirements.txt
```

Space a file (UTF-8, one line of manuscript text per line):

```bash
.venv/bin/python space.py --run runs/full_e10_s1 --in input.txt --out output.txt
```

Behaviour per line:
- Runs of Devanagari letters are re-spaced from scratch. Existing spaces between two runs are removed first, so input that is already partly spaced is handled.
- Dandas `।` `॥`, digits and `ॐ` are kept in place and end a run; dandas and numbers then get one space on each side, as in printed editions (`--no-punct-spacing` to skip).
- A run containing anything outside the Sanskrit alphabet is copied unchanged.
- Runs longer than 256 letters are processed in overlapping windows.

`--run` accepts any directory under `runs/` that holds `best.pt` and `threshold.json`. The best model is the 10-pass full-data run, `runs/full_e10_s1`.

Self-test (checks the tool against the saved test-set predictions):

```bash
.venv/bin/python space.py --run runs/full_e10_s1 --selftest
```

## Spacing a TEI transcription (`segment_xml.py`)

For Manuscribe TEI exports in which the OCR'd pages are marked `<pb … level="#ocr"/>`:

```bash
.venv/bin/python segment_xml.py --run auto FILE.xml [MORE.xml ...]        # in place; keeps FILE.xml.orig once
.venv/bin/python segment_xml.py --run auto --out OUT.xml FILE.xml         # write elsewhere
```

- Only pages at level `#ocr` are touched; every other page, the header and all formatting stay byte-identical.
- Only `<pb>` and `<p>`/`</p>` are word boundaries. Every other tag (`<lb>` with or without `break="no"`, `<unclear>`, `<add>`, …) is kept exactly where it is and the text flows through it, so a word split over two lines is spaced as one word.
- Spaces are inserted inside Devanagari letter runs, and every danda, double danda and number gets one space on each side, as in printed editions (`--no-punct-spacing` to skip). Latin text is left alone, no tag is modified, and no letter is ever changed (the script checks this). A boundary that falls exactly at a tag is written as a trailing space before the tag (after a closing tag), e.g. `चैव ⏎<lb n="2" break="no"/>किम…`.
- Each processed page gets `level="#segmented"` and a `<change xml:id="segmented">` entry is added once to the header (`--no-header` to skip), so re-running the script on its own output changes nothing.
- `--run auto` uses the run under `runs/` with the best test F1; pass a run directory to choose one.

## Reproducing everything

Run from the project root; every step is re-runnable. The full specification, with every constant and decision, is in [IMPLEMENTATION_PLAN.md](IMPLEMENTATION_PLAN.md).

```bash
export PYTHONPATH=.
.venv/bin/python -m pytest tests -q          # unit tests
.venv/bin/python -m src.s01_download         # ~545 MB from Hugging Face
.venv/bin/python -m src.s02_extract          # passages -> cleaned sentences
.venv/bin/python -m src.s03_audit            # drop documents with the wrong spacing convention
.venv/bin/python -m src.s04_split            # test / val / training tiers
for t in 1 5 10 20 full; do .venv/bin/python -m src.s05_train --tier $t --seed 1; done
for r in 1mb 5mb 10mb 20mb full; do .venv/bin/python -m src.s06_evaluate --run runs/${r}_s1; done
# multi-pass run on the full data (epoch mode)
.venv/bin/python -m src.s05_train --tier full --seed 1 --epochs 10 --batch 256 --eval-every 1000 --patience 12 --name full_e10_s1
.venv/bin/python -m src.s06_evaluate --run runs/full_e10_s1
.venv/bin/python -m src.s07_report
```

Each fixed-budget run takes roughly 20 to 30 minutes on an Apple M2 Pro; the number of updates is fixed, so run time does not depend on the amount of training data. The 10-pass run takes about 1 hour 50 minutes. Training speed is bound by the GPU, not by data loading: on this machine batch 256 is the fastest setting (about 2,500 sentences/s), larger batches run out of memory, and half precision is slower. Keep memory-hungry applications closed and the machine plugged in and awake while training.

## How the data is built

1. **Source.** The openly licensed part of the [Pramāṇa](https://indike.org/pramana/) library, downloaded as Parquet from Hugging Face (`srajma/pramana`, pinned revision in `config.py`). Only Sanskrit documents from Sanskrit Wikisource, SARIT and Ambuda are used (758 documents).
2. **Sentences.** Every character that is not a letter, space or avagraha ends a sentence. That covers `।`, `॥`, `|`, `||`, verse numbers, brackets and line breaks. Sentences with 12 to 240 letters are kept; longer ones are cut at word boundaries. Exact duplicates are removed.
3. **Spacing convention.** Romanised scholarly editions put spaces where Devanagari editions do not (`kim akurvata` vs `किमकुर्वत`). A document is dropped if more than 3% of its spaces fall between a consonant and a following vowel, a pattern typical of the romanised style; documents with implausible space rates or under 1,000 letters are also dropped. This keeps 560 of 758 documents.
4. **Input and target.** The target is the spaced sentence. The input is the same sentence with spaces removed. Text is converted to SLP1, in which each sound is exactly one character, so removing spaces gives exactly what a manuscript line contains (in Devanagari, `तम् उवाच` would otherwise become `तम्उवाच` rather than `तमुवाच`).
5. **Splits.** Test and validation sets are about 2.5 MB each, built from whole works (at most 100 KB per work). All recensions and commentaries of a work go to the same split, so no verse seen in training can appear in the test set. Training tiers are nested prefixes of one shuffled pool.

## Model

A character-level Transformer encoder: 4 layers, 256 dimensions, 4 attention heads, about 3.2 million parameters, one output per letter. It is trained with binary cross-entropy to predict "space follows this letter". The decision threshold is tuned on the validation set and stored in `threshold.json`.

## Project layout

```
config.py            every constant
space.py             command-line tool for plain text files
segment_xml.py       spaces the #ocr pages of a Manuscribe TEI file
src/                 pipeline steps s01..s07, model, transliteration, segmentation, metrics
tests/               unit tests
data/raw/            downloaded Parquet (kept)
data/interim/        extracted and audited sentences, audit tables
data/splits/         test, val and training files
runs/<size>_s1/      best.pt, log.jsonl, threshold.json, metrics_test.json, predictions_test.jsonl
reports/             results.md, learning_curve.png
```

## Licence and attribution

The code in this repository has no licence stated yet; add one before sharing it.

The training data keeps the licences of its sources: Sanskrit Wikisource (CC BY-SA 4.0), SARIT (CC BY-SA 3.0) and Ambuda (CC0). Any redistributed copy of the dataset or of derivative text must carry the same CC BY-SA terms and credit those sources. Models trained on the data are not covered by this note; check with a licensing adviser before redistributing them.

Data compilation: Sri Mahalingam, *Pramāṇa: an open, linked database of Indian literature and primary sources*, https://doi.org/10.5281/zenodo.24408374.

## Known limitations

- Quality depends on the spacing convention of the training texts; manuscripts or editions that space differently will score lower.
- Training data is mostly Puranic, epic, technical and commentarial prose and verse from three sources. Other genres are untested.
- About 1 in 3 sentences still contains at least one wrong space, even with the best model.
- Single training run per size; no confidence intervals.

## Reference pipeline for the browser port (2026-11-24)

`spacer_reference.py` puts word spaces into Devanagari text as pure functions, with no transliteration library: what
the JavaScript port in Manuscribe copies and is checked against. `space_text(text, network)` removes whitespace between
Sanskrit runs, splits each run into orthographic units (`units`: a consonant with its nukta, virama or vowel sign and
any candrabindu, anusvāra or visarga; or any other character with those marks), transliterates each unit to SLP1 by
table, runs the network (in windows of 256 letters every 128 for longer runs), puts a space after a unit where the
probability at its last letter reaches the threshold, and sets dandas and numbers off by one space. The network is a
function from letter ids to logits (`torch_network`, or `onnx_network` on an exported model: one exported with a free
length, as since 24 November 2026, is given the letters as they are; one exported at a fixed length is given them
padded to it).

Its parameters and tables are in `spacer.json`, built by `tools/make_spacer_json.py` from `indic_transliteration` and
checked against it on all 26,325 possible letter units (the same decision for every one; the same SLP1 wherever it
lies in the 52-letter alphabet; nukta forms fall outside it either way). Checked against `segment_xml.py`: the same
units and refusals on all 130,392 distinct runs of the OCR'd TEI files and 5,000 test sentences; the same spaced text
on 400 test sentences, 60 OCR passages and 40 single runs of 312–1,345 letters (which need windows).

**The JavaScript port** (Manuscribe's `app/js/recogspace.js`, 2026-11-24) is held to this reference by
`tools/make_spacer_fixtures.py` (`../manuscript_ocr/.venv-onnx/bin/python tools/make_spacer_fixtures.py`), which writes
459 texts to `manuscript_ocr/data/fixtures/spacer/<pack>/` (test sentences, long runs that need windows, mixed and
refused texts, random strings, hand-made edge cases, the fixture pages' blocks) with the units, the probabilities and
the spaced text the reference gives, and by Manuscribe's `tests/t-recog-spacer.js`: units and spaced text identical on
all 459, probabilities within 2·10⁻⁶.

**A stray virama gets a space after it, on purpose.** A unit with no letters, which only a stray virama makes, still
decides a space at `p[pos - 1]`: at the start of a run it reads `p[-1]` (the run's last letter), in the middle the unit
before it, so the stray virama gets a space after it, and often one before (`"्यायने"` → `"् यायने"`, as on
082328_00063_1). Found by the port and first taken for a bug; the maintainer wants it so (24 November 2026), and the
port gives the same (Manuscribe's t-recog-spacer.js checks it on the 67 fixture texts with a stray virama).
