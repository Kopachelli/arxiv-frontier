# Protocol Amendments

Any change to `review-protocol.md`, `codebook.md`, or `screening-prompts.md` made after
screening begins is recorded here with date, what changed, why, and at what project stage.

---

## A1 — 2026-07-25 — Boundary rules and rule-based re-screen

**Stage.** After the exploratory dual-pass screening of all 1,359 candidates, before coding.

**Trigger (two facts).**
1. The two screening passes disagreed or flagged borderline on **292/1,359 papers (21.5%)**.
   Inspection of the disagreements showed they were **not** randomly distributed: they
   concentrated on seven recurring classes of paper at the edge of the field's own
   vocabulary (assistive research tools, automated literature-review pipelines, Bayesian
   optimization / self-driving-lab infrastructure, human-AI-usage measurement and AI-text
   detection, data-science agents, general-purpose "deep research" web agents, and ethics
   frameworks for human AI use). Protocol v1.0's IC1–IC3 / EC1–EC5 did not determine these
   cases, so consistent adjudication was impossible without explicit rules.
2. Agreed includes reached **646**, above the 400 threshold at which protocol §5
   pre-specifies a documented scope narrowing before coding.

**Change.** Seven boundary rules (BR1–BR7) are added, with four new exclusion codes, and
the *entire* corpus is re-screened against the amended criteria in a single rule-application
pass (see "Application" below). BR1–BR7 are strictly interpretive: they specify how IC1–IC3
and EC1–EC5 apply to the seven classes, in the direction the RQs require — the object of
this review is **AI as a producer of research**, not AI as a research aid for humans, not
detection of AI text, and not general-purpose agents.

### New exclusion codes

| code | meaning |
|---|---|
| `EC6_ASSISTIVE` | Human-driven tool: the human makes the substantive research judgments; the AI supplies suggestions, feedback, retrieval, or interface. No stage-level AI autonomy. |
| `EC7_HUMAN_AI_USE` | Object is human *use* of AI in research/writing, or methods to detect AI-assisted text — not research conducted by an AI system. |
| `EC8_GENERIC_ANALYSIS` | Data-analysis / data-science / BI / ML-engineering agents and benchmarks not framed around scientific claims or domain science. |
| `EC9_GENERIC_DEEPRESEARCH` | General-purpose "deep research" web/QA agents whose stated purpose and evaluation are generic information seeking, not scientific research. |

### Boundary rules

- **BR1 (autonomy floor).** A SYSTEM paper is in scope only if, for at least one research
  lifecycle stage, the AI produces the substantive research output rather than assisting a
  human who produces it. The human may set the task, review, or approve. Interactive
  ideation/writing/retrieval aids where the human makes the research judgments →
  `EC6_ASSISTIVE`.
- **BR2 (hypothesis generation).** Machine generation of *scientific* hypotheses is in scope
  (IC1, ideation stage) even without a full agent loop, provided the hypotheses concern a
  real scientific domain. Inductive-reasoning studies on toy or general-purpose tasks, and
  studies of LLM reasoning properties as such → `EC1`.
- **BR3 (literature synthesis).** Systems that autonomously screen, extract, or synthesize
  literature for a research review are in scope (IC1, literature stage). Workflow/tool
  suites that orchestrate human reviewers and third-party tools → `EC6_ASSISTIVE`.
- **BR4 (autonomous experimentation / self-driving labs).** In scope if the paper's subject
  is a system that autonomously decides *what experiment to run next* from prior results (a
  closed experimental decision loop), or a framework/benchmark/governance study for such
  systems. Optimizer libraries, acquisition-function-only contributions driven by an
  external loop, robotic execution or measurement capability, and surrogate models →
  `EC2`.
- **BR5 (integrity scope).** IC3 covers the epistemic integrity of research *produced by AI
  systems*: auditability, calibration, verification, governance, and fraud arising from
  AI research pipelines (including studies of AI-produced fraudulent research artifacts at
  scale). Prevalence measurement of human LLM-assisted writing, AI-text/AI-paper detector
  methods, and institutional ethics guidance for researchers using AI → `EC7_HUMAN_AI_USE`.
