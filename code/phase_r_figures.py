"""Figures for Phase R area ledgers.

Usage: python code/phase_r_figures.py A1_discovery
"""

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
FIG = ROOT / "figures"
FIG.mkdir(exist_ok=True)

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9, "figure.dpi": 200,
    "savefig.bbox": "tight", "axes.spines.top": False, "axes.spines.right": False,
    "axes.grid": True, "grid.alpha": 0.22, "axes.axisbelow": True,
})

ORDER = ["SUPPORTED", "DIVERGENT", "NOT_LOCATED", "CONTRADICTED", "UNVERIFIABLE"]
COLORS = {
    "SUPPORTED": "#2e6f4e",
    "DIVERGENT": "#c98b2e",
    "NOT_LOCATED": "#c1502e",
    "CONTRADICTED": "#7a2020",
    "UNVERIFIABLE": "#9aa7b0",
}
LABEL = {
    "SUPPORTED": "supported",
    "DIVERGENT": "divergent",
    "NOT_LOCATED": "not located",
    "CONTRADICTED": "contradicted",
    "UNVERIFIABLE": "unverifiable",
}
TYPE_LABEL = {
    "METHOD_COMPONENT": "method component",
    "ARTIFACT_RELEASE": "artifact release",
    "DATASET": "dataset",
    "NUMERIC_RESULT": "numeric result",
    "EXTERNAL_VALIDATION": "external validation",
}


def main(area):
    rows = list(csv.DictReader(open(DATA / f"phase-r-ledger-{area}.csv", encoding="utf-8")))
    by = defaultdict(Counter)
    for r in rows:
        by[r["claim_type"]][r["verdict"]] += 1
    # order claim types by share supported, descending
    types = sorted(by, key=lambda t: -by[t]["SUPPORTED"] / sum(by[t].values()))

    fig, ax = plt.subplots(figsize=(7.4, 3.1))
    left = [0.0] * len(types)
    for v in ORDER:
        vals = [by[t][v] / sum(by[t].values()) for t in types]
        ax.barh([TYPE_LABEL.get(t, t) for t in types], vals, left=left,
                color=COLORS[v], label=LABEL[v], height=0.66)
        for i, (val, l) in enumerate(zip(vals, left)):
            if val >= 0.07:
                ax.text(l + val / 2, i, f"{val:.0%}", ha="center", va="center",
                        fontsize=7.5, color="white" if v != "UNVERIFIABLE" else "#333")
        left = [l + val for l, val in zip(left, vals)]
    for i, t in enumerate(types):
        ax.text(1.015, i, f"n={sum(by[t].values())}", va="center", fontsize=7.5, color="#555")
    ax.set_xlim(0, 1)
    ax.set_xlabel("share of claims")
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.set_title("Do the artifacts support the claims? Discovery papers (n=32, 255 claims)",
                 loc="left")
    ax.legend(frameon=False, fontsize=7.5, ncols=5, loc="upper center",
              bbox_to_anchor=(0.5, -0.24))
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"phase-r-{area}.{ext}")
    plt.close(fig)
    print(f"figures/phase-r-{area}.png")


if __name__ == "__main__":
    main(sys.argv[1])
