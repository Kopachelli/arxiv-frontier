# Programme roadmap

Set by Khristian Kopachelli, 2026-07-25. Paper 1 (this repository) is the first of a planned
series. Recorded here so scope is explicit and later phases are not re-litigated from memory.

---

## Paper 1 — *When the Instrument Studies Itself* (current, draft complete)

Systematic map of 811 papers; reflexive case study. Awaiting human review and publication
decision (Phase 7).

## Phase V — Blind cross-model verification of Paper 1

**Khristian's specification.** Verify the work again using Fable 5 and Opus 5, where the
verifying models do not know whose work they are checking. Both models verify Fable-5-produced
output; both models verify Opus-5-produced output.

**Design implied (2×2 producer × verifier matrix).**

| | verified by Fable 5 | verified by Opus 5 |
|---|---|---|
| **produced by Fable 5** | self-family, same model | cross-model |
| **produced by Opus 5** | cross-model | self-family, same model |

The interesting quantity is the *interaction*: does a model rate work more favourably when the
work happens to be its own (without being told)? That is a measurable self-preference effect,
and to our knowledge it has not been measured in the systematic-review setting.

**Blinding requirements (must be enforced mechanically, not by instruction).**
- Strip all model-identifying metadata from the artifacts under review.
- Normalise prose style where it could reveal provenance (or, better, accept style leakage and
  test whether verifiers can identify provenance above chance — that is itself a result).
- Verifiers must not see this roadmap, the process logs, or any file naming the producing
  model.
- Produce both conditions from the *same* inputs so the comparison is like-for-like: e.g.
  re-run screening/coding on an identical sample with each model as producer.

**Decided (Khristian, 2026-07-25): both, as two separate arms.**

- **Arm 1 — independent re-doing.** Each model re-runs screening and coding on an identical
  sample without seeing prior decisions. Yields inter-model reliability, and supports the
  self-preference test (blinded, does a model rate its own prior output more favourably?).
- **Arm 2 — audit of existing decisions.** Each model is given the recorded decisions and
  asked to find errors. Yields an error-detection rate against our released corpus, and tells
  us directly whether Paper 1 contains mistakes.

The two arms answer different questions — *do models agree?* and *do models catch mistakes?* —
and a model can score well on one and badly on the other. Report both; do not average them.

## Phase R — Repository verification programme (multi-paper)

**Khristian's specification.** Extract every paper with a repository link; access the public
repositories; download them; work through them to check whether what the paper *states* matches
what the artifacts *contain*. Split into 7–10 general areas; produce a series of at least 5–7
papers, one per area, plus a synthesising paper.

**Starting material already in hand.** `data/artifact-verification.csv` holds full-text
extraction for all 811 papers: 489 with at least one repository URL, plus the URLs themselves.
That is the sampling frame; no new harvesting is needed to begin.

**Per-area pipeline (draft).**
1. Partition the 489 repo-bearing papers into areas (see open question below).
2. For each area: clone public repos; record availability (live / 404 / private / empty).
3. Extract the paper's checkable claims (numeric results, released-artifact claims, method
   claims) into a structured claim list.
4. For each claim, classify against the artifact: **supported** (reproducible or directly
   evidenced), **present but divergent**, **absent from artifact**, **contradicted**.
5. Where feasible and cheap, attempt actual re-execution; where not, evidence-level checking
   only — and say which was done, per claim.
6. Report per-area rates with the full claim ledger released.

**Why this is the strongest continuation.** Paper 1 measures what the field *reports*. Phase R
measures whether the reports are *true*.

**Framing decided (Khristian, 2026-07-25):** the unmarked-hypothesis question is the
programme's organising frame, not a side essay. Every area paper reports, alongside its
domain findings, the rate at which claims are **supported / divergent / absent / contradicted**
relative to the paper's own released artifacts. "Absent" and "contradicted" are the measured
instances of unlicensed synthesis. The synthesising paper aggregates these into a
field-level rate and tests whether papers reporting provenance mechanisms (D6) differ from
those that do not — which turns the remedy claim in `notes/unmarked-hypothesis.md` §3 into a
falsifiable prediction rather than an argument.

**Partition — DECIDED 2026-07-26 (Khristian).** He chose to combine six of the candidate
schemes rather than pick one. The design that implements this is
`protocol/phase-r-design.md`; the essential move is that the six occupy three different
roles rather than being six competing partitions:

- **A (what the repository is supposed to support)** is the partition — 8 areas, 8 papers.
- **E (artifact archetype)** is the *method router*: it decides which verification levels are
  even possible for a given repository, so a prompts-only repo is never scored as though
  execution had been attempted.
- **B (domain), D (cohort), F (lineage), H (institution type)** are cross-cutting dimensions
  recorded on every paper, reported inside every area, and aggregated into three additional
  cross-area papers (lineage, trend, synthesis).

One shared ledger schema serves all of them, so collection happens once and every paper is a
slice of the same rows. Dimension H carries an extra constraint fixed in advance: aggregate
by institution *type* only, never ranking or naming institutions, with small cells merged or
suppressed (`protocol/phase-r-design.md` §7).

**Remaining open design questions for Khristian.**
- Repository access ethics and load: cloning ~489 public repos is heavy but ordinary; we should
  set a rate limit, respect licences, and publish only aggregate findings plus per-paper
  claim ledgers, not redistributed code.
- Whether a paper failing verification is named. Our position should be decided *before* we see
  results, not after.

## Sequencing

Phase V is small and should run first: it validates the instrument used in Paper 1 before
Phase R relies on the same instrument at ten times the scale.
