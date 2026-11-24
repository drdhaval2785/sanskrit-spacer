# Sanskrit spacer: results

A small character-level Transformer (about 3.2 M parameters) was trained to decide, for every gap between two letters of unspaced Sanskrit, whether a space belongs there. The same model and hyperparameters were trained on 1, 5, 10 and 20 MB of text and on the full cleaned training pool (all 20,000 steps, identical settings) and scored on one fixed test set. "MB" means 1,000,000 bytes of the spaced sentences written in Devanagari (UTF-8, one sentence per line).

## Dataset

| split | sentences | letters | words | Devanagari MB | groups | base rate |
|---|---|---|---|---|---|---|
| test | 23,782 | 872,369 | 93,692 | 2.52 | 74 | 8.24% |
| val | 23,910 | 875,271 | 87,657 | 2.52 | 63 | 7.49% |
| train_1mb | 9,000 | 345,237 | 36,610 | 1.00 | 262 | 8.21% |
| train_5mb | 44,931 | 1,725,103 | 183,277 | 5.00 | 376 | 8.23% |
| train_10mb | 89,700 | 3,450,362 | 365,901 | 10.00 | 400 | 8.22% |
| train_20mb | 179,219 | 6,900,272 | 732,146 | 20.00 | 408 | 8.23% |
| train_full | 1,463,635 | 56,357,826 | 5,985,866 | 163.35 | 410 | 8.24% |

## Results on the test set

| Train size | Sentences | Best step | Threshold | Boundary P | Boundary R | Boundary F1 | Word F1 | Sentence acc. |
|---|---|---|---|---|---|---|---|---|
| 1 MB | 9,000 | 17500 | 0.35 | 79.85% | 67.63% | 73.23% | 55.40% | 30.98% |
| 5 MB | 44,931 | 17500 | 0.6 | 87.77% | 78.62% | 82.94% | 69.29% | 46.12% |
| 10 MB | 89,700 | 19000 | 0.5 | 89.46% | 82.05% | 85.60% | 73.53% | 51.70% |
| 20 MB | 179,219 | 19000 | 0.5 | 90.66% | 83.46% | 86.91% | 75.82% | 55.38% |
| Full (163 MB) | 1,463,635 | 20000 | 0.5 | 92.27% | 83.83% | 87.85% | 77.46% | 57.72% |

## Multi-pass runs on the full data

Same data as the full-data row above, but an effective batch of 256 and a budget of up to 10 passes with early stopping (patience 12 evaluations of 1,000 updates). Not part of the learning curve: the training budget differs from the comparable tiers.

| Run | Params | Passes done | Best step | Threshold | Boundary P | Boundary R | Boundary F1 | Word F1 | Sentence acc. |
|---|---|---|---|---|---|---|---|---|---|
| Full, 10 passes, base model (4 layers, 256 wide) | 3.2 M | 9.97 | 53000 | 0.45 | 93.08% | 88.02% | 90.48% | 81.84% | 64.35% |

## Full-data run by source repository

| | Sentences | Boundary P | Boundary R | Boundary F1 | Word F1 |
|---|---|---|---|---|---|
| sa.wikisource | 22,774 | 92.38% | 83.95% | 87.96% | 77.54% |
| ambuda | 862 | 92.56% | 83.59% | 87.85% | 79.53% |
| sarit | 112 | 47.98% | 42.35% | 44.99% | 28.67% |
| ambuda+sa.wikisource | 34 | 94.79% | 93.81% | 94.30% | 88.12% |

## Full-data run by passage kind

| | Sentences | Boundary P | Boundary R | Boundary F1 | Word F1 |
|---|---|---|---|---|---|
| verse | 22,823 | 92.37% | 83.98% | 87.98% | 77.58% |
| prose | 959 | 89.48% | 79.92% | 84.43% | 74.40% |

## Error examples (full-data run)

- gold: अर्थापरोक्ष्यलक्षणस्याति व्याप्ति मां शंक्य निराकरोति न चेत्यादिना  
  pred: अर्थापरोक्ष्य लक्षणस्यातिव्याप्तिमां शंक्यनिराकरोति न चेत्यादिना
- gold: द्वादशीको मंडल होय तो राजा पुरोहितका नाश हो  
  pred: द्वादशीको मंडल हो यतो राजा पुरोहितका नाश हो
- gold: अयमभेदः किं वेदांतप्रमाणकः किम् वा तदन्यप्रमाणकस्तत्र  
  pred: अयमभेदः किं वेदांतप्रमाणकः किम्वा तदन्यप्रमाणकस्तत्र
