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

# --- Wikisource validated pages (data/wsv): only scan pages validated by a second proofreader ---
WSV_DUMP = "data/raw/sawikisource/sawikisource-latest-pages-articles.xml.bz2"
WSV_LEVELS = {"4"}                 # pagequality level: 4 = validated (पुष्टितम्)
WSV_PAGE_HINDI_RATE = 0.03         # a page whose words are more than 3% Hindi/Marathi function words is dropped
WSV_MIN_SEP_RATE = None            # no filter: both यत् पथ्यम् and यत्पथ्यम् editions are kept. (Measured: books that
                                   # separate a halanta word from a following consonant do so in 1.1-9% of spaces, books
                                   # that join it in 0-0.6%; set e.g. 0.01 to keep only the separating ones.)
WSV_MAX_OLD_OVERLAP = 0.05         # a book with more of its sentences in the old training pool is kept out of val/test
WSV_TEST_BYTES = 2_000_000         # Devanagari UTF-8 bytes
WSV_VAL_BYTES = 2_000_000
WSV_EVAL_GROUP_MAX = 1_000_000     # val/test take whole works up to this size; larger works stay in training
