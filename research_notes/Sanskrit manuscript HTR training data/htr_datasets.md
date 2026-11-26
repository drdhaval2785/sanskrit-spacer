# Released datasets and models for HTR of handwritten Sanskrit (Devanagari) manuscripts

Research date: 2026-11-26/27. "Verified" below means the URL returned HTTP 200 to curl or the record was read through the site's API on that date. Zenodo HTML pages return 403 to curl (bot blocking), but the same records answered through `zenodo.org/api/records/<id>`, so they are live. The CVIT site (cvit.iiit.ac.in) failed DNS on the research date.

Bottom line for the requester: only **three** public sets pair real handwritten Devanagari manuscript images with line-level transcriptions: **AnciDev**, **VedOCR** and FLAME's **Sanskrit Manuscript Layout Regimes**. Together they hold roughly 4,500 lines. Everything else I found is layout-only, printed, modern handwriting, synthetic, in another script, or announced but not released.

---

## Q1. Which academic datasets of handwritten Devanagari (Sanskrit) manuscripts with aligned transcriptions exist?

### Takeaway
Three releases have real manuscript line images and transcriptions you can download: AnciDev (3,000 lines, Hindi plus Sanskrit, 16th–19th c., licence not stated), VedOCR (681 lines from one Vedic manuscript, CC BY-NC-SA 4.0) and FLAME's Sanskrit Manuscript Layout Regimes (31 pages, 882 lines in PAGE-XML with baselines and diplomatic transcriptions; images for 16 pages included). Indiscapes/Indiscapes2 has layout only, with no text. Several well-known projects (FLAME's Vādakautūhala ground truth, Oxford/OCHS, Penn Libraries, UniLipi, Old Nepali) have **not released** their transcribed data.

### Cited Findings

