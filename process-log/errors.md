# Error Log (RQ4 primary data)

Every AI failure encountered during this project is recorded here contemporaneously:
hallucinated or wrong facts caught by verification, tool misuse, incorrect code, coding
mistakes found in the reliability check, reasoning errors caught by the human or by later
passes. Format: date, phase, description, how caught, consequence, correction.

This log is analyzed in the paper's Reflexive Case Study section. Nothing is deleted from
this file; corrections are appended.

---

## #15 — 2026-08-18 — Paper 1, self-verification — We committed the failure we documented in
## 490 other papers, in the sentence claiming we had not

**Description.** Phase R's naming policy §5 ("we go first") requires Paper 1 to be verified by
the procedure applied to everyone else, before any author is contacted. Six adversarial
verifiers were run over the paper against this repository. Of 54 claims, **19 were supported
(35%) and 15 were marked `CONTRADICTED`.** Nine distinct defects survived source-level
adjudication by the AI lead; every one below was confirmed by hand, deterministically, against
the released files.

| # | claim as published | what the artifact holds |
|---|---|---|
| a | "Every number in the paper is generated into a macro file by the analysis script; **none is transcribed by hand**" | ~40 own-study statistics are typed as literals. The whole of §3.5 — `149`, κ `0.92/0.87/0.86/0.83/0.78/0.92/0.81/0.37`, `50`, `92.6%`, `77.9%`, `78.5%` — has no macro backing |
| b | "**Nine** of the ten dimensions reach substantial agreement" | `data/coding-reliability.csv`, written by our own script, has **eight** rows reading `substantial`; D3 is `moderate`, D9 is `fair` |
| c | Abstract: "**every one** of our own failures was caught by a cheap reconciliation check, and none would have been visible in the finished paper" | Error #14 in this file records, verbatim, "An external reader's critique of the published v2, **not by us**" and "A published paper asserted a difference its own data did not support" |
| d | "**Five** failures were logged" | This file contains **fourteen** numbered entries; six even on the narrowest review-only reading |
| e | "Full results, **including the confusion matrix**, are in `data/CODING-RELIABILITY-RESULTS.md`" | That file contains no confusion matrix — one prose sentence describing its dominant cell |
| f | "the data files permit independent recomputation of **every** statistic" | The 149-paper double-coding study cannot be recomputed: `coding_reliability.py score()` globs `rel-*.json`, and **zero** such files are tracked or present on disk |
| g | "`check_consistency.py` **now runs as a gate** on every regeneration of the analysis" | It is invoked by nothing. `analyze.py` does not import or shell out to it; it is a script a human must remember to run |
| h | "of which 2 failed to parse … computed over the 805 papers that parsed" | 811 − 2 = **809**, not 805. Both macros are individually right; the sentence joining them is arithmetically false. 805 is the intersection with the 807-paper v3 corpus, which the prose never says |
| i | "a record of **every** point where the human co-author intervened" | `human-interventions.md` holds six entries, all 2026-07-25, last touched at commit `a9cb1d5`, while the repository runs to 37 commits. `timeline.md` itself records later interventions with no entry |

**How caught.** By our own procedure, turned on ourselves, at the moment the policy required —
after all nine areas were verified and before a single author was contacted. Not by a reader.

**Consequence.** Nine false or unsupported statements stand in the published v3, on Zenodo,
under a DOI. Five of them (a, c, d, f, g) are **completeness claims** — *every*, *none*, *all* —
which is the cheapest kind of sentence to write and the most expensive to satisfy. The
verifiers were told to be alert to exactly that construction, and it is where they found us.

**Correction.** Fixes are of two kinds, and the distinction matters. Where the claim was worth
keeping we made it *true* (generated the missing macros; wired the consistency checker into
`analyze.py` so it genuinely gates). Where it was not recoverable we made the text *accurate*
(the recomputation and confusion-matrix claims withdrawn, counts fixed, the abstract's
"every failure" sentence corrected to say plainly that one was found from outside).

