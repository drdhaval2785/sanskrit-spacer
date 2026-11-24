from huggingface_hub import snapshot_download
import pyarrow.parquet as pq
import glob

from config import HF_REPO, HF_REVISION

snapshot_download(
    repo_id=HF_REPO, repo_type="dataset", revision=HF_REVISION,
    local_dir="data/raw/pramana",
    allow_patterns=["catalogue.parquet", "passages/*.parquet", "README.md", "LICENCES.md", "stats.json"],
)

cat = pq.read_metadata("data/raw/pramana/catalogue.parquet").num_rows
files = sorted(glob.glob("data/raw/pramana/passages/*.parquet"))
pas = sum(pq.read_metadata(f).num_rows for f in files)
print("catalogue rows", cat, "passage files", len(files), "passage rows", pas)
assert cat == 299705, cat
assert len(files) == 4 and pas == 3819508, (len(files), pas)
print("GATE 1 OK")
