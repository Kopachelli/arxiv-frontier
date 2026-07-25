# Review Protocol — v1.0 (2026-07-25)

**Project:** *When the Instrument Studies Itself: A Systematic Map of Autonomous AI Research
Systems (2024–2026), Conducted by a Frontier AI*

**Team:** Khristian Kopachelli (human lead, independent researcher); Claude Fable 5, Anthropic
(AI lead — conducted the review; see `process-log/` for the complete process record).

**Status:** Draft pending human approval (Checkpoint 1). Any change after screening begins is
recorded in `protocol/amendments.md` with date and rationale.

---

## 1. Objectives and research questions

- **RQ1 (Landscape).** What systems, benchmarks, and frameworks constitute the autonomous
  AI-research ("AI scientist") field, January 2024 – July 2026? Characterized by: paper type,
  autonomy level, research-lifecycle coverage, scientific domain, evaluation method,
  auditability mechanisms, released artifacts.
- **RQ2 (Auditability gap).** How are capability and discovery claims evaluated versus audited?
  Which papers pair strong claims with weak verification (LLM-judge-only evaluation, no
  artifacts), and which provide verification mechanisms (held-out transfer, human expert
  validation, real-world outcomes, reproducibility artifacts)?
- **RQ3 (Trajectory).** Quantitative growth and composition of the field over time, from arXiv
  metadata (2022-01 → 2026-07 for trend context; coded corpus limited to 2024-01 → 2026-07).
- **RQ4 (Reflexive).** What does a fully-disclosed AI-conducted systematic review reveal about
  AI-led scholarship in practice — capabilities, failure modes, and required human oversight?
  Evidence: the complete process log, error log, and human-intervention log of this project.

## 2. Sources

- **Primary:** arXiv (the field publishes there first and predominantly). Metadata via the
  public arXiv API (titles, abstracts, categories, dates, authors).
- **Recall cross-check:** OpenAlex and Semantic Scholar keyword samples are compared against
  the harvest to estimate arXiv-only coverage loss; result reported in the Limitations section.

## 3. Search strategy

Harvest window: submissions dated **2022-01-01 through 2026-07-31** (window end = last full day
before harvest; exact harvest date recorded in `data/HARVEST_MANIFEST.md`).
Categories searched: cs.AI, cs.CL, cs.LG, cs.MA, cs.DL, cs.CY, cs.SE, cs.HC (a paper qualifies
if listed in any).

Query families (exact query strings live in `code/harvest.py`, which is the normative record):

- **QF1 — system identity terms:** "AI scientist", "AI co-scientist", "autonomous research
  agent", "research agent", "autonomous scientific discovery", "automated scientific
  discovery", "agentic scientific discovery", "autonomous experimentation", "self-driving
  lab(oratory)", "automated research", "end-to-end research automation", "paper-generation
  system".
- **QF2 — lifecycle-stage terms (agent-conditioned):** hypothesis generation / research
  ideation / experiment design / scientific writing, each conjoined with agent/LLM terms.
- **QF3 — audit & integrity terms (scoped to AI research):** auditable AI scientist,
  calibration of AI research claims, integrity of AI-generated research, evaluation of
  research agents.

Deduplication by canonical arXiv ID (latest version kept). Output: `data/candidates.csv`.

## 4. Eligibility criteria

**Include if (any of IC1–IC3, and IC4):**

- **IC1.** The paper's primary subject is an AI system/agent that autonomously performs at
  least one substantial stage of the scientific research lifecycle (ideation, literature
  synthesis, experiment design, experiment execution, analysis, scientific writing, or peer
  review) with an agentic loop — i.e., beyond single-shot tool invocation.
- **IC2.** The paper's primary contribution is a benchmark, evaluation methodology, or dataset
  specifically for such systems.
- **IC3.** The paper is a framework, position, survey, or case-study paper specifically about
  autonomous AI research — including auditability, calibration, governance, or integrity of
  AI-conducted research.
- **IC4.** English; on arXiv; first submission dated 2024-01-01 – 2026-07-31 (papers from the
  2022–2023 harvest tail inform RQ3 trends only and are not coded).

**Exclude if (any):**

- **EC1.** Generic LLM/agent work not aimed at performing research (coding assistants, RAG QA,
  web agents, recommender/ops agents, game agents), even if the word "research" appears.
- **EC2.** AI-for-science *models* used as instruments (e.g., property predictors, folding
  models, PDE surrogates) without an agentic research loop as the paper's subject.
- **EC3.** Papers about human use of AI writing assistance (or its detection) where no
  autonomous research system is the subject — *except* integrity papers qualifying under IC3.
- **EC4.** Superseded versions, withdrawn papers, comments, or non-paper records.
- **EC5.** Off-window or wrong language.

## 5. Screening procedure

1. Title+abstract screening of every candidate by **two independent AI screening passes**
   (differently-worded prompts, structured output: `include | exclude | borderline` + reason
   code IC1–IC3 / EC1–EC5 + one-sentence justification).
