"""Repair repository URLs that our own extractor mangled, then recompute the dead-link rate.

Diagnosing the 404s showed that some were not the papers' fault but ours: PDF text
extraction breaks long URLs across lines, so the regex captured a truncated repository name
("SimpleDeepSear" for "SimpleDeepSearcher"), and a trailing ".git" was not stripped in the
availability pass. Reporting those as dead links would blame authors for our defect.

Repair rule (conservative, and recorded per URL):
  a dead URL is repaired only if the same owner has a repository whose name is a
  PREFIX-COMPATIBLE near match (similarity >= 0.85 and the cited name is a prefix of the
  real one, or differs only by a .git suffix or trailing punctuation).
Anything else stays dead.

Usage: python code/phase_r_repair_urls.py
"""

import csv
import json
import os
import re
import urllib.error
import urllib.request
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
GH = re.compile(r"github\.com/([\w.\-]+)/([\w.\-]+)", re.I)


def head(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "arxiv-frontier-phase-r", "Accept": "application/vnd.github+json",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
    try:
        with urllib.request.urlopen(req, timeout=40) as r:
            return r.status, json.load(r)
    except urllib.error.HTTPError as e:
        return e.code, None
    except Exception:
        return -1, None


def main():
    dead = list(csv.DictReader(open(DATA / "phase-r-dead-repos.csv", encoding="utf-8")))
    repairs = []
    for r in dead:
        m = GH.search(r["url"])
        if not m:
            continue
        owner = m.group(1)
        cited = m.group(2).removesuffix(".git").rstrip(".-_")
        cand = r.get("closest_repo_same_owner", "")
        if not cand:
            continue
        # conservative: cited name must be a prefix of the real name (truncation), or equal
        # after stripping .git / trailing punctuation
        prefix_ok = cand.lower().startswith(cited.lower()) and len(cited) >= 6
        exact_ok = cand.lower() == cited.lower()
        if not (prefix_ok or exact_ok):
            continue
        fixed = f"https://github.com/{owner}/{cand}"
        code, d = head(f"https://api.github.com/repos/{owner}/{cand}")
        if code == 200:
            repairs.append({"arxiv_id": r["arxiv_id"], "cited_url": r["url"],
                            "repaired_url": fixed,
                            "reason": "truncated_by_extractor" if prefix_ok else "git_suffix",
                            "similarity": r.get("name_similarity", "")})

    with open(DATA / "phase-r-url-repairs.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["arxiv_id", "cited_url", "repaired_url",
                                          "reason", "similarity"])
        w.writeheader()
        w.writerows(repairs)

    # recompute headline rates
    avail = list(csv.DictReader(open(DATA / "phase-r-availability.csv", encoding="utf-8")))
    repaired_urls = {r["cited_url"] for r in repairs}
    gh = [r for r in avail if r["host"] == "github"]
    dead_before = [r for r in gh if r["status"] == "404"]
    dead_after = [r for r in dead_before if r["url"] not in repaired_urls]

    bypaper = {}
    for r in avail:
        ok = r["status"] == "200" or r["url"] in repaired_urls
        bypaper[r["arxiv_id"]] = bypaper.get(r["arxiv_id"], False) or ok

    print(f"repairs made: {len(repairs)}")
    print("  by reason:", dict(Counter(r["reason"] for r in repairs)))
    for r in repairs:
        print(f"    {r['arxiv_id']}  {r['cited_url'].split('/')[-1]} -> "
              f"{r['repaired_url'].split('/')[-1]}")
    print(f"\nGitHub URL dead rate: {len(dead_before)}/{len(gh)} = "
          f"{len(dead_before) / len(gh):.1%}  ->  corrected "
          f"{len(dead_after)}/{len(gh)} = {len(dead_after) / len(gh):.1%}")
    live_papers = sum(1 for v in bypaper.values() if v)
    print(f"papers with a resolvable repo: {live_papers}/{len(bypaper)} = "
          f"{live_papers / len(bypaper):.1%}")
    print(f"papers where NO linked repo resolves: {len(bypaper) - live_papers} "
          f"({(len(bypaper) - live_papers) / len(bypaper):.1%})")
    print("\nwrote data/phase-r-url-repairs.csv")


if __name__ == "__main__":
    main()
