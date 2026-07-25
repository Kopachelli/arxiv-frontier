# Human Intervention Log (RQ4 primary data)

Every point where the human co-author (Khristian Kopachelli) directed, corrected, decided,
or gated the work. Format: date, trigger (AI-requested vs human-initiated), decision, effect
on the project.

---

## #1 — 2026-07-25 — Project framing and four design decisions (AI-requested)

Trigger: AI presented scouting results and four decision questions with recommendations.
Decisions by the human:

1. **Topic**: reflexive systematic review + bibliometrics of autonomous AI research systems
   (AI's recommended option).
2. **Authorship handling**: dual-venue — arXiv version with human as listed author and full
   AI-role disclosure (compliant with arXiv's policy prohibiting AI authors); Zenodo/OSF
   record with explicit AI co-authorship framing; cross-referenced. (Human chose this over
   the AI's recommended single-venue disclosure option — a substantive human decision.)
3. **Empirical depth**: full design — PRISMA-style review with human reliability check AND
   quantitative bibliometrics with released data/code (AI's recommended option).
4. **Venue path**: first-time arXiv submitter; plan endorsement path (cs.DL/cs.CY) with
   Zenodo DOI as immediate fallback.

Effect: fixed the research design and publication strategy.

## #2 — 2026-07-25 — Plan approval (Checkpoint 0)

Trigger: AI submitted the full written research plan. Human approved without modification.
Effect: execution authorized through the phase checkpoints.

## #3 — 2026-07-25 — Protocol approval (Checkpoint 1) (AI-requested)

Trigger: AI presented final corpus (1,426 candidates; 1,357 codable) and the protocol
package for the formal pre-screening gate. Human approved protocol v1.0 as-is and
authorized phase-wise git commits (history as process evidence).
Effect: protocol locked; screening authorized; later changes require logged amendments.

## #4 — 2026-07-25 — Scope checkpoint: three decisions, one overruling the AI (AI-requested)

Trigger: AI presented the screened corpus (628 included), the boundary rules, the
pre-specified >400 narrowing trigger, and a 40-item audit worksheet.

1. **Corpus size** — human chose to code all 628 rather than narrow (AI's recommendation;
   amendment A2a).
2. **Human screening audit** — human declined the audit, stating trust in the rules. The
   AI had recommended doing it. **Consequence, recorded plainly: this review has no
   independent human validation of its screening decisions.** Reported in Limitations, and
   the AI substituted a third independent AI screening pass on a random sample to estimate
   Layer-2 self-consistency — which measures stability, not correctness, and is described
   as such.
3. **Deep-research agents (BR7)** — human **overruled the AI**, ruling the 175 excluded
   "generic deep research" papers back into scope, on the grounds that deep research is
   how the field productized autonomous research and excluding it would define the field
   to fit the reviewer's framing. AI had recommended and defended exclusion. Amendment A2b.

Effect: corpus retained in full and enlarged; the AI's largest scope judgment reversed;
one methodological safeguard (human screening audit) removed from the design.
