"""The cross-area figure: described methods versus reported numbers, per area.

Usage: python code/phase_r_crossfig.py
"""

import csv
from collections import Counter
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

LABEL = {
    "A1_discovery": "discovery",
    "A2_auditability": "auditability",
    "A3_end_to_end": "end-to-end",
    "A4_physical_life_sciences": "physical & life sci.",
    "A5_benchmark": "benchmark",
    "A6_deep_research": "deep research",
    "A7_ideation": "ideation",
    "A8_scholarly_record": "scholarly record",
    "A9_research_infrastructure": "research infra.",
}
INK = "#1f3b57"
ACCENT = "#c1502e"


def main():
    rows = []
    for p in sorted(DATA.glob("phase-r-ledger-*.csv")):
        rows += list(csv.DictReader(open(p, encoding="utf-8")))
    areas = sorted({r["area"] for r in rows})

    data = []
    for a in areas:
        sub = [r for r in rows if r["area"] == a]
        m = [r for r in sub if r["claim_type"] == "METHOD_COMPONENT"]
        n = [r for r in sub if r["claim_type"] == "NUMERIC_RESULT"]
        if not m or not n:
            continue
        data.append((
            LABEL.get(a, a),
            sum(1 for r in m if r["verdict"] == "SUPPORTED") / len(m),
            sum(1 for r in n if r["verdict"] == "SUPPORTED") / len(n),
            len({r["arxiv_id"] for r in sub}),
        ))
    data.sort(key=lambda d: -(d[1] / d[2] if d[2] else 0))

    fig, ax = plt.subplots(figsize=(7.0, 3.3))
    y = range(len(data))
    for i, (lab, mv, nv, np_) in enumerate(data):
        ax.plot([nv, mv], [i, i], color="#c9d1d8", lw=3, solid_capstyle="round", zorder=1)
        ax.scatter([nv], [i], s=58, color=ACCENT, zorder=3)
        ax.scatter([mv], [i], s=58, color=INK, zorder=3)
        ax.text(mv + 0.02, i, f"{mv:.0%}", va="center", fontsize=7.5, color=INK)
        ax.text(nv - 0.02, i, f"{nv:.0%}", va="center", ha="right", fontsize=7.5, color=ACCENT)
        ax.text(1.04, i, f"{mv / nv:.1f}×", va="center", fontsize=7.5, color="#444")

    m_all = [r for r in rows if r["claim_type"] == "METHOD_COMPONENT"]
    n_all = [r for r in rows if r["claim_type"] == "NUMERIC_RESULT"]
    pm = sum(1 for r in m_all if r["verdict"] == "SUPPORTED") / len(m_all)
    pn = sum(1 for r in n_all if r["verdict"] == "SUPPORTED") / len(n_all)

    ax.set_yticks(list(y))
    ax.set_yticklabels([f"{d[0]}  (n={d[3]})" for d in data])
    ax.set_xlim(0, 1.0)
    ax.set_xlabel("share of claims located in the paper's own repository")
    ax.xaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.set_title("What a paper describes vs what it reports, by area", loc="left")
    ax.scatter([], [], s=58, color=INK, label="described method components")
    ax.scatter([], [], s=58, color=ACCENT, label="reported numeric results")
    ax.set_ylim(-0.7, len(data) - 0.3)
    ax.legend(frameon=False, fontsize=8, loc="upper center",
              bbox_to_anchor=(0.5, -0.22), ncols=2)
    ax.text(1.04, len(data) - 0.5, "ratio", fontsize=7.5, color="#444", fontweight="bold")
    fig.text(0.5, -0.20,
             f"Pooled across {len({(r['area'], r['arxiv_id']) for r in rows})} papers: "
             f"methods {pm:.0%} located, numbers {pn:.0%} located ({pm / pn:.1f}×). "
             f"Same direction in every area.",
             ha="center", fontsize=8, color="#333")
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"phase-r-cross-area.{ext}")
    plt.close(fig)
    print(f"figures/phase-r-cross-area.png  ({len(data)} areas)")


if __name__ == "__main__":
    main()
