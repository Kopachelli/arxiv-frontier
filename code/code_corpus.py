"""Phase 4 coding: export included papers in batches, merge coded results.

  python code/code_corpus.py export <dir>          # batches of included papers
  python code/code_corpus.py merge  <dir>          # -> data/coded-corpus.csv
  python code/code_corpus.py consistency <dir>     # export random sample for 3rd screening pass
  python code/code_corpus.py consistency-merge <dir>

Coding dimensions are defined in protocol/codebook.md (normative) and the agent prompt in
protocol/coding-prompt.md.
"""

import csv
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
BATCH = 12
SEED = 20260725

FIELDS = ["arxiv_id", "title", "first_submitted", "primary_category",
          "D1", "D2", "D3", "D4", "D5", "D6", "D7_code", "D7_data", "D8", "D9",
          "needs_fulltext", "evidence"]

VALID = {
    "D1": {"SYSTEM", "BENCHMARK", "FRAMEWORK", "POSITION", "SURVEY", "CASE_STUDY", "UNCLEAR"},
    "D2": {"L0_ASSISTIVE", "L1_STAGE", "L2_PIPELINE", "L3_CLOSED_LOOP", "L4_FULL", "NA", "UNCLEAR"},
    "D3": {"IDEATION", "LITERATURE", "EXP_DESIGN", "EXECUTION", "ANALYSIS", "WRITING", "REVIEW",
           "NA", "UNCLEAR"},
    "D4": {"GENERAL_ML", "MATERIALS", "BIOMED", "PHYSICS", "CHEMISTRY", "MATH_FORMAL", "SOFTWARE",
           "SOCIAL_SCI", "MULTI", "OTHER", "UNCLEAR"},
    "D5": {"NONE", "LLM_JUDGE", "HUMAN_EXPERT", "BENCHMARK_METRIC", "HELD_OUT_TRANSFER",
           "REAL_WORLD", "UNCLEAR"},
    "D6": {"TRACES", "PROVENANCE", "REPRO_ARTIFACTS", "FORMAL_VERIF", "UNCERTAINTY", "NONE",
           "UNCLEAR"},
    "D7_code": {"YES", "PARTIAL", "NO", "UNCLEAR"},
    "D7_data": {"YES", "PARTIAL", "NO", "UNCLEAR"},
    "D8": {"DISCOVERY", "CAPABILITY", "METHOD", "CONCEPTUAL", "UNCLEAR"},
    "D9": {"NONE_CLAIMED", "GATEKEEPER", "EVALUATOR", "CO_PERFORMER", "UNSPECIFIED", "UNCLEAR"},
}
MULTI = {"D3", "D5", "D6"}


def load_included():
    cand = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "candidates.csv", encoding="utf-8"))}
    cand.update(json.loads((DATA / "expert-identified-meta.json").read_text(encoding="utf-8")))
    fin = [r for r in csv.DictReader(open(DATA / "screening-final.csv", encoding="utf-8"))
           if r["final_decision"] == "include"]
    out = []
    for r in fin:
        m = cand[r["arxiv_id"]]
        out.append({"arxiv_id": r["arxiv_id"], "title": m["title"], "abstract": m["abstract"],
                    "first_submitted": m.get("first_submitted", ""),
                    "primary_category": m.get("primary_category", "")})
    out.sort(key=lambda p: p["arxiv_id"])
    return out


def export(out_dir):
    papers = load_included()
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    for i in range(0, len(papers), BATCH):
        chunk = [{k: p[k] for k in ("arxiv_id", "title", "abstract")}
                 for p in papers[i:i + BATCH]]
        (out / f"code-{i // BATCH:03d}.json").write_text(
            json.dumps(chunk, indent=1), encoding="utf-8")
    print(f"{len(papers)} papers -> {(len(papers) + BATCH - 1) // BATCH} coding batches in {out}")


