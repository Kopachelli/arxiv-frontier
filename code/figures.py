"""Generate all figures from data/*.csv. Every figure is reproducible from released data.

Usage: python code/figures.py
"""

import csv
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
    "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
    "figure.dpi": 200, "savefig.bbox": "tight", "axes.spines.top": False,
    "axes.spines.right": False, "axes.grid": True, "grid.alpha": 0.25,
    "grid.linestyle": "-", "axes.axisbelow": True,
})
INK = "#1f3b57"
ACCENT = "#c1502e"
MUTED = "#8a9ba8"


def load(name):
    return list(csv.DictReader(open(DATA / name, encoding="utf-8")))


def save(fig, name):
    for ext in ("pdf", "png"):
        fig.savefig(FIG / f"{name}.{ext}")
    plt.close(fig)
    print(f"  figures/{name}.pdf")


def quarter(d):
    return f"{d[:4]}Q{(int(d[5:7]) - 1) // 3 + 1}" if len(d) >= 7 else None


def fig_growth(coded):
    qs = [quarter(r["first_submitted"]) for r in coded]
    c = Counter(q for q in qs if q)
    keys = sorted(c)
    vals = [c[k] for k in keys]
    fig, ax = plt.subplots(figsize=(5.4, 2.9))
    partial = keys[-1]
    colors = [INK] * (len(keys) - 1) + [MUTED]
    ax.bar(keys, vals, color=colors, width=0.72)
    for x, v in zip(keys, vals):
        ax.text(x, v + max(vals) * 0.02, str(v), ha="center", fontsize=7.5, color="#444")
    ax.set_ylabel("papers (first submission)")
    ax.set_title("Autonomous AI research papers per quarter (arXiv)", loc="left")
    ax.tick_params(axis="x", rotation=45)
    ax.set_ylim(0, max(vals) * 1.16)
    ax.annotate(f"{partial}: partial\n(July only)", xy=(len(keys) - 1, vals[-1] * 1.06),
                xytext=(len(keys) - 3.2, max(vals) * 0.34), fontsize=7.5, color="#666",
                ha="center",
                arrowprops=dict(arrowstyle="->", color="#999", lw=0.8,
                                connectionstyle="arc3,rad=-0.2"))
    save(fig, "fig1-growth")


def fig_stages_autonomy(coded):
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 2.9))
    fig.subplots_adjust(wspace=0.5)
    stages = ["IDEATION", "LITERATURE", "EXP_DESIGN", "EXECUTION", "ANALYSIS", "WRITING", "REVIEW"]
    stage_lab = ["ideation", "literature", "experiment design", "execution",
                 "analysis", "writing", "peer review"]
    c = Counter()
    for r in coded:
        for s in r["D3"].split(";"):
            if s in stages:
                c[s] += 1
    ax = axes[0]
    ax.barh(stage_lab[::-1], [c[s] for s in stages[::-1]], color=INK, height=0.66)
    for i, s in enumerate(stages[::-1]):
        ax.text(c[s] + 5, i, str(c[s]), va="center", fontsize=7.5, color="#444")
    ax.set_xlabel("papers")
    ax.set_title("Research stages performed", loc="left")
    ax.set_xlim(0, max(c.values()) * 1.22)

    order = ["L0_ASSISTIVE", "L1_STAGE", "L2_PIPELINE", "L3_CLOSED_LOOP", "L4_FULL"]
    labels = ["L0 assistive", "L1 single stage", "L2 gated pipeline",
              "L3 closed loop", "L4 full autonomy"]
    ca = Counter(r["D2"] for r in coded)
    ax = axes[1]
    vals = [ca.get(k, 0) for k in order]
    ax.barh(labels[::-1], vals[::-1], color=[ACCENT if k == "L4_FULL" else INK for k in order][::-1],
            height=0.66)
    for i, v in enumerate(vals[::-1]):
        ax.text(v + 2, i, str(v), va="center", fontsize=7.5, color="#444")
    ax.set_xlabel("system / case-study papers")
    ax.set_title("Demonstrated autonomy level", loc="left")
    ax.set_xlim(0, max(vals) * 1.15)
    save(fig, "fig2-stages-autonomy")


