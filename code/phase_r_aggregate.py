"""Aggregate every completed Phase R area ledger and test the cross-area pattern.

Reads all data/phase-r-ledger-*.csv that exist, so it works at any point in the programme
and will serve the cycle-6 cross-cutting papers unchanged.

Usage: python code/phase_r_aggregate.py
"""

import csv
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"

ORDER = ["SUPPORTED", "DIVERGENT", "NOT_LOCATED", "CONTRADICTED", "UNVERIFIABLE"]
AREA_LABEL = {
    "A1_discovery": "A1 discovery",
    "A2_auditability": "A2 auditability",
    "A3_end_to_end": "A3 end-to-end",
    "A4_physical_life_sciences": "A4 physical & life sci",
    "A5_benchmark": "A5 benchmark",
    "A6_deep_research": "A6 deep research",
    "A7_ideation": "A7 ideation",
    "A8_scholarly_record": "A8 scholarly record",
    "A9_research_infrastructure": "A9 research infra",
}


def load_all():
    rows = []
    for p in sorted(DATA.glob("phase-r-ledger-*.csv")):
        rows += list(csv.DictReader(open(p, encoding="utf-8")))
    return rows


def pct(n, d):
    return f"{n / d:.0%}" if d else "--"


def main():
    rows = load_all()
    if not rows:
        print("no ledgers yet")
        return
    areas = sorted({r["area"] for r in rows})
    papers = {(r["area"], r["arxiv_id"]) for r in rows}
    print(f"PHASE R AGGREGATE — {len(areas)} of 9 areas | {len(papers)} papers | "
          f"{len(rows)} claims\n")

    print("VERDICTS OVERALL")
    c = Counter(r["verdict"] for r in rows)
    for v in ORDER:
        if c[v]:
            print(f"  {v:14s} {c[v]:5d}  {pct(c[v], len(rows)):>5s}")

    print("\n\nTHE CROSS-AREA TEST: are described methods more locatable than reported numbers?\n")
    hdr = f'{"area":24s}{"n papers":>9s}{"method supported":>18s}{"numeric supported":>19s}{"ratio":>7s}'
    print(hdr)
    print("-" * len(hdr))
    for a in areas:
        sub = [r for r in rows if r["area"] == a]
        np_ = len({r["arxiv_id"] for r in sub})
        m = [r for r in sub if r["claim_type"] == "METHOD_COMPONENT"]
        n = [r for r in sub if r["claim_type"] == "NUMERIC_RESULT"]
        ms = sum(1 for r in m if r["verdict"] == "SUPPORTED")
        ns = sum(1 for r in n if r["verdict"] == "SUPPORTED")
        ratio = (ms / len(m)) / (ns / len(n)) if m and n and ns else float("nan")
        print(f"{AREA_LABEL.get(a, a):24s}{np_:>9d}"
              f"{pct(ms, len(m)) + f' (n={len(m)})':>18s}"
              f"{pct(ns, len(n)) + f' (n={len(n)})':>19s}"
              f"{ratio:>7.1f}")
    m_all = [r for r in rows if r["claim_type"] == "METHOD_COMPONENT"]
    n_all = [r for r in rows if r["claim_type"] == "NUMERIC_RESULT"]
    ms = sum(1 for r in m_all if r["verdict"] == "SUPPORTED")
    ns = sum(1 for r in n_all if r["verdict"] == "SUPPORTED")
    print("-" * len(hdr))
    print(f'{"POOLED":24s}{len(papers):>9d}'
          f"{pct(ms, len(m_all)) + f' (n={len(m_all)})':>18s}"
          f"{pct(ns, len(n_all)) + f' (n={len(n_all)})':>19s}"
          f"{(ms / len(m_all)) / (ns / len(n_all)):>7.1f}")

    print("\n\nNUMERIC RESULTS: what happens to them")
    hdr2 = f'{"area":24s}{"supported":>11s}{"divergent":>11s}{"not located":>13s}{"unverifiable":>14s}'
    print(hdr2)
    print("-" * len(hdr2))
    for a in areas:
        sub = [r for r in rows if r["area"] == a and r["claim_type"] == "NUMERIC_RESULT"]
        c2 = Counter(r["verdict"] for r in sub)
        print(f"{AREA_LABEL.get(a, a):24s}{pct(c2['SUPPORTED'], len(sub)):>11s}"
              f"{pct(c2['DIVERGENT'], len(sub)):>11s}"
              f"{pct(c2['NOT_LOCATED'], len(sub)):>13s}"
              f"{pct(c2['UNVERIFIABLE'], len(sub)):>14s}")
    c3 = Counter(r["verdict"] for r in n_all)
    print("-" * len(hdr2))
    print(f'{"POOLED":24s}{pct(c3["SUPPORTED"], len(n_all)):>11s}'
          f'{pct(c3["DIVERGENT"], len(n_all)):>11s}'
          f'{pct(c3["NOT_LOCATED"], len(n_all)):>13s}'
          f'{pct(c3["UNVERIFIABLE"], len(n_all)):>14s}')

    print("\n\nBY CLAIM TYPE, POOLED")
    bt = defaultdict(Counter)
    for r in rows:
        bt[r["claim_type"]][r["verdict"]] += 1
    hdr3 = f'{"claim type":24s}{"n":>6s}' + "".join(f"{v[:11]:>13s}" for v in ORDER)
    print(hdr3)
    print("-" * len(hdr3))
    for t in sorted(bt, key=lambda t: -bt[t]["SUPPORTED"] / sum(bt[t].values())):
        cc = bt[t]
        tot = sum(cc.values())
        print(f"{t:24s}{tot:>6d}" + "".join(f"{pct(cc[v], tot):>13s}" for v in ORDER))

    # verification depth — never imply a stronger check than performed
    print("\n\nVERIFICATION DEPTH")
    for lvl, n in sorted(Counter(r["level_reached"] for r in rows).items()):
        print(f"  {lvl}: {n} ({pct(n, len(rows))})")

    out = DATA / "phase-r-aggregate.csv"
    with open(out, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["area", "claim_type", "verdict", "n"])
        for a in areas:
            for t in sorted(bt):
                cc = Counter(r["verdict"] for r in rows
                             if r["area"] == a and r["claim_type"] == t)
                for v in ORDER:
                    if cc[v]:
                        w.writerow([a, t, v, cc[v]])
    print(f"\nwrote {out.name}")


if __name__ == "__main__":
    main()
