# Clean-test comparison

The clean test set is 23,761 sentences (2.49 MB of Devanagari) from 15 works whose scan pages were validated by a second proofreader on Sanskrit Wikisource. None of its sentences occurs in the Pramāṇa training pool, so all models are scored on text they have not seen. The original test set is the noisier one from the Pramāṇa pool.

| Model | Size | Trained on | Clean test: P | R | Boundary F1 | Word F1 | Sentence acc. | Original test: Boundary F1 |
|---|---|---|---|---|---|---|---|---|
| `full_e10_s1` | 4×256, 3.2 M | Pramāṇa pool (163 MB), 10 passes | 95.36% | 93.52% | **94.43%** | 89.40% | 79.44% | 90.48% |
| `full_e10_L_s1` | 6×384, 10.8 M | Pramāṇa pool (163 MB), stopped by hand after 4.4 of 10 passes | 95.54% | 92.85% | **94.18%** | 89.06% | 79.17% | 90.30% |
| `wsv_base_s1` | 4×256, 3.2 M | Validated Wikisource (30 MB), 10 passes | 93.43% | 88.74% | **91.02%** | 83.41% | 69.70% | 86.01% |
| `wsv_L_s1` | 6×384, 10.8 M | Validated Wikisource (30 MB), 10 passes | 93.72% | 91.35% | **92.52%** | 86.02% | 73.75% | 87.65% |

Test works: विक्रमाङ्कदेवचरितम्, Jyautisha Vedangam, Mudrarakshasa, शब्दनिर्णयः, शिशुपालवधम्, संस्कृतकथासङ्ग्रहः, प्रपञ्चसारः, शिवगीता, रसगङ्गाधरः, शब्दापशब्दविवेकः, कादम्बरीकथासारसङ्ग्रहः, चोरचत्वारिंशीकथा, पद्मिनीपरिणयः, साहित्यसारः, काव्यालङ्कारसूत्रवृत्तिः.

