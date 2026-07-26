# Phase R — how to cut the corpus into 7–10 areas

Decision reserved for the human co-author (`protocol/phase-r-protocol.md` §6). Real counts
from the 491 repo-bearing papers, so the options below are sized, not guessed.

## What the single-dimension cuts look like

| dimension | distribution | verdict |
|---|---|---|
| **Domain (D4)** | GENERAL_ML 228 · MULTI 71 · BIOMED 56 · OTHER 51 · MATERIALS 30 · PHYSICS 18 · SOCIAL_SCI 18 · CHEMISTRY 9 · MATH_FORMAL 7 | badly unbalanced — one area is half the corpus |
| **Paper type (D1)** | SYSTEM 253 · BENCHMARK 141 · FRAMEWORK 60 · SURVEY 16 · CASE_STUDY 14 · POSITION 7 | only three areas of usable size |
| **Claim strength (D8)** | METHOD 227 · CAPABILITY 209 · DISCOVERY 32 · CONCEPTUAL 23 | two areas, and DISCOVERY is small |
| **Autonomy (D2)** | NA 224 · L3 99 · L1 82 · L2 62 · L4 14 · L0 7 | NA dominates |

No single dimension gives 7–10 coherent areas. The three options below are hybrids.

---

## Option A — by *what the repository is supposed to support* (recommended)

Areas defined by the kind of claim under test, which is what Phase R actually measures. Each
yields a paper with its own question. Assignment is by first match, so areas are disjoint.

| # | area | rule | approx n |
|---|---|---|---|
| 1 | **Discovery claims** | D8 = DISCOVERY | 32 |
| 2 | **End-to-end autonomous systems** | D2 ∈ {L3, L4} | 113 |
| 3 | **Benchmarks and evaluation** | D1 = BENCHMARK | 141 |
| 4 | **Deep research agents** | entered via BR7 | ~120 |
| 5 | **Autonomous experimentation / self-driving labs** | D3 ∋ EXECUTION and D4 ∈ {MATERIALS, CHEMISTRY, PHYSICS} | ~45 |
| 6 | **Biomedical systems** | D4 = BIOMED | 56 |
| 7 | **Ideation and hypothesis generation** | D3 ∋ IDEATION, single-stage | ~60 |
| 8 | **Auditability and integrity tooling** | screened IC3 | ~70 |

**Why this one.** Each area asks a question a reader would actually pose. Area 1 is the
highest-stakes paper in the programme (do papers claiming AI-made discoveries contain those
discoveries?). Area 8 is pointedly reflexive: do the papers *proposing* auditability tools
ship them? Area 3 is the most mechanically checkable — a benchmark either has its data or
does not.

**Cost.** Overlaps require a precedence order; the one above reads top-down.

## Option B — by scientific domain

Areas 1–8 = GENERAL_ML (split into three sub-areas by task), MULTI, BIOMED, MATERIALS+CHEMISTRY,
PHYSICS, SOCIAL_SCI, OTHER.

**Why you might.** Domain experts can review each paper; findings map onto communities that
can act on them. **Why not.** The GENERAL_ML split is arbitrary, and the interesting variation
in Paper 1's data is by claim type, not by domain.

## Option C — by evidentiary difficulty (the ladder in §3)

Areas by how far verification can go: mechanically checkable artifacts → data-only claims →
requires execution → requires a laboratory.

**Why you might.** Honest about what we can establish, and the areas are naturally ordered by
cost. **Why not.** The areas are about *our method* rather than about the field; less useful
to a reader.

---

## Recommendation

**Option A**, with Area 1 (discovery claims) first — it is small enough to do thoroughly, it
carries the programme's central question, and if the result is that discovery claims *are*
well supported, that is a finding worth having early and cheaply.

## Open sub-decisions

1. Precedence order for overlapping areas (Option A's top-down order is a proposal).
2. Whether area papers are released as they complete, or held and released together.
3. Whether to attempt R3 (execution) at all in the first area, or defer it to a later one
   once the R0–R2 pipeline is proven.