**A. AnciDev (IIT Mandi / BharatGen), BHASHA 2025 workshop at IJCNLP-AACL, Dec 2025**
- The paper describes AnciDev as "comprising 3,000 transcribed text lines sourced from 500 pages of different ancient Devanagari manuscripts", in Hindi and Sanskrit. It calls itself "the first publicly available, open-source dataset" of its kind — [ACL Anthology PDF](https://aclanthology.org/2025.bhasha-1.8.pdf); [abstract page](https://aclanthology.org/2025.bhasha-1.8/) (DOI 10.18653/v1/2025.bhasha-1.8)
- Source: "National Manuscript Mission archives of historical texts spanning the 16th to 19th centuries". Genres are religious, literary and administrative. Lines were extracted by "semi-automated segmentation followed by manual verification". There was a single annotator, and a random 25% of images were independently reviewed — [paper §3.1](https://aclanthology.org/2025.bhasha-1.8.pdf)
- Splits used: 2,458 training and 627 validation line images (80:20). Note that 2,458 + 627 = 3,085, not 3,000 — [paper §4.3](https://aclanthology.org/2025.bhasha-1.8.pdf)
- Appendix Table 3 lists the manuscripts and page counts. Several are Jain or Hindi devotional works: Bhaṭṭī Kāvya (18), Gauḍīpārśvastavana/Kamalā Ārtī/Madanāṣṭaka (4), Hanumān Cālīsā (5), Śānti Pāṭha (7), Jānakī Prāta Padakam (6), Bārahkhaṛī (36), Rāmāyaṇa Bāla Kāṇḍa (65), Lāvanī Pada Saṅgraha (69), Śiva Stotra/Skanda Purāṇa/Candrakumāra Caupaī (5), **Gommaṭasāra (22)**, Kṛtibodha (25), Kiśansinha Kavi (100), Rakṣā Bandhana Kathā (7), Vicāramālā (36), **Candana-ṣaṣṭhī Vrata Kathā (18)**, **Mukhavāstrikā Carcā Dohā (7)**, **Vinatī-Saṅgraha (18)**, **Samaya Sāra Nāṭaka (8)**. These rows sum to 456 pages, not the 500 claimed — [paper Appendix A](https://aclanthology.org/2025.bhasha-1.8.pdf)
- Baselines on the test set: fine-tuned Tesseract-5 gave 30.06% CER and 87.42% WER. Attention-LSTM gave 46.33% CER and CNN-RNN 48.59% CER. TrOCR and Donut were "very discouraging" — [paper Tables 1–2, §5](https://aclanthology.org/2025.bhasha-1.8.pdf)
- Download: the GitHub README links a Google Drive folder. The folder shows one item, "National_Manuscript_Mission", modified 6 July. The repo holds scripts only, with no data and no licence file (GitHub API `license: null`). The repo was created 2025-11-21 and last pushed 2026-10-22 — [github.com/vriti2003/AnciDev](https://github.com/vriti2003/AnciDev) (verified 200); [Drive folder](https://drive.google.com/drive/folders/1wOqHgSUPieIoBwQ1ACn6ixpOxBuVo3T6?usp=sharing) (verified 200)
- Neither the paper nor the README says whether the transcription is diplomatic or normalised, what the image resolution is, or which format is used beyond "line images + train.txt/val.txt" — [README](https://github.com/vriti2003/AnciDev)

**B. VedOCR (Delhi Technological University, with IGNCA permission), DALL 2026 workshop at ICDAR 2026, Vienna, Sept 2026**
- Kaggle v1 was last updated 2026-07-06 and is licensed **CC BY-NC-SA 4.0** ("with IGNCA's permission"). It holds "681 line-level image crops paired with ground-truth Unicode Devanagari transcriptions — 41,286 character instances across 87 unique grapheme classes, including archaic conjunct consonants and Vedic tone marks". Each line was transcribed and cross-verified by "multiple Sanskrit scholars". Splits are by page: 45/5/7 of 57 pages. "Roughly 150 additional pages" are transcribed and awaiting verification for a later version. Total size is 19.2 MB — [Kaggle](https://www.kaggle.com/datasets/suyashkumarbhagat/vedocr-vedic-sanskrit-manuscript-ocr-dataset) (read via Kaggle API; verified 200)
- The source is a Pada-pāṭha Vedic Sanskrit manuscript from IGNCA on ochre-coloured paper (the authors call it "parchment"). The README says "dataset will be released under CC BY-NC-SA 4.0 upon paper acceptance", but the GitHub repo already contains `dataset/master.tsv`, 681 PNG line crops, train/val/test TSV and JSONL files, and a HuggingFace-format CSV. Fine-tuned TrOCR brought CER from 75.74% down to 48.89% — [github.com/Suyashkb/VedOCR](https://github.com/Suyashkb/VedOCR) (verified 200; 681 PNGs counted in the git tree)
- What I saw in `master.tsv` (first lines): transcriptions put a space after every akṣara (e.g. "स॒ र्व्वं च य ज्ञं॒ प रि गृ॒ ह्य …"). They keep scribal gemination after r (र्व्व, र्द्ध्य) and the anudātta U+0952. Each row carries bounding boxes x0,y0,x1,y1 for its page. A sample crop measured 1535 × 149 px RGB — [master.tsv](https://raw.githubusercontent.com/Suyashkb/VedOCR/main/dataset/master.tsv)

**C. Sanskrit Manuscript Layout Regimes (FLAME University, Pune), first release 2026; last dataset commit 2026-10-23**
- "31 pages from three Sanskrit manuscripts, with human ground truth for text-line structure, region grouping, reading direction and **diplomatic transcription**." The PAGE-XML `Baseline` (a through-line) and `Unicode` are human ground truth. The `Coords` polygons were generated from the baselines plus a CRAFT heatmap and are "sometimes imprecise" — [DATASET.md](https://github.com/flame-cai/gnn-synthetic-layout-historical/tree/main/dataset_release)
- The three manuscripts:

| Manuscript | Source | Pages | Images |
|---|---|---|---|
| Yājñavalkyasmṛti (Ācārādhyāya) | Lalchand Research Library, DAV College, Chandigarh | 15 | **withheld**: "research use permitted, redistribution not permitted"; you rebuild them from the library's viewer with `tools/prepare_images.py` |
| Muhūrta Mārtaṇḍa | eGangotri/Dharmarth Trust J&K | 7 | shipped, CC0 |
| Tantrarāja with yantras | eGangotri/Dharmarth Trust J&K | 9 | shipped, CC0 |

  — [DATASET.md §1.1, §7](https://github.com/flame-cai/gnn-synthetic-layout-historical/tree/main/dataset_release)
- There are 882 lines in all. 172 are single-node "point" lines (folio numbers, yantra cells), and 125 of the Tantrarāja's 255 lines are single glyphs. Page rasters are capped at 3,500 px on the longest side; one Yājñavalkya page is 2500 × 940 — [DATASET.md §4.2, §7.2, §10](https://github.com/flame-cai/gnn-synthetic-layout-historical/tree/main/dataset_release)
- The repo licence is GPL-3.0 (GitHub API). The repo also ships Gemini/Claude/GPT/Sarvam predictions, which are "predictions, not ground truth" — [repo](https://github.com/flame-cai/gnn-synthetic-layout-historical)

**D. FLAME's earlier case study (Vādakautūhala and others): described but NOT released**
- Chincholikar, Dwivedi, Gopalan and Awasthi, "A Case Study of HTR from Early Modern Sanskrit Manuscripts" (WSC-CSDH 2025). They annotated 50 pages of the 517-page Vādakautūhala (1721), all 16 pages of Mahāvākyārtha, and 17 pages of Dvādaśamahāvākyavicāra, all from the Lalchand Research Library. Fine-tuning EasyOCR's CNN-BiLSTM-CTC on 40 pages gave **2.3% CER / 5% GCER** on Vādakautūhala. Post-correction used ByT5-Sanskrit — [ACL Anthology PDF](https://aclanthology.org/2025.wsc-csdh.4.pdf)
- The paper's code repo has an `annotations/` folder holding only a placeholder README and no data. The README says "Development of this project is continued" in gnn-synthetic-layout-historical, and that repo's dataset does not include the Vādakautūhala pages — [github.com/flame-cai/case-study-handwritten-sanskrit-ocr](https://github.com/flame-cai/case-study-handwritten-sanskrit-ocr) (verified 200)

**E. Indiscapes / Indiscapes2 (IIIT Hyderabad): layout only, no transcriptions**
- Indiscapes2 (Palmira, ICDAR 2021) has 1,275 documents: PIH (Penn-in-Hand) 449, Bhoomi 576, ASR 61 (Telugu) and **Jain 189** ("early paper-based documents as well as palm-leaf manuscripts", 16–17 lines per page). The 9 region classes include **Character Line Segment** polygons. There are no text transcriptions, and OCR is listed as future work. The original Indiscapes had 508 documents — [ar5iv of arXiv 2108.09436](https://ar5iv.labs.arxiv.org/html/2108.09436); [Palmira page](https://ihdia.iiit.ac.in/Palmira/)
- Access is by Google Form: "To gain access to the dataset, please fill and submit this form". The repo is MIT and was last pushed 2019 — [github.com/ihdia/indiscapes](https://github.com/ihdia/indiscapes) (verified 200); [form](https://forms.gle/yjPyug3zqVumacL37) (verified 200)

**F. UniLipi (IIIT-H), ICDAR 2026: announced, data not released**
- It covers 13 Indic scripts. Training used about 2.5M synthetic lines per script (32.5M in total), rendered onto backgrounds inpainted from real manuscript lines. Lines are labelled with a **Roman WX transcription**, a script label and a glyph count. Overall CER is 6.9%. "Dataset and checkpoints: coming soon" — [ihdia.iiit.ac.in/unilipi](https://ihdia.iiit.ac.in/unilipi/); [arXiv 2608.28195](https://arxiv.org/abs/2608.28195)
- The code repo contains only a one-line README (created and last pushed 2026-05-21) — [github.com/lekhya-ai/UniLipi](https://github.com/lekhya-ai/UniLipi)

**G. Other entries: described, restricted or not usable as GT**
- **IEEE DataPort "Ancient Handwritten Devanagari Documents"** (Ramteke et al., 2025-02-01, DOI 10.21227/4s5p-fm19): 100 JPEGs in a 46.5 MB RAR, licensed CC BY 4.0. It needs an IEEE DataPort subscription, and **no transcriptions are mentioned** — [IEEE DataPort](https://ieee-dataport.org/documents/ancient-handwritten-devanagari-documents)
- **Oxford/OCHS project** (announced 2026-06-08): a Transkribus model was fine-tuned on more than 500 pages of handwritten Devanāgarī Sanskrit manuscripts from the OCHS Indic Manuscript Database, with "97% accuracy or above" expected. The announcement gives no model name, does not say whether it is public, and does not say whether the ground truth will be released. The project runs to June 2027 — [Oxford Theology news](https://www.theology.ox.ac.uk/node/4943706); [project page](https://www.theology.ox.ac.uk/digital-humanities-hindu-studies-creating-ai-models-handwriting-and-text-recognition-south-asian)
- **Penn Libraries** (article 2026-04-29): staff are building an eScriptorium/Kraken Sanskrit model from about 8 months of ground truth made on an 18th-century Sanskrit manuscript (Ms. Coll. 390 Item 2478). The article states no release, page count or accuracy — [Penn Libraries news](https://www.library.upenn.edu/news/handwritten-text-recognition)
- **Old Nepali (Devanagari script, not Sanskrit)**: Sarawgi, Garces Arias and Zotter (arXiv 2512.17111, Dec 2025) report 4.9% CER, but "the dataset we used for evaluation is confidential". Only code is released — [arXiv](https://arxiv.org/abs/2512.17111)

**H. Competitions**
- I found no ICDAR or ICFHR competition on historical Devanagari manuscripts. The ICDAR 2023 IHTR competition covered 10 scripts including Devanagari, but its data is modern handwriting (page marked "All Rights Reserved") — [IHTR 2023](https://ilocr.iiit.ac.in/ihtr/). The only historical Indic competition found was ICDAR REID 2017/2019, which is printed Bengali — [heiDATA REID2019 GT](https://doi.org/10.11588/DATA/AIQSXL)

### Inferences
- About 4,500 public real-manuscript Devanagari lines exist in total (AnciDev ~3,000, VedOCR 681, FLAME 882 including ~172 single glyphs). That is smaller than a few of the requester's own hands.
- The transcription conventions differ. VedOCR spaces every akṣara and carries Vedic accents, and FLAME is diplomatic, so both need converting to the requester's convention before training. VedOCR's akṣara spacing would teach a spacing model the wrong word breaks; stripping those spaces leaves continuous text without word division. AnciDev's convention is unknown and needs inspection.
- AnciDev mixes Hindi (Old Hindi/Braj devotional verse) with Sanskrit. To keep only Sanskrit, filter by manuscript title. Its five Jain works (Gommaṭasāra, Samayasāra Nāṭaka and others) are the closest match in the inventory to Jain paper manuscripts. From their titles, some are likely in Prakrit or Old Hindi rather than Sanskrit; this is an inference, not stated in the paper.
- AnciDev's 30% best CER, and its declared single annotator, suggest noisy or very hard lines. Check the quality before mixing it in.
- VedOCR's NC licence would bar any commercial reuse. ShareAlike would force a CC BY-SA-compatible licence on derived models or data.
- The `image_path` column in VedOCR's master.tsv points at MorphBG-binarised page images. The crops may therefore be binarised rather than original colour; check before use.

### Gaps
- I did not download the AnciDev Drive folder, so its file format, image resolution, transcription convention and any licence file inside it are unverified.
- The licence of FLAME's labels, as distinct from its code (GPL-3.0) and source images (CC0 or restricted), is not stated in the sections I read.
- I found no released Jain-manuscript HTR ground truth apart from the AnciDev Jain titles. Indiscapes2's "Jain" collection has layout only.
- IIT Kanpur, "Akṣara", "Bhoomi" (only a collection inside Indiscapes) and "Pratham": nothing relevant was found under these names.

---

## Q2. Transkribus / READ-COOP: public Devanagari or Sanskrit models and ground truth

### Takeaway
Every public Transkribus model for Devanagari that I found is for **printed** text (Naval Kishore Press letterpress and lithographs, from Heidelberg). Only one of them has downloadable training data: heiDATA EGOKEI, ALTO, CC BY 4.0. I found no public handwritten-Devanagari Sanskrit model. The only public handwritten Sanskrit manuscript model is for Pracalit script (Nepal), which is not Devanagari.

### Cited Findings
- **Devanagari mixed M1A**: model ID 45909, PyLaia, by Nicole Merkel-Hilf (UB Heidelberg), published 2022-11-05. Languages are Awadhi, Braj, Hindi and Sanskrit; printed Naval Kishore Press, 19th–20th c. Trained on 209 pages, 26,598 words, **4,333 lines**, with 2.2% validation CER — [transkribus.org/models/devanagari-mixed-m1a](https://www.transkribus.org/models/devanagari-mixed-m1a) (verified 200)
- **Devanagari Lithography NKP M4**: model ID 509677, PyLaia, published 2026-02-12. Braj, Hindi and Sanskrit lithographs; trained on 79 pages, 20,519 words and 1,890 lines, with 5.58% CER. The page does not mention downloadable training data — [transkribus.org/models/devanagari-lithography-nkp-m4](https://www.transkribus.org/models/devanagari-lithography-nkp-m4) (verified 200)
- Older CITlab HTR+ models "Devanagari mixed M1" (2018-06-08, 5.58% CER per a search snippet) and "Devanagari_nagara_M1" (1.77% CER per a search snippet) now return 404 — [devanagari-mixed-m1](https://www.transkribus.org/models/devanagari-mixed-m1), [devanagarinagaram1](https://www.transkribus.org/models/devanagarinagaram1)
- **Downloadable GT**: "Ground Truth data for printed Devanagari" (heiDATA, DOI 10.11588/DATA/EGOKEI, 2022-10-26). JPG plus ALTO, about 220 pages and 27,000 words, 4,333 lines (as listed in HTR-United). Licence CC BY 4.0; "Diplomatic transcription, no correction of misspelling"; 18 per-book zips — [heiDATA](https://doi.org/10.11588/DATA/EGOKEI) (verified 200); [HTR-United catalogue](https://htr-united.github.io/)
- The Heidelberg FID4SA dataverse "Ground truth data for HTR on South Asian Scripts" holds exactly 4 datasets: printed Devanagari (EGOKEI), printed Malayalam, printed Bengali (REID), and Pracalit Sanskrit/Newar manuscripts — [heiDATA FID4SA-GT](https://heidata.uni-heidelberg.de/dataverse/FID4SA-GT) (read through the API)
- **Pracalit to IAST**: model ID 628689, PyLaia, by A. J. O'Neill (Musashino Univ.), published 2026-09-01. Classical Nepal Bhasa and Sanskrit; the output is IAST. Trained on 202 pages and 1,448 lines, with 9.91% CER. It does not use Devanagari script — [transkribus.org/models/pracalit-to-iast](https://www.transkribus.org/models/pracalit-to-iast) (verified 200)
- The Oxford/OCHS handwritten Devanāgarī model (see Q1-G) has no public listing — [Oxford news](https://www.theology.ox.ac.uk/node/4943706)

### Inferences
- EGOKEI's 4,333 lines match M1A's 4,333 training lines exactly, so EGOKEI is almost certainly M1A's training set.
- The printed NKP data could serve as pretraining material for glyph shapes, but it is print, not a scribal hand.

### Gaps
- The full Transkribus public-model list (app.transkribus.org) is not crawlable by these tools. A private or newly published handwritten Devanagari model could exist without showing up in search.

---

## Q3. eScriptorium / HTR-United / Kraken (Zenodo ocr_models)

### Takeaway
None of them has a handwritten Devanagari or Sanskrit entry. The HTR-United catalogue contains only printed Devanagari, and the Kraken model community on Zenodo has no Indic models at all.

### Cited Findings
- I downloaded and searched `htr-united.yml`: 16,047 lines, last commit 2026-10-19, HEAD 682d3eb. Only **two** entries carry `iso: Deva`. One is "Ground truth data for printed Devanagari" (EGOKEI, `script-type: only-typed`). The other is "Projet Exposition universelle de 1878", a French printed book with some Devanagari, also `only-typed`. There is no manuscript Devanagari entry and no other Indic script except printed Malayalam — [HTR-United catalogue](https://htr-united.github.io/); [raw yml](https://raw.githubusercontent.com/HTR-United/htr-united/master/htr-united.yml)
- The Zenodo `ocr_models` community (the Kraken model repository) held 86 records on 2026-11-27. Searches for devanagari, sanskrit, hindi, nepal, newar, pracalit, sharada, grantha, nandinagari and indic returned **0 hits**, and listing all 86 titles and languages showed no Indic entries — [Zenodo ocr_models](https://zenodo.org/communities/ocr_models) (read through the API)
- **kraken_devanagari** (shreeshrii, 2020): an experimental model trained with kraken 2.0.8 on synthetic printed data. The author notes Kraken's segmentation "fails for certain types of Devanagari page images" — [github.com/shreeshrii/kraken_devanagari](https://github.com/shreeshrii/kraken_devanagari) (verified 200)
- Penn Libraries' eScriptorium Sanskrit model is in progress and unreleased (Q1-G) — [Penn Libraries](https://www.library.upenn.edu/news/handwritten-text-recognition)

### Inferences
- Publishing the requester's own CC BY-SA ground truth to HTR-United or Zenodo would be the first handwritten Devanagari entry in both catalogues.

### Gaps
- Models shared privately on individual eScriptorium instances are not discoverable.

---

## Q4. Comparison table: what each candidate holds and whether it can be used for training

### Takeaway
For ground truth that needs no new typing: AnciDev, if its terms are cleared with the authors; VedOCR, for non-commercial use only; and FLAME's set. Treat the rest as pretraining, layout, or nothing.

### Cited Findings

| Name (version/date) | Script / language | Kind | Size | Transcription style | Alignment / format | Images | Licence / access | URL | Usable as HTR GT? |
|---|---|---|---|---|---|---|---|---|---|
| AnciDev (BHASHA 2025; repo pushed 2026-10-22) | Deva / Hindi + Sanskrit | Handwritten MSS, 16th–19th c. (NMM) | 3,000 lines / "500" pages (456 itemised) | not stated | line images + txt splits | not stated | **none stated**; Google Drive | [repo](https://github.com/vriti2003/AnciDev) | Yes, but confirm the licence |
| VedOCR v1 (Kaggle 2026-07-06; DALL@ICDAR 2026) | Deva / Vedic Sanskrit (Pada-pāṭha) | Handwritten MS (IGNCA) | 57 pages, 681 lines, 41,286 chars | diplomatic, accents kept, spaces between akṣaras | line crops + TSV/JSONL with bounding boxes | e.g. 1535×149 crop | **CC BY-NC-SA 4.0** | [Kaggle](https://www.kaggle.com/datasets/suyashkumarbhagat/vedocr-vedic-sanskrit-manuscript-ocr-dataset), [GitHub](https://github.com/Suyashkb/VedOCR) | Yes (NC); re-space the text |
| FLAME Sanskrit Manuscript Layout Regimes (first release; 2026-10-23) | Deva / Sanskrit | Handwritten MSS (3) | 31 pages, 882 lines | **diplomatic** | **PAGE-XML with baselines** + layout graph | ≤3500 px; 16 pages shipped, 15 withheld | images CC0 (16 pp) / research-only (15 pp); repo GPL-3.0 | [repo](https://github.com/flame-cai/gnn-synthetic-layout-historical/tree/main/dataset_release) | Yes |
| FLAME VK/MV/DMV case study (WSC-CSDH 2025) | Deva / Sanskrit | Handwritten MSS | 83 annotated pages | — | — | — | not released | [paper](https://aclanthology.org/2025.wsc-csdh.4.pdf) | No |
| Indiscapes2 (ICDAR 2021) | multiple Indic incl. Jain collection | Handwritten MSS | 1,275 docs | **no text** | region and line polygons | — | request form | [repo](https://github.com/ihdia/indiscapes) | Layout only |
| UniLipi (ICDAR 2026) | 13 Indic scripts | real + 32.5M synthetic lines | — | WX romanisation | line-level | — | "coming soon" | [page](https://ihdia.iiit.ac.in/unilipi/) | Not yet |
| IEEE DataPort Ancient Handwritten Devanagari (2025-02-01) | Deva / unstated | Handwritten MSS | 100 images | none stated | images only | — | CC BY 4.0 but subscription required | [DataPort](https://ieee-dataport.org/documents/ancient-handwritten-devanagari-documents) | No |
| Oxford/OCHS (2026-06-08) | Deva / Sanskrit | Handwritten MSS | >500 pages GT | — | Transkribus | — | not released | [news](https://www.theology.ox.ac.uk/node/4943706) | No (ask) |
| Old Nepali (arXiv 2512.17111) | Deva / Old Nepali | Handwritten docs | — | — | lines | — | confidential | [arXiv](https://arxiv.org/abs/2512.17111) | No |

Sources: rows as cited in Q1–Q3.

### Inferences
- Line images with bounding boxes (VedOCR) and PAGE-XML baselines (FLAME) both slot into a line-recogniser pipeline. FLAME's polygons are machine-made, so crop from the baselines.
- The requester's GitHub repos (devanagari-manuscript-ocr, manuscribe-models) appear in GitHub search results for "Devanagari manuscript"; they are the requester's own and are excluded here.

### Gaps
- AnciDev's image resolution and transcription conventions are unverified.

---

## Q5. Related non-Devanagari scripts (brief, all NON-DEVANAGARI)

### Takeaway
The only real manuscript HTR ground truth in a related script is the Pracalit (Nepālākṣara/Newar) set from SOAS. The Śāradā, Modi and Nandinagari items found are synthetic or glyph-level only. I found no Grantha line GT.

### Cited Findings
- **Pracalit, Sanskrit + Newar MSS, 16th–19th c.** (O'Neill, SOAS), NON-DEVANAGARI. Zenodo 6967421 (2022-08-05, v1, CC BY 4.0): PNG plus XML Transkribus export of four manuscripts, 441 training and 242 validation pages, transcribed in Pracalit Unicode as scriptio continua; 504 MB zip. Mirrored on heiDATA (DOI 10.11588/DATA/WI9184) and described in JOHD (DOI 10.5334/johd.90) — [Zenodo API record](https://zenodo.org/api/records/6967421); [heiDATA](https://doi.org/10.11588/DATA/WI9184) (verified 200); [JOHD](https://doi.org/10.5334/johd.90) (verified 200). There was a follow-up talk, "Revisiting HTR for Nepalese Manuscripts in Pracalit Script" (2025-10-04) — [Zenodo 17268040](https://zenodo.org/records/17268040)
- **Lipi** (Kathmandu Univ., Zenodo 24240673, 2026-11-15, CC BY 4.0), NON-DEVANAGARI and glyph-level only: 16,350 glyph images in 327 classes covering Brahmi, Licchavi, Bhujimol, **Nandinagari**, Maithili/Tirhuta, Tibetan and Kirat — [Zenodo API record](https://zenodo.org/api/records/24240673)
- **Śāradā / Modi**: only synthetic folios found, e.g. varunbhoyar/indic-historical-manuscripts (CC BY 4.0, machine-generated) and SarthDhakade963/indic-manuscript-dataset. The latter says "Modi and Sharada text is transliterated from Devanagari … not verified by a native reader" — [HF varunbhoyar](https://huggingface.co/datasets/varunbhoyar/indic-historical-manuscripts); [HF SarthDhakade963](https://huggingface.co/datasets/SarthDhakade963/indic-manuscript-dataset)

### Gaps
- No Grantha or Śāradā manuscript line ground truth found.

---

## Q6. Printed-book, modern-handwriting and synthetic Devanagari sets (out of scope, one line each)

### Takeaway
These suit pretraining or post-correction only, not ground truth for scribal hands.

### Cited Findings
**Printed Sanskrit / Devanagari**
- Heidelberg printed Devanagari GT (EGOKEI, 2022, CC BY 4.0, ALTO, 4,333 lines, Hindi/Sanskrit/Braj) — [heiDATA](https://doi.org/10.11588/DATA/EGOKEI)
- PE-OCR Sanskrit (Maheshwari et al., Findings of EMNLP 2022): post-edited OCR text plus 500 test images with GT from three printed books (Brahmasūtra-bhāṣya, Grahalāghava, Golādhyāya); no licence file — [github.com/ayushbits/pe-ocr-sanskrit](https://github.com/ayushbits/pe-ocr-sanskrit)
- Shirorekha line/word masks for 125 PE-OCR pages (Zenodo 20663949, 2026-06-12, CC BY 4.0). The record calls them "manuscript folios", but they come from PE-OCR's printed books, and the record holds masks only, no text — [Zenodo API record](https://zenodo.org/api/records/20663949)
- IIIT-H sanskrit-ocr / IndicOCR (Dwivedi et al., CVPRW 2020; MIT): printed classical Sanskrit, models on Drive. IHDIA calls it a printed OCR, although the FLAME paper describes Dwivedi 2020 as a "dataset of Sanskrit manuscripts annotated at the line level" — [github.com/ihdia/sanskrit-ocr](https://github.com/ihdia/sanskrit-ocr); [IHDIA](https://ihdia.iiit.ac.in/)
- IIT Bombay OCR team's Tesseract-5 Sanskrit models, trained on 7,000 synthetic and 3,000 printed lines (per AnciDev's footnote) — [cse.iitb.ac.in/~ocr](https://www.cse.iitb.ac.in/~ocr/)
- HF text and typed sets: cfilt/RoundTripOCR-sanskrit, Process-Venue/Sanskrit-OCR-Typed-Dataset, tkamle/typed_sanskrit_multiline_dataset, chronbmm/sanskrit-ocr-postcorrection (text only, 208k sentences) — [HF search](https://huggingface.co/datasets?search=sanskrit)

**Modern handwriting (Devanagari, not manuscripts)**
- IIIT-HW-Dev (DAS 2018): about 95K handwritten word images. The CVIT page was unreachable on the research date; a derived copy is on HF — [HF c3rl/IIIT-HW-Hindi](https://huggingface.co/datasets/c3rl/IIIT-HW-Hindi)
- IIIT-INDIC-HW-WORDS (ICDAR 2021), word-level — [HF c3rl/IIIT-INDIC-HW-WORDS-Hindi](https://huggingface.co/datasets/c3rl/IIIT-INDIC-HW-WORDS-Hindi)
- CHIPS / PLATTER (Kasuba et al., IIT Bombay, arXiv 2502.06172, Feb 2025): page-level handwriting in 10 Indic languages, said to be released — [arXiv](https://arxiv.org/abs/2502.06172)
- DohaScript (arXiv 2602.18089, Feb 2026): 531 writers copying the same six Hindi dohās; release not confirmed — [arXiv](https://arxiv.org/abs/2602.18089)

**Synthetic "manuscript" Devanagari**
- Sourav-Kulkarni/synthetic-devanagari-manuscripts (CC BY-NC-SA 4.0): GRETIL Sanskrit rendered as reed-pen pages with line polylines and text — [HF](https://huggingface.co/datasets/Sourav-Kulkarni/synthetic-devanagari-manuscripts)
- Dozens of near-identical student "synthetic manuscript generator" sets for Devanagari, Modi and Śāradā (Aug–Nov 2026), e.g. latentabhigyan/synthetic-indic-manuscripts — [HF search "manuscript"](https://huggingface.co/datasets?search=manuscript)

### Gaps
- I did not inspect the HF typed and synthetic sets for licence or quality, since they are out of scope.