def merge(results_dir):
    papers = {p["arxiv_id"]: p for p in load_included()}
    coded, problems = {}, []
    for f in sorted(Path(results_dir).glob("code-*.json")):
        try:
            items = json.loads(f.read_text(encoding="utf-8"))
        except json.JSONDecodeError as e:
            problems.append(f"{f.name}: unparseable ({e})")
            continue
        for it in items:
            pid = str(it.get("arxiv_id", "")).strip()
            if pid not in papers:
                problems.append(f"{f.name}: unknown id {pid!r}")
                continue
            if pid in coded:
                problems.append(f"{f.name}: duplicate {pid}")
            coded[pid] = it

    rows, invalid = [], Counter()
    for pid in sorted(papers):
        it = coded.get(pid)
        if it is None:
            problems.append(f"{pid}: not coded")
            continue
        row = {"arxiv_id": pid, "title": papers[pid]["title"],
               "first_submitted": papers[pid]["first_submitted"],
               "primary_category": papers[pid]["primary_category"]}
        for dim, allowed in VALID.items():
            raw = str(it.get(dim, "") or "").strip()
            if dim in MULTI:
                vals = [v.strip().upper() for v in raw.replace(",", ";").split(";") if v.strip()]
                bad = [v for v in vals if v not in allowed]
                for b in bad:
                    invalid[f"{dim}:{b}"] += 1
                vals = [v for v in vals if v in allowed] or ["UNCLEAR"]
                row[dim] = ";".join(dict.fromkeys(vals))
            else:
                v = raw.upper()
                if v not in allowed:
                    invalid[f"{dim}:{v}"] += 1
                    v = "UNCLEAR"
                row[dim] = v
        row["needs_fulltext"] = "1" if it.get("needs_fulltext") in (True, "true", "1") else "0"
        row["evidence"] = str(it.get("evidence", ""))[:400].replace("\n", " ")
        rows.append(row)

    with open(DATA / "coded-corpus.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)
    print(f"coded {len(rows)}/{len(papers)} papers -> data/coded-corpus.csv")
    print(f"needs_fulltext flagged: {sum(1 for r in rows if r['needs_fulltext'] == '1')}")
    if invalid:
        print("invalid codes coerced to UNCLEAR:", dict(invalid.most_common(15)))
    for p in problems[:25]:
        print(" -", p)
    if len(problems) > 25:
        print(f" ... and {len(problems) - 25} more")


def consistency(out_dir):
    """Random sample of screened papers for an independent third screening pass."""
    fin = list(csv.DictReader(open(DATA / "screening-final.csv", encoding="utf-8")))
    cand = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "candidates.csv", encoding="utf-8"))}
    cand.update(json.loads((DATA / "expert-identified-meta.json").read_text(encoding="utf-8")))
    sample = random.Random(SEED).sample(fin, 120)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    papers = [{"arxiv_id": r["arxiv_id"], "title": cand[r["arxiv_id"]]["title"],
               "abstract": cand[r["arxiv_id"]]["abstract"]} for r in sample]
    for i in range(0, len(papers), 20):
        (out / f"cons-{i // 20:03d}.json").write_text(
            json.dumps(papers[i:i + 20], indent=1), encoding="utf-8")
    print(f"{len(papers)} papers -> {(len(papers) + 19) // 20} consistency batches")


def consistency_merge(results_dir):
    fin = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "screening-final.csv", encoding="utf-8"))}
    third = {}
    for f in sorted(Path(results_dir).glob("cons-*.json")):
        for it in json.loads(f.read_text(encoding="utf-8")):
            third[it["arxiv_id"]] = it["decision"]
    pairs = [(fin[p]["final_decision"], d) for p, d in third.items() if p in fin]
    agree = sum(1 for a, b in pairs if a == b)
    rows = [{"arxiv_id": p, "layer2": fin[p]["final_decision"], "pass3": d,
             "agree": int(fin[p]["final_decision"] == d)} for p, d in third.items() if p in fin]
    with open(DATA / "screening-consistency.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["arxiv_id", "layer2", "pass3", "agree"])
        w.writeheader()
        w.writerows(rows)
    print(f"third-pass agreement with Layer 2: {agree}/{len(pairs)} = {agree / len(pairs):.3f}")


if __name__ == "__main__":
    {"export": export, "merge": merge, "consistency": consistency,
     "consistency-merge": consistency_merge}[sys.argv[1]](sys.argv[2])
