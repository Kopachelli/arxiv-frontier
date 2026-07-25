"""Screening support: batch preparation and result merging (protocol section 5).

  python code/screen.py batches <batch_dir>   # split codable candidates into JSON batches
  python code/screen.py merge <results_dir>   # merge pass A/B results -> screening CSV

Batches contain candidates first-submitted >= 2024-01-01 plus the expert-identified
records (fetched live by ID). Merge writes data/screening-decisions.csv with both passes
joined per paper and an `agreement` column; disagreements/borderlines are adjudicated
separately and appended by the adjudication step.
"""

import csv
import json
import sys
from collections import Counter
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
BATCH_SIZE = 25
CODABLE_FROM = "2024-01-01"
NS = {"atom": "http://www.w3.org/2005/Atom"}


def fetch_meta(arxiv_id):
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"id_list": arxiv_id, "max_results": 1})
    with urllib.request.urlopen(url, timeout=60) as r:
        root = ET.fromstring(r.read())
    e = root.find("atom:entry", NS)
    title = " ".join(e.findtext("atom:title", "", NS).split())
    abstract = " ".join(e.findtext("atom:summary", "", NS).split())
    return {"arxiv_id": arxiv_id, "title": title, "abstract": abstract}


def make_batches(batch_dir):
    out = Path(batch_dir)
    out.mkdir(parents=True, exist_ok=True)
    rows = list(csv.DictReader(open(DATA / "candidates.csv", encoding="utf-8")))
    papers = [
        {"arxiv_id": r["arxiv_id"], "title": r["title"], "abstract": r["abstract"]}
        for r in rows if r["first_submitted"] >= CODABLE_FROM
    ]
    seen = {p["arxiv_id"] for p in papers}
    for r in csv.DictReader(open(DATA / "expert-identified.csv", encoding="utf-8")):
        if r["arxiv_id"] not in seen:
            papers.append(fetch_meta(r["arxiv_id"]))
            time.sleep(3)
    for i in range(0, len(papers), BATCH_SIZE):
        name = f"batch-{i // BATCH_SIZE:03d}"
        (out / f"{name}.json").write_text(
            json.dumps(papers[i:i + BATCH_SIZE], indent=1), encoding="utf-8")
    n_batches = (len(papers) + BATCH_SIZE - 1) // BATCH_SIZE
    print(f"{len(papers)} papers -> {n_batches} batches in {out}")


