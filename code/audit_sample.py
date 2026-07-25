"""Generate the human co-author's screening audit sample (protocol §5 + amendment A1).

Stratified random sample of Layer-2 decisions, written as a markdown worksheet the human
fills in. Deterministic seed so the sample is reproducible from the released data.

Usage: python code/audit_sample.py
"""

import csv
import json
import random
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEED = 20260725
N_INCLUDE = 15
N_EXCLUDE = 15
N_REVERSAL = 10


def main():
    cand = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "candidates.csv", encoding="utf-8"))}
    cand.update(json.loads((DATA / "expert-identified-meta.json").read_text(encoding="utf-8")))
    fin = list(csv.DictReader(open(DATA / "screening-final.csv", encoding="utf-8")))

    rng = random.Random(SEED)
    inc = [r for r in fin if r["final_decision"] == "include"]
    exc = [r for r in fin if r["final_decision"] != "include"
           and r["reverses_unanimous_include"] != "1"]
    rev = [r for r in fin if r["reverses_unanimous_include"] == "1"]

    # excludes stratified proportionally over reason codes
    by_reason = defaultdict(list)
    for r in exc:
        by_reason[r["final_reason"]].append(r)
    exc_sample = []
    counts = Counter(r["final_reason"] for r in exc)
    for reason, rows in sorted(by_reason.items()):
        k = max(1, round(N_EXCLUDE * counts[reason] / len(exc)))
        exc_sample += rng.sample(rows, min(k, len(rows)))
    exc_sample = exc_sample[:N_EXCLUDE]

    picks = ([("INCLUDE", r) for r in rng.sample(inc, N_INCLUDE)]
             + [("EXCLUDE", r) for r in exc_sample]
             + [("REVERSAL", r) for r in rng.sample(rev, min(N_REVERSAL, len(rev)))])
    rng.shuffle(picks)

    lines = [
        "# Screening Audit Worksheet — for Khristian Kopachelli",
        "",
        f"Stratified random sample of {len(picks)} Layer-2 screening decisions "
        f"(seed {SEED}, reproducible via `python code/audit_sample.py`).",
        "",
        "**What to do:** for each paper, read the title + abstract and the AI's decision.",
        "Write `agree` or `disagree` on the VERDICT line. If you disagree, add one line",
        "saying what it should be and why. Do not feel obliged to agree — disagreements",
        "are the point, and every one of them is reported in the paper.",
        "",
        "Decision vocabulary: **include** = a paper about AI *producing* research (a system",
        "that performs a research stage, a benchmark/framework for such systems, or a study",
        "of the integrity of AI-produced research). **exclude** = everything else, with a",
        "reason code (EC6_ASSISTIVE = human-driven tool; EC7_HUMAN_AI_USE = human use of AI /",
        "AI-text detection; EC8_GENERIC_ANALYSIS = generic data science; EC9_GENERIC_DEEPRESEARCH",
        "= general web-research agent; EC1 = generic agent work; EC2 = instrument/model, no",
        "research decision loop).",
        "",
        "The sample is blinded in one respect only: it does not tell you which stratum",
        "(include / exclude / reversal) a paper came from.",
        "",
        "---",
        "",
    ]
    for i, (_, r) in enumerate(picks, 1):
        pid = r["arxiv_id"]
        m = cand.get(pid, {})
        abstract = (m.get("abstract", "") or "")[:1200]
        lines += [
            f"## {i}. arXiv:{pid} — {m.get('title', '?')}",
            "",
            f"*{abstract}*",
            "",
            f"- **AI decision:** `{r['final_decision']}` / `{r['final_reason']}`"
            f"{' (rule ' + r['rule_applied'] + ')' if r['rule_applied'] != 'none' else ''}",
            f"- **AI reasoning:** {r['justification']}",
            "- **VERDICT:** ",
            "",
        ]
    (DATA / "screening-audit-worksheet.md").write_text("\n".join(lines), encoding="utf-8")

    with open(DATA / "screening-audit-key.csv", "w", newline="", encoding="utf-8") as f:
        wr = csv.writer(f)
        wr.writerow(["item", "arxiv_id", "stratum", "ai_decision", "ai_reason",
                     "rule", "human_verdict", "human_note"])
        for i, (stratum, r) in enumerate(picks, 1):
            wr.writerow([i, r["arxiv_id"], stratum, r["final_decision"],
                         r["final_reason"], r["rule_applied"], "", ""])
    print(f"wrote data/screening-audit-worksheet.md ({len(picks)} items) "
          f"and data/screening-audit-key.csv")
    print("strata:", dict(Counter(s for s, _ in picks)))


if __name__ == "__main__":
    main()
