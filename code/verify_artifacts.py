"""Mechanically verify artifact release (D7) from full text rather than abstracts.

Coding D7_code/D7_data from abstracts systematically undercounts release, because
repository links usually appear in the body, a footnote, or a data-availability
statement. This script downloads each included paper's PDF, extracts text, and searches
for repository/archive URLs with a fixed regex. No model judgment is involved, so the
result is deterministic and reproducible.

  python code/verify_artifacts.py            # all included papers
  python code/verify_artifacts.py 2607.09195 # single paper (debug)

Writes data/artifact-verification.csv incrementally (resumable: existing rows are kept).
"""

import csv
import io
import re
import sys
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "artifact-verification.csv"
FIELDS = ["arxiv_id", "status", "n_pages", "repo_urls", "has_repo",
          "has_data_archive", "availability_statement"]

REPO = re.compile(
    r"(?:https?://)?(?:www\.)?("
    r"github\.com/[\w.\-]+/[\w.\-]+"
    r"|gitlab\.com/[\w.\-/]+"
    r"|bitbucket\.org/[\w.\-]+/[\w.\-]+"
    r"|huggingface\.co/(?:datasets/)?[\w.\-]+/[\w.\-]+"
    r"|anonymous\.4open\.science/r/[\w.\-]+"
    r"|codeocean\.com/capsule/[\w.\-]+"
    r")", re.I)
DATA_ARCHIVE = re.compile(
    r"(zenodo\.org/record|zenodo\.org/doi|figshare\.com|osf\.io/|dryad|dataverse|"
    r"10\.5281/zenodo)", re.I)
AVAIL = re.compile(
    r"(data availability|code availability|availability statement|"
    r"code and data (?:are|is) available|we (?:release|open.?source)|"
    r"publicly available at|available at:?\s*http)", re.I)


def fetch_text(arxiv_id, timeout=90):
    url = f"https://arxiv.org/pdf/{arxiv_id}"
    req = urllib.request.Request(url, headers={"User-Agent": "arxiv-frontier-artifact-check"})
    with urllib.request.urlopen(req, timeout=timeout) as r:
        raw = r.read()
    from pypdf import PdfReader
    reader = PdfReader(io.BytesIO(raw))
    pages = reader.pages
    text = []
    for p in pages:
        try:
            text.append(p.extract_text() or "")
        except Exception:
            text.append("")
    return "\n".join(text), len(pages)


def analyze(text):
    urls = sorted({m.group(1).rstrip(".,);") for m in REPO.finditer(text)})
    return {
        "repo_urls": " | ".join(urls[:6]),
        "has_repo": "1" if urls else "0",
        "has_data_archive": "1" if DATA_ARCHIVE.search(text) else "0",
        "availability_statement": "1" if AVAIL.search(text) else "0",
    }


def one(pid):
    row = {"arxiv_id": pid, "status": "ok", "n_pages": 0, "repo_urls": "",
           "has_repo": "0", "has_data_archive": "0", "availability_statement": "0"}
    try:
        text, pages = fetch_text(pid)
        row["n_pages"] = pages
        if len(text) < 500:
            row["status"] = "no_text_layer"
        else:
            row.update(analyze(text))
    except Exception as e:
        row["status"] = f"error: {type(e).__name__}"
    return row


def main():
    ids = [r["arxiv_id"] for r in csv.DictReader(open(DATA / "coded-corpus.csv", encoding="utf-8"))]
    if len(sys.argv) > 1:
        ids = sys.argv[1:]
    done = {}
    if OUT.exists():
        done = {r["arxiv_id"]: r for r in csv.DictReader(open(OUT, encoding="utf-8"))}
    todo = [i for i in ids if i not in done]
    print(f"{len(ids)} papers; {len(done)} already done; {len(todo)} to fetch", flush=True)

    from concurrent.futures import ThreadPoolExecutor
    with open(OUT, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if not done:
            w.writeheader()
        # 6 workers: fast enough to finish in ~15 min, gentle enough for arXiv.
        with ThreadPoolExecutor(max_workers=6) as ex:
            for n, row in enumerate(ex.map(one, todo), 1):
                w.writerow(row)
                f.flush()
                if n % 50 == 0:
                    print(f"  {n}/{len(todo)}", flush=True)
    print("done -> data/artifact-verification.csv")


if __name__ == "__main__":
    main()
