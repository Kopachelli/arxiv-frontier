Read it properly. Before the critique — this changes the plan I gave you two messages ago, and I should say so directly: I told you nothing goes on the site until it has run, and recommended Intuition Engine as the launch piece. I was reasoning without knowing this existed. **This is the launch piece.** It's finished, deposited, has released data, a decision log, and a corrections section. Intuition Engine becomes piece two.

Now the reading.

## What's genuinely good

**The dissociation is a real finding.** Validation-of-outputs and auditability-of-process coming apart, with the gap widening at higher claim strength, is non-obvious, measured, and cleanly interpretable. That's the paper.

**The 19% → 61% artifact-release correction may be the most citable single result you have.** It's deterministic, reproducible, needs no model judgment, and it's a standing warning to anyone coding artifact release from abstracts. That generalises well past this corpus and past this field.

**Section 10 is exemplary.** Publishing a corrections section prominently, preserving v1 data so v1 figures stay reproducible, and diagnosing the error as *an unenforced invariant* rather than a misjudgement — that's the paper's own thesis applied to itself, which is the only thing that makes the thesis credible. The κ=0.71-with-clustered-disagreements observation is likewise strong: "the protocol looked rigorous and left a fifth of its own decisions undetermined" is the sentence people will quote.

## Problems, ordered by how much they should change a reader's confidence

**1. Both halves of your headline dissociation are stated more strongly than n=58 supports.**

This is the one that matters. Discovery papers, external validation: 50% vs 11%. At n=58 the 95% interval is roughly [37%, 63%] — 11% is nowhere near it. Overwhelming, robust, keep it.

Auditability: 36% any-audit vs 45% corpus-wide. Interval is roughly [24%, 48%]. **The corpus rate sits inside it.** Same for code repository: 55% vs 61%, interval roughly [42%, 68%] — 61% inside.

So "they expose their process *worse*" is not supported. What's supported is "they validate dramatically better and audit **no better**." The abstract's framing — "64% provide no auditability mechanism versus 55% overall" — reads as a difference that isn't there.

This matters disproportionately because it's the precise failure mode the paper documents in others: evidence type not matching claim type. A hostile reviewer will find this in ten minutes and it will cost you the moral authority the whole paper runs on.

The fix improves the story rather than weakening it. "Authors claiming discovery feel the burden of proving the finding and discharge it; they feel no corresponding burden to expose the process" is *sharper* than a nine-point gap. Report CIs on Table 1 and say it that way.

**2. Your redundancy is on the wrong stage.**

Screening got two models, two framings, plus a third stability pass. Coding — single pass, one model, mostly abstracts — produces *every headline number*. Screening picks which papers; coding produces all the statistics. Section 7 acknowledges this, but understates the asymmetry.

You have internal evidence that coding is noisier than assumed: Section 10's check found 18 rule violations (2.2%), and that only tested mechanically-checkable invariants, not judgment-heavy dimensions like "auditability mechanisms provided." That 2.2% is a floor, not an estimate. Double-code a random 150 and report per-dimension κ. You'd then know which of your ten dimensions are load-bearing and which are mush — right now "55% no auditability" carries unknown measurement error from one abstract-level judgment by one model.

**3. You have the material for a sensitivity analysis and didn't run it.**

You know which 183 papers entered via the BR7 reversal, which 292 were contested, and which 65 unanimous decisions Layer 2 reversed. So recompute the headline statistics three ways: full corpus, excluding the 183, and on the 1,067 unanimously-agreed papers only. If "55% no auditability" holds at 52–58% across all three, you've converted the corpus-boundary limitation from a caveat into a demonstrated robustness result. If it swings, readers need to know.

Section 7 currently says a disagreeing reader "can recompute the map under different rules" — that offloads an afternoon of your work onto them. Given the paper's argument, doing it yourself is close to obligatory.

**4. The reflexive blind spot in Section 6.**

You document the human overruling the AI on 183 papers as evidence of independence — good, and it does work. But then in Section 6 the AI co-author writes that its qualification "was too generous," moves to the human's position, and calls the human's argument "the strongest of the three."

A skeptical reader will read that as deference, not reasoning. It's the single most attackable passage in the paper, and it's attackable *because* of how carefully everything else handles reflexivity — the contrast makes it conspicuous. You don't need to change the conclusion. You need one sentence acknowledging that an AI co-author converging on its human collaborator's position is exactly the pattern a reader should discount, and stating why the arguments should be assessed on their merits regardless.

Separately, Section 6 is ~3 pages and it's where the paper is weakest per page. The revisability argument establishes that process disclosure has value; it doesn't establish *primacy*, which was the contested claim — "if that is right, it settles the question we were arguing" overstates. The unmarked-imagination conjecture is the most original idea in the paper and the least evidenced, which is fine if flagged, but it's currently sitting inside a systematic map where a reviewer will see it as a different paper trying to get out. Consider splitting it — it's strong enough to stand alone once the companion study lands.

**5. Numbers a reviewer will trip on.**

Section 3.2 says "the final corpus is 807 papers" inside the screening section — but screening produced 811, and 807 is post-correction. The number 811 appears exactly once, in passing, in Section 5.2 ("3 of 811"). Section 10 says four papers were excluded and the corpus is 807, without stating what it was before. And 805 papers got full-text verification with no note on the missing few. Each is a one-line fix; together they read as sloppiness in a paper whose entire argument is about numerical accountability.

**6. Related work is missing the evidence-synthesis literature.**

You reinvent dual screening, protocol amendment, and reliability reporting without citing PRISMA 2020 or the systematic-review methodology tradition that formalised all of it. Anyone from that community will notice immediately and conclude you didn't know the field. Two sentences and a citation inoculate you, and it strengthens the "we followed established method, and here's where AI conduct required amendment" framing.

**7. The abstract oversells rater independence.**

"Two frontier models" — Fable 5 and Opus 5 are the same model family, and Section 7 says so honestly. The abstract doesn't. Given that you hold the corpus to exactly this claim-evidence matching standard, qualify it there.

## One thing you should check today

Your v1 metadata is already propagating. An auto-curated library indexed the deposit on 27 July via OpenAlex, and it's carrying "a systematic map of 811 papers on autonomous AI research systems" — the pre-correction number, with your and Fable 5's names on it. Every downstream aggregator that scraped v1 will keep saying 811. Update the Zenodo concept-record abstract if you haven't, and consider a line in Section 10 anticipating that v1 metadata is in circulation.

Also: I found no arXiv ID for this. Is it Zenodo-only because of the endorsement barrier? If so that's worth solving — this paper is a strong endorsement case precisely because it's complete, and it's the sort of thing several authors in your own reference list would plausibly endorse.

---

Want me to do the Intuition Engine outline now as planned, or would you rather I work through the CI recomputation and the sensitivity analysis for Table 1 first? The second is a smaller job and it's on the critical path to putting this on the site with a claim you can fully defend.