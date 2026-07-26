"""Phase R: assign the partition and cross-cutting dimensions to every repo-bearing paper.

Mechanical wherever possible. Each dimension records how it was derived so a reader can
check it:
  A  area          — from Paper 1's codes, first-match-wins precedence (protocol §3)
  B  domain        — Paper 1 code D4
  D  cohort        — half-year bin of first submission
  E  archetype     — from the repository's own file listing (GitHub API tree)
  F  lineage       — seed-system citation / fork / explicit mention
  H  institution   — author affiliation type, aggregate-only per protocol §7

  python code/phase_r_dimensions.py assign     # A, B, D — instant, no network
  python code/phase_r_dimensions.py archetype  # E — needs GITHUB_TOKEN
  python code/phase_r_dimensions.py lineage    # F — full-text scan (uses cached PDFs)
"""

import csv
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

# ---------------------------------------------------------------- A: areas
def area_of(coded, fin, cand):
    """First match wins, in protocol order."""
    d1, d2, d3, d4, d8 = coded["D1"], coded["D2"], coded["D3"], coded["D4"], coded["D8"]
    stages = set(d3.split(";"))
    if d8 == "DISCOVERY":
        return "A1_discovery"
    if fin.get("final_reason") == "IC3":
        return "A2_auditability"
    if d2 in ("L3_CLOSED_LOOP", "L4_FULL"):
        return "A3_end_to_end"
    if "EXECUTION" in stages and d4 in ("MATERIALS", "CHEMISTRY", "PHYSICS"):
        return "A4_self_driving_lab"
    if d1 == "BENCHMARK":
        return "A5_benchmark"
    if fin.get("rule_applied") == "BR7":
        return "A6_deep_research"
    if "IDEATION" in stages:
        return "A7_ideation"
    if d4 == "BIOMED":
        return "A8_biomedical"
    return "A9_other"


def cohort_of(date):
    if len(date) < 7:
        return "unknown"
    y, m = date[:4], int(date[5:7])
    return f"{y}-H{1 if m <= 6 else 2}"


def assign(_arg=None):
    cand = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "candidates.csv", encoding="utf-8"))}
    cand.update(json.loads((DATA / "expert-identified-meta.json").read_text(encoding="utf-8")))
    coded = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "coded-corpus.csv", encoding="utf-8"))}
    fin = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "screening-final.csv", encoding="utf-8"))}
    art = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "artifact-verification.csv", encoding="utf-8"))}

    rows = []
    for pid, c in coded.items():
        a = art.get(pid, {})
        if a.get("has_repo") != "1":
            continue
        rows.append({
            "arxiv_id": pid,
            "title": c["title"],
            "area": area_of(c, fin.get(pid, {}), cand.get(pid, {})),
            "domain": c["D4"],
            "cohort": cohort_of(c["first_submitted"]),
            "first_submitted": c["first_submitted"],
            "claim_strength": c["D8"],
            "autonomy": c["D2"],
            "paper_type": c["D1"],
            "repo_urls": a.get("repo_urls", ""),
            "archetype": "", "lineage": "", "institution": "",
        })
    rows.sort(key=lambda r: (r["area"], r["arxiv_id"]))
    _write(rows, "phase-r-dimensions.csv")
    print(f"{len(rows)} repo-bearing papers assigned\n")
    print("AREAS (partition A):")
    for k, n in sorted(Counter(r["area"] for r in rows).items()):
        print(f"  {k:24s} {n:4d}")
    print("\nCOHORTS (dimension D):")
    for k, n in sorted(Counter(r["cohort"] for r in rows).items()):
        print(f"  {k:10s} {n:4d}")
    print("\nDOMAINS (dimension B):")
    for k, n in Counter(r["domain"] for r in rows).most_common():
        print(f"  {k:14s} {n:4d}")


# ------------------------------------------------------- E: artifact archetype
CODE_EXT = {".py", ".ipynb", ".r", ".jl", ".cpp", ".c", ".java", ".go", ".rs", ".ts", ".js",
            ".sh", ".m", ".lean", ".f90"}
DATA_EXT = {".csv", ".json", ".jsonl", ".parquet", ".h5", ".hdf5", ".npy", ".npz", ".tsv",
            ".xlsx", ".pkl", ".arrow", ".db", ".sqlite", ".mat", ".cif", ".pdb"}
CONFIG = {"requirements.txt", "environment.yml", "pyproject.toml", "setup.py", "dockerfile",
          "conda.yaml", "poetry.lock", "package.json", "makefile", "environment.yaml"}
PROMPT_HINT = re.compile(r"prompt|template|instruction", re.I)
APP_HINT = re.compile(r"(streamlit|gradio|app\.py|demo|frontend|webui)", re.I)


