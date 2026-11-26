# Muktabodha's e-texts outweigh every released Devanagari dataset

Only one online source pairs images of handwritten Devanagari Sanskrit manuscripts with existing full transcriptions at a scale worth a training run. It is **Muktabodha's set of diplomatic e-texts typed from eGangotri's scans**, mostly of manuscripts in the Raghunath Temple library, Jammu. Eight of those manuscripts still have live CC0 or public-domain scans on archive.org. Together they cover **about 1,630 transcribed folio sides, which I estimate at roughly 20,000 lines**. The e-texts mark each folio side, and in the one text checked they keep the manuscript's own line breaks. That is exactly the page-text-with-line-breaks input your pairing step turns into line ground truth. The licence is the catch. The e-texts are **CC BY-NC 4.0, and Muktabodha states that the non-commercial term covers AI training**, so they cannot go into CC BY-SA weights without its written permission.

Everything else ready-made is small. Three research datasets have real manuscript line images: AnciDev (3,000 lines, no licence), FLAME's Sanskrit Manuscript Layout Regimes (882 lines in PAGE-XML, 566 of them with CC0 images) and VedOCR (681 lines, CC BY-NC-SA). They add up to **about 4,500 lines, fewer than your own 6,000**. Western catalogues and editions add line-anchored fragments, such as Cambridge's catalogue excerpts and two British Library witnesses of a Vahnipurāṇa chapter, and nearly all of these are non-commercial too. **No source pairs a Jain manuscript's images with a full transcription.** The largest handwritten Devanagari Sanskrit ground truth, Oxford/OCHS's 500+ pages, is unreleased. Image-paired material you could put into CC BY-SA weights today without asking anyone amounts to a few hundred lines, and even that comes with caveats. Wikisource, Commons, Ambuda, the crowdsourcing platforms, HTR-United and Transkribus's public models hold nothing usable.

## Eleven sources, ranked by lines, alignment and domain fit

The ranking weighs three things:

- how many lines a source yields with images attached;
- whether its text keeps the manuscript's own readings and line breaks, so your pairing step works without hand alignment;
- how close its hands are to 15th–19th-century paper manuscripts.

Licence sits in its own column. It decides what can ship, not what helps a model learn. Counts are from the research notes. Where they are estimates, the table says so.