- **BR6 (data-science agents).** In scope only if the agent's task is framed as scientific
  research (hypotheses, mechanisms, scientific claims, domain science data). Generic data
  analysis, dashboarding, Kaggle-style modeling → `EC8_GENERIC_ANALYSIS`.
- **BR7 (deep research agents).** In scope only if purpose or evaluation centers on
  scientific/academic research work (literature synthesis for science, survey or scientific
  report generation, scientific QA). General web-research/QA agents evaluated primarily on
  generic browsing benchmarks → `EC9_GENERIC_DEEPRESEARCH`.

### Application

Because the 1,067 agreed decisions were also made without BR1–BR7, applying the rules only
to the 292 disagreements would produce an internally inconsistent corpus. The **entire
corpus of 1,359 papers is therefore re-screened** in one rule-application pass against the
amended criteria. Both screening layers are retained and reported:

- **Layer 1 (exploratory, preserved in `data/screening-decisions.csv`):** two independent
  passes on different base models with different framings. Its agreement statistics are
  reported as a finding about AI rater reliability in scope judgment (RQ4), and its
  disagreement structure is the documented reason for this amendment.
- **Layer 2 (final, `data/screening-final.csv`):** rule-based application of the amended
  criteria to every candidate, carrying Layer-1 justifications as context. This layer
  determines the corpus. The human co-author audits a stratified random sample of ≥30
  Layer-2 decisions plus every paper where Layer 2 reverses a unanimous Layer-1 include.

**Rationale for direction of narrowing.** RQ1/RQ2 concern autonomous AI research systems
and the verification of their claims. A corpus admitting assistive tools, AI-text
detectors, and generic web agents would measure a different, broader object ("AI touching
research somehow") and would make the auditability-gap analysis incoherent, since those
papers do not make AI research claims at all. The excluded classes are not discarded
silently: each is counted by reason code and reported as a boundary-class table, since the
contested boundary is itself a finding about a field that has not settled what counts as an
"AI scientist".

---

## A2 — 2026-07-25 — Corpus retained in full; BR7 revised by the human co-author

**Stage.** After the Layer-2 re-screen, before coding. Both changes decided by the human
co-author (Khristian Kopachelli) at the scope checkpoint; see
`process-log/human-interventions.md` #4.

### A2a — No further scope narrowing (>400 threshold set aside)

Protocol §5 pre-specified a documented narrowing if the corpus exceeded 400 papers; it
reached 628. The threshold is **set aside rather than applied**, with the reasoning stated
openly: 400 was an a priori guess at manageable workload written before the field's size
was known, not a scientific criterion. Narrowing at this point would remove in-scope work
for convenience and would understate the field. The study is reported as a systematic
**map**, for which completeness of the identified corpus is a strength, and all included
papers are coded.

### A2b — BR7 revised: "deep research" agents are in scope

**Original BR7 (A1).** General-purpose deep-research/web-QA agents evaluated primarily on
generic browsing benchmarks were excluded (`EC9_GENERIC_DEEPRESEARCH`; 175 papers — the
largest single exclusion class).

**Revised BR7.** Deep-research agents — systems that perform multi-step information
seeking, evidence synthesis, and report generation — **are in scope** (IC1: literature
synthesis and/or scientific writing stages), whether or not their benchmarks are
science-specific. Still excluded as `EC1`: transactional or navigational web agents
(shopping, booking, form filling, UI automation) and single-hop question answering without
a synthesis or report-production step.

**Rationale (human co-author's, recorded as given).** "Deep research" is how the field
actually productized autonomous research; a map that excludes it misses where the
attention and engineering went. Excluding an entire product category because its
benchmarks are generic risks defining the field to match the reviewer's preferred framing
rather than its real composition.

**Note on provenance and RQ4.** This reverses a judgment the AI made and defended. It is
the clearest instance in this project of the human co-author changing a substantive
scientific decision, and it is reported as such: the AI's original rule, the human's
override, the reasoning on both sides, and the effect on the corpus (n changes from 628).

**Application.** Every excluded paper decided under BR7 or coded
`EC9_GENERIC_DEEPRESEARCH`, plus every excluded paper whose title or abstract mentions
"deep research"/"deep researcher" (to catch cases routed to `EC1` instead), is re-screened
under revised BR7. No other decisions are disturbed. Set membership is computed by script
so the affected set is reproducible.
