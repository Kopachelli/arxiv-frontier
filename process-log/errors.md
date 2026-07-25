# Error Log (RQ4 primary data)

Every AI failure encountered during this project is recorded here contemporaneously:
hallucinated or wrong facts caught by verification, tool misuse, incorrect code, coding
mistakes found in the reliability check, reasoning errors caught by the human or by later
passes. Format: date, phase, description, how caught, consequence, correction.

This log is analyzed in the paper's Reflexive Case Study section. Nothing is deleted from
this file; corrections are appended.

---

## #1 — 2026-07-25 — Phase 2 (harvest) — Query design error: unanticipated stemming

**Description.** The AI designed query `qf3_auditable_agent` as
`(abs:"auditable" AND (abs:agent OR ... OR abs:LLM))`, intending to catch papers on
auditability of research agents. The arXiv API stems `"auditable"` to `audit*`
(audit/auditing/audits), which co-occurs with agent/LLM vocabulary in ~2,300 in-window
papers (bias audits, safety audits, etc.). Result: 2,276 of 3,348 harvested candidates
(68%) matched only this query and were, on sampling, clearly out of scope.

**How caught.** The AI noticed the per-query count anomaly in the harvest manifest
(2,336 vs a median of ~40 for other queries), sampled the only-matched-here papers, and
ran controlled API queries. Initial hypothesis (boolean mis-parsing) was WRONG — nested
and flattened forms returned identical counts; controlled tests isolated stemming as the
cause. Note: the AI's first diagnosis was incorrect and was corrected by its own
follow-up experiment.

**Consequence.** One wasted harvest run (~10 min); no downstream contamination —
caught before screening began.

**Correction.** Query replaced with three precise phrase queries ("auditable AI
scientist": 3 hits; "auditable agent": 33; "auditable research": 6); full harvest re-run
from scratch so `data/HARVEST_MANIFEST.md` reflects only the corrected strategy.
