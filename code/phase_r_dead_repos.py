"""Why do linked repositories 404 — were they deleted, or never created?

A GitHub 404 is returned both for a repository that once existed and was removed, and for
one that never existed. The owner account distinguishes the common cases:

  owner exists, repo does not   -> the account is real; the repository was renamed, made
                                   private, or (the interesting case) never created
  owner does not exist          -> the account itself is gone or was never created

This matters because the dead-link rate rises in recent cohorts, which is the opposite of
what link rot predicts. Link rot should hit OLD papers hardest.

Usage: python code/phase_r_dead_repos.py
"""

import csv
import json
import os
import re
import urllib.error
import urllib.request
from collections import Counter, defaultdict
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
GH = re.compile(r"github\.com/([\w.\-]+)/([\w.\-]+)", re.I)


def api_status(url):
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


def check(row):
    m = GH.search(row["url"])
    if not m:
        return {**row, "owner_exists": "", "owner_type": "", "diagnosis": "non-github"}
    owner = m.group(1)
    code, d = api_status(f"https://api.github.com/users/{owner}")
    if code == 200:
        return {**row, "owner_exists": "1", "owner_type": d.get("type", ""),
                "diagnosis": "owner_exists_repo_missing"}
    if code == 404:
        return {**row, "owner_exists": "0", "owner_type": "",
                "diagnosis": "owner_missing"}
    return {**row, "owner_exists": "?", "owner_type": "", "diagnosis": f"http_{code}"}


def similar_repo_under_owner(url):
    """Is there a repo under the same owner with a near-identical name?

    Distinguishes a mis-typed URL (artifact exists, citation is wrong) from an artifact that
    is simply absent. A rename is already excluded: the GitHub API follows rename redirects,
    so a renamed repository would have returned 200 rather than 404.
    """
    from difflib import SequenceMatcher
    m = GH.search(url)
    if not m:
        return "", 0.0
    owner, repo = m.group(1), m.group(2).removesuffix(".git").lower()
    best, score = "", 0.0
    for page in (1, 2):
        code, d = api_status(
            f"https://api.github.com/users/{owner}/repos?per_page=100&page={page}")
        if code != 200 or not d:
            break
        for r in d:
            s = SequenceMatcher(None, repo, r["name"].lower()).ratio()
            if s > score:
                best, score = r["name"], s
        if len(d) < 100:
            break
    return best, round(score, 3)


def main():
    avail = list(csv.DictReader(open(DATA / "phase-r-availability.csv", encoding="utf-8")))
    coded = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "coded-corpus.csv", encoding="utf-8"))}
    dead = [{"arxiv_id": r["arxiv_id"], "url": r["url"]}
            for r in avail if r["host"] == "github" and r["status"] == "404"]
    print(f"{len(dead)} dead GitHub URLs to diagnose", flush=True)

    seen, uniq = set(), []
    for d in dead:
        key = GH.search(d["url"]).group(1).lower() if GH.search(d["url"]) else d["url"]
        uniq.append(d)
        seen.add(key)

    with ThreadPoolExecutor(max_workers=8 if TOKEN else 1) as ex:
        out = list(ex.map(check, uniq))

    print("checking for near-name matches under the same owner ...", flush=True)
    with ThreadPoolExecutor(max_workers=6 if TOKEN else 1) as ex:
        sims = list(ex.map(lambda r: similar_repo_under_owner(r["url"]), out))
    for r, (name, score) in zip(out, sims):
        r["closest_repo_same_owner"] = name
        r["name_similarity"] = score
        r["likely_typo"] = "1" if score >= 0.85 else "0"

    for r in out:
        c = coded.get(r["arxiv_id"], {})
        r["cohort"] = (lambda d: f"{d[:4]}-H{1 if int(d[5:7]) <= 6 else 2}"
                       if len(d) >= 7 else "unknown")(c.get("first_submitted", ""))
        r["title"] = c.get("title", "")[:70]

    with open(DATA / "phase-r-dead-repos.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(out[0].keys()))
        w.writeheader()
        w.writerows(out)

    print("\nDIAGNOSIS:")
    for k, n in Counter(r["diagnosis"] for r in out).most_common():
        print(f"  {k:28s} {n:4d}  ({n / len(out):.1%})")

    print("\nBY COHORT:")
    by = defaultdict(Counter)
    for r in out:
        by[r["cohort"]][r["diagnosis"]] += 1
    for co in sorted(by):
        c = by[co]
        print(f"  {co:10s} owner-exists {c['owner_exists_repo_missing']:3d}   "
              f"owner-missing {c['owner_missing']:3d}   total {sum(c.values()):3d}")
    typos = [r for r in out if r["likely_typo"] == "1"]
    print(f"\nNEAR-NAME MATCH under the same owner (>=0.85 similarity): {len(typos)}/{len(out)}")
    for r in typos[:12]:
        print(f"  {r['arxiv_id']}  cited '{r['url'].split('/')[-1]}'  "
              f"-> owner has '{r['closest_repo_same_owner']}' ({r['name_similarity']})")
    absent = [r for r in out if r["likely_typo"] == "0"]
    print(f"\nNO near match — artifact absent, not mis-cited: {len(absent)}/{len(out)} "
          f"({len(absent) / len(out):.1%} of dead links)")
    print("\nwrote data/phase-r-dead-repos.csv")


if __name__ == "__main__":
    main()
