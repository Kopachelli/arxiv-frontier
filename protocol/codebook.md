# Codebook — v1.0 (2026-07-25)

Normative coding scheme for the included corpus. One row per paper in
`data/coded-corpus.csv`. Multi-select dimensions are semicolon-separated. Every code has a
decision rule; when in doubt, coders quote the abstract sentence that justifies the code in
the `evidence` column.

## Identification

| column | content |
|---|---|
| `arxiv_id` | canonical ID, no version suffix |
| `title` | as on arXiv |
| `first_submitted` | YYYY-MM-DD (v1 date) |
| `primary_category` | arXiv primary category |
| `evidence` | short quote(s) from abstract justifying non-obvious codes |

## D1 — paper_type (single)

| code | rule |
|---|---|
| `SYSTEM` | Presents a new AI system/agent that performs research stage(s). Rule: the artifact is the contribution. |
| `BENCHMARK` | Presents a benchmark/dataset/eval methodology for research agents. |
| `FRAMEWORK` | Presents a method/protocol/architecture pattern intended to be applied across systems (e.g., auditability protocols) without a full system as the headline. |
| `POSITION` | Argues a thesis; no new system/benchmark/data. |
| `SURVEY` | Reviews existing literature as its main contribution. |
| `CASE_STUDY` | Empirical account of deploying/using autonomous research AI in a real setting (incl. autoethnographic accounts). |

Priority when mixed: what the abstract presents as the headline contribution.

## D2 — autonomy_level (single; SYSTEM and CASE_STUDY papers; else `NA`)

Highest level actually *demonstrated* (not merely envisioned):

| code | rule |
|---|---|
| `L0_ASSISTIVE` | Human drives; AI assists within a stage (suggestions, drafts). |
| `L1_STAGE` | AI autonomously completes one lifecycle stage end-to-end (e.g., ideation only). |
| `L2_PIPELINE` | AI chains multiple stages with human approval gates between them. |
| `L3_CLOSED_LOOP` | AI runs the multi-stage loop autonomously; human oversight is monitoring/exception-handling, not gating. |
| `L4_FULL` | Paper claims full autonomy from question to manuscript with no substantive human intervention. |

## D3 — lifecycle_stages (multi)

`IDEATION; LITERATURE; EXP_DESIGN; EXECUTION; ANALYSIS; WRITING; REVIEW`
Code a stage only if the system substantively performs it (not merely mentions it).

## D4 — domain (single)

`GENERAL_ML` (ML/AI research itself) | `MATERIALS` | `BIOMED` | `PHYSICS` | `CHEMISTRY` |
`MATH_FORMAL` | `SOFTWARE` | `SOCIAL_SCI` | `MULTI` (explicitly domain-general with ≥2
demonstrated domains) | `OTHER`

## D5 — evaluation_method (multi; how the paper's claims are evaluated)

| code | rule |
|---|---|
| `NONE` | No empirical evaluation. |
| `LLM_JUDGE` | LLM(s) score outputs (incl. LLM reviewers). |
| `HUMAN_EXPERT` | Domain experts assess outputs. |
| `BENCHMARK_METRIC` | Automatic metrics on a benchmark/task suite. |
| `HELD_OUT_TRANSFER` | Selected result re-tested on data/tasks outside the optimization loop. |
| `REAL_WORLD` | External validation: wet-lab confirmation, deployed A/B, peer-reviewed acceptance of generated work, reproduced known results. |

## D6 — auditability_mechanisms (multi; what the system/paper provides for verification)

| code | rule |
|---|---|
| `TRACES` | Inspectable reasoning/decision traces as a designed feature. |
| `PROVENANCE` | Explicit evidence/source linking (claims → data/literature). |
| `REPRO_ARTIFACTS` | Materials sufficient to re-run the pipeline (code+config+prompts). |
| `FORMAL_VERIF` | Machine-checkable verification (e.g., proof checkers, DRC-style rules). |
| `UNCERTAINTY` | Calibration/uncertainty/claim-strength reporting as a feature. |
| `NONE` | None of the above. |

## D7 — artifacts (two columns)

`code_released`: `YES | PARTIAL | NO` (YES requires a working link in the paper).
`data_released`: `YES | PARTIAL | NO`.

## D8 — claim_strength (single; the paper's headline claim)

| code | rule |
|---|---|
| `DISCOVERY` | Claims new scientific knowledge produced by the AI (new material, theorem, empirical finding about the world). |
| `CAPABILITY` | Claims the system can perform research tasks at some quality level. |
| `METHOD` | Claims a better way to build/evaluate/audit such systems. |
| `CONCEPTUAL` | Conceptual/normative claims only. |

## D9 — human_role (single; role of humans in the reported workflow)

`NONE_CLAIMED` | `GATEKEEPER` (approval gates) | `EVALUATOR` (assess outputs only) |
`CO_PERFORMER` (human does part of the research itself) | `UNSPECIFIED`

---

### Auditability-gap operationalization (RQ2, prespecified)

A paper is flagged **strong-claim/weak-verification** iff
`D8 ∈ {DISCOVERY, CAPABILITY}` AND `D5 ⊆ {NONE, LLM_JUDGE}` AND `code_released ≠ YES`.
The complement ("audited claims") requires at least one of `{HUMAN_EXPERT, HELD_OUT_TRANSFER,
REAL_WORLD}` in D5 **or** `REPRO_ARTIFACTS/FORMAL_VERIF` in D6.