def merge(results_dir):
    res = Path(results_dir)
    passes = {"A": {}, "B": {}}
    problems = []
    for f in sorted(res.glob("batch-*-pass*.json")):
        pass_id = f.stem[-1]
        try:
            items = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{f.name}: unparseable ({e})")
            continue
        for it in items:
            pid = it.get("arxiv_id", "").strip()
            if not pid:
                problems.append(f"{f.name}: entry without arxiv_id")
                continue
            if pid in passes[pass_id]:
                problems.append(f"{f.name}: duplicate {pid} in pass {pass_id}")
            passes[pass_id][pid] = it

    all_ids = sorted(set(passes["A"]) | set(passes["B"]))
    out_rows = []
    for pid in all_ids:
        a, b = passes["A"].get(pid), passes["B"].get(pid)
        if a is None or b is None:
            problems.append(f"{pid}: missing pass {'A' if a is None else 'B'}")
            continue
        da, db = a["decision"], b["decision"]
        if da == db and da != "borderline":
            agreement, final = "agree", da
        else:
            agreement, final = "needs_adjudication", ""
        out_rows.append({
            "arxiv_id": pid,
            "passA_decision": da, "passA_reason": a.get("reason_code", ""),
            "passA_justification": a.get("justification", ""),
            "passB_decision": db, "passB_reason": b.get("reason_code", ""),
            "passB_justification": b.get("justification", ""),
            "agreement": agreement, "final_decision": final,
            "final_reason": a.get("reason_code", "") if agreement == "agree" else "",
            "adjudicated": "0", "adjudication_rationale": "",
        })

    fields = list(out_rows[0].keys())
    with open(DATA / "screening-decisions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(out_rows)

    n_agree = sum(1 for r in out_rows if r["agreement"] == "agree")
    n_adj = len(out_rows) - n_agree
    n_inc = sum(1 for r in out_rows if r["final_decision"] == "include")
    print(f"papers merged: {len(out_rows)}  agree: {n_agree}  need adjudication: {n_adj}")
    print(f"included so far (pre-adjudication): {n_inc}")
    if problems:
        print(f"\nPROBLEMS ({len(problems)}):")
        for p in problems:
            print(" -", p)


CHUNK = 40


def rescreen_batches(out_dir):
    """Amendment A1: export ALL candidates with Layer-1 context for rule-based re-screening."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cand = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "candidates.csv", encoding="utf-8"))}
    # Expert-identified papers are not in candidates.csv; their metadata is cached here so
    # every paper reaching a screener has a real title+abstract (see errors.md #5).
    meta_cache = DATA / "expert-identified-meta.json"
    if meta_cache.exists():
        cand.update(json.loads(meta_cache.read_text(encoding="utf-8")))
    else:
        extra = {}
        for r in csv.DictReader(open(DATA / "expert-identified.csv", encoding="utf-8")):
            if r["arxiv_id"] not in cand:
                extra[r["arxiv_id"]] = fetch_meta(r["arxiv_id"])
                time.sleep(3)
        meta_cache.write_text(json.dumps(extra, indent=1), encoding="utf-8")
        cand.update(extra)
    l1 = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "screening-decisions.csv", encoding="utf-8"))}
    papers = []
    for pid, d in l1.items():
        c = cand.get(pid, {})
        if not c.get("abstract"):
            raise SystemExit(f"refusing to export {pid} with no abstract — fix metadata first")
        papers.append({
            "arxiv_id": pid,
            "title": c.get("title", ""),
            "abstract": c.get("abstract", ""),
            "layer1_A": f'{d["passA_decision"]}: {d["passA_justification"]}',
            "layer1_B": f'{d["passB_decision"]}: {d["passB_justification"]}',
        })
    papers.sort(key=lambda p: p["arxiv_id"])
    size = 25
    for i in range(0, len(papers), size):
        (out / f"rs-{i // size:03d}.json").write_text(
            json.dumps(papers[i:i + size], indent=1), encoding="utf-8")
    print(f"{len(papers)} papers -> {(len(papers) + size - 1) // size} re-screen batches in {out}")


def rescreen_merge(results_dir):
    """Merge rule-based re-screen results into data/screening-final.csv."""
    l1 = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "screening-decisions.csv", encoding="utf-8"))}
    final, problems = {}, []
    for f in sorted(Path(results_dir).glob("rs-*.json")):
        try:
            items = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{f.name}: unparseable ({e})")
            continue
        for it in items:
            pid = it.get("arxiv_id", "").strip()
            if not pid:
                problems.append(f"{f.name}: entry without arxiv_id")
                continue
            final[pid] = it
    missing = [p for p in l1 if p not in final]
    rows = []
    for pid in sorted(l1):
        it = final.get(pid)
        if it is None:
            continue
        d1a, d1b = l1[pid]["passA_decision"], l1[pid]["passB_decision"]
        l1_unanimous_include = d1a == "include" and d1b == "include"
        rows.append({
            "arxiv_id": pid,
            "final_decision": it.get("decision", ""),
            "final_reason": it.get("reason_code", ""),
            "rule_applied": it.get("rule", ""),
            "justification": it.get("justification", ""),
            "layer1_A": d1a, "layer1_B": d1b,
            "layer1_agreement": l1[pid]["agreement"],
            "reverses_unanimous_include":
                "1" if (l1_unanimous_include and it.get("decision") != "include") else "0",
        })
    with open(DATA / "screening-final.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    inc = [r for r in rows if r["final_decision"] == "include"]
    print(f"final screened: {len(rows)}   INCLUDED: {len(inc)}   excluded: {len(rows) - len(inc)}")
    print("exclusion reasons:", dict(Counter(
        r["final_reason"] for r in rows if r["final_decision"] != "include").most_common()))
    print("inclusion reasons:", dict(Counter(r["final_reason"] for r in inc).most_common()))
    print("reversals of unanimous L1 includes:",
          sum(1 for r in rows if r["reverses_unanimous_include"] == "1"))
    if missing:
        print(f"MISSING from re-screen ({len(missing)}): {missing[:20]}")
    for p in problems:
        print(" -", p)


def adjudicate_export(out_dir):
    """Write needs_adjudication rows (joined with abstracts) into chunk files."""
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    cand = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "candidates.csv", encoding="utf-8"))}
    for r in csv.DictReader(open(DATA / "expert-identified.csv", encoding="utf-8")):
        cand.setdefault(r["arxiv_id"], {"title": r["title"], "abstract": "(expert-identified; fetch on demand)"})
    rows = [r for r in csv.DictReader(open(DATA / "screening-decisions.csv", encoding="utf-8"))
            if r["agreement"] == "needs_adjudication"]
    for i in range(0, len(rows), CHUNK):
        chunk = [{
            "arxiv_id": r["arxiv_id"],
            "title": cand.get(r["arxiv_id"], {}).get("title", "?"),
            "abstract": cand.get(r["arxiv_id"], {}).get("abstract", "?"),
            "A": f'{r["passA_decision"]}/{r["passA_reason"]}: {r["passA_justification"]}',
            "B": f'{r["passB_decision"]}/{r["passB_reason"]}: {r["passB_justification"]}',
        } for r in rows[i:i + CHUNK]]
        (out / f"adj-{i // CHUNK:02d}.json").write_text(
            json.dumps(chunk, indent=1), encoding="utf-8")
    print(f"{len(rows)} papers -> {(len(rows) + CHUNK - 1) // CHUNK} adjudication chunks in {out}")


def adjudicate_apply(dec_dir):
    """Apply adj-*-decisions.json ({arxiv_id: [decision, reason, rationale]}) to the CSV."""
    decisions = {}
    for f in sorted(Path(dec_dir).glob("adj-*-decisions.json")):
        decisions.update(json.loads(f.read_text(encoding="utf-8")))
    rows = list(csv.DictReader(open(DATA / "screening-decisions.csv", encoding="utf-8")))
    n = 0
    for r in rows:
        if r["arxiv_id"] in decisions:
            d, reason, rationale = decisions[r["arxiv_id"]]
            r.update(final_decision=d, final_reason=reason, adjudicated="1",
                     adjudication_rationale=rationale, agreement="adjudicated")
            n += 1
    with open(DATA / "screening-decisions.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    remaining = sum(1 for r in rows if r["agreement"] == "needs_adjudication")
    inc = sum(1 for r in rows if r["final_decision"] == "include")
    print(f"applied {n} adjudications; remaining unadjudicated: {remaining}; total included: {inc}")


if __name__ == "__main__":
    cmd, arg = sys.argv[1], sys.argv[2]
    {"batches": make_batches, "merge": merge,
     "rescreen-batches": rescreen_batches, "rescreen-merge": rescreen_merge,
     "adjudicate-export": adjudicate_export, "adjudicate-apply": adjudicate_apply}[cmd](arg)
