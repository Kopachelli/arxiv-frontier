# Screening Prompts — v1.0 (2026-07-25)

Normative record of the two independent AI screening passes (protocol section 5). Each
candidate title+abstract is screened by BOTH passes. Two decorrelation measures: the
passes are worded differently, AND they run on different base models — Pass A on Claude
Fable 5 (claude-fable-5), Pass B on Claude Opus 5 (claude-opus-5). (Recorded 2026-07-25,
before screening began; both models share the Claude family — residual correlation is
acknowledged in Limitations.) Structured output schema (both passes):

```json
{
  "arxiv_id": "...",
  "decision": "include | exclude | borderline",
  "reason_code": "IC1 | IC2 | IC3 | EC1 | EC2 | EC3 | EC4 | EC5",
  "justification": "one sentence"
}
```

`include` requires citing an IC code; `exclude` requires an EC code. Date criterion IC4 is
applied mechanically by script, not by the screener.

---

## Pass A prompt (criteria-first framing)

> You are screening papers for a systematic review of autonomous AI research systems
> ("AI scientists"). For the paper below (title + abstract), decide inclusion strictly by
> these criteria.
>
> INCLUDE if ANY apply:
> - IC1: The paper's primary subject is an AI system/agent that autonomously performs at
>   least one substantial stage of the scientific research lifecycle (ideation, literature
>   synthesis, experiment design, experiment execution, analysis, scientific writing, or
>   peer review) with an agentic loop — beyond single-shot tool invocation.
> - IC2: The primary contribution is a benchmark, evaluation methodology, or dataset
>   specifically for such systems.
> - IC3: A framework, position, survey, or case-study paper specifically about autonomous
>   AI research — including auditability, calibration, governance, or integrity of
>   AI-conducted research.
>
> EXCLUDE if ANY apply (exclusion wins only when no IC applies):
> - EC1: Generic LLM/agent work not aimed at performing research (coding assistants,
>   RAG QA, web agents, recommender/ops/game agents), even if "research" appears.
> - EC2: AI-for-science models used as instruments (property predictors, folding models,
>   surrogates) without an agentic research loop as the paper's subject.
> - EC3: About human use of AI writing assistance or its detection, with no autonomous
>   research system as subject — UNLESS it qualifies as an IC3 integrity paper.
> - EC5: Not English.
>
> Use "borderline" whenever you are genuinely uncertain; borderlines are adjudicated
> separately — do not force a decision.

## Pass B prompt (question-first framing)

> Read this title and abstract. Answer three questions, then decide.
>
> Q1: Is the paper fundamentally ABOUT machines doing science — an AI agent that itself
> ideates, searches literature, designs or runs experiments, analyzes results, writes
> papers, or reviews them, in a loop with some autonomy? (Systems papers.)
> Q2: If not a system, is it a measuring stick or rulebook FOR machines doing science — a
> benchmark, evaluation method, audit/calibration framework, survey, position, or
> integrity study specifically about AI-conducted research?
> Q3: Or is it really about something else — an ordinary agent application (coding, QA,
> web, ops, games), a scientific prediction model used as a tool, or human writers using
> AI assistance?
>
> Yes to Q1 → include (reason IC1). Yes to Q2 → include (IC2 for benchmarks/evaluation,
> IC3 for framework/position/survey/integrity). Yes to Q3 only → exclude (EC1 for agent
> applications, EC2 for tool models, EC3 for human writing assistance). Genuinely unsure →
> borderline. Do not include a paper because it is impressive; include it because it is
> in scope.

## Adjudication

Disagreements (A≠B) and all borderlines go to the AI lead with the full abstract and both
justifications; the lead's decision + rationale is recorded in
`data/screening-decisions.csv` (`adjudicated=1`).

## Human audit

Khristian audits ≥30 randomly sampled decisions stratified over include/exclude
(and all adjudications flagged surprising, if any); outcomes reported in the paper.