| # | Source | Script, language, contents | Size with images | Diplomatic? Line-aligned? | Licence for CC BY-SA weights | Links |
|---|---|---|---|---|---|---|
| 1 | Muktabodha diplomatic e-texts + eGangotri scans | Devanagari (at least one Śāradā exception). Sanskrit tantric and Śaiva works. Paper manuscripts from the Raghunath Temple (Jammu), UPSS and Rashtriya Sanskrit Sansthan (Lucknow) | 8 MSS with live scans: ~1,630 folio sides, ~20,000 lines (estimate). 44 MSS and ~5,800 sides if withdrawn scans are recovered | Diplomatic since Nov 2023. No word spaces. `pṛ0 1a)` marks each folio side. Manuscript line breaks kept in the text checked | **No, not without permission.** Text CC BY-NC 4.0, with NC explicitly covering AI training. Scans CC0 or Public Domain Mark | [IAST zip](https://muktalib7.com/DL_CATALOG_ROOT/MUKTABODHA-LIBRARY-IAST.zip), [Devanagari zip](https://muktalib7.com/DL_CATALOG_ROOT/MUKTABODHA-LIBRARY-DEVANAGARI.zip), [scans](https://archive.org/details/dharmarthtrustjkcollectionbyegangotri) |
| 2 | AnciDev (IIT Mandi, BHASHA 2025) | Devanagari. Sanskrit plus Hindi (and, judging by title, Prakrit/Old Hindi Jain works). National Mission for Manuscripts (NMM) archives, 16th–19th c. | 3,000 line crops (3,085 in the splits) from "500" pages (456 itemised) | Line images + text. Convention unstated. One annotator | **Unclear.** No licence in the paper, repo or README. NMM clearance unknown | [repo](https://github.com/vriti2003/AnciDev), [data](https://drive.google.com/drive/folders/1wOqHgSUPieIoBwQ1ACn6ixpOxBuVo3T6?usp=sharing), [paper](https://aclanthology.org/2025.bhasha-1.8.pdf) |
| 3 | FLAME Sanskrit Manuscript Layout Regimes (2026) | Devanagari Sanskrit: Muhūrtamārtaṇḍa, Tantrarāja with yantras, Yājñavalkyasmṛti | 31 pages, 882 lines. 16 pages and 566 lines ship with images | Diplomatic. Human baselines and Unicode text in PAGE-XML | **Mostly.** eGangotri images CC0. Labels sit under the repo's GPL-3.0. Yājñavalkya images are research-only | [DATASET.md](https://github.com/flame-cai/gnn-synthetic-layout-historical/blob/main/dataset_release/DATASET.md) |
| 4 | VedOCR (DTU, DALL@ICDAR 2026) | Devanagari. Vedic Sanskrit pada-pāṭha. One IGNCA manuscript | 57 pages, 681 lines | Diplomatic, with svara marks. A space after every akṣara. Line crops with boxes | **No.** CC BY-NC-SA 4.0 | [Kaggle](https://www.kaggle.com/datasets/suyashkumarbhagat/vedocr-vedic-sanskrit-manuscript-ocr-dataset), [GitHub](https://github.com/Suyashkb/VedOCR) |
| 5 | Cambridge Digital Library catalogue excerpts | Devanagari Sanskrit, including Jain works. Incipit, explicit and colophon in IAST | ~10 anchored lines per MS. Total not counted (estimate: 2,000–4,000 partial lines) | Diplomatic. `[1v4]` anchors give folio, side and line. Lines often partial | **No.** Images and metadata CC BY-NC 4.0 | [example manifest](https://cudl.lib.cam.ac.uk/iiif/MS-ADD-02432), [conventions](https://www.repository.cam.ac.uk/handle/1810/326907) |
| 6 | Muktabodha e-texts of IFP paper transcripts | 20th-c. handwritten Devanagari copies, mostly of Grantha originals. Śaiva works | 69 e-texts. The transcript collection is ~210,000 pages | Page markers. Word-spaced, so not diplomatic. Transcript line breaks appear kept | **No.** Images CC BY-NC-ND 3.0 or "All Rights Reserved". Text CC BY-NC | [IFP access page](https://muktalib7.com/DL_CATALOG_ROOT/IFP_CATALOG/access_page.htm) |
| 7 | Vahnipurāṇa edition (Charles Li) | Devanagari Sanskrit. British Library IO SAN 1425 (1589) and IO SAN 1001 (Benares 1804) | 17 pages, 127 lines | Full diplomatic TEI with `pb` and numbered `lb`. IAST | **No.** TEI and images CC BY-NC-SA 4.0 | [repo](https://github.com/tst-project/siberupakhyana), [images](https://api.nakala.fr/datas/10.34847/nkl.a8fej594) |
| 8 | Texts Surrounding Texts (TST) project paratexts | ~26 BnF/Hamburg files in Devanagari hands. Colophons and headers, not all Sanskrit | ~340 lines (174 in one file) | Diplomatic TEI. `lb` plus `facs` page pointers | **Text yes** (CC BY-SA 4.0). BnF image terms not checked | [tst-project/mss](https://github.com/tst-project/mss) |
| 9 | Suśruta Project, BL IOLR Taylor 1842 | Devanagari Sanskrit. Ḍalhaṇa's commentary | 18 pages, 157 lines. **No images found** | Diplomatic TEI with `pb` and `lb` | **Text yes** (CC BY-SA 4.0) | [repo](https://github.com/wujastyk/sushrutaproject) |
| 10 | Nepalese-German Manuscript Cataloguing Project (NGMCP) excerpts | ~15,800 entries. ~52% Devanagari in a 160-entry sample | A few lines per MS | Semi-diplomatic IAST. Folio references, no line numbers | **Unclear.** Text licence not stated. Scans bought from the Staatsbibliothek zu Berlin (SBB) | [mirror](https://tylergneill.github.io/ngmcp-wiki-mirror/), [ordering](https://list.indology.info/pipermail/indology/2024-December/059992.html) |
| 11 | Bodleian South Asian catalogue | Devanagari Sanskrit. Incipits and explicits in IAST | A few lines per MS | Folio reference only | **No or unclear.** TEI has no licence. Images CC BY-NC 4.0, with a request not to re-host | [TEI](https://github.com/bodleian/south-asian-mss), [terms](https://digital.bodleian.ox.ac.uk/terms/) |

Three rules sit behind the licence column:

- **NC material (BY-NC, BY-NC-SA, BY-NC-ND) cannot be relicensed under CC BY-SA**, and CC BY-SA lets anyone reuse your weights commercially. Whether trained weights legally count as an adaptation of their training data is unsettled. The conservative course is to keep NC data out of released weights unless the rights holder agrees. Muktabodha has removed that ambiguity for its own texts.
- **Data with no licence, like AnciDev, is all rights reserved by default.** Its authors may in turn need permission from the NMM libraries their pages came from.
- **GPL-3.0 on FLAME's repository is a software licence, and it may not be the licence of the labels.** It is worth asking FLAME to state a Creative Commons licence for them.

## Muktabodha's Jammu e-texts hold about 20,000 lines behind an NC clause

Muktabodha's Varanasi office typed its e-texts "from manuscript images made available to the public by the generosity of the eGangotri organisation". From the June 2023 batch onward it noted that "word breaks (or lack of word breaks) is as in the devanagari manuscripts" ([Indology, Jun 2023](https://list.indology.info/pipermail/indology/2023-June/057803.html)). In November 2023 it announced 13 tantric e-texts as "diplomatic transcriptions of the manuscripts they are transcribed from" and revised five earlier ones to the same standard ([Indology, Nov 2023](https://list.indology.info/pipermail/indology/2023-November/058476.html)).

The whole library is an official download in two zips, IAST (41.9 MB) and Devanagari (48.0 MB), so no scraping is needed ([IAST zip](https://muktalib7.com/DL_CATALOG_ROOT/MUKTABODHA-LIBRARY-IAST.zip); [Devanagari zip](https://muktalib7.com/DL_CATALOG_ROOT/MUKTABODHA-LIBRARY-DEVANAGARI.zip)). In the IAST zip, **44 e-texts name a source manuscript** and carry folio-side markers. The manuscripts are in the Raghunath Temple, UPSS, Rashtriya Sanskrit Sansthan or Dogra Art Museum collections. Together these e-texts hold about **5,800 folio sides and 72,700 text lines**; that rough count includes some table-of-contents lines.

The e-texts are laid out like this:

- Each header gives the manuscript number and often the archive.org link.
- Markers such as `pṛ0 2ba)` open each folio side.
- The text runs on without spaces and breaks mid-word. In the Ūrdhvāmnāya, for example, a line ends "…pravakṣyāmiyatmātvaṃparipṛchasi ta / syaśravaṇamātreṇa…", so the e-text lines appear to follow the manuscript's lines ([IAST zip](https://muktalib7.com/DL_CATALOG_ROOT/MUKTABODHA-LIBRARY-IAST.zip)).

That is page-level text with line breaks, which your pipeline already handles. Line-break fidelity has been checked on only one text, however. Confirm it per manuscript by running your pairing and reading the residuals.

**Images are the weak link.** Five archive.org items linked from e-text headers have since been withdrawn: they return `is_dark` with no files. They include Ānandeśvarapaddhati 5520 and Navārṇacaṇḍīpañcāṅga 4818 ([archive.org metadata](https://archive.org/metadata/AnandeshwarPaddhatiWithPujasOfManyDevatasIncludingSharikaSharadaAndKubjika5520Al)). Eight items are confirmed live:

| Manuscript | Folio sides |
|---|---|
| [Āgamakalpalatā 4914](https://archive.org/details/AgamaKalpalataYadunathSharma4914Alm22Shlf3DevanagariTantra) | 607 |
| [Bagalāmukhīpañcāṅga 6025](https://archive.org/details/BagulaMukhiPanchangamAlm27Shlf16025DevanagariTantra) | 302 |
| [Mṛgendravṛtti 4387](https://archive.org/details/MrigendraVrittiBhattNarayanKantha4387Alm20Shlf4DevanagariTantra) | 275 |
| [Svātantryadīpikā](https://archive.org/details/SwatantryaDeepikaMansaRamMonghaAlm5593DevanagariTantra) | 220 |
| [Parāmbārcanacandrikā UPSS 1322](https://archive.org/details/1322UPSSParambarchanaChandrikaDevanagari) | 131 |
| [Ūrdhvāmnāya 4894](https://archive.org/details/Urdhvamnaya4894Alm22Shlf2DevanagariTantra) | 68 |
| [Śrīgurustutiratnāvalī 1307k](https://archive.org/details/ShriGuruStutiRatnavaliGovindKaulDiscipleOfSahibKaul57671307KaAlmira26Shlf1DevanagariTantra) | 19 |
| [Tattvaśodhana UPSS 2042](https://archive.org/details/2042UPSSTattvaShodhanaDevanagari) | 10 |

That makes **about 1,630 sides**. The 44 texts average about 12.5 lines per side (72,700 lines over 5,800 sides). At that rate the eight live manuscripts give **roughly 20,000 lines**, more than four times all the released research sets together. This is my arithmetic, not a count: median lines per side run from 4 to 36 across the texts.

The live items carry CC0 or the Public Domain Mark, set by the uploader; the Ūrdhvāmnāya has no licence field. The eGangotri Raghunath collection holds 532 items, 492 of them under CC0 and 477 with "Devanagari" in the title ([collection](https://archive.org/details/dharmarthtrustjkcollectionbyegangotri)). More pairs appear wherever an e-text's manuscript number matches a live item.

Two traps need attention. Raghunath MS 3887, the source of e-text M00630, is titled Śāradā on archive.org. Some files labelled diplomatic were typed from printed books: M00660 was "Copied from volume 34 of the K.S.T.S. series". Read every header, and use the latest revision. These are Brahmanical paper manuscripts in a north Indian hand, so they suit your base model better than a Jain fine-tune.

**The licence closes the door for released weights.** Every one of the 499 files in the zip says "Use of this material (e-texts) is covered by Creative Commons license BY-NC 4.0" ([IAST zip](https://muktalib7.com/DL_CATALOG_ROOT/MUKTABODHA-LIBRARY-IAST.zip)). Muktabodha's new library site adds: "The non-commercial terms above also apply to training AI or machine-learning models on E-Text material" ([Muktabodha about](https://muktabodha-digital-library.org/about)). The website's general terms are stricter still and conflict with the per-file licence: "intended solely for personal use", and no "screen scraping" ([Muktabodha terms](https://muktabodha.org/terms-and-conditions/)). The images are clean and the text is not. Internal experiments that never ship stay within NC. Releasing CC BY-SA weights trained on these texts needs Muktabodha's written permission.

A second Muktabodha pairing is bigger but harder to use. Sixty-nine e-text headers name an IFP/EFEO transcript; the Candrajñānāgama, for example, cites "IFP/EFEO transcript T0012". These e-texts carry page markers like "p. 327)" that match the transcript pages. Their lines appear to follow the transcript's lines, but words are separated by spaces ([IAST zip](https://muktalib7.com/DL_CATALOG_ROOT/MUKTABODHA-LIBRARY-IAST.zip)).

The transcripts are 1,144 volumes, about 210,000 pages, "clearly written in ink on paper in the well-known Devanagari script". Most were copied from Grantha palm leaves, and they are available as DjVu and PDF after registration ([IFP access page](https://muktalib7.com/DL_CATALOG_ROOT/IFP_CATALOG/access_page.htm)). Their licence is contradictory: the legacy page says CC BY-NC-ND 3.0, while the new site says "©2023 … All Rights Reserved" ([Muktabodha about](https://muktabodha-digital-library.org/about)). The tidy 20th-century hand adds one more hand type. It does not add the period letter forms your manuscripts show.

Muktabodha's new 75-manuscript project with IFP works directly from Grantha palm leaves, so it yields nothing in Devanagari ([Muktabodha](https://muktabodha.org/75-saiva-texts-in-new-project-with-ifp-2/)).

## Three research datasets total 4,500 lines, fewer than your own 6,000

**AnciDev is the largest set and the closest to your Jain domain, and its terms are the least clear.** It has 3,000 transcribed lines from NMM archive manuscripts of the 16th to 19th centuries: religious, literary and administrative texts. Lines were cut by semi-automated segmentation and checked by hand. A single annotator did the work, and a random 25% was independently reviewed ([paper](https://aclanthology.org/2025.bhasha-1.8.pdf)).

The appendix lists Jain titles: Gommaṭasāra (22 pages), Candana-ṣaṣṭhī Vrata Kathā (18), Vinatī-Saṅgraha (18), Samaya Sāra Nāṭaka (8) and Mukhavastrikā Carcā Dohā (7). They sit next to Hindi devotional works such as the Hanumān Cālīsā and the Lāvanī Pada Saṅgraha. Going by their titles, several of the Jain works are Prakrit or Old Hindi rather than Sanskrit; the paper does not state the language line by line. A Sanskrit-only model would have to filter by title.

Its best baseline was fine-tuned Tesseract at **30.06% CER and 87.42% WER**, which points to hard or noisy lines. The set also averages six lines per page (3,000 lines over 500 pages), fewer than a manuscript page holds, which suggests not every line was transcribed. Treat it as line-level data, not page-level.

The data sits in a Google Drive folder named "National_Manuscript_Mission". The repository holds only scripts, and GitHub reports `license: null` ([repo](https://github.com/vriti2003/AnciDev); [Drive](https://drive.google.com/drive/folders/1wOqHgSUPieIoBwQ1ACn6ixpOxBuVo3T6?usp=sharing)). Its transcription convention is unknown, because nobody in this research opened the Drive folder.

**FLAME's Layout Regimes release is the best documented of the three, and the only one with clearly licensed images.** It has 31 pages from three manuscripts. Human ground truth covers the baselines and a "diplomatic transcription" in PAGE-XML. The region outlines (`Coords` polygons) were generated from those baselines and a CRAFT heatmap and are "sometimes imprecise", so crop from the baselines ([DATASET.md](https://github.com/flame-cai/gnn-synthetic-layout-historical/blob/main/dataset_release/DATASET.md)).

The Muhūrtamārtaṇḍa (7 pages, 311 lines) and the Tantrarāja (9 pages, 255 lines) are eGangotri scans, shipped under CC0. The Yājñavalkyasmṛti (15 pages, 316 lines) comes from the Lalchand Research Library and is withheld: "research use permitted, redistribution not permitted". You rebuild those images from the library's viewer with `tools/prepare_images.py`.

Of the 882 lines, 172 are single-point "lines" such as folio numbers and yantra cells. In the Tantrarāja, 125 of the 255 lines are single glyphs. The CC0 part therefore holds about 440 real text lines at most. Jyotiṣa tables and yantra diagrams make it a hard test set rather than bulk training data.

FLAME's recogniser is a CNN-BiLSTM-CTC, the same architecture as yours, so its error rates compare directly with your own ([repo](https://github.com/flame-cai/gnn-synthetic-layout-historical)).

**VedOCR is the cleanest-verified set and the furthest from your domain.** It has 681 line crops from 57 pages of one pada-pāṭha Vedic manuscript held by IGNCA: 41,286 characters in 87 grapheme classes, including Vedic tone marks. Several Sanskrit scholars cross-checked the transcriptions, and the train/validation/test split is by page, 45/5/7 ([Kaggle](https://www.kaggle.com/datasets/suyashkumarbhagat/vedocr-vedic-sanskrit-manuscript-ocr-dataset)). Kaggle states **CC BY-NC-SA 4.0** "with IGNCA's permission". The GitHub README still promises release on paper acceptance, but the data is already in the repository ([GitHub](https://github.com/Suyashkb/VedOCR)).

The transcription puts a space after every akṣara, as in "स॒ र्व्वं च य ज्ञं॒ प रि गृ॒ ह्य …". It keeps doubled consonants after r and the anudātta sign ([master.tsv](https://raw.githubusercontent.com/Suyashkb/VedOCR/main/dataset/master.tsv)). The `image_path` column points at MorphBG-binarised pages, so check whether the crops are binarised too. One hand, Vedic accents and an NC-SA licence make it the least valuable of the three for you.

All three need converting to your own label convention. Combined, they come to about 4,500 lines, fewer than the 6,000 you have already corrected across ten hands.

## Catalogues and editions offer line-anchored fragments, mostly non-commercial

**Cambridge has the most usable catalogue excerpts, and they include Jain manuscripts.** The catalogue records of the Sanskrit Manuscripts Project carry an "Excerpts" field. It holds diplomatic transcriptions of the rubric, incipit, explicit and colophon, each tagged with folio, side and line. For MS Add.2432, a ten-folio Devanāgarī Śṛṅgāratilakaṭīkā dated 1844 CE, an excerpt reads "[1v4] bāhu dvau ca \ mṛ / ṇālamāsyakamalaṃ … śṛoṇītīrtha[1v5]śilā" ([manifest](https://cudl.lib.cam.ac.uk/iiif/MS-ADD-02432)). Images come through IIIF at up to 7921 × 4969 px. Both images and metadata are **CC BY-NC 4.0**.

The anchors map straight onto your segmented line numbers. Excerpts usually start or stop partway through a line, though, so partial lines must be cropped or aligned. The text is IAST and uses editorial signs, which the project documents ([conventions](https://www.repository.cam.ac.uk/handle/1810/326907)):

- (!) for scribal errors;
- 〚 〛 for deletions;
- \ / for insertions;
- `_` for virāma.

Jain items are catalogued too: MS Add.2313 is tagged Sanskrit, Jaina, Vyākaraṇa ([manifest](https://cudl.lib.cam.ac.uk/iiif/MS-ADD-02313)). That makes Cambridge one of the very few places with Jain-manuscript lines whose text is already typed. Nobody counted the yield, because the site's HTML blocks scripts. At about ten anchored lines per manuscript, a few hundred Devanagari items would give **2,000–4,000 partial lines**, which is an estimate.

**Charles Li's Vahnipurāṇa edition is the only full diplomatic transcription with downloadable images.** The edition "includes diplomatic transcriptions of all witnesses", linked to images where they exist ([edition](https://tst-project.github.io/siberupakhyana)). Two British Library Devanagari witnesses have images on Nakala:

- IO SAN 1425: 8 pages, 60 lines; its colophon gives saṃvat 1646;
- IO SAN 1001: 9 pages, 67 lines; written in Benares in 1804.

A BORI witness (5 pages, 44 lines) has no images ([repo](https://github.com/tst-project/siberupakhyana)). The TEI marks pages and lines as `<pb n="146v" facs="1"/>` and `<lb n="5"/>`, and the text is in IAST. Both the TEI and the IO SAN 1425 images are **CC BY-NC-SA 4.0** ([Nakala](https://api.nakala.fr/datas/10.34847/nkl.a8fej594)). At 127 lines, it is a clean test set, not training data.

**Two sources carry the right licence but lack usable images.** In the Suśruta Project, the only Devanagari witness is BL IOLR Taylor 1842, a diplomatic TEI file of 18 pages and 157 lines under CC BY-SA, with no image link. The main witnesses (KL 699, NAK 1-1079, NAK 5-333) are in Newar script ([repo](https://github.com/wujastyk/sushrutaproject)). If the British Library supplies Taylor 1842 images on compatible terms, those 157 lines become the only licence-clean diplomatic Devanagari Sanskrit set from any edition.

The TST project's repository is CC BY-SA 4.0. About 26 of its files, from BnF and Hamburg manuscripts in Devanagari hands, hold about 340 transcribed lines of colophons and headers; BnF NAF_8895 alone has 174. These files point to the BnF's digitised images, whose reuse terms were not checked. Not every file is in Sanskrit ([tst-project/mss](https://github.com/tst-project/mss)).

**Folio-only catalogues need a recognition pass before they give ground truth.** The Bodleian's TEI catalogue on GitHub has 3,025 files and no licence. It gives IAST incipits and explicits located by folio, such as "F. 3v", and links to Digital Bodleian images, which are CC BY-NC 4.0 with a request not to re-host them ([GitHub](https://github.com/bodleian/south-asian-mss); [terms](https://digital.bodleian.ox.ac.uk/terms/)).

NGMCP has about 15,800 entries. Each gives semi-diplomatic IAST excerpts (Beginning, Sub-colophon, End) with references like "(fol. 108r) (exp. 005)". In a 160-entry sample, 84 were Devanagari ([mirror](https://tylergneill.github.io/ngmcp-wiki-mirror/)). Scans are bought from the Staatsbibliothek zu Berlin by microfilm number ([ordering](https://list.indology.info/pipermail/indology/2024-December/059992.html)). Without line numbers, you would have to run the recogniser and fuzzy-match each excerpt. That is a correction pass, not free ground truth.

**For Jain manuscripts, no source online pairs images with a full transcription.** Kobā holds about 250,000 manuscripts, supplies photocopies to scholars on request, and has no online images ([Kobā](https://www.kobatirth.org/gyan-tirth/gyanmandir/manuscripts/)). Its catalogue, the *Kailāsa Śrutasāgara Granthasūcī*, lets you look a work up by its opening or closing sentence ([Granthasūcī](https://jainqq.org/explore/018025/15)). The L. D. Institute's printed catalogue gives "Beg." lines ([jainqq](https://jainqq.org/explore/018007/168)). JAINpedia offers downloadable images marked CC0 1.0, but the "Transcription" tab was empty on the page sampled ([JAINpedia](https://jainpedia.org/manuscript/section-1)). For manuscripts you already hold, the opening and closing sentences in the Kobā and L. D. catalogues can fill in the first and last lines without typing. That is only a few lines per manuscript, but they come from the same manuscripts.

## The largest handwritten sets are unreleased, and the crowd platforms are empty

**The material worth asking for is held by four groups:**

- **Oxford/OCHS** fine-tuned a Transkribus model on "more than 500 pages of handwritten, digitised manuscripts from the OCHS Indic Manuscript Database" and expects "97% accuracy or above". The project runs to June 2027 and has said nothing about releasing ground truth ([Oxford news](https://www.theology.ox.ac.uk/node/4943706); [project page](https://www.theology.ox.ac.uk/digital-humanities-hindu-studies-creating-ai-models-handwriting-and-text-recognition-south-asian)).
- **FLAME's earlier case study** annotated **83 Lalchand pages**: 50 of the Vādakautūhala (1721), all 16 of the Mahāvākyārtha and 17 of the Dvādaśamahāvākyavicāra. Fine-tuning a CNN-BiLSTM-CTC on 40 pages reached **2.3% CER** on the Vādakautūhala. The repository's annotations folder holds only a placeholder ([paper](https://aclanthology.org/2025.wsc-csdh.4.pdf); [repo](https://github.com/flame-cai/case-study-handwritten-sanskrit-ocr)).
- **Penn Libraries** is building an eScriptorium/Kraken Sanskrit model from about eight months of ground truth on Ms. Coll. 390 Item 2478. No release has been stated ([Penn news](https://www.library.upenn.edu/news/handwritten-text-recognition)). The collection's OPenn images are public domain item by item ([OPenn](https://openn.library.upenn.edu/Data/0002/html/mscoll390_item825.html)), so a Penn release could be licence-clean.
- **The Sanskrit Library's NEH project** reports 1,063 transcribed pages of Brown and Penn manuscripts, aligned at passage level and unpublished. That figure comes from a search snippet of the final report, which I could not open ([NEH page](https://sanskritlibrary.org/neh2012dev.html); [report](https://core.ac.uk/download/147825347.pdf)).

Two smaller items are pending. VedOCR has about 150 more pages awaiting verification, which would keep the NC-SA licence. UniLipi's data is "coming soon"; it consists of synthetic lines labelled in WX romanisation ([UniLipi](https://ihdia.iiit.ac.in/unilipi/)).

**Platform and catalogue checks came back empty:**

- **Wikisource:** Sanskrit Wikisource has 538 Index pages and all of them are printed books; Hindi and Gujarati Wikisource have no manuscript Index either ([sa.wikisource API](https://sa.wikisource.org/w/api.php?action=query&list=allpages&apnamespace=106&aplimit=max&format=json)).
- **Wikimedia Commons:** a few hundred Sanskrit and Devanagari manuscript images, with no transcriptions attached ([Commons](https://commons.wikimedia.org/wiki/Category:Sanskrit-language_manuscripts)).
- **Ambuda:** proofreads printed books; its one handwriting project is a single empty page ([Ambuda](https://ambuda.org/proofing/handwrittentexttext/)).
- **Crowdsourcing:** Zooniverse has no Sanskrit projects ([API](https://www.zooniverse.org/api/projects?search=sanskrit)), and FromThePage's Sanskrit hits are English archival papers ([FromThePage](https://fromthepage.com/findaproject?search=sanskrit)).
- **HTR-United:** lists only printed Devanagari ([HTR-United](https://htr-united.github.io/)).
- **Zenodo's Kraken model community:** none of its 86 models are Indic ([Zenodo](https://zenodo.org/communities/ocr_models)).
- **Transkribus:** every public Devanagari model is trained on print ([M1A](https://www.transkribus.org/models/devanagari-mixed-m1a)).
- **Hugging Face:** the "manuscript" datasets are synthetic ([example](https://huggingface.co/datasets/varunbhoyar/indic-historical-manuscripts)).

**Layout data, restricted holdings and other scripts are dead ends too:**

- **Indiscapes2** includes 189 Jain documents but gives only layout polygons ([repo](https://github.com/ihdia/indiscapes)).
- **IEEE DataPort's "Ancient Handwritten Devanagari Documents"** is 100 images with no transcriptions, behind a subscription ([DataPort](https://ieee-dataport.org/documents/ancient-handwritten-devanagari-documents)).
- **Documenta Nepalica** keeps original line breaks under CC BY-SA, but it is mostly Nepali-language legal documents, and its facsimiles need written permission from the National Archives of Nepal ([HAdW](https://www.hadw-bw.de/en/nepal)).
- **The Old Nepali HTR dataset** is confidential ([arXiv](https://arxiv.org/abs/2512.17111)).
- **Lalchand, IGNCA, BORI and Gyan Bharatam** offer images only, under no-reproduction, all-rights-reserved, subscription or view-only terms ([IGNCA](https://ignca.gov.in/?p=114720); [BORI](https://edesiderata.crl.edu/resources/bhandarkar-oriental-research-institute-bori-digital-library)).
- **SOAS's Pracalit ground truth** (441 training and 242 validation pages, CC BY 4.0) is the best-licensed manuscript HTR set in the region, but it is in Pracalit script, not Devanagari ([Zenodo](https://zenodo.org/records/6967421)).
- **DHARMA's diplomatic editions** are in Oriya and Bhujimol script ([GitHub](https://github.com/erc-dharma/tfd-sanskrit-philology)).

**Several collections offer images under licences compatible with yours, but no transcriptions:**

- Penn OPenn (Public Domain Mark);
- Wellcome (CC BY or Public Domain Mark, item by item) ([Wellcome](https://wellcomecollection.org/works/n5usb8kq));
- the University of Tokyo (CC BY 4.0) ([UTokyo](https://da.dl.itc.u-tokyo.ac.jp/portal/en/collection/skt_manuscripts));
- the eGangotri collections (CC0);
- the Ganesh Varni Digambar Jain collection on archive.org (CC0, including 30 items with "manuscript" in the title) ([archive.org](https://archive.org/details/ganeshvarnilibrary)).

They hold no existing transcriptions. They are where your predict-and-correct loop can produce data you are free to release.

**Printed-book data is useful only for pretraining on letter shapes.** Heidelberg's printed Devanagari ground truth has 4,333 lines over about 220 pages of Naval Kishore Press Hindi, Sanskrit and Braj. It is ALTO, diplomatic and CC BY 4.0, and it was the training set of Transkribus's M1A model, which reached 2.2% CER ([heiDATA](https://doi.org/10.11588/DATA/EGOKEI)). PE-OCR covers three printed Sanskrit books and has no licence ([GitHub](https://github.com/ayushbits/pe-ocr-sanskrit)). Ambuda has about 51,700 proofread printed pages ([Ambuda](https://ambuda.org/proofing/)).

## Conclusion: fetch three things, ask five groups, skip the rest

**Fetch first:**

1. **The two Muktabodha zips and the eight live archive.org items.** Run your pairing on the Ūrdhvāmnāya 4894 (68 sides) to confirm that the e-text lines match your segmented lines, then on the Āgamakalpalatā 4914 (607 sides). Keep the results in internal experiments that never ship. They will also show whether 20,000 north Indian lines are worth the permission request.
2. **FLAME's `dataset_release`.** Hold its 16 CC0 pages out as a hard-layout test set, cropping from the baselines.
3. **AnciDev's Drive folder.** Inspect its transcription convention and lines per page, and pull out its Jain titles as a Jain-domain test set. Do not put it into released weights.

VedOCR is optional, worth taking only if you want a Vedic-accent test set.

**Ask:**

- **Muktabodha:** written permission to train and release CC BY-SA weights on the 44 eGangotri-based diplomatic e-texts, copies of the withdrawn scans, and which e-texts keep the manuscript's line breaks.
- **OCHS Oxford** (Wernicke-Olesen and Wong): a PAGE-XML export of their 500+ pages under CC BY or CC BY-SA.
- **FLAME:** the 83 Vādakautūhala-group pages, a Creative Commons licence for the labels, and whether Lalchand permits released models.
- **AnciDev's authors:** a licence, and clearance from the NMM.
- **Penn Libraries:** the Item 2478 ground truth. Its images are already public domain, so it could be released clean.

**Skip:**

- Wikisource, Commons, Ambuda and the crowdsourcing platforms;
- HTR-United, Zenodo's Kraken models, Transkribus's public models and the Hugging Face synthetic sets;
- Indiscapes, IEEE DataPort, Documenta Nepalica and the Old Nepali set;
- Lalchand, IGNCA, BORI and Gyan Bharatam;
- the Kobā, L. D. Institute and JAINpedia catalogues, beyond their opening and closing lines;
- the Pracalit, DHARMA and Newar Suśruta material.

The deeper finding is that your own corpus is already the field's largest open handwritten Devanagari Sanskrit ground truth. Your 6,000 corrected lines from ten hands exceed every released real-manuscript Devanagari set combined. Neither HTR-United nor Zenodo's Kraken community lists a single handwritten Devanagari ground-truth set, so publishing yours there under CC BY-SA would make it the reference dataset. Existing transcriptions top out at NC data that needs permission. The licence-clean way to grow is therefore CC0 and public-domain images (eGangotri, OPenn, the Ganesh Varni Jain collection) run through your correct-the-predictions loop. Jain paper manuscripts in particular will come from your own work or from nowhere.
