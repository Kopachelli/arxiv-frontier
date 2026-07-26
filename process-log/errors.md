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

## #2 — 2026-07-25 — Phase 3 (screening) — Silent-empty workflow success

**Description.** The first screening-workflow launch returned success in 106 ms having
done nothing (0 agents). The orchestration script destructured its arguments assuming an
object; the runtime delivered a JSON string, so the job-construction loop produced an
empty list and the workflow "succeeded" with zero work.

**How caught.** The AI noticed the result payload was all zeros. Nothing in the success
signal itself indicated failure.

**Consequence.** None beyond a wasted launch — caught before any data was produced.

**Correction.** Defensive parsing plus a loud assertion that throws when any required
argument is missing, so this class of failure fails loudly rather than silently.

**Why this matters for RQ4.** An autonomous research pipeline that reports success
without doing the work is precisely the failure mode that abstract-level review cannot
detect. It was caught only because a human-designed reconciliation (expected vs actual
counts) existed.

## #3 — 2026-07-25 — Phase 3 (screening) — Dropped items in batch outputs

**Description.** 7 of 1,359 papers (0.5%) were missing a screening decision: individual
agents wrote result files containing fewer entries than the input batch, despite explicit
instructions to output exactly one entry per paper. Distribution: 5 missing pass B, 2
missing pass A, spread across different batches.

**How caught.** The merge script reconciles per-paper across passes and reports missing
entries by ID; it does not assume completeness.

**Consequence.** None: the 7 gaps were re-run individually and merged.

**Why this matters for RQ4.** Silent item-dropping in long structured outputs is a
quantifiable AI failure mode in systematic-review work (~0.5% here). Without explicit
per-item reconciliation it would have shown up as a slightly smaller corpus and nothing
else — invisible in the final paper.

## #4 — 2026-07-25 — Phase 3 (screening) — Underspecified protocol at field boundaries

**Description.** The AI-written protocol v1.0 produced criteria that failed to determine
21.5% of screening decisions (292/1,359). Two independent frontier models disagreed
systematically — not randomly — on seven recurring classes of boundary paper.

**How caught.** Layer-1 dual-pass design plus inspection of the disagreement structure
(the AI examined the actual disagreements rather than treating the agreement rate as a
single quality number).

**Consequence.** A full re-screen of the corpus (amendment A1) — roughly a doubling of
screening cost.

**Correction.** Boundary rules BR1–BR7 + refined exclusion codes; entire corpus
re-screened for internal consistency; both layers preserved and reported.

**Why this matters for RQ4.** The AI wrote a protocol that *looked* rigorous and passed
human review, yet under-determined a fifth of its own decisions. The gap was invisible in
the protocol document and surfaced only by running two raters against each other — an
argument that AI-conducted reviews need redundancy specifically at the definitional layer,
not just the extraction layer.

## #5 — 2026-07-25 — Phase 3 (re-screen) — Two data-plumbing defects in the AI's own pipeline

