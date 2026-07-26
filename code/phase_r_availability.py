"""Phase R, step 1: does the repository a paper links to actually exist and contain anything?

This is the cheapest and most basic claim a paper makes about its artifact, and it is
checkable mechanically with no model judgement: resolve each repository URL via the host's
API and record what is there. Nothing is cloned at this stage.

Recorded per URL: HTTP status, whether the repo is public, default branch, last push date,
size, file/commit counts where available, and whether it appears empty.

  python code/phase_r_availability.py            # all repo URLs in the corpus
  python code/phase_r_availability.py <arxiv_id> # one paper (debug)

Writes data/phase-r-availability.csv incrementally and is resumable.
"""

import csv
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
OUT = DATA / "phase-r-availability.csv"
FIELDS = ["arxiv_id", "url", "host", "status", "public", "default_branch",
          "pushed_at", "size_kb", "stars", "archived", "empty", "note"]

GH = re.compile(r"github\.com/([\w.\-]+)/([\w.\-]+)", re.I)
HF = re.compile(r"huggingface\.co/(?:(datasets)/)?([\w.\-]+)/([\w.\-]+)", re.I)
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")


def api(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "arxiv-frontier-phase-r",
        "Accept": "application/vnd.github+json",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {}),
    })
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r), r.status


def check(arxiv_id, url):
    row = dict.fromkeys(FIELDS, "")
    row.update(arxiv_id=arxiv_id, url=url, status="", public="", empty="")
    m = GH.search(url)
    if m:
        owner, repo = m.group(1), m.group(2).removesuffix(".git")
        row["host"] = "github"
        try:
            d, _ = api(f"https://api.github.com/repos/{owner}/{repo}")
            row.update(status="200", public=str(not d.get("private", False)),
                       default_branch=d.get("default_branch", ""),
                       pushed_at=(d.get("pushed_at") or "")[:10],
                       size_kb=str(d.get("size", "")),
                       stars=str(d.get("stargazers_count", "")),
                       archived=str(d.get("archived", False)),
                       empty=str(d.get("size", 1) == 0))
        except urllib.error.HTTPError as e:
            row["status"] = str(e.code)
            row["note"] = {404: "not found or private", 403: "rate limited or blocked",
                           451: "unavailable for legal reasons"}.get(e.code, "")
        except Exception as e:
            row["status"] = f"error:{type(e).__name__}"
        return row

    m = HF.search(url)
    if m:
        kind, owner, repo = m.group(1) or "models", m.group(2), m.group(3)
        row["host"] = "huggingface"
        seg = "datasets" if kind == "datasets" else "models"
        try:
            d, _ = api(f"https://huggingface.co/api/{seg}/{owner}/{repo}")
            row.update(status="200", public=str(not d.get("private", False)),
                       pushed_at=(d.get("lastModified") or "")[:10],
                       empty=str(len(d.get("siblings", []) or []) == 0))
        except urllib.error.HTTPError as e:
            row["status"] = str(e.code)
        except Exception as e:
            row["status"] = f"error:{type(e).__name__}"
        return row

    row["host"] = "other"
    row["note"] = "unsupported host; needs manual check"
    return row


def main():
    art = list(csv.DictReader(open(DATA / "artifact-verification.csv", encoding="utf-8")))
    targets = []
    for r in art:
        if r["has_repo"] != "1":
            continue
        for u in r["repo_urls"].split(" | "):
            if u.strip():
                targets.append((r["arxiv_id"], u.strip()))
    if len(sys.argv) > 1:
        targets = [t for t in targets if t[0] in sys.argv[1:]]

    done = set()
    if OUT.exists():
        done = {(r["arxiv_id"], r["url"]) for r in csv.DictReader(open(OUT, encoding="utf-8"))}
    todo = [t for t in targets if t not in done]
    print(f"{len(targets)} repo URLs; {len(done)} done; {len(todo)} to check", flush=True)
    if TOKEN:
        print("using GITHUB_TOKEN (5000 req/hr)", flush=True)
    else:
        print("NO GitHub token found — unauthenticated limit is 60 req/hr; "
              "set GITHUB_TOKEN to run the full sweep", flush=True)

    with open(OUT, "a", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        if not done:
            w.writeheader()
        workers = 8 if TOKEN else 1
        with ThreadPoolExecutor(max_workers=workers) as ex:
            for n, row in enumerate(ex.map(lambda t: check(*t), todo), 1):
                w.writerow(row)
                f.flush()
                if n % 50 == 0:
                    print(f"  {n}/{len(todo)}", flush=True)
                if not TOKEN:
                    time.sleep(1.2)
    print("done -> data/phase-r-availability.csv")


if __name__ == "__main__":
    main()
