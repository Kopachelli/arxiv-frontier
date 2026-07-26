"""Mechanical internal-consistency checks on the published corpus.

These are rules the protocol and codebook already imply; violating them is an error
regardless of anyone's judgement. Prompted by Phase V audit flags (see
data/phase-v-arm2.csv), which surfaced one genuine violation among many false alarms.

Usage: python code/check_consistency.py
"""

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def main():
    coded = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "coded-corpus.csv", encoding="utf-8"))}
    fin = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "screening-final.csv", encoding="utf-8"))}
    violations = Counter()
    detail = []

    for pid, c in coded.items():
        f = fin.get(pid, {})
        included = f.get("final_decision") == "include"

        # C1. Amendment A1, BR1 (autonomy floor): an included paper may not demonstrate only
        # assistive autonomy — L0 is precisely what BR1 excludes as EC6_ASSISTIVE.
        if included and c["D2"] == "L0_ASSISTIVE":
            violations["C1_included_but_L0_assistive"] += 1
            detail.append(("C1", pid, c["title"][:70],
                           f"included / {f.get('final_reason', '?')} but coded L0_ASSISTIVE"))

        # C2. Codebook D2: autonomy applies only to SYSTEM or CASE_STUDY; anything else is NA.
        if c["D1"] in ("SYSTEM", "CASE_STUDY") and c["D2"] == "NA":
            violations["C2_system_with_NA_autonomy"] += 1
            detail.append(("C2", pid, c["title"][:70], f"D1={c['D1']} but D2=NA"))
        if c["D1"] not in ("SYSTEM", "CASE_STUDY") and c["D2"] not in ("NA", "UNCLEAR"):
            violations["C3_nonsystem_with_autonomy_level"] += 1
            detail.append(("C3", pid, c["title"][:70], f"D1={c['D1']} but D2={c['D2']}"))

        # C4. UNCLEAR should be paired with a full-text flag, per the coding instruction.
        if any("UNCLEAR" in c[d] for d in ("D1", "D2", "D3", "D4", "D5", "D6", "D8", "D9")) \
                and c["needs_fulltext"] != "1":
            violations["C4_unclear_without_fulltext_flag"] += 1
            detail.append(("C4", pid, c["title"][:70], "has UNCLEAR but needs_fulltext=0"))

        # C5. A paper with no system should not be credited with lifecycle stages.
        if c["D1"] in ("POSITION", "SURVEY") and c["D3"] not in ("NA", "UNCLEAR", ""):
            violations["C5_position_survey_with_stages"] += 1
            detail.append(("C5", pid, c["title"][:70], f"D1={c['D1']} but D3={c['D3']}"))

    print(f"corpus: {len(coded)} coded papers\n")
    if not violations:
        print("no internal-consistency violations")
    for k, n in violations.most_common():
        print(f"  {k}: {n}")
    print()
    for code in sorted({d[0] for d in detail}):
        rows = [d for d in detail if d[0] == code]
        print(f"\n--- {code} ({len(rows)}) ---")
        for _, pid, title, why in rows[:12]:
            print(f"  {pid}  {title}\n      {why}")
        if len(rows) > 12:
            print(f"  ... and {len(rows) - 12} more")

    with open(DATA / "consistency-violations.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["rule", "arxiv_id", "title", "detail"])
        w.writerows(detail)
    print(f"\nwrote data/consistency-violations.csv ({len(detail)} rows)")


if __name__ == "__main__":
    main()
