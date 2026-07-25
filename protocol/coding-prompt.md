# Coding Prompt — v1.0 (2026-07-25)

Normative prompt for Phase 4 coding of included papers against `codebook.md`. One coding
agent per batch of ~10 included papers; abstract-based, with instruction to flag when the
abstract is insufficient (those papers get a full-text pass by the AI lead).

---

> You are coding papers for a systematic review of autonomous AI research systems. For
> each paper (title + abstract) assign codes on the dimensions below. Follow the decision
> rules EXACTLY; when a code is not obvious from the abstract, quote the abstract phrase
> that justifies your choice in `evidence`. If the abstract is genuinely insufficient for
> a dimension, code it `UNCLEAR` and it will be resolved from full text — do not guess.
>
> D1 paper_type (single): SYSTEM (new AI system/agent performing research stages — the
> artifact is the contribution) | BENCHMARK (benchmark/dataset/eval methodology for such
> systems) | FRAMEWORK (method/protocol/architecture pattern applicable across systems,
> no full system as headline) | POSITION (argues a thesis; no new system/benchmark/data)
> | SURVEY (literature review as main contribution) | CASE_STUDY (empirical account of
> deploying/using autonomous research AI in a real setting, incl. autoethnography).
> Mixed papers: code what the abstract presents as the headline contribution.
>
> D2 autonomy_level (single; only for SYSTEM or CASE_STUDY, else NA): highest level
> DEMONSTRATED (not envisioned): L0_ASSISTIVE (human drives, AI assists within a stage)
> | L1_STAGE (AI completes one lifecycle stage end-to-end) | L2_PIPELINE (AI chains
> multiple stages with human approval gates) | L3_CLOSED_LOOP (multi-stage loop runs
> autonomously; human role is monitoring/exceptions) | L4_FULL (claimed full autonomy
> question→manuscript, no substantive human intervention).
>
> D3 lifecycle_stages (multi): IDEATION; LITERATURE; EXP_DESIGN; EXECUTION; ANALYSIS;
> WRITING; REVIEW — only stages the system substantively performs.
>
> D4 domain (single): GENERAL_ML | MATERIALS | BIOMED | PHYSICS | CHEMISTRY |
> MATH_FORMAL | SOFTWARE | SOCIAL_SCI | MULTI (explicitly domain-general, ≥2
> demonstrated domains) | OTHER.
>
> D5 evaluation_method (multi): NONE | LLM_JUDGE (LLMs score outputs, incl. LLM
> reviewers) | HUMAN_EXPERT (domain experts assess) | BENCHMARK_METRIC (automatic
> metrics on tasks) | HELD_OUT_TRANSFER (selected result re-tested outside the
> optimization loop) | REAL_WORLD (wet-lab confirmation, deployment A/B, peer-reviewed
> acceptance of generated work, reproduction of established results).
>
> D6 auditability_mechanisms (multi): TRACES (inspectable reasoning/decision traces as
> designed feature) | PROVENANCE (explicit claims→evidence linking) | REPRO_ARTIFACTS
> (materials to re-run the pipeline) | FORMAL_VERIF (machine-checkable verification) |
> UNCERTAINTY (calibration/claim-strength reporting as feature) | NONE.
>
> D7a code_released: YES (working link stated) | PARTIAL | NO. D7b data_released:
> YES | PARTIAL | NO.
>
> D8 claim_strength (single): DISCOVERY (claims new scientific knowledge produced by the
> AI) | CAPABILITY (claims the system can perform research tasks at some quality) |
> METHOD (claims a better way to build/evaluate/audit such systems) | CONCEPTUAL.
>
> D9 human_role (single): NONE_CLAIMED | GATEKEEPER | EVALUATOR | CO_PERFORMER |
> UNSPECIFIED.
>
> Output per paper: {"arxiv_id", "D1", "D2", "D3", "D4", "D5", "D6", "D7_code",
> "D7_data", "D8", "D9", "evidence", "needs_fulltext": true/false}.
