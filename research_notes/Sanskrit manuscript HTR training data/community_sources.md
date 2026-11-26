# Community, crowd-sourced and open-repository sources of Devanagari Sanskrit manuscript scans paired with typed transcriptions

Research date: 2026-11-26/27. Counts were taken live from site APIs or listing pages on those dates unless stated otherwise. Scope: handwritten Sanskrit manuscripts in Devanagari. Printed-book corpora are summarised in one paragraph at the very end.

Short version for the report writer: **no community platform holds a usable body of page-aligned, line-broken transcriptions of Devanagari Sanskrit manuscripts.** Sanskrit Wikisource has no manuscript Index at all (538 indexes, all printed books). Hindi and Gujarati Wikisource have none either. Ambuda has one empty one-page test project. Zooniverse and FromThePage have nothing. Wikimedia Commons has a few hundred manuscript images and no attached transcriptions. The real pairs come from three places. (a) Small open research datasets on GitHub: VedOCR (57 pages, 681 lines), FLAME's PAGE-XML release (31 pages, 882 lines) and AnciDev (500 pages, 3,000 lines). (b) Muktabodha's "diplomatic" e-texts typed from manuscript images that eGangotri put on archive.org: tens of manuscripts, text-level pairs, no confirmed line breaks, CC BY-NC. (c) The Wikisource + Transkribus manuscript workflow, which has been proven on Balinese palm-leaf manuscripts but never used for Sanskrit/Devanagari.

---

## 1. Sanskrit, Hindi and other Wikisources: do Index:/Page: namespaces built on handwritten manuscripts exist?

### Takeaway
No. All 538 Index pages on Sanskrit Wikisource are typed "book" and are printed editions. Hindi and Gujarati Wikisource searches found no manuscript Index either. Two Sanskrit-Wikisource manuscript efforts exist on paper. One grant claims "4 manuscripts uploaded", but nothing reached the Index namespace. The other proposal (LipiSetu-2) was not funded. Wikisource could host page-by-page manuscript proofreading, and it can now use Transkribus HTR, but for Devanagari Sanskrit this is possible only in principle.

