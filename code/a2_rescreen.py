"""Amendment A2b: identify papers affected by the revised BR7 and export them for
re-screening; then merge the revised decisions back into data/screening-final.csv.

  python code/a2_rescreen.py export <dir>
  python code/a2_rescreen.py apply  <dir>

Affected set (reproducible): excluded papers where BR7 was the deciding rule OR the reason
was EC9_GENERIC_DEEPRESEARCH OR the title/abstract mentions "deep research"/"deep
researcher". No other decisions are touched.
"""

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
PAT = re.compile(r"deep\s+research(er)?", re.I)


def affected(fin, cand):
    out = []
    for r in fin:
        if r["final_decision"] == "include":
            continue
        m = cand.get(r["arxiv_id"], {})
        text = (m.get("title", "") + " " + m.get("abstract", ""))
        if (r["rule_applied"] == "BR7"
                or r["final_reason"] == "EC9_GENERIC_DEEPRESEARCH"
                or PAT.search(text)):
            out.append(r)
    return out


def load():
    cand = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "candidates.csv", encoding="utf-8"))}
    cand.update(json.loads((DATA / "expert-identified-meta.json").read_text(encoding="utf-8")))
    fin = list(csv.DictReader(open(DATA / "screening-final.csv", encoding="utf-8")))
    return cand, fin


def export(out_dir):
    cand, fin = load()
    aff = affected(fin, cand)
    out = Path(out_dir)
    out.mkdir(parents=True, exist_ok=True)
    papers = []
    for r in aff:
        m = cand[r["arxiv_id"]]
        papers.append({
            "arxiv_id": r["arxiv_id"], "title": m["title"], "abstract": m["abstract"],
            "prior_decision": f'{r["final_decision"]}/{r["final_reason"]} ({r["rule_applied"]})',
        })
    size = 25
    for i in range(0, len(papers), size):
        (out / f"a2-{i // size:03d}.json").write_text(
            json.dumps(papers[i:i + size], indent=1), encoding="utf-8")
    print(f"affected: {len(papers)} papers -> {(len(papers) + size - 1) // size} batches")
    print("prior reasons:", dict(Counter(r["final_reason"] for r in aff).most_common()))


def apply(dec_dir):
    cand, fin = load()
    new = {}
    for f in sorted(Path(dec_dir).glob("a2-*.json")):
        for it in json.loads(f.read_text(encoding="utf-8")):
            new[it["arxiv_id"]] = it
    aff_ids = {r["arxiv_id"] for r in affected(fin, cand)}
    missing = sorted(aff_ids - set(new))
    flipped = 0
    for r in fin:
        it = new.get(r["arxiv_id"])
        if not it:
            continue
        if it["decision"] != r["final_decision"]:
            flipped += 1
        r.update(final_decision=it["decision"], final_reason=it["reason_code"],
                 rule_applied=it.get("rule", ""), justification=it.get("justification", ""))
    with open(DATA / "screening-final.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(fin[0].keys()))
        w.writeheader()
        w.writerows(fin)
    inc = sum(1 for r in fin if r["final_decision"] == "include")
    print(f"re-decided {len(new)} papers; flipped {flipped}; corpus now {inc} included")
    if missing:
        print(f"MISSING ({len(missing)}): {missing[:20]}")


if __name__ == "__main__":
    {"export": export, "apply": apply}[sys.argv[1]](sys.argv[2])
