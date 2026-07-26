# Version 2 — corrections

Issued 2026-07-26, one day after v1. Prompted by Phase V, which was designed to test v1's
instrument and did its job. Per `protocol/phase-v-protocol.md` §6, errors found in the
published corpus are reported publicly and corrected rather than quietly amended.

**v1 remains retrievable** at its own DOI, and the pre-correction data files are preserved in
`data/v1/` so every v1 number stays exactly reproducible.

---

## What was wrong

A mechanical check (`code/check_consistency.py`) of rules the protocol already stated found
18 records violating them:

- **15 papers were included while coded `L0_ASSISTIVE`.** Amendment A1's boundary rule BR1
  excludes assistive tools as `EC6_ASSISTIVE`; `L0_ASSISTIVE` means exactly "human drives, AI
  assists". The two cannot both be right.
- **3 `POSITION` papers were credited with lifecycle stages**, where the codebook assigns `NA`
  to papers presenting no system.

Root cause: the pipeline never tested that coded output obeyed the screening rules. The rule
existed; nothing enforced it (`process-log/errors.md` #10).

## How each was resolved

All 18 were adjudicated **against the papers' full text**, with a verbatim supporting quote
required for every verdict. All 18 verdicts carry one; none was decided on the abstract alone.
Full ledger with quotes: `data/v2-changelog.csv`.

| verdict | n | meaning |
|---|---|---|
| `FIX_CODING` → autonomy raised | 11 | the paper was correctly included; the autonomy code was too low (9 → `L1_STAGE`, 2 → `L2_PIPELINE`) |
| `FIX_SCREENING` → excluded | 4 | the paper is genuinely assistive and should not have been included |
| `FIX_CODING` → `D3 = NA` | 3 | position papers credited with stages they do not perform |
| `NO_CHANGE` | 0 | — |

## Effect on the corpus and the findings

| | v1 | v2 |
|---|---|---|
| papers | 811 | **807** |
| no auditability mechanism | 54.9% | 55.0% |
| held-out transfer | 4.6% | 4.6% |
| real-world validation | 10.7% | 10.7% |
| human role unstated | 70.7% | 71.0% |
| autonomy `L0_ASSISTIVE` | 15 | **0** |
| autonomy `L1_STAGE` | 144 | 153 |
| autonomy `L2_PIPELINE` | 86 | 88 |
| autonomy `L3_CLOSED_LOOP` | 148 | 148 |
| autonomy `L4_FULL` | 19 | 19 |

**No headline finding changed by more than 0.3 percentage points**, and none changed
direction. The dissociation between output validation and process auditability, the growth
curve, and the missing-human result are unaffected. What changed is the autonomy
distribution, which is now internally consistent with the review's own inclusion rule.

## A finding produced by the correction itself

Eleven of the fifteen flagged papers were **under-coded, not wrongly included**. The
adjudications repeatedly note the same pattern: a paper presents itself as a "co-scientist",
"human-in-the-loop", or "assistive" system while demonstrating a research stage the AI in fact
performs unaided. Examples, with the quotes that settled them:

- **arXiv:2510.14861 (LabOS)** — marketed as an AI-XR co-scientist that "works with humans";
  the paper states the system "autonomously identified and refined candidate regulators", with
  a nominated target validated in a physical assay. Corrected `L0` → `L2_PIPELINE`.
- **arXiv:2511.02071 (APEX)** — framed as co-embodied human-AI intelligence, but the division
  of labour is the inverse of assistive: the human is the physical actuator while the system
  produces the fabrication protocol. Corrected `L0` → `L2_PIPELINE`.
- **arXiv:2508.19200 (Ramon Llull's Thinking Machine)** — fully automated ideation over 7,483
  papers. Corrected `L0` → `L1_STAGE`.

This runs against the expected direction. The usual concern about this literature is that it
*oversells* autonomy; here a measurable subset **understates** it, describing as collaboration
a process in which the AI produces the substantive output and the human supplies the question
or the hands. Both directions of mis-description are obstacles to a reader trying to
establish what a system actually did, which is the paper's central point about process
disclosure.

## What we changed in how we work

`code/check_consistency.py` now runs as a gate: rules the protocol states are tested against
the data, mechanically, every time the analysis is regenerated. As of v2 it reports zero
violations. The general lesson is in the paper's Discussion — stating an invariant and
checking it by script catches what judgement-based review does not, a claim Phase V measured
directly.