- gold: स च विविदिषावाक्यविरुद्ध इति  
  pred: स च विविदिषा वाक्यविरुद्ध इति
- gold: साक्षात् साध्यते  
  pred: साक्षात्साध्यते
- gold: पुरु चैवयेन सम्पादित्स्य यज्ञस्य चेतन्त्वेन विद्वत्वसम्भवादित्याह तस्य  
  pred: पुरुचैव येन सम्पादित्स्ययज्ञस्य चेतन्त्वेन विद्वत्वसम्भवादित्याह तस्य
- gold: दर्पणाद्यवछिन्न चैतन्यनिष्ठाज्ञानस्यति वृतत्वाता  
  pred: दर्पणाद्यवछिन्नचैतन्यनिष्ठा ज्ञानस्यतिवृतत्वाता
- gold: सिताविप्रे नृपे रक्ता पीता वैश्यो सितेतरा  
  pred: सिता विप्रे नृपे रक्ता पीता वैश्योसितेतरा
- gold: परदेवताभक्तिप्रधानत्वात् तद्बलेनैव मत्तः सम्भूतत्वाच्च देवताभक्ता  
  pred: परदेवताभक्तिप्रधानत्वात्तद्बलेनैव मत्तः सम्भूतत्वाच्च देवताभक्ता
- gold: अत तत् कारणस्येति  
  pred: अत तत्कारणस्येति
- gold: कामिनीमानसञ्चारा कालिका कालकालिका  
  pred: कामिनी मानसञ्चारा कालिका कालकालिका
- gold: सिद्धार्थेऽपिव्युत्पत्तिसम्भवाच  
  pred: सिद्धार्थेऽपि व्युत्पत्तिसम्भवाच
- gold: गुण पुरुषान्यताख्यातिर्ज्ञानम्  
  pred: गुणपुरुषान्यताख्यातिर्ज्ञानम्
- gold: लगाना कूँवामें गिरी  
  pred: लगानाकूँ वा में गिरी
- gold: तु प्रधानस्य सर्वज्ञत्वे साक्षिणी सत्वोत्कर्षे येगिसार्वज्ञप्रसिद्धिः  
  pred: तु प्रधानस्य सर्वज्ञत्वे साक्षिणीसत्वोत्कर्षे ये गिसार्वज्ञप्रसिद्धिः
- gold: यावभासाभ्युपगमे पूर्वदृष्टत्वं भाष्योक्तं विरुध्येत तचाह अत एवेति  
  pred: यावभासाभ्युपगमे पूर्वदृष्टत्वं भाष्योक्तं विरुध्येत त चाह अत एवेति
- gold: कर्मान्तरमिति प्रतिज्ञाय हेतुमाह पूर्वदेवतात इति  
  pred: कर्मान्तरमिति प्रतिज्ञाय हेतुमाह पूर्वदेव तात इति
- gold: यद्यपि केवलाय भाव शुद्धे बन्यशब्ठो न प्रसिद्धस्तथलिष कामचारादिमति  
  pred: यद्यपि केवलायभावशुद्धे बन्यशब्ठो न प्रसिद्धस्तथ लिषकामचारादिमति
- gold: प्रतीकमधृत्वैवेवशब्दार्थमाह  
  pred: प्रतीकमधृत्वैवेव शब्दार्थमाह
- gold: आनू पुरार्पितसुजातसुगन्धिपुष्प  
  pred: आनूपुरार्पितसुजातसुगन्धिपुष्प

## Data provenance

Pramāṇa open data release (Hugging Face `srajma/pramana`, revision `76b82194cd64ec912b06545337e355a342af26c3`, https://doi.org/10.5281/zenodo.24408373). Source repositories used: Sanskrit Wikisource (CC BY-SA 4.0), SARIT (CC BY-SA 3.0), Ambuda (CC0). Wikisource and SARIT texts are CC BY-SA: any redistributed derivative of the dataset must carry the same licence and credit the sources.

## Pipeline counts

| stage | count |
|---|---|
| extract: passages_read | 584,196 |
| extract: segments_seen | 2,387,512 |
| extract: sentences_written | 1,777,587 |
| extract: reject_too_short | 456,807 |
| extract: reject_hiatus | 27,573 |
| extract: reject_duplicate | 116,324 |
| extract: reject_non_iast | 11,324 |
| extract: reject_repeat | 19 |
| extract: documents | 758 |
| audit: kept_letters | 65,600,356 |
| audit: kept_groups | 547 |
| audit: kept_deva_bytes_estimate | 177,120,961 |
| audit: documents keep | 560 |
| audit: documents tiny | 128 |
| audit: documents analytic | 22 |
| audit: documents underspaced | 30 |