**Description.** Two distinct defects in code the AI wrote:
(a) One paper (2603.06677) present in the input was absent from all re-screen outputs —
    an item silently dropped by a batch agent (same class as #3, recurring at ~0.07%).
(b) The re-screen exporter looked up metadata only in `candidates.csv`, so the two
    expert-identified papers — deliberately added *because* the queries missed them —
    reached the screener with **empty title and abstract**. One of them
    (2605.28102) was consequently judged on nothing but a leftover note and flagged
    `UNDECIDED`; the other (2606.02184, the Ghost Couple study, a motivating paper for
    this review) was decided blind.

**How caught.** (a) by the merge script's completeness reconciliation against the
Layer-1 roster; (b) by reading the single `UNDECIDED` justification instead of treating
it as noise — it said "title/abstract missing", which exposed the plumbing defect.

**Consequence.** Three papers screened on absent or degraded input.

**Correction.** Metadata for expert-identified papers is now fetched into a cached
`data/expert-identified-meta.json`, and the exporter **refuses to emit any paper with an
empty abstract** rather than silently passing blanks to a screener. All three papers
re-screened with full metadata.

**Why this matters for RQ4.** The failure was not in judgment but in plumbing, and it hit
precisely the records that had been rescued by human expertise — the AI's own pipeline
quietly nullified the correction the humans-and-AI had made earlier. Systems that look
like they are reasoning may be reasoning over nothing; only an explicit
refuse-on-empty-input check turns that from silent corruption into a loud failure.

**Why this matters for RQ4.** The failure was not in judgment but in plumbing, and it hit
precisely the records that had been rescued by human expertise — the AI's own pipeline
quietly nullified a correction made earlier in the project. Systems that appear to be
reasoning may be reasoning over nothing; only an explicit refuse-on-empty-input check
turns that from silent corruption into a loud failure.

## #6 — 2026-07-25 — Phase 6 (writing) — Draft thesis contradicted by the AI's own data

**Description.** The first full draft asserted that papers claiming AI-produced discoveries
were "among the least checkable in the corpus". When the artifact-verification run
completed and the claim-strength cross-tabulation was computed, the data said something
different and more interesting: discovery papers report external validation at
**50% versus 11% corpus-wide** and strong evaluation at 60% versus 29% — markedly *better*
than average — while providing auditability mechanisms at 36% versus 45% and code
repositories at 55% versus 61% — worse. The draft's framing was wrong.

**How caught.** The AI computed the cross-tabulation to populate a table and noticed the
numbers did not support the prose it had already written, rather than filling the table and
leaving the narrative intact.

**Consequence.** Abstract, introduction, results, and conclusion rewritten around the
corrected finding: this literature validates outputs better than it exposes process, and
the dissociation is widest for the strongest claims.

**Why this matters for RQ4.** This is the failure mode most dangerous to AI-conducted
research and the hardest to detect externally: a fluent, plausible thesis written before
the evidence was complete, which would have survived review because it sounded right and
pointed the same direction as the aggregate numbers. Nothing but recomputing and reading
the specific cross-tabulation caught it. Note also that the corrected finding is
*sharper* than the wrong one — following the data cost nothing scientifically.

## #10 — 2026-07-26 — Paper 1 corpus — 18 internal-consistency violations (2.2%)

**Description.** A mechanical check of rules the protocol already implied found 18 records in
the published corpus that violate them:
- **15 papers included while coded `L0_ASSISTIVE`**, contradicting amendment A1's boundary
  rule BR1, under which assistive tools where the human makes the research judgments are
  excluded as `EC6_ASSISTIVE`. Either the inclusion or the autonomy code is wrong; which one
  differs by paper and requires adjudication.
- **3 `POSITION` papers credited with lifecycle stages**, where the codebook assigns `NA` to
  papers presenting no system.

**How caught.** Indirectly. The Phase V LLM audit produced one true positive among fourteen
flags on uncorrupted records; that one flag prompted writing `code/check_consistency.py`,
which then found all 18 deterministically across the full corpus.

**Consequence.** Affects the published Zenodo record. Under the Phase V protocol §6 commitment,
this is reported publicly and a corrected version is to be deposited. The headline findings
(auditability 55%, held-out transfer 5%, human role unstated 71%, the discovery dissociation)
do not depend on D2 and are unaffected in direction; the autonomy distribution and the
corpus size will change slightly.

**Why this matters for RQ4.** The error is not a wrong judgement but an **unenforced
invariant**: the protocol stated a rule (BR1) and the pipeline never checked that the coded
output obeyed it. Nothing in the review's design connected the screening rule to the coding
output, so the contradiction sat in a published dataset. Systematic reviews — human or AI —
routinely state rules of this kind and routinely do not test them.

## #9 — 2026-07-26 — Phase V — Verification prompt paraphrased the rule it was verifying

**Description.** The Arm 2 audit prompt rendered the codebook's autonomy rule as "NA if the
paper presents no system", where the codebook says autonomy applies *only* to `SYSTEM` and
`CASE_STUDY` papers and is `NA` for everything else. Both auditors, following the paraphrase,
flagged correctly-coded `FRAMEWORK` papers as errors — producing most of the 14 apparent
false positives.

**How caught.** Adjudicating the flagged items against the codebook rather than accepting the
auditors' agreement as evidence. Two independent models agreeing did not make them right; they
were both faithfully applying an instruction that was wrong.

**Consequence.** Inflated apparent error rate in Paper 1's corpus (7.8% flagged versus 2.2%
genuine violations). No effect on published data.