**Why this matters for RQ4 — and it matters more than any other entry here.**

This is the paper's own thesis landing on the paper. We measured 490 papers and found that
described methods are 2.4× more locatable than reported numbers, and argued the field's
problem is not fabrication but *unpreserved provenance*. Then:

- our reliability study's **inputs were not preserved** (f) — the exact R0 failure we recorded
  against others, in the one study our headline reliability claims rest on;
- our numbers were **hand-transcribed in the section about our own rigour** (a);
- and the claim that we had not done so **was itself unchecked**, because the invariant checker
  we wrote after error #10 — whose lesson was recorded in this very file as *"state your
  invariants and check them by script"* — was never wired to anything (g).

We wrote the rule, we wrote the checker, and we did not connect them. Error #10's lesson was
learned in prose and not in code, which is precisely the distinction this paper exists to draw.

Two further observations belong in the paper, not just the log:

1. **Our worst defects cluster in the reflexive section** — the part describing our own
   process. The section arguing that process auditability is more fundamental than results is
   the least auditable section we wrote. That is not irony; it is evidence for the mechanism.
   Prose about method is unconstrained by the pipeline that produces the results, so nothing
   catches it. The same is true of every methods section we verified in 490 other papers.
2. **The 35% support rate is not comparable to the corpus figures and must never be quoted as
   though it were.** The verifiers here were adversarially prompted ("assume there are
   unsupported claims"), had the whole repository on local disk with `grep` and a shell, and
   were steered toward completeness claims. The area verifiers were calibrated the opposite way
   ("most claims will be SUPPORTED"), worked from a remote file listing, and sampled claims
   broadly. **The individual verdicts survive adjudication; the rate is an artifact of the
   instrument.** Reporting 35% against the corpus's 56% would repeat error #14 — a number
   carrying more weight than its construction supports — in the correction for error #14.

The honest summary is not "we scored badly." It is: **when we pointed our own instrument at
ourselves, it worked, and what it found was us.**

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

## #14 — 2026-07-31 — Paper v2 — Headline claim stated more strongly than n supports

**Description.** Version 2 claimed that papers making discovery claims "expose their process
worse" than the corpus: auditability 36% vs 45%, code release 55% vs 61%. At $n=58$ the 95%
Wilson intervals are 25--49% and 42--67%, **both of which contain the corpus rate**. The
comparison does not support a difference. The validation half of the dissociation is
unaffected and remains large (real-world validation 50% vs 11%, interval 38--62%).

**How caught.** An external reader's critique of the published v2, not by us. This is the
first substantive error in the project found from outside.

**Consequence.** A published paper asserted a difference its own data did not support, in the
direction that made its story sharper. Corrected in v3: the claim is now "audits no better",
intervals are reported throughout, and a sensitivity analysis was added.

**Why this matters for RQ4.** The paper's central charge against the literature is that
evidence is not matched to the strength of the claim it is asked to carry. We committed
exactly that error, in our own headline, while the machinery for catching it — the released
per-paper data — was sitting in the repository the whole time. Nothing in our process computed
an interval, because nothing required one. That is the same shape as failure #10: a rule we
believed in, never enforced by anything mechanical. The general lesson holds a third time —
**a standard that is not implemented as a check is not a standard, it is an intention.**

Note also what did work: the error was findable *because* the data was released. A reader
could recompute and did.

## #13 — 2026-07-31 — Paper — Our citation verifier silently dropped the last field of
## every bibliography entry

**Description.** `code/verify_bib.py` — the script whose entire purpose is to guarantee no
unverified citation reaches the paper — parsed fields with a pattern requiring a trailing
newline. The final field of a BibTeX entry is followed directly by the closing brace, so
**every entry's last field was silently discarded**. The defect was invisible for 17 entries
because the fields it checks (`eprint`, `doi`) happened never to be last. It surfaced only
when a newly added reference put `doi` last, which the verifier then reported as
"unverifiable — no eprint or doi field".

**How caught.** By the verifier failing loudly on a citation known to be correct, which is
the good failure mode. Had the new entry been ordered differently, the bug would still be
latent.

**Consequence.** None to published output: no citation was wrongly passed, and all 18 now
verify at exact title match. But the guarantee the script provided was weaker than believed
for the whole project.

**Why this matters for RQ4.** A verification tool with a silent data-dropping bug provides
false assurance, which is worse than no tool, because it stops anyone looking. This is the
fourth instance in the project of silent truncation (see #3, #5, #11) and the first inside a
*checker* rather than a producer. The pattern is now unambiguous enough to state as a rule:
**anything that parses or transfers data must be tested with an input where the failure would
be visible.** A checker that has never failed has not been shown to work.

## #12 — 2026-07-26 — Phase R — Our extractor truncated URLs, inflating a headline rate
## against other people's papers

**Description.** The repository-URL regex ran over PDF-extracted text, in which long URLs are
broken across lines. It therefore captured truncated repository names — `SimpleDeepSear` for
`SimpleDeepSearcher`, `NeuralSymbolicRegressionThatS` for
`NeuralSymbolicRegressionThatScales`, `diffus` for `diffusion` — and did not strip a trailing
`.git`. Those URLs 404, so **17 working repositories were counted as dead links belonging to
other researchers' papers.** The reported rate was 8.3% when the measured rate was 6.2%.

**How caught.** Not by the rate looking wrong — 8.3% was entirely plausible. It was caught by
asking *why* the links were dead rather than only how many: diagnosing owner-account existence
and near-name matches under the same owner surfaced a pattern of names that were prefixes of
real repositories, which is a signature of truncation rather than of author error.

**Consequence.** A published-facing statistic about other people's work was overstated by a
third, in the direction unfavourable to them. Corrected before any area paper was written:
URL dead rate 8.3% → **6.2%**; papers with no resolvable repository 9.4% → **8.1%**. All 17
repairs are recorded in `data/phase-r-url-repairs.csv` with the reason for each.

**Correction.** A conservative repair rule (repair only when the cited name is a prefix of a
real repository under the same owner, or differs only by `.git`), applied mechanically and
logged per URL rather than applied silently.

**Why this matters for RQ4.** This is the first error in the project whose cost would have
fallen on **third parties**: a measurement error in our tooling, presented as a finding about
other researchers' rigour. It is also the error most likely to have survived review, because
the number was plausible, the method was described accurately, and nothing about the output
looked wrong. The general point for a verification programme: **before reporting that someone
else's artifact is missing, establish why it is missing.** An aggregate failure rate computed
without mechanism analysis will silently include your own defects and attribute them to the
people you are measuring. The naming policy's requirement that every `NOT_LOCATED` verdict
record the specific search performed exists for exactly this reason, and this episode is why
it is not optional.

## #11 — 2026-07-26 — Phase R — Shell pipeline silently truncated a sweep, exit code 0

**Description.** The repository-availability sweep was launched as
`python ... | Tee-Object -FilePath log | Select-Object -First 3`. PowerShell's
`Select-Object -First N` terminates the pipeline once it has N objects, which killed the
Python process after roughly 100 of 982 URLs. The command reported **exit code 0**.

**How caught.** The summary showed 100 URLs checked where ~982 were expected, and the log
ended mid-progress at "50/982" with no error.

**Consequence.** None: the script is resumable and was re-run. But the run would have been
reported as a completed 982-URL sweep on the basis of a clean exit status.

**Why this matters for RQ4.** This is the third instance in this project of **work reported
as successful that did not happen** (see #2, #7), and the first caused by the AI's own
tooling rather than by an agent or a remote service. The pattern is now well enough
evidenced to state as a rule: in an automated research pipeline, *exit status is not
evidence of completion*. Only comparing produced output against expected output is. Every
one of these was caught by that comparison and by nothing else.

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
