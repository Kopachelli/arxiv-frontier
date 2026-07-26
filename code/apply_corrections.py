"""Apply adjudicated corrections to the published corpus and write a changelog.

Every change is driven by an adjudication record carrying a verbatim quote from the paper.
Originals are preserved: the pre-correction files are copied to data/v1/ before anything is
modified, so the published v1 record remains exactly reproducible.

  python code/apply_corrections.py <adjudication_results_dir>
"""

import csv
import json
import shutil
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
V1 = DATA / "v1"


def main(resdir):
    items = []
    for f in sorted(Path(resdir).glob("adj-*.json")):
        items += json.loads(f.read_text(encoding="utf-8"))
    adj = {i["arxiv_id"]: i for i in items}
    bad = [i["arxiv_id"] for i in items if len(str(i.get("quote", "")).strip()) < 20]
    if bad:
        sys.exit(f"refusing to apply: verdicts without evidence quotes: {bad}")

    # preserve v1 exactly
    V1.mkdir(exist_ok=True)
    for name in ("screening-final.csv", "coded-corpus.csv"):
        if not (V1 / name).exists():
            shutil.copy2(DATA / name, V1 / name)

    fin = list(csv.DictReader(open(V1 / "screening-final.csv", encoding="utf-8")))
    coded = list(csv.DictReader(open(V1 / "coded-corpus.csv", encoding="utf-8")))
    changes = []

    for r in fin:
        a = adj.get(r["arxiv_id"])
        if a and a["verdict"] == "FIX_SCREENING":
            before = f'{r["final_decision"]}/{r["final_reason"]}'
            r["final_decision"] = "exclude"
            r["final_reason"] = "EC6_ASSISTIVE"
            r["justification"] = ("corrected in v2 after full-text adjudication: "
                                  + str(a.get("reasoning", ""))[:220])
            changes.append({"arxiv_id": r["arxiv_id"], "field": "screening",
                            "before": before, "after": "exclude/EC6_ASSISTIVE",
                            "quote": a["quote"][:300]})

    excluded = {c["arxiv_id"] for c in changes if c["field"] == "screening"}
    new_coded = []
    for r in coded:
        pid = r["arxiv_id"]
        if pid in excluded:
            changes.append({"arxiv_id": pid, "field": "corpus",
                            "before": "in corpus", "after": "removed (now excluded)",
                            "quote": adj[pid]["quote"][:300]})
            continue
        a = adj.get(pid)
        if a and a["verdict"] == "FIX_CODING":
            nv = a["new_value"].strip()
            if nv in ("L1_STAGE", "L2_PIPELINE", "L3_CLOSED_LOOP", "L4_FULL", "L0_ASSISTIVE"):
                changes.append({"arxiv_id": pid, "field": "D2", "before": r["D2"],
                                "after": nv, "quote": a["quote"][:300]})
                r["D2"] = nv
            elif nv == "NA":
                changes.append({"arxiv_id": pid, "field": "D3", "before": r["D3"],
                                "after": "NA", "quote": a["quote"][:300]})
                r["D3"] = "NA"
            else:
                sys.exit(f"unhandled new_value for {pid}: {nv!r}")
        new_coded.append(r)

    with open(DATA / "screening-final.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(fin[0].keys()))
        w.writeheader()
        w.writerows(fin)
    with open(DATA / "coded-corpus.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(new_coded[0].keys()))
        w.writeheader()
        w.writerows(new_coded)
    with open(DATA / "v2-changelog.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["arxiv_id", "field", "before", "after", "quote"])
        w.writeheader()
        w.writerows(changes)

    print(f"corpus: {len(coded)} -> {len(new_coded)} papers")
    print("changes:", dict(Counter(c["field"] for c in changes).most_common()))
    print(f"changelog -> data/v2-changelog.csv ({len(changes)} rows)")
    print("v1 originals preserved in data/v1/")


if __name__ == "__main__":
    main(sys.argv[1])