**Why this matters for RQ4.** A verifier is only as good as the statement of what it is
verifying against, and here the AI paraphrased its own normative document when constructing
the check. **Two models agreeing at 97% told us nothing about correctness — it told us they
received the same wrong instruction.** High inter-rater agreement is routinely reported as
evidence of quality; this is a concrete case where it measured shared instruction-following
instead.

## #8 — 2026-07-26 — Phase 7 (submission) — Recommendation made without checking a
## necessary condition

**Description.** The AI recommended `cs.DL` as the arXiv primary category and, in the same
document, recommended Takahara & Mizoguchi as the preferred endorsers. Both recommendations
were reasonable in isolation and jointly impossible: arXiv endorsement is category-specific,
and those authors publish in cs.AI and cond-mat, not cs.DL. The same defect applied to two of
the three named candidates.

**How caught.** Before drafting the request, the AI checked the candidates' actual arXiv
categories mechanically (`code/find_endorsers.py`) rather than relying on its own earlier
reasoning. Four of six candidates could not have endorsed for the recommended category.

**Consequence.** None realised — caught before any request was sent. Had it not been, the
human co-author would have written to researchers who were unable to help, in his own name.

**Correction.** Primary category changed to cs.AI (defensible on the merits: it is where the
mapped literature and its audience live), cs.DL retained as a cross-list, and the endorser
analysis rebuilt from verified category data.

**Why this matters for RQ4.** The failure is not a hallucinated fact but an **unchecked
precondition**: two individually sound recommendations that could not both hold. This kind of
error survives review easily, because each half reads as correct and nothing in the text
signals that a joint constraint exists. It is also a case where the cost would have been borne
by the human — the AI's error would have reached third parties under his signature. That
asymmetry is worth naming: an AI collaborator's mistakes are not always paid for by the AI.

## #7 — 2026-07-26 — Phase 7 (deposit) — A failed action that partially succeeded

**Description.** While filling the Zenodo deposit form, a long description was typed into
the rich-text editor in a single browser action. The action **returned an explicit error**
("Input.dispatchKeyEvent timed out; the renderer may be frozen"). The AI treated this as a
failure and re-entered the text in smaller chunks. The first attempt had in fact partially
landed, so the saved description contained several duplicated paragraphs.

**How caught.** The AI screenshotted the description field to verify the content rather
than trusting the sequence of successful-looking type actions, and saw the repetition.

**Consequence.** None published — caught while the record was still an unpublished draft.
The field was cleared and re-entered, and the rendered preview was checked before stopping.
A stray empty required-field row, introduced by the select-all-and-delete recovery, was
also found and removed in the same check.

**Why this matters for RQ4.** The error signal was *wrong in the dangerous direction*: a
timeout reported failure, but the action had partly succeeded. An agent that trusts error
messages symmetrically with success messages will corrupt state precisely here — retrying
an operation it believes did not happen. This is the mirror image of failure #2, where a
success signal reported work that had not happened. Together they make the general point:
**an autonomous system's own status reports are not evidence about the world; only
inspecting the resulting state is.** That is the same claim this paper makes about the
literature it maps, arrived at from our own operational logs.
