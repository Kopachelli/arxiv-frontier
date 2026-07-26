"""Phase R, R2: prepare an area for claim-vs-artifact verification, and merge the results.

  python code/phase_r_area.py prepare A1_discovery <outdir>
  python code/phase_r_area.py merge   A1_discovery <resultsdir>

`prepare` assembles, for each paper in the area, everything a verifier needs and nothing it
should not have: the paper's own text, the repository's full file listing, and its README.
The verifier is never shown Paper 1's codes or any prior verdict, so its assessment is not
anchored on ours.

`merge` writes the area's claim ledger. A verdict is discarded, not averaged in, if it lacks
the evidence its verdict type requires (protocol §5): SUPPORTED/DIVERGENT/CONTRADICTED need a
file path; NOT_LOCATED needs the search performed.
"""

import csv
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
TOKEN = os.environ.get("GITHUB_TOKEN") or os.environ.get("GH_TOKEN")
GH = re.compile(r"github\.com/([\w.\-]+)/([\w.\-]+)", re.I)
VERDICTS = {"SUPPORTED", "DIVERGENT", "NOT_LOCATED", "CONTRADICTED", "UNVERIFIABLE"}


def api(url, raw=False):
    req = urllib.request.Request(url, headers={
        "User-Agent": "arxiv-frontier-phase-r",
        "Accept": "application/vnd.github.raw" if raw else "application/vnd.github+json",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read() if raw else json.load(r)


def paper_text(arxiv_id, max_chars=48000):
    """Full text of the paper, from its PDF."""
    try:
        req = urllib.request.Request(f"https://arxiv.org/pdf/{arxiv_id}",
                                     headers={"User-Agent": "arxiv-frontier-phase-r"})
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = r.read()
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        out = []
        for p in reader.pages:
            try:
                out.append(p.extract_text() or "")
            except Exception:
                pass
        return "\n".join(out)[:max_chars]
    except Exception as e:
        return f"(paper text unavailable: {type(e).__name__})"


def repo_snapshot(url, branch, max_files=600):
    m = GH.search(url)
    if not m:
        return {"error": "unsupported host"}
    owner, repo = m.group(1), m.group(2).removesuffix(".git")
    snap = {"owner": owner, "repo": repo, "url": url}
    try:
        tree = api(f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1")
    except Exception as e:
        return {**snap, "error": f"tree unavailable: {type(e).__name__}"}
    files = [t["path"] for t in tree.get("tree", []) if t.get("type") == "blob"]
    snap["n_files"] = len(files)
    snap["truncated"] = bool(tree.get("truncated"))
    snap["files"] = sorted(files)[:max_files]
    for name in ("README.md", "readme.md", "README.rst", "README.txt"):
        if name in files:
            try:
                snap["readme"] = api(
                    f"https://api.github.com/repos/{owner}/{repo}/contents/{name}",
                    raw=True).decode("utf-8", "replace")[:20000]
                break
            except Exception:
                pass
    return snap


def prepare(area, outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    dims = [r for r in csv.DictReader(open(DATA / "phase-r-dimensions.csv", encoding="utf-8"))
            if r["area"] == area]
    avail = {}
    for r in csv.DictReader(open(DATA / "phase-r-availability.csv", encoding="utf-8")):
        if r["status"] == "200" and r["host"] == "github":
            avail.setdefault(r["arxiv_id"], []).append(r)
    repairs = {}
    p = DATA / "phase-r-url-repairs.csv"
    if p.exists():
        for r in csv.DictReader(open(p, encoding="utf-8")):
            repairs[r["arxiv_id"]] = r["repaired_url"]

    def build(row):
        pid = row["arxiv_id"]
        cands = avail.get(pid, [])
        if cands:
            best = max(cands, key=lambda r: int(r["size_kb"] or 0))
            snap = repo_snapshot(best["url"], best["default_branch"] or "main")
        elif pid in repairs:
            snap = repo_snapshot(repairs[pid], "main")
        else:
            snap = {"error": "no resolvable repository"}
        return {
            "arxiv_id": pid,
            "title": row["title"],
            "archetype": row["archetype"],
            "paper_text": paper_text(pid),
            "repository": snap,
        }

    with ThreadPoolExecutor(max_workers=5) as ex:
        items = list(ex.map(build, dims))

    for i, it in enumerate(items):
        (out / f"{area}-{i:03d}.json").write_text(json.dumps(it, indent=1), encoding="utf-8")
    ok = sum(1 for it in items if "error" not in it["repository"])
    print(f"{area}: {len(items)} papers prepared, {ok} with a readable repository tree")
    print(f"  -> {out}")


def merge(area, resultsdir):
    rows, discarded = [], []
    for f in sorted(Path(resultsdir).glob(f"{area}-*.json")):
        try:
            items = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            discarded.append((f.name, f"unparseable: {e}"))
            continue
        for it in items if isinstance(items, list) else [items]:
            for c in it.get("claims", []):
                v = str(c.get("verdict", "")).upper()
                ev = str(c.get("evidence", "")).strip()
                if v not in VERDICTS:
                    discarded.append((it.get("arxiv_id"), f"bad verdict {v!r}"))
                    continue
                # evidence requirement, per protocol §5
                if v in ("SUPPORTED", "DIVERGENT", "CONTRADICTED") and len(ev) < 3:
                    discarded.append((it.get("arxiv_id"), f"{v} without a file path"))
                    continue
                if v == "NOT_LOCATED" and len(ev) < 10:
                    discarded.append((it.get("arxiv_id"), "NOT_LOCATED without a search record"))
                    continue
                rows.append({
                    "arxiv_id": it.get("arxiv_id", ""),
                    "area": area,
                    "claim_id": c.get("claim_id", ""),
                    "claim_type": c.get("claim_type", ""),
                    "claim_text": str(c.get("claim_text", ""))[:400],
                    "verdict": v,
                    "evidence": ev[:400],
                    "level_reached": c.get("level_reached", "R2"),
                    "note": str(c.get("note", ""))[:300],
                })
    if not rows:
        print("no usable verdicts")
        return
    with open(DATA / f"phase-r-ledger-{area}.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    papers = {r["arxiv_id"] for r in rows}
    print(f"{area}: {len(rows)} claims across {len(papers)} papers")
    print("\nVERDICTS:")
    for k, n in Counter(r["verdict"] for r in rows).most_common():
        print(f"  {k:14s} {n:4d}  ({n / len(rows):.1%})")
    print("\nBY CLAIM TYPE:")
    bt = {}
    for r in rows:
        bt.setdefault(r["claim_type"], Counter())[r["verdict"]] += 1
    for t, c in sorted(bt.items()):
        tot = sum(c.values())
        print(f"  {t:22s} n={tot:3d}  supported={c['SUPPORTED'] / tot:.0%}  "
              f"not_located={c['NOT_LOCATED'] / tot:.0%}  contradicted={c['CONTRADICTED'] / tot:.0%}")
    if discarded:
        print(f"\nDISCARDED for missing evidence ({len(discarded)}):")
        for d in discarded[:15]:
            print("  ", d)
    print(f"\nwrote data/phase-r-ledger-{area}.csv")


if __name__ == "__main__":
    cmd, area, arg = sys.argv[1], sys.argv[2], sys.argv[3]
    {"prepare": prepare, "merge": merge}[cmd](area, arg)
