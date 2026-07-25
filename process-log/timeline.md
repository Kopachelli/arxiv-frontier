# Process Timeline (RQ4 primary data)

Chronological record of the AI-led research process. Every working session gets an entry:
date, actor, what was done, tools used, outputs. Written contemporaneously, not
reconstructed. Companion files: `errors.md` (AI failures), `human-interventions.md`
(every point where the human co-author shaped the work).

---

## 2026-07-25 — Session 1 (Claude Fable 5, with Khristian Kopachelli)

**Project initiation and topic selection.**

- Khristian proposed the collaboration frame: produce a real, public research paper as
  independent researchers, with the AI (Claude Fable 5) doing the research using live
  literature access (arXiv + multi-source paper-search MCP servers). Topic selection was
  explicitly delegated to the AI ("define what our research is").
- The AI ran a 4-query scouting sweep on live arXiv (July 2026 state):
  (a) superintelligence/frontier-safety discourse, (b) AI-scientist/autonomous-research
  systems, (c) self-improving agents, (d) AI authorship & research integrity.
  ~60 abstracts reviewed. Key observations that shaped topic choice:
  - The AI-scientist systems literature is growing fast with a distinct auditability
    subthread (e.g., arXiv:2607.09195, 2607.05682, 2606.31273).
  - The integrity literature documents industrialized AI ghost-authorship
    (arXiv:2606.02184) and poisoning of AI-driven science (arXiv:2607.10712).
  - No rigorous, fully-disclosed systematic study of the field conducted *by* the class
    of system it studies was found.
- The AI proposed four candidate directions with an explicit recommendation; the human
  selected the recommended reflexive systematic-review design and made three further
  design decisions (see `human-interventions.md` #1).
- The AI drafted the full research plan; the human approved it (Checkpoint 0).
- Wrote `protocol/review-protocol.md` v1.0 and `protocol/codebook.md` v1.0; created repo
  skeleton and this process log.

*Tools used: arXiv MCP search (4 queries), file tools. No harvest code run yet.*

**Phase 2 — corpus harvest (same session).**

- Wrote `code/harvest.py` (stdlib-only; 30 queries in 3 families; manifest with per-query
  counts; no silent truncation) and `code/verify_bib.py` (citation-integrity gate).
- Harvest run #1: 3,348 unique candidates — but 68% matched only one anomalous query.
  Diagnosed via controlled API experiments: arXiv stems "auditable"→audit*; the AI's
  first hypothesis (boolean mis-parsing) was wrong and corrected by its own experiments.
  Full record: `errors.md` #1.
- Query family corrected (three precise phrases replace the broad conjunction);
  harvest re-run from scratch for a clean manifest.
- Harvest run #2 (corrected): 1,110 unique candidates; year distribution
  11/49/135/391/524 (2022→2026-07) — field growth directly visible in raw counts.
- Recall cross-check: 13/15 known landmark papers present. Two vocabulary-outlier misses
  routed via `data/expert-identified.csv` (standard PRISMA "other methods" route).
  Cross-source sampling (OpenAlex) revealed bio-domain systems (Biomni, SpatialAgent)
  publish on bioRxiv → documented arXiv-coverage limitation (`data/recall-check.md`).
- Probing surfaced under-covered field vocabulary — notably "deep research" (343 hits);
  11 supplementary queries added; final harvest run #3 launched. All query-set changes
  made BEFORE any screening (no amendment required; logged here).
- **Final harvest (run #3): 1,426 unique candidates** (+2 expert-identified);
  1,357 in the codable window (≥2024-01-01). Year curve: 14/55/149/508/700 (2026 =
  7 months). All 15 known landmarks present (13 via queries, 2 via expert route).
  Phase 2 complete. Paused for Checkpoint 1: human approval of protocol before screening.

**Checkpoint 1 passed; Phase 3 — screening (same session).**

- Human approved protocol v1.0 unchanged and authorized phase-wise git commits
  (`human-interventions.md` #3). Phases 1–2 committed (9f0c1b6).
- Pre-screening enhancement recorded in `screening-prompts.md`: Pass B runs on a
  different base model (Opus 5) than Pass A (Fable 5) to decorrelate rater error.
- Screening infrastructure: `code/screen.py` (batching + merge); 1,359 papers
  (1,357 codable + 2 expert-identified) → 55 batches of ≤25.
- Workflow launch #1 failed instantly: the orchestration script assumed `args` arrives
  as an object; it arrived as a JSON string → the job loop silently built 0 jobs. An
  infrastructure bug (silent-empty failure), not a screening error; fixed with defensive
  parsing + loud assertion. Relaunched: 110 screening agents (55 batches × 2 passes).
- Layer-1 screening completed: 110 agents, 13.7 min, 0 failures, ~6.0M subagent tokens.
  Raw agreement 1,067/1,359 (78.5%); 292 needing adjudication; 646 agreed includes.
  7 papers had a missing pass (agent wrote fewer entries than the batch contained) —
  detected by the merge script's per-paper reconciliation, re-run individually
  (`errors.md` #2).
- **Inspection of the 292 disagreements produced the session's most consequential
  finding**: they were not noise. They concentrated on seven recurring boundary classes
  (assistive tools, automated literature review, self-driving-lab infrastructure,
  human-AI-usage/detection studies, data-science agents, generic deep-research agents,
  ethics-of-human-AI-use frameworks) that protocol v1.0 simply did not determine. Two
  frontier models disagreeing systematically on *what counts as an AI scientist* is a
  finding about the field, not merely about the raters.
- Wrote **amendment A1**: boundary rules BR1–BR7 + four refined exclusion codes, and —
  because applying rules to only the 292 would make the corpus internally inconsistent —
  a rule-based re-screen of ALL 1,359 candidates as Layer 2. Layer 1 is preserved and
  reported (its agreement statistics are an RQ4 result). Launched 55 re-screen agents.
- Layer-2 re-screen complete (55 agents, 8 min): **628 included / 731 excluded**.
  Largest exclusion class: generic deep-research agents (175, BR7). 65 reversals of
  unanimous Layer-1 includes. Two plumbing defects found and fixed (`errors.md` #5).
  Measured Layer-1 reliability: raw agreement 0.833, Cohen's κ 0.715 (3-way) / 0.804
  (binary include-vs-not).

**Scope checkpoint and human override (same session).**

- AI presented the corpus, the >400 narrowing trigger, a 40-item audit worksheet, and
  the BR7 judgment for human review. Outcomes (`human-interventions.md` #4):
  code all 628 (A2a); **human declined the screening audit** (recorded as a design
  weakness, with an AI-self-consistency pass substituted and described honestly);
  **human overruled BR7**, ruling deep-research agents back into scope (A2b).
- A2b applied: 253 affected papers re-screened under revised BR7 (the 175 EC9 exclusions
  plus 78 more found by a text-match sweep for deep-research vocabulary routed to other
  codes); 183 flipped to include. **Final corpus: 811 papers.**

**Phase 4 — coding (same session).**

- 811 papers → 68 batches of 12; coding prompt derived from the normative codebook,
  with UNCLEAR + needs_fulltext available so agents can decline to guess.
- Launched 74 agents: 68 coding + 6 running an independent third screening pass over a
  random 120-paper sample (Layer-2 self-consistency estimate).