def fig_verification(coded):
    """The RQ2 figure: what verification and auditability the corpus actually provides."""
    fig, axes = plt.subplots(1, 2, figsize=(8.4, 3.0))
    fig.subplots_adjust(wspace=0.55)
    ev = ["BENCHMARK_METRIC", "LLM_JUDGE", "HUMAN_EXPERT", "REAL_WORLD",
          "HELD_OUT_TRANSFER", "NONE"]
    ev_lab = ["benchmark metric", "LLM judge", "human expert", "real-world",
              "held-out transfer", "no evaluation"]
    c = Counter()
    for r in coded:
        for x in r["D5"].split(";"):
            if x in ev:
                c[x] += 1
    n = len(coded)
    ax = axes[0]
    colors = [INK, INK, ACCENT, ACCENT, ACCENT, MUTED]
    ax.barh(ev_lab[::-1], [c[k] for k in ev[::-1]], color=colors[::-1], height=0.66)
    for i, k in enumerate(ev[::-1]):
        ax.text(c[k] + 8, i, f"{c[k]}  ({c[k] / n:.0%})", va="center", fontsize=7.5, color="#444")
    ax.set_xlabel(f"papers (n={n}; multi-select)")
    ax.set_title("How claims are evaluated", loc="left")
    ax.set_xlim(0, max(c.values()) * 1.42)

    au = ["REPRO_ARTIFACTS", "PROVENANCE", "TRACES", "UNCERTAINTY", "FORMAL_VERIF", "NONE"]
    au_lab = ["repro artifacts", "provenance", "traces", "uncertainty",
              "formal verification", "none"]
    c2 = Counter()
    for r in coded:
        for x in r["D6"].split(";"):
            if x in au:
                c2[x] += 1
    ax = axes[1]
    colors2 = [INK] * 5 + [ACCENT]
    ax.barh(au_lab[::-1], [c2[k] for k in au[::-1]], color=colors2[::-1], height=0.66)
    for i, k in enumerate(au[::-1]):
        ax.text(c2[k] + 8, i, f"{c2[k]}  ({c2[k] / n:.0%})", va="center", fontsize=7.5, color="#444")
    ax.set_xlabel(f"papers (n={n}; multi-select)")
    ax.set_title("Auditability mechanisms provided", loc="left")
    ax.set_xlim(0, max(c2.values()) * 1.42)
    save(fig, "fig3-verification")


def fig_claim_vs_evidence(coded, artifacts):
    """Claim strength against verification strength — the auditability-gap figure."""
    strong_eval = {"HUMAN_EXPERT", "HELD_OUT_TRANSFER", "REAL_WORLD"}
    claims = ["DISCOVERY", "CAPABILITY", "METHOD", "CONCEPTUAL"]
    labels = ["discovery", "capability", "method", "conceptual"]
    rows = []
    for cl in claims:
        sub = [r for r in coded if r["D8"] == cl]
        if not sub:
            continue
        n = len(sub)
        se = sum(1 for r in sub if set(r["D5"].split(";")) & strong_eval) / n
        au = sum(1 for r in sub if r["D6"] != "NONE") / n
        code = sum(1 for r in sub if artifacts.get(r["arxiv_id"], {}).get("has_repo") == "1") / n
        rows.append((n, se, au, code))

    fig, ax = plt.subplots(figsize=(5.8, 3.0))
    x = range(len(rows))
    w = 0.26
    ax.bar([i - w for i in x], [r[1] for r in rows], w, label="strong evaluation", color=INK)
    ax.bar(list(x), [r[2] for r in rows], w, label="any auditability mechanism", color="#5b7f9e")
    ax.bar([i + w for i in x], [r[3] for r in rows], w, label="code repository (full text)",
           color=ACCENT)
    ax.set_xticks(list(x))
    ax.set_xticklabels([f"{l}\n(n={r[0]})" for l, r in zip(labels, rows)])
    ax.set_ylabel("share of papers")
    ax.set_ylim(0, 1)
    ax.yaxis.set_major_formatter(lambda v, _: f"{v:.0%}")
    ax.set_title("Verification provided, by strength of headline claim", loc="left")
    ax.legend(frameon=False, fontsize=7.5, loc="upper left", ncols=1)
    save(fig, "fig4-claim-vs-evidence")


def fig_domains(coded):
    c = Counter(r["D4"] for r in coded)
    order = [k for k, _ in c.most_common() if k != "UNCLEAR"]
    fig, ax = plt.subplots(figsize=(5.4, 2.8))
    vals = [c[k] for k in order]
    ax.bar([k.replace("_", " ").lower() for k in order], vals, color=INK, width=0.7)
    for i, v in enumerate(vals):
        ax.text(i, v + max(vals) * 0.02, str(v), ha="center", fontsize=7.5, color="#444")
    ax.set_ylabel("papers")
    ax.set_title("Scientific domain of the corpus", loc="left")
    ax.tick_params(axis="x", rotation=45)
    ax.set_ylim(0, max(vals) * 1.14)
    save(fig, "fig5-domains")


def main():
    coded = load("coded-corpus.csv")
    artifacts = {}
    p = DATA / "artifact-verification.csv"
    if p.exists():
        artifacts = {r["arxiv_id"]: r for r in load("artifact-verification.csv")}
    print(f"figures from {len(coded)} coded papers, {len(artifacts)} artifact checks:")
    fig_growth(coded)
    fig_stages_autonomy(coded)
    fig_verification(coded)
    fig_domains(coded)
    if artifacts:
        fig_claim_vs_evidence(coded, artifacts)


if __name__ == "__main__":
    main()