def api(url):
    req = urllib.request.Request(url, headers={
        "User-Agent": "arxiv-frontier-phase-r", "Accept": "application/vnd.github+json",
        **({"Authorization": f"Bearer {TOKEN}"} if TOKEN else {})})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def classify_repo(url, branch):
    m = GH.search(url)
    if not m:
        return "UNSUPPORTED", 0, ""
    owner, repo = m.group(1), m.group(2).removesuffix(".git")
    try:
        tree = api(f"https://api.github.com/repos/{owner}/{repo}/git/trees/{branch}?recursive=1")
    except urllib.error.HTTPError as e:
        return ("DEAD" if e.code == 404 else f"ERR{e.code}"), 0, ""
    except Exception as e:
        return f"ERR:{type(e).__name__}", 0, ""

    files = [t["path"] for t in tree.get("tree", []) if t.get("type") == "blob"]
    if not files:
        return "STUB", 0, ""
    low = [f.lower() for f in files]
    has_code = any(Path(f).suffix in CODE_EXT for f in low)
    has_data = any(Path(f).suffix in DATA_EXT for f in low)
    has_cfg = any(Path(f).name in CONFIG for f in low)
    has_prompt = any(PROMPT_HINT.search(f) for f in low)
    has_app = any(APP_HINT.search(f) for f in low)
    non_doc = [f for f in low if Path(f).suffix not in {".md", ".txt", ".rst", ".pdf", ".png",
                                                        ".jpg", ".gitignore", ""}]

    if len(non_doc) <= 1:
        arch = "STUB"
    elif has_code and has_data and has_cfg:
        arch = "FULL_PIPELINE"
    elif has_app and not has_cfg:
        arch = "DEMO_APP"
    elif has_code:
        arch = "CODE_ONLY"
    elif has_data:
        arch = "DATA_ONLY"
    elif has_prompt:
        arch = "PROMPTS_ONLY"
    else:
        arch = "STUB"
    return arch, len(files), ";".join(sorted({Path(f).suffix for f in low if Path(f).suffix})[:12])


def archetype(_arg=None):
    dims = list(csv.DictReader(open(DATA / "phase-r-dimensions.csv", encoding="utf-8")))
    avail = {}
    for r in csv.DictReader(open(DATA / "phase-r-availability.csv", encoding="utf-8")):
        if r["status"] == "200" and r["host"] == "github":
            avail.setdefault(r["arxiv_id"], []).append(r)

    def work(row):
        cands = avail.get(row["arxiv_id"], [])
        if not cands:
            return row["arxiv_id"], "DEAD", 0, ""
        best = max(cands, key=lambda r: int(r["size_kb"] or 0))
        a, n, ext = classify_repo(best["url"], best["default_branch"] or "main")
        return row["arxiv_id"], a, n, ext

    out = {}
    with ThreadPoolExecutor(max_workers=8 if TOKEN else 1) as ex:
        for n, (pid, a, nf, ext) in enumerate(ex.map(work, dims), 1):
            out[pid] = (a, nf, ext)
            if n % 50 == 0:
                print(f"  {n}/{len(dims)}", flush=True)
    for r in dims:
        a, nf, ext = out.get(r["arxiv_id"], ("", 0, ""))
        r["archetype"] = a
        r["n_files"] = nf
        r["extensions"] = ext
    _write(dims, "phase-r-dimensions.csv")
    print("\nARCHETYPES (dimension E):")
    for k, n in Counter(r["archetype"] for r in dims).most_common():
        print(f"  {k:16s} {n:4d}")


# --------------------------------------------------------------- F: lineage
SEEDS = {
    "ai_scientist": re.compile(r"AI[- ]Scientist|SakanaAI/AI-Scientist|2408\.06292|2504\.08066", re.I),
    "agent_laboratory": re.compile(r"Agent Laborator|AgentLaboratory|2501\.04227", re.I),
    "co_scientist": re.compile(r"co-scientist|coscientist|2502\.18864", re.I),
    "chemcrow": re.compile(r"ChemCrow", re.I),
    "aider_swe": re.compile(r"SWE-?agent|OpenHands|Devin", re.I),
    "deep_research_openai": re.compile(r"OpenAI Deep Research|Gemini Deep Research", re.I),
}


def lineage(_arg=None):
    dims = list(csv.DictReader(open(DATA / "phase-r-dimensions.csv", encoding="utf-8")))
    cand = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "candidates.csv", encoding="utf-8"))}
    for r in dims:
        text = (cand.get(r["arxiv_id"], {}).get("title", "") + " "
                + cand.get(r["arxiv_id"], {}).get("abstract", ""))
        hits = [k for k, pat in SEEDS.items() if pat.search(text)]
        r["lineage"] = ";".join(hits) if hits else "none_detected_abstract"
    _write(dims, "phase-r-dimensions.csv")
    print("LINEAGE from title+abstract (dimension F, provisional — full-text pass pending):")
    c = Counter(x for r in dims for x in r["lineage"].split(";"))
    for k, n in c.most_common():
        print(f"  {k:28s} {n:4d}")
    print("\nNOTE: abstracts rarely name the seed system. The authoritative lineage pass reads "
          "full text and GitHub fork metadata; this is a floor, not an estimate.")


def _write(rows, name):
    with open(DATA / name, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


if __name__ == "__main__":
    {"assign": assign, "archetype": archetype, "lineage": lineage}[sys.argv[1]]()