2. Agreement → accepted. Disagreement or any `borderline` → adjudication by the AI lead with
   the full abstract, logged with rationale.
3. The human lead audits a random sample of ≥30 screening decisions (stratified
   include/exclude); audit outcome reported in the paper.
4. Every decision recorded in `data/screening-decisions.csv`. PRISMA-style flow reported:
   records identified → deduplicated → screened → included/excluded by reason.

Target corpus size expectation: ~150–300 included papers. If >400, a documented scope
narrowing (e.g., restrict IC3 to auditability/evaluation only) is applied as amendment A1
*before* coding begins, never after.

## 6. Coding procedure

Each included paper is coded on the dimensions defined in `protocol/codebook.md` (normative).
Coding uses abstract + introduction/conclusion where the abstract is insufficient (full text
retrieved on demand). AI coding via structured-output agents; a whole-corpus consistency pass
by the AI lead follows (same rater assumption stated in the paper).

**Reliability check (Checkpoint 2):** the human lead independently codes a simple random
sample of ~30 papers on the categorical dimensions; Cohen's kappa (per dimension) is reported.
Disagreements are resolved by discussion; any codebook clarification is an amendment.

## 7. Analysis plan (prespecified)

Descriptive only — no inferential hypothesis tests:

- **RQ1:** frequency distributions of all codebook dimensions; taxonomy figure.
- **RQ2:** cross-tabulation of claim strength × evaluation method × auditability mechanisms ×
  artifact release ("auditability-gap matrix"); enumeration of strong-claim/weak-verification
  papers.
- **RQ3:** quarterly volume curves (harvest-wide, 2022→2026); composition-over-time of paper
  types and evaluation methods within the coded corpus.
- **Reliability:** Cohen's kappa per coded dimension on the human-coded sample.
- **RQ4:** qualitative analysis of `process-log/` (error taxonomy, human-intervention taxonomy,
  time/effort accounting), reported as a structured case study.

## 8. Threats to validity (acknowledged in advance)

- arXiv-only primary source (mitigated by recall cross-check; residual bias reported).
- Query-based corpus construction may miss papers that avoid the field's vocabulary.
- AI screener/coder correlated errors (mitigated by dual screening with distinct prompts,
  human audit, and human-coded reliability sample — but the raters share a base model; this
  is itself a finding for RQ4 and is discussed honestly).
- July 2026 right-censoring: the last weeks of the window under-count due to indexing lag.

## 8a. Human co-author consultation (added 2026-07-25 at the human co-author's request)

Co-authorship is a working relationship, not a sign-off at the end. The AI lead consults the
human co-author on the following classes of decision, and does not merely inform him:

1. **Any decision that changes what the paper claims** — scope, operationalisations,
   thresholds, framing of a headline finding, or a change of thesis. (Precedent: the BR7
   override, `human-interventions.md` #4; the thesis correction, `errors.md` #6.)
2. **Any point where the AI is choosing between defensible alternatives** rather than
   following the protocol — including cases where the AI has a recommendation. The
   recommendation is stated, with its reasoning and the strongest case against it.
3. **Any discovery that a prior joint decision was wrong**, reported as soon as it is known,
   not at the next checkpoint.
4. **Anything outward-facing** — uploads, submissions, deposits, public repositories —
   requires explicit per-item approval, never inferred from earlier approval.
5. **Conceptual contributions from the human** are developed and answered in writing, with
   the AI's honest assessment including disagreement, and are attributed to him in any
   artifact that uses them. (Precedent: `notes/unmarked-hypothesis.md`.)

When the human declines a safeguard the AI recommended, the AI states the cost once, plainly,
records the decision and its consequence, and does not re-litigate it.

**Minimal-intervention condition and the AI's wildcard** (added 2026-07-25 at the human's
request). The human co-author operates a deliberate least-intervention policy: the object of
this work is what frontier systems produce when left to define and settle matters themselves,
so he supplies direction, requested decisions, and judgment where the work would otherwise
commit to something unexamined — but does not correct the AI's execution, and does not audit
work merely to make it safer. Within that policy the AI holds a **wildcard**: in areas the
human has not reserved, the AI decides and proceeds without seeking approval, and is expected
to. Consultation classes 1–5 above are the reserved areas; everything else is the AI's call.
The wildcard is a working instruction, not a transfer of accountability: the human remains
responsible for the published work, and the AI still logs what it decided under it.

The AI does *not* consult on: routine execution, mechanical fixes, or work that follows
directly from decisions already made — asking permission for these wastes the collaboration.

## 9. Ethics & integrity commitments

- No fabricated or imputed data; every count traceable to a CSV in `data/`.
- Every citation in the paper machine-verified against live arXiv/DOI metadata before
  submission (`code/verify_bib.py`).
- Full disclosure of the AI's role (dedicated AI Contribution Statement; dual-venue plan:
  arXiv version compliant with arXiv's authorship policy, Zenodo record with explicit AI
  co-authorship framing; the two cross-reference).
- All AI failures encountered during the project are logged in `process-log/errors.md` and
  reported — they are RQ4 data, not embarrassments to hide.