### Cited Findings
- **Sanskrit Wikisource namespaces and size.** Page namespace = `पृष्ठम्` (ns 104) and Index namespace = `अनुक्रमणिका` (ns 106). Site statistics on 2026-11-26: 165,563 pages in all namespaces, 20,453 articles, 18 active users, 64 local files. — [sa.wikisource siteinfo API](https://sa.wikisource.org/w/api.php?action=query&meta=siteinfo&siprop=namespaces|statistics&format=json)
- **Index count.** Sanskrit Wikisource has **538 Index pages** (full `list=allpages` enumeration of ns 106). — [allpages API, ns 106](https://sa.wikisource.org/w/api.php?action=query&list=allpages&apnamespace=106&aplimit=max&format=json)
- **Index types.** I downloaded the wikitext of all 538 Index pages and parsed the `Proofreadpage_index_template` fields. 449 have `Type=book` and 89 have no Type field; no index has any other Type. The `Progress` codes are: OCR 392, C 39, T 6, V 5, MS 4, L 3, none 89. I did not check the labels sa.wikisource attaches to these codes. — same API, `prop=revisions&rvprop=content` on all 538 titles ([API endpoint](https://sa.wikisource.org/w/api.php))
- **Keyword scan for manuscript terms.** I searched all 538 index wikitexts for manuscript/handwrit/हस्तलिखित/हस्तप्रत/पाण्डुलिपि/पांडुलिपि/मातृका/हस्तलेख/पोथी. There was one hit, `अनुक्रमणिका:समयमातृका.pdf`, a false positive: Kṣemendra's *Samayamātṛkā*, Nirṇayasāgara, Bombay, 1888, a printed book. — [sa.wikisource API](https://sa.wikisource.org/w/api.php)
- **Commons metadata of the scan files.** I pulled the Commons metadata (categories and description) of 300 of the 538 index files through the sa.wikisource `imageinfo/extmetadata` proxy. None is a manuscript. The only matches were:
  - `Sanskrit Catalogue.djvu`, a printed catalogue (Rice 1884, *Catalogue of Sanskrit Manuscripts in Mysore and Coorg*).
  - `Ashtavakra Gita Handwritten Translation By Vinod Kad.djvu`, which returned no file metadata. The file appears to be missing; this is a modern handwritten translation, not a manuscript.

  The common categories are "Scans from the Internet Archive", "PD-scan", "Sanskrit-language books" and "Uploaded with IA Upload". — [sa.wikisource API](https://sa.wikisource.org/w/api.php)
- **The other 238 titles.** I could not query their metadata because of rate limits, but every title is an identifiable printed edition: Kāvyamālā, TSS, Nirṇayasāgara, Bālamanoramā volumes, Rāmāyaṇa volumes and so on. — titles from the [allpages listing](https://sa.wikisource.org/w/api.php?action=query&list=allpages&apnamespace=106&aplimit=max&format=json)
- **Local uploads.** The 63 files uploaded locally to sa.wikisource are 2011-era illustration JPGs, logos and about ten printed-book PDFs/DjVus. None is a manuscript. — [allimages API](https://sa.wikisource.org/w/api.php?action=query&list=allimages&ailimit=100&aiprop=size|user|timestamp|mime&format=json)
- **Rapid Fund grant ID 21976965**, "Digitization of manuscripts and other material for Sanskrit Wikisource and Wikipedia". The final report says "Uploaded 4 Manuscripts", but it gives no titles, scripts or page counts. The link targets did not survive extraction. Its reported outputs are about 22 Sanskrit Wikipedia articles, not Wikisource transcriptions. — [Final Report](https://meta.wikimedia.org/wiki/Grants:Programs/Wikimedia_Community_Fund/Rapid_Fund/Digitization_of_manuscripts_and_other_material_for_Sanskrit_Wikisource_and_Wikipedia_%28ID:_21976965%29/Final_Report)
- **The grantee's Wikisource work.** In the visible part of the grantee's contributions (NehalDaveND, 2020-05 to 2026-10), the Wikisource edits are Page/Index edits on printed books (`Dvisandhanam kavya.pdf`, `श्रीमच्छङ्करदिग्विजयः.djvu`, `शुक्लयजुर्वेदीयवैदिकवास्तुशान्तिप्रयोगः.pdf`, `वैशेषिकदर्शनम्.djvu`). No title is a manuscript. — [usercontribs API](https://sa.wikisource.org/w/api.php?action=query&list=usercontribs&ucuser=NehalDaveND&uclimit=500&ucprop=title|timestamp|sizediff&format=json)
- **"Project LipiSetu – 2" (2026).** The proposal was to transcribe "10 Manuscripts and 20 Rare Books" in archaic Devanagari and Śāradā into modern Devanagari for Sanskrit Wikisource, with a target of 30 Wikisource items. Status: **Not funded**. The applicant wrote "I can't give any timeline". — [Meta proposal](https://meta.wikimedia.org/wiki/Community_Resources_and_Partnerships/India_Rapid_Project/Project_LipiSetu_-_A_Research_Project_for_Digitizing_and_Decoding_Sanskrit_Manuscripts_-_2)
- **Hindi Wikisource namespaces.** Page = `पृष्ठ` (ns 250) and Index = `विषयसूची` (ns 252). — [hi.wikisource siteinfo](https://hi.wikisource.org/w/api.php?action=query&meta=siteinfo&siprop=namespaces&format=json)
- **Hindi Wikisource search.** A full-text search for हस्तलिखित OR पांडुलिपि OR manuscript in the Index, Category and Project namespaces gives 5 hits. The only Index is `विषयसूची:हस्तलिखित हिंदी पुस्तकों का संक्षिप्त विवरण.pdf` (Type=book), a printed catalogue of Hindi manuscripts. A project page, `विकिस्रोत:हिंदी विकिस्रोत क्षमता निर्माण कार्यशाला 14 नवंबर 2025`, covers digitising and proofreading manuscripts at a 14 Nov 2025 workshop; its content timed out and was not read. — [hi.wikisource search API](https://hi.wikisource.org/w/api.php?action=query&list=search&srsearch=%E0%A4%B9%E0%A4%B8%E0%A5%8D%E0%A4%A4%E0%A4%B2%E0%A4%BF%E0%A4%96%E0%A4%BF%E0%A4%A4%20OR%20%E0%A4%AA%E0%A4%BE%E0%A4%82%E0%A4%A1%E0%A5%81%E0%A4%B2%E0%A4%BF%E0%A4%AA%E0%A4%BF%20OR%20manuscript&srnamespace=252|14|4&srlimit=50&format=json)
- **Gujarati Wikisource** (relevant because Jain manuscripts are often catalogued in Gujarat). A search for હસ્તપ્રત ("manuscript") gives 13 hits, all main-namespace Gujarati printed texts that merely mention a manuscript. There is no manuscript Index. — [gu.wikisource search API](https://gu.wikisource.org/w/api.php?action=query&list=search&srsearch=%E0%AA%B9%E0%AA%B8%E0%AB%8D%E0%AA%A4%E0%AA%AA%E0%AB%8D%E0%AA%B0%E0%AA%A4&srnamespace=106|0|4|14&srlimit=30&format=json)
- **Transkribus on Wikisource.** The Wikimedia Foundation added Transkribus as a third OCR/HTR engine on Wikisource, specifically to allow transcription of handwritten documents in under-resourced languages. It started with Balinese manuscripts and was meant to extend to "more languages" later. — [Transkribus blog](https://blog.transkribus.org/en/preserving-cultural-heritage-transkribus-integration-with-wikimedia-projects); [Phabricator T326385](https://phabricator.wikimedia.org/T326385); [Wikisource Loves Manuscripts](https://meta.wikimedia.org/wiki/Wikisource_Loves_Manuscripts)
- **The Balinese model case** (not Devanagari), as reported in search snippets: a workshop in May 2023 transcribed 63 manuscript pages; in September 2024, 10 participants transcribed more than 86 pages from 3 lontar bundles on Balinese Wikisource. The baseline Transkribus model used 50 pages of ground truth. WiLMa digitised more than 28,000 manuscript pages from 10 collections in 2023 (Balinese, Javanese, Indonesian). — [WiLMa Updates](https://meta.wikimedia.org/wiki/Wikisource_Loves_Manuscripts/Updates); [WiLMa Report](https://meta.wikimedia.org/wiki/Wikisource_Loves_Manuscripts/Report); [Open GLAM Medium post](https://medium.com/open-glam/balinese-wikisource-wikipustaka-gives-a-new-life-to-palm-leaf-manuscripts-e04ba87e9ec1)
- **WiLMa Learning Partners Network.** The South Asian participant it names is an Assamese Wikimedian working on manuscripts of Assam's Satras. No Sanskrit or Devanagari partner is listed. — [WiLMa Learning Partners Network](https://meta.wikimedia.org/wiki/Wikisource_Loves_Manuscripts/Learning_Partners_Network)
- **Bulk download.** The Sanskrit Wikisource XML dumps are online (HTTP 200 on 2026-11-26) and include `sawikisource-latest-pages-articles.xml.bz2`. — [dumps.wikimedia.org/sawikisource/latest/](https://dumps.wikimedia.org/sawikisource/latest/)
- **API rate limits.** Repeated anonymous API calls during this research were refused with "You are making too many requests to the API". Bulk work should use dumps or throttled, identified clients. — [Wikimedia API rate limits](https://www.mediawiki.org/wiki/Wikimedia_APIs/Rate_limits)

### Inferences
- **Expected yield from Wikisource: 0 manuscript pages and 0 lines today**, on Sanskrit, Hindi and Gujarati Wikisource alike.
- **Wikisource as a host for the requester's own work.** Wikisource's Page: model (one wiki page per scan page; the wikitext keeps typed newlines; a 4-level proofread status; CC BY-SA 4.0 text over PD scans on Commons) fits page-level ground truth with line breaks. The Transkribus engine makes HTR-assisted proofreading possible. The requester could seed Sanskrit Wikisource with their own manuscripts, which would make them a source for others, but there is nothing to harvest now.
- **The grant's "4 manuscripts"** were probably uploaded to Commons only, not transcribed. They did not create any Index page.

### Gaps
- I could not read the 14 Nov 2025 Hindi Wikisource workshop page (timeout), so I don't know whether any Hindi/Sanskrit manuscript Index came out of it. The search results suggest none exists yet.
- Metadata for 238 of the 538 sa.wikisource files was not fetched because of rate limiting; I judged them by title only.
- I did not survey other Indic Wikisources (Marathi, Bengali, Nepali, Odia) or the multilingual wikisource.org for Sanskrit-in-Devanagari manuscripts.
- I could not confirm the labels of the sa.wikisource Progress codes (T/V/C/MS/L/OCR).

---

## 2. Wikimedia Commons: categories of Devanagari Sanskrit manuscripts with transcriptions attached

### Takeaway
Commons holds only a few hundred Sanskrit and Devanagari manuscript images in its manuscript categories, mostly Wellcome Collection images. I found no case of a transcription attached to a Commons manuscript file. Transcriptions on Wikimedia live in Wikisource Page: namespaces, and none exist for these files. Commons is a source of images, not of pairs.

### Cited Findings
- `Category:Sanskrit-language manuscripts`: **133 files, 17 subcategories**. — [Commons categoryinfo API](https://commons.wikimedia.org/w/api.php?action=query&prop=categoryinfo&titles=Category:Sanskrit-language_manuscripts|Category:Sanskrit_Manuscripts,_Wellcome_Collection|Category:Sanskrit_manuscripts&format=json); [category page](https://commons.wikimedia.org/wiki/Category:Sanskrit-language_manuscripts)
- `Category:Sanskrit Manuscripts, Wellcome Collection`: **143 files, 5 subcategories**. — [Commons categoryinfo API](https://commons.wikimedia.org/w/api.php?action=query&prop=categoryinfo&titles=Category:Sanskrit-language_manuscripts|Category:Sanskrit_Manuscripts,_Wellcome_Collection|Category:Sanskrit_manuscripts&format=json)
- `Category:Sanskrit manuscripts`: 0 files and 0 subcategories. It appears to be an empty or redirect category. — same API call
- `Category:Manuscripts in Devanagari`: **78 files, 2 subcategories**. The subcategories are `Category:Rasikapriya` (37 files, a Braj/Hindi work) and `Category:梵文般若心経` (1 file). — [Commons API](https://commons.wikimedia.org/w/api.php?action=query&generator=categorymembers&gcmtitle=Category:Manuscripts_in_Devanagari&gcmtype=subcat&prop=categoryinfo&format=json)
- `Category:Jain manuscripts`: **41 files, 5 subcategories**. — [Commons API](https://commons.wikimedia.org/w/api.php?action=query&prop=categoryinfo&titles=Category:Jain_manuscripts&format=json)
- Commons subcategories found by title search include `Astasahasrika Prajnaparamita manuscript (Wellcome Sanskrit Epsilon 1)` and `Pancaraksa manuscript (Wellcome Or Sanskrit MS delta 33)`, both Nepalese Buddhist manuscripts, and `Sanskrit language Grantha manuscript`. — [Commons category search](https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=14&srlimit=40&srsearch=intitle:Sanskrit%20intitle:manuscripts&format=json)
- A full-text search of Commons File pages for "Sanskrit manuscript Devanagari transcription" gives 17 hits, all printed catalogues or books (British Museum catalogue, Gough's *Papers relating to … Sanskrit literature*, Stein's *Rājataraṅgiṇī*, and similar). None is a manuscript with a transcription. — [Commons file search](https://commons.wikimedia.org/w/api.php?action=query&list=search&srnamespace=6&srlimit=30&srsearch=Sanskrit%20manuscript%20Devanagari%20transcription&format=json)

### Inferences
- **Expected yield from Commons: 0 paired pages.** At most about 300–400 unpaired Sanskrit/Devanagari manuscript images sit in these categories, many of them Nepalese scripts rather than Devanagari. These counts cover direct members only; deeper subcategory trees may hold more.
- Licence: Commons manuscript scans are usually PD-old with the image licence on each file page, so they could be transcribed afresh. That is not what the requester wants.

### Gaps
- The Commons API was intermittently unreachable (timeouts and connection resets), so I did not walk the full subcategory trees, including the 17 subcategories of Sanskrit-language manuscripts. The numbers are direct-member counts only.
- I did not check Structured Data on Commons (SDC) "transcription" statements, which are rarely used.

---

## 3. Crowdsourcing platforms: Zooniverse, FromThePage, Transkribus, Smithsonian, Library of Congress, Indian initiatives

### Takeaway
No crowdsourcing platform hosts a Sanskrit-in-Devanagari manuscript transcription project with public output. This held for every platform checked: Zooniverse, FromThePage, the Smithsonian Transcription Center, LoC By the People, Transkribus public collections and models, and India's Gyan Bharatam portal. The Transkribus Devanagari public models are trained on print. The only large handwritten Devanagari Sanskrit HTR effort, Oxford/OCHS with more than 500 pages, has published a model announcement but no ground truth.

### Cited Findings
- **Zooniverse.** Searches of the projects API for "sanskrit", "devanagari", "hindi", "jain" and "manuscript india", including non-launched projects for "sanskrit", returned **0 relevant projects**. "india" returned only two unrelated wildlife projects. — [Zooniverse projects API (search=sanskrit)](https://www.zooniverse.org/api/projects?search=sanskrit)
- **FromThePage.** A search for "sanskrit" gives 49 results (4 works, 45 pages), all English-language archival documents that mention Sanskrit: Stanford University Archives correspondence, Ohio University Farfel research notebooks, and similar. "devanagari" gives no project results. — [FromThePage find-a-project, search=sanskrit](https://fromthepage.com/findaproject?search=sanskrit)
- **Smithsonian Transcription Center.** Its example material is English-language (for example, 20th-century African American political pamphlets). A web search found no Sanskrit project. The site's search is behind bot verification. — [transcription.si.edu/about](https://transcription.si.edu/about)
- **Library of Congress By the People.** Its search sits behind a JavaScript/cookie challenge, and a web search found no Sanskrit campaign. LoC does hold Sanskrit manuscripts in its South Asian rare books collection, but they are not in a transcription campaign. — [crowd.loc.gov search](https://crowd.loc.gov/search/?q=sanskrit); [LoC blog on Sanskrit manuscripts](https://blogs.loc.gov/international-collections/2018/01/sanskrit-manuscripts-in-the-south-asian-rare-books-collection/)
- **Transkribus public Devanagari models** are trained on print:
  - "Devanagari mixed M1A" (PyLaia, Nicole Merkel-Hilf, UB Heidelberg, 2022): about 26,000 words of late 19th/early 20th-century Naval Kishore Press letterpress, 2.2% validation CER. — [model page](https://www.transkribus.org/models/devanagari-mixed-m1a)
  - "Devanagari mixed M1" (CITlab, 2018). — [model page](https://www.transkribus.org/models/devanagari-mixed-m1)
  - "Devanagari Lithography NKP M4" (NKP lithographs). — [model page](https://www.transkribus.org/models/devanagari-lithography-nkp-m4)
- **Oxford/OCHS.** Oxford fine-tuned a Transkribus Devanagari model on **more than 500 pages of handwritten, digitised manuscripts from the OCHS Indic Manuscript Database** (with the OCHS Kathmandu Office). The project is extended to June 2027. The announcement describes a model, not a ground-truth release. — [Oxford Theology news](https://www.theology.ox.ac.uk/node/4943706); [earlier project page](https://theology.web.ox.ac.uk/node/4399991)
- **SOAS Pracalit ground truth** (Transkribus PyLaia model, Sanskrit and Newar manuscripts, 16th–19th c.): png + xml ground truth, 441 training pages and 242 validation pages, CC BY 4.0. The script is **Pracalit, not Devanagari**. — [Zenodo 6967421](https://zenodo.org/records/6967421); [Transkribus model "pracalit to iast"](https://www.transkribus.org/models/pracalit-to-iast); [SOAS data paper](https://soas-repository.worktribe.com/OutputFile/419512)
- **Gyan Bharatam portal** (Ministry of Culture, launched 12 Sept 2025). Government figures differ by date: 1.29 lakh manuscripts on the portal (Lok Sabha reply, Feb 2026), more than 3.90 lakh in view mode (July 2026), and more than 4.40 lakh available for public access (PIB). The platform advertises OCR/HTR, script recognition and machine translation; its "Gyan Bharatam Community" is described as a scholars' network. I found **no volunteer transcription programme**. — [PIB release](https://www.pib.gov.in/PressReleasePage.aspx?PRID=2293807); [ThePrint](https://theprint.in/india/over-7-5-lakh-manuscripts-digitised-under-gyan-bharatam-45-centres-onboarded-govt-to-ls/2843844); [IMPRI note](https://www.impriindia.com/?p=76026)
- **Crowd contribution to Indian manuscripts.** A 2014 study found no prior work on crowd tagging or transcription of Indian manuscripts. — [Emerald JCHMSD 2014](https://www.emeraldinsight.com/insight/content/doi/10.1108/JCHMSD-12-2014-0043/full/html)
- **Paid crowd transcription in India.** A 2019 Microsoft Research India study reports 98.9% accuracy at INR 1.19 per word for crowd transcription of regional-language handwriting by rural workers. This is evidence about cost, not a data source. — [Chopra et al. 2019 PDF](https://metadataetc.org/gigontology/pdf/Chopra%20et%20al.%20-%202019%20-%20Exploring%20Crowdsourced%20Work%20in%20Low-Resource%20Settin.pdf)

### Inferences
- **Expected yield from crowdsourcing platforms: 0 pages.**
- **OCHS** (the Kathmandu office and Indic Manuscript Database) is the one organisation known to hold more than 500 pages of handwritten Devanagari Sanskrit ground truth in Transkribus. Asking for a data-sharing arrangement is the most promising route in this category.
- **The SOAS Pracalit ground truth** is directly downloadable and openly licensed. It could serve as auxiliary pretraining data for line-level HTR, with caution because the script is different.

### Gaps
- Transkribus "Read&Search" public sites and public collections could not be searched without an account. A public Devanagari manuscript collection could exist there unindexed by search engines.
- I found no Indian crowdsourcing platform such as e-Sangrahan, and no NMM volunteer transcription scheme, with Devanagari Sanskrit manuscript output. Absence of evidence comes from web search only.

---

## 4. GitHub/GitLab/Hugging Face/Zenodo repositories with page or line images of Devanagari manuscripts plus text, and Ambuda

### Takeaway
There are three small open datasets of real handwritten Devanagari Sanskrit pages with line-level transcriptions:
- **AnciDev**: 500 pages, 3,000 lines, Google Drive, no licence file.
- **VedOCR**: 57 pages, 681 lines, CC BY-NC-SA promised.
- **FLAME "Sanskrit Manuscript Layout Regimes"**: 31 pages, 882 lines, PAGE-XML, eGangotri images under CC0.

Together they come to roughly 590 pages and 4,500 lines. Most other hits are synthetic. Ambuda proofs printed books only: its one "handwritten" project is a 1-page empty test marked for removal.

### Cited Findings
- **VedOCR** (Suyashkb/VedOCR, DALL 2026 @ ICDAR):
  - Content: 57 expert-annotated pages of one *pada-pāṭha* Vedic Sanskrit manuscript on "ochre parchment". It has 681 line-level transcriptions, 41,286 character instances and 87 grapheme classes, including Vedic tone marks.
  - Repository files: `dataset/line_crops/` (681 PNG line crops), `dataset/master.tsv`, `hf_format/`, `jsonl/` and `splits/`.
  - Licence: the README says the data "will be released under CC BY-NC-SA 4.0 upon paper acceptance". The repository has no licence file. Size about 40 MB.

  — [github.com/Suyashkb/VedOCR](https://github.com/Suyashkb/VedOCR)
- **AnciDev** (vriti2003/AnciDev, AACL BHASHA): 3,000 transcribed lines from 500 pages of ancient Devanagari manuscripts drawn from National Mission for Manuscripts archives. The data is on Google Drive. The repository holds the paper and the line-segmentation and Tesseract-training scripts, with no licence file. — [github.com/vriti2003/AnciDev](https://github.com/vriti2003/AnciDev); [paper](https://aclanthology.org/2025.bhasha-1.8/)
- **FLAME "Sanskrit Manuscript Layout Regimes"** (flame-cai/gnn-synthetic-layout-historical, `dataset_release/`; paper arXiv 2608.18696, Aug 2026):
  - Content: 31 pages from 3 Sanskrit manuscripts, **882 text lines**, in PAGE-XML with human Unicode line transcriptions, baselines, regions and reading direction.
  - `dense_layout`: *Muhūrtamārtaṇḍa*, eGangotri, "Devanagari Jyotish". 7 pages, 311 lines. Images shipped, CC0.
  - `circular_layout`: *Tantrarāja with yantra and mantra uddhāra*, eGangotri, "Devanagari Stotra". 9 pages, 255 lines. Images shipped, CC0.
  - `moderate_layout`: *Yājñavalkyasmṛti, Ācārādhyāya*, Lalchand Research Library, DAV College Chandigarh. 15 pages, 316 lines. Images withheld: research use only, no redistribution.
  - The repository code is GPL-3.0.

  — [DATASET.md](https://github.com/flame-cai/gnn-synthetic-layout-historical/blob/main/dataset_release/DATASET.md); [repo](https://github.com/flame-cai/gnn-synthetic-layout-historical); [arXiv 2608.18696](https://arxiv.org/abs/2608.18696); source scans [Muhurta Martanda](https://archive.org/details/MuhurtaMartanda841GhaAlm4Shlf5DevanagariJyotish), [Tantra Raj](https://archive.org/details/TantraRajWithYantraAndMantraUddhara58901430KaAlmira26Shlf3DevanagariStotr), [DAV Yajnavalkyasmriti](https://dav.splrarebooks.com/collection/view/yajnavalakyasmritih-acharadhyayah)
- **FLAME's pipeline** uses CNN-BiLSTM-CTC recognition plus GNN line segmentation, with iterative per-manuscript fine-tuning. This is the same architecture as the requester's. FLAME's earlier repository `flame-cai/case-study-handwritten-sanskrit-ocr` points to this one. — [repo README](https://github.com/flame-cai/gnn-synthetic-layout-historical); [case-study repo](https://github.com/flame-cai/case-study-handwritten-sanskrit-ocr)
- **Shreeshrii/kraken_devanagari** is a kraken model trained on **synthetic** printed lines (38,761 training lines made with text2image/linegen). It contains no manuscripts. — [github.com/Shreeshrii/kraken_devanagari](https://github.com/Shreeshrii/kraken_devanagari)
- **Other GitHub search hits are not usable data.** Searches for "devanagari manuscript", "sanskrit manuscript ocr", "sanskrit htr", "devanagari ground truth" and "jain manuscript" mostly return synthetic manuscript generators for Devanagari, Modi and Śāradā (about 15 repositories, 2026) or OCR apps without data. "sanskrit pagexml" and "devanagari manuscript htr" return nothing. — [GitHub search API](https://api.github.com/search/repositories?q=devanagari+manuscript)
- **Hugging Face.** Dataset search for "sanskrit manuscript" returns **0**. "devanagari manuscript" returns 1 (synthetic). "indic manuscript" returns about 18, all synthetic or machine-generated. For example, `varunbhoyar/indic-historical-manuscripts` is tagged `annotations_creators: machine-generated` and `source_datasets: synthetic-indic-manuscripts`. "sanskrit ocr" datasets are printed-text OCR or post-correction sets. — [HF datasets API](https://huggingface.co/api/datasets?search=sanskrit%20manuscript); [varunbhoyar/indic-historical-manuscripts](https://huggingface.co/datasets/varunbhoyar/indic-historical-manuscripts)
- **Zenodo.** Record searches for "sanskrit manuscript ground truth", "devanagari manuscript transcription", "sanskrit htr", "devanagari htr" and "sanskrit manuscripts transkribus" found only the SOAS **Pracalit** ground truth (record 6967421) as a relevant hit. — [Zenodo API search](https://zenodo.org/api/records?q=sanskrit%20manuscript%20ground%20truth)
- **TEI diplomatic transcriptions (lead).** The Saktumiva/upama platform encodes each manuscript's diplomatic transcription in TEI, with `<lb n>` line numbers and `<pb n>` folio numbers, shown beside the manuscript images. The Suśruta Project keeps TEI transcriptions on GitHub under CC BY-SA, with a `<pb>` link to the manuscript image of each folio. Its witnesses are largely Nepalese manuscripts; I did not check their scripts. — [Saktumiva TEI guide](https://saktumiva.org/_export/xhtml/wiki/tei); [upama code](https://github.com/chchch/upama); [Suśruta Project](https://wujastyk.github.io/sushrutaproject); [Suśruta "Laboratory"](https://sushrutaproject1.github.io/content/06-the-laboratory.html)
- **Ambuda proofing.** "Showing 1–25 of **231 projects**"; the summed page counts of all 231 projects come to **about 51,735 pages**; 345 published texts. Proofing statuses are "Needs more work / Proofed once / Proofed twice / Not relevant". The site banner reads "Thousands of Sanskrit texts are available only in print". — [ambuda.org/proofing](https://ambuda.org/proofing/); [ambuda.org/proofing/texts](https://ambuda.org/proofing/texts)
- **Ambuda's only handwriting-related project** is "HandWrittenTextText": **1 page**, "This project doesn't have any edits yet", and the one discussion post is "Remove it" (created about 2 years ago). Ambuda's guide tells proofreaders to exclude handwritten notes, stamps and similar marks from printed pages. — [ambuda.org/proofing/handwrittentexttext](https://ambuda.org/proofing/handwrittentexttext/); [Ambuda complete guide](https://ambuda.org/proofing/help/complete-guide)
- **Ambuda's original scope** (2021 proposal) was "scanned Devanagari books". — [sanskrit-programmers proposal](https://groups.google.com/g/sanskrit-programmers/c/4Duld5WXJlU/m/VbQoSD-iAAAJ)

### Inferences
- **Line-image ground truth available today from open repositories: about 4,560 lines** (3,000 AnciDev + 681 VedOCR + 882 FLAME). Of these, only FLAME's 566 eGangotri lines carry a clear open licence for the images (CC0) as well as the labels.
  - AnciDev pages come from NMM archives with no stated licence; treat them as research use only.
  - VedOCR is a single Vedic manuscript on ochre parchment with svara marks, so its domain differs from Jain paper manuscripts.
- **Fit with the requester's pipeline:**
  - FLAME's PAGE-XML gives line polygons and baselines with text, so it can be converted directly. Its jyotiṣa and tantra genres, dense marginalia and yantra diagrams make it a hard test set rather than a bulk training set.
  - AnciDev ships line crops with text; the requester's aligner is not needed.
- **Ambuda yields 0 manuscript pages.** Its export tooling is a model for publishing page-level proofreading data, not a source of it.

### Gaps
- I did not download AnciDev from Google Drive, so its line-crop format, transcription conventions and per-page line breaks are unverified. Whether pages are Jain or Brahmanical, and their dates, are also unknown.
- I did not check GitLab, Codeberg or Kaggle.
- The scripts of the Suśruta and Saktumiva manuscript witnesses, and whether their images are openly downloadable, were not verified.

---

## 5. archive.org items carrying both a manuscript scan and a separate transcription, and image-plus-e-text pairs across sites

### Takeaway
archive.org almost never pairs a Sanskrit manuscript scan with a transcription file inside the same item: a metadata search found 1 hit, which I did not verify. The productive pairing is **across sites**. eGangotri has uploaded tens of thousands of items to archive.org under CC0, including more than 500 Devanagari manuscripts from the Raghunātha Temple / Dharmārth Trust, Jammu. **Muktabodha** has typed **diplomatic e-texts** of dozens of those same manuscripts from the eGangotri images. These pairs are at manuscript (text) level: folio and line markers are not confirmed. The text is licensed CC BY-NC 4.0, with an explicit non-commercial clause for AI training.

### Cited Findings
- **archive.org advanced search.**
  - `language:sanskrit AND manuscript AND (description:transcription OR transcribed)` gives **1 hit**: `eap1736-1-4`, a Sanskrit manuscript from EAP1736 with an Assamese-script title. Its transcription status is unverified.
  - The variants `subject:"sanskrit manuscript" AND transcript*`, `title:manuscript AND title:transcription`, and the Jain-subject variant give **0**.

  — [archive.org advancedsearch](https://archive.org/advancedsearch.php); [eap1736-1-4](https://archive.org/details/eap1736-1-4)
- **eGangotri scale on archive.org:**
  - `creator:eGangotri` returns 13,037 items, of which 1,356 have "manuscript" in the title.
  - The collection `dharmarthtrustjkcollectionbyegangotri` has **532 items**, with licence URL CC0 1.0 (`http://creativecommons.org/publicdomain/zero/1.0/`).
  - Items titled with the Jammu shelf-mark pattern ("Alm … Shlf … Devanagari …") number about 687–718.

  — [archive.org advancedsearch](https://archive.org/advancedsearch.php); [collection](https://archive.org/details/dharmarthtrustjkcollectionbyegangotri)
- **Jain manuscripts on archive.org.** The `ganeshvarnilibrary` collection (Ganesh Varni Digambar Jain collection, Varanasi) has **1,607 items** under CC0, mostly printed; 30 have "manuscript" in the title (for example "Dasavaikalaka Devanagari Manuscript"). These are images only, with no transcriptions. — [collection](https://archive.org/details/ganeshvarnilibrary)
- **Muktabodha e-texts from eGangotri images:**
  - Muktabodha's Varanasi office produced e-texts "from manuscript images made available to the public by the generosity of the eGangotri organisation", under Dr Anirban Dash. — [INDOLOGY, June 2023 (4 new)](https://list.indology.info/pipermail/indology/2023-June/057803.html); [INDOLOGY, June 2023 (3 new)](https://go.mail-archive.com/indology@list.indology.info/msg02902.html)
  - The transcriptions are "not normalized": word breaks follow the manuscript, and v/b are kept as written. — [INDOLOGY, June 2023 (3 new)](https://go.mail-archive.com/indology@list.indology.info/msg02902.html)
  - Batches announced:
    - Oct 2021: 5 e-texts from the Shri Raghunatha MSS Library, Jammu (for example the Agastyasaṁhitā, MS 5294). — [INDOLOGY, Oct 2021](https://list.indology.info/pipermail/indology/2021-October/055320.html)
    - June 2023: 4 + 3 e-texts (for example the Dakṣiṇāmūrtisaṁhitā; mudrāprakāśaḥ MS 1406; mātṛkārṇa-nighaṇṭu MS 4858; navārṇavacaṇḍipañjāṅgam MS 4818). — [INDOLOGY, June 2023 (4 new)](https://list.indology.info/pipermail/indology/2023-June/057803.html); [INDOLOGY, June 2023 (3 new)](https://go.mail-archive.com/indology@list.indology.info/msg02902.html)
    - Nov 2023: 13 tantric e-texts. 11 are Raghunātha Temple MSS (nos. 3887, 4913, 5295, 5605, 4853, 4930, 4972, 4826, 5753, 4894, 1309), 1 is Rashtriya Sanskrit Sansthan MS 72 and 1 is UPSS MS 1322. The post says "they are diplomatic transcriptions of the manuscripts they are transcribed from", and five earlier Raghunātha e-texts were revised to the same diplomatic standard. — [INDOLOGY, Nov 2023](https://list.indology.info/pipermail/indology/2023-November/058475.html)
- **Muktabodha holdings.**
  - E-text library: more than 570 searchable e-texts, of which more than 380 were edited from manuscripts under Dyczkowski's supervision. Typists were trained to read scripts such as Newari.
  - IFP paper transcripts: more than 2,000 mostly Śaiva Siddhānta texts with more than 1,100 PDF images.
  - Gokarna Vedic collection: manuscript images.

  — [muktabodha.org/digital-library](https://muktabodha.org/digital-library/); [IFP catalogue (legacy)](https://muktalib7.com/DL_CATALOG_ROOT/IFP_CATALOG/access_page.htm); [legacy library](https://muktalib7.com/DL_CATALOG_ROOT/digital_library.htm)
- **Script of the IFP transcripts.** A web-search snippet from Muktabodha's site states that the IFP paper transcripts are "clearly written in the well-known Devanagari script", while the originals are often in South Indian scripts. I did not open the source page. The fetched digital-library page does not name the script. — search result pointing to [muktabodha.org/?p=43](https://muktabodha.org/?p=43) (unverified)
- **Muktabodha licences:**
  - The E-Text Library is under **CC BY-NC 4.0**: "The non-commercial terms above also apply to training AI or machine-learning models on E-Text material".
  - Texts numbered `I000##` were made under the IFP agreement and require credit to IFP too.
  - IFP Paper Transcripts are "©2023 … All Rights Reserved".
  - Gokarna Vedic PDFs are for private study only.

  — [muktabodha-digital-library.org/about](https://muktabodha-digital-library.org/about)
- **Access.** The new Muktabodha e-text interface (muktabodha-digital-library.org) sits behind a Cloudflare Turnstile check; every library path redirects to `/turnstile/verify`. Automated bulk download is therefore blocked, and the site offers no bulk export. — observed 2026-11-27 at [muktabodha-digital-library.org](https://muktabodha-digital-library.org/)

### Inferences
- **Estimated yield.** At least about 25 Raghunātha/eGangotri manuscripts have Muktabodha diplomatic e-texts (5 + 7 + 11 announced; there are probably more, since the library has more than 570 e-texts). At a typical 20–150 folios each, that could mean very roughly 1,000–3,000 page images (2,000–6,000 sides), or tens of thousands of lines. This is an order-of-magnitude guess, not a count.
- **Fit with the requester's pipeline.** The pairs are text-level, not page-level. To use them, the requester would need to find each Muktabodha text's eGangotri item by the Raghunātha MS number in the archive.org title, then align continuous text to a page sequence. The pipeline's existing line aligner could do this with a monotonic forced alignment per manuscript, given a decent recogniser. "Diplomatic" with manuscript word-spacing and v/b retention suggests the text tracks the manuscript closely.
- **Domain.** These are tantric and Śaiva Brahmanical paper manuscripts, mostly 18th–19th c. Jammu Devanagari, so they are close in medium to Jain paper manuscripts.
- **Licence.** The pairing is usable for non-commercial research model training only (CC BY-NC). The requester's model licence is CC BY-SA 4.0, so a model trained on this text would need checking against Muktabodha's ML clause, or written permission.
- **IFP lead.** If some `I000##` e-texts were keyed from the handwritten Devanagari IFP paper transcripts, then the IFP PDFs (all rights reserved) plus the Muktabodha e-texts form another pairing. That pairing is closed-licence on the image side.

### Gaps
- I could not verify whether Muktabodha e-texts mark folio boundaries (for example `[1v]`) or line ends. The library is behind Turnstile and the posts do not say. This one detail decides whether the pairs are page-level.
- There is no complete list of Muktabodha e-texts derived from eGangotri images and their archive.org identifiers. It would have to be built from the catalogue by MS number.
- I did not inspect the single archive.org hit (`eap1736-1-4`) for an attached transcription.

---

## 6. Per-source inventory: script and language, pages/lines, transcription quality, line breaks, licence, URLs, bulk-download method

### Takeaway
Summary table. "Pairs" means manuscript image plus existing typed text. Only rows 1–4 give line-level or page-level pairs today. Row 5 gives text-level pairs that need alignment, and rows 6 onward are empty or exist only in principle.

### Cited Findings

| # | Source | Script / language | Pages / lines with text (2026-11) | Transcription quality | Line breaks | Licence | Bulk method |
|---|---|---|---|---|---|---|---|
| 1 | [AnciDev](https://github.com/vriti2003/AnciDev) | Devanagari, Sanskrit, NMM manuscripts | 500 pages / 3,000 lines | Research ground truth | Line-level | None stated | Google Drive folder linked in README |
| 2 | [VedOCR](https://github.com/Suyashkb/VedOCR) | Devanagari, Vedic Sanskrit (pada-pāṭha) | 57 pages / 681 lines | "Expert-annotated" | Line crops + TSV | CC BY-NC-SA 4.0 promised; no licence file | `git clone` |
| 3 | [FLAME layout regimes](https://github.com/flame-cai/gnn-synthetic-layout-historical/blob/main/dataset_release/DATASET.md) | Devanagari, Sanskrit (jyotiṣa, tantra, smṛti) | 31 pages / 882 lines (16 pages / 566 lines with images) | Human diplomatic, PAGE-XML | Line-level with baselines | eGangotri images CC0; DAV images withheld; repo GPL-3.0 | `git clone` |
| 4 | [SOAS Pracalit GT](https://zenodo.org/records/6967421) | **Pracalit**, Sanskrit/Newar (Nepal) | 441 + 242 pages | Transkribus GT | PAGE-XML lines | CC BY 4.0 | Zenodo download |
| 5 | [Muktabodha](https://muktabodha.org/digital-library/) e-texts + [eGangotri Jammu scans](https://archive.org/details/dharmarthtrustjkcollectionbyegangotri) | Devanagari, Sanskrit (tantra/Śaiva) | ≥ about 25 MSS confirmed; ~500 MSS scanned | Diplomatic since Nov 2023 | Unverified (probably continuous) | Text CC BY-NC 4.0; scans CC0 | archive.org API for scans; Muktabodha manual (Turnstile) |
| 6 | Sanskrit Wikisource | n/a | **0** manuscript indexes of 538 | n/a | n/a | Text CC BY-SA / scans PD | [dumps](https://dumps.wikimedia.org/sawikisource/latest/), API |
| 7 | Hindi / Gujarati Wikisource | n/a | **0** | n/a | n/a | n/a | dumps |
| 8 | Commons | Mixed (many Nepalese) | ~300–400 images, **0** with text | n/a | n/a | Mostly PD | Commons API |
| 9 | Ambuda | n/a | **0** (1-page empty test) | n/a | n/a | n/a | n/a |
| 10 | Zooniverse / FromThePage / Smithsonian / LoC | n/a | **0** | n/a | n/a | n/a | n/a |
| 11 | Transkribus public models; OCHS | Devanagari (models: print; OCHS: handwritten) | OCHS more than 500 pages, **not public** | n/a | n/a | n/a | Contact OCHS |
| 12 | [Saktumiva/upama](https://saktumiva.org/_export/xhtml/wiki/tei), [Suśruta TEI](https://wujastyk.github.io/sushrutaproject) | Mostly Nepalese scripts (unverified) | Unknown | Diplomatic TEI | `<lb n>`/`<pb n>` encoded | CC BY-SA (Suśruta) | git |

Each row's sources are cited in sections 1–5 above.

### Inferences
- **Best immediate actions, in order:**
  1. Ingest FLAME's 566 CC0 lines and AnciDev's 3,000 lines, if the licence is clarified with the authors, as supplementary or validation data.
  2. Prototype aligning Muktabodha diplomatic e-texts to their eGangotri scans. This is the only route that scales into thousands of pages of existing transcription, at the cost of a non-commercial licence.
  3. Ask OCHS about sharing its more than 500 pages of Transkribus ground truth.
- **Jain coverage.** None of these sources is Jain. The Jain paper-manuscript domain (15th–19th c.) is not covered by any community-transcribed pair source. Jain material on archive.org (the Ganesh Varni collection) has images only.

### Gaps
- I did not count lines per page for rows 1 and 5, and I did not verify AnciDev's transcription conventions.
- Muktabodha line and folio marking is unverified (see section 5).

### Printed-book proofreading corpora (out of scope; approximate scale only)
- **Sanskrit Wikisource:** 538 Index pages, all printed editions such as Nirṇayasāgara, Kāvyamālā and TSS. 39 are at Progress C, 6 at T and 5 at V; most (392) are at Progress "OCR". The site has 165,563 pages in all namespaces. — [siteinfo API](https://sa.wikisource.org/w/api.php?action=query&meta=siteinfo&siprop=namespaces|statistics&format=json)
- **Ambuda:** 231 printed-book proofing projects totalling about 51,700 scanned pages, with 345 published texts. — [ambuda.org/proofing](https://ambuda.org/proofing/)
- **Hindi Wikisource:** its overall size was not measured (the statistics query timed out).

These are useful for pretraining a printed-Devanagari recogniser but contain no manuscripts.
