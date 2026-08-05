"""Confidence intervals and sensitivity analysis for the paper's headline claims.

Written 2026-07-31 in response to an external critique arguing that the paper's headline
dissociation is stated more strongly than n=58 supports. The critique is testable, so we
test it rather than argue about it.

Wilson score intervals (better than normal approximation at these n and near 0/1).

Usage: python code/confidence_intervals.py
"""

import csv
import math
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
STRONG_EVAL = {"HUMAN_EXPERT", "HELD_OUT_TRANSFER", "REAL_WORLD"}


def wilson(k, n, z=1.96):
    """Wilson score interval for a binomial proportion."""
    if n == 0:
        return (float("nan"), float("nan"), float("nan"))
    p = k / n
    d = 1 + z * z / n
    centre = (p + z * z / (2 * n)) / d
    half = z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return p, max(0.0, centre - half), min(1.0, centre + half)


def fmt(k, n):
    p, lo, hi = wilson(k, n)
    return f"{p:5.1%}  [{lo:4.1%}, {hi:4.1%}]  (n={n})"


def load():
    coded = list(csv.DictReader(open(DATA / "coded-corpus.csv", encoding="utf-8")))
    art = {r["arxiv_id"]: r for r in csv.DictReader(
        open(DATA / "artifact-verification.csv", encoding="utf-8"))}
    return coded, art


def metrics(rows, art):
    n = len(rows)
    return {
        "any auditability (D6 != NONE)": sum(1 for r in rows if r["D6"] != "NONE"),
        "no auditability (D6 == NONE)": sum(1 for r in rows if r["D6"] == "NONE"),
        "strong evaluation": sum(1 for r in rows if set(r["D5"].split(";")) & STRONG_EVAL),
        "real-world validation": sum(1 for r in rows if "REAL_WORLD" in r["D5"].split(";")),
        "held-out transfer": sum(1 for r in rows if "HELD_OUT_TRANSFER" in r["D5"].split(";")),
        "human role unstated": sum(1 for r in rows if r["D9"] in ("NONE_CLAIMED", "UNSPECIFIED")),
        "code repository (full text)": sum(
            1 for r in rows if art.get(r["arxiv_id"], {}).get("has_repo") == "1"),
    }, n


def main():
    coded, art = load()
    disc = [r for r in coded if r["D8"] == "DISCOVERY"]
    print("=" * 78)
    print("1. THE HEADLINE DISSOCIATION, WITH INTERVALS")
    print("=" * 78)
    print(f"\ndiscovery papers n={len(disc)}, whole corpus n={len(coded)}\n")
    dm, dn = metrics(disc, art)
    cm, cn = metrics(coded, art)
    print(f'{"metric":32s}{"discovery":>26s}{"corpus":>26s}')
    print("-" * 84)
    for k in dm:
        print(f"{k:32s}{fmt(dm[k], dn):>26s}{fmt(cm[k], cn):>26s}")

    print("\nVERDICT ON EACH COMPARISON (does the corpus rate fall inside the discovery CI?)")
    for k in dm:
        _, lo, hi = wilson(dm[k], dn)
        corpus_p = cm[k] / cn
        inside = lo <= corpus_p <= hi
        tag = "NOT SUPPORTED - corpus rate inside CI" if inside else "supported - corpus rate outside CI"
        print(f"  {k:32s} corpus={corpus_p:5.1%}  {tag}")

    # ---------------------------------------------------------------- sensitivity
    print("\n" + "=" * 78)
    print("2. SENSITIVITY OF HEADLINE STATISTICS TO CORPUS-BOUNDARY DECISIONS")
    print("=" * 78)
    fin = {r["arxiv_id"]: r for r in csv.DictReader(
        open(DATA / "screening-final.csv", encoding="utf-8"))}
    l1 = {r["arxiv_id"]: r for r in csv.DictReader(
        open(DATA / "screening-decisions.csv", encoding="utf-8"))}

    br7 = {p for p, r in fin.items() if r.get("rule_applied") == "BR7"}
    unanimous = {p for p, r in l1.items() if r["agreement"] == "agree"}

    variants = {
        "full corpus (as published)": coded,
        f"excluding BR7 deep-research entrants (-{len([r for r in coded if r['arxiv_id'] in br7])})":
            [r for r in coded if r["arxiv_id"] not in br7],
        "only papers both Layer-1 passes agreed on":
            [r for r in coded if r["arxiv_id"] in unanimous],
    }
    keys = ["no auditability (D6 == NONE)", "held-out transfer", "real-world validation",
            "human role unstated"]
    print(f'\n{"variant":48s}' + "".join(f"{k[:18]:>20s}" for k in keys))
    print("-" * (48 + 20 * len(keys)))
    for name, rows in variants.items():
        m, n = metrics(rows, art)
        print(f"{name:48s}" + "".join(f"{m[k] / n:>19.1%} " for k in keys) + f" n={n}")

    print("\nSpread across variants (max - min):")
    for k in keys:
        vals = [metrics(rows, art)[0][k] / len(rows) for rows in variants.values()]
        print(f"  {k:32s} {min(vals):5.1%} to {max(vals):5.1%}  "
              f"(spread {max(vals) - min(vals):.1%})")

    # ---------------------------------------------------------------- corpus counts
    print("\n" + "=" * 78)
    print("3. CORPUS COUNT RECONCILIATION")
    print("=" * 78)
    v1 = list(csv.DictReader(open(DATA / "v1" / "coded-corpus.csv", encoding="utf-8")))
    art_ok = [r for r in art.values() if r["status"] == "ok"]
    print(f"  screened (Layer 2)                      {len(fin)}")
    print(f"  included at v1                          {len(v1)}")
    print(f"  excluded in v2 correction               {len(v1) - len(coded)}")
    print(f"  included at v2 (published corpus)       {len(coded)}")
    print(f"  full-text artifact checks attempted     {len(art)}")
    print(f"  ... of which parsed successfully        {len(art_ok)}")
    print(f"  ... failed (reported as such)           {len(art) - len(art_ok)}")


if __name__ == "__main__":
    main()
