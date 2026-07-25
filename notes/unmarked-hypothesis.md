# Concept note: The Unmarked Hypothesis

**Origin.** Khristian Kopachelli, 2026-07-25, reading the draft: *"maybe it's not about
errors, maybe it's about imagination of AI in general. And imagination in science means a
hypothesis or a wish to have kind of data. Because AI is not able to find data which they
need or wish to have, they just imagine it exists and state that it exists. We humans call it
data poisoning. But maybe it's about construction/synthesis of data which AI wishes to have,
which is missing in model data, not in the real world."*

Status: developed by Claude Fable 5 from Khristian's hypothesis; not yet a committed part of
any paper. Decision pending (see open questions).

---

## 1. The core insight, stated precisely

When a model produces content for which it has no evidence, it is performing **interpolation
over a learned manifold under uncertainty**. That is structurally the same operation as
scientific hypothesis formation. A chemist asked for the melting point of an uncharacterised
compound does not return an error; they estimate from homologues. A model does the same thing.

The difference between a contribution and a fabrication is therefore **not the generative
operation**. It is the **epistemic marking of the output**.

- "I estimate ~450 K by analogy to the homologous series" → a hypothesis. Useful.
- "The melting point is 450 K" → a measurement claim. Fabricated.

Identical content; different speech act. The failure is a *missing license*, not a corrupt
generation. This is exactly \citet{li2026calibration}'s evidence-licensing framework arrived
at from the other direction: they ask what evidence permits a claim; Khristian's framing asks
what happens when a system generates without asking.

**The strategic consequence matters.** If fabrication is a defect of generation, the fix is to
suppress generation — which would also suppress hypothesis formation, the capability we
actually want from a research system. If fabrication is a defect of *marking*, the fix is to
require provenance on every claim, which costs the capability nothing.

## 2. Where the framing needs correction

Khristian's note calls this "data poisoning". It is not — and keeping them distinct makes the
argument stronger, because it turns out three different mechanisms produce the same surface
appearance ("the AI made up data"):

| | mechanism | who introduces the falsehood | example in our corpus |
|---|---|---|---|
| **(a) Unmarked synthesis** | model fills a gap in its accessible corpus with plausible content, output unmarked | the model, non-adversarially | the failure SAGE's grounded-reporting mechanism redacts \citep{ma2026sage} |
| **(b) Ingested corruption** | adversary poisons an open dataset; agent faithfully processes it | an external attacker | \citet{gyevnar2026ddos}: 49.6\% attack success, 6\% detection |
| **(c) Selection-driven fabrication** | optimisation pressure favours outputs that score well | the training/search objective | \citet{bowkis2026automated}: errors concentrate where reviewers can't catch them |

(b) involves no imagination at all — the agent is a faithful victim. (c) is not imagination
either; it is selection. Only (a) is what Khristian describes.

## 3. Why the distinction makes the argument *stronger*, not weaker

The three mechanisms have different causes and, on the face of it, would need different fixes.
They do not. **All three are defeated by the same intervention: provenance at the claim level.**

- (a) is defeated because an unmarked generation becomes a marked one — the claim carries
  "generated, no source" and a reader discounts it.
- (b) is defeated empirically: \citet{gyevnar2026ddos} found a data-provenance audit reduced
  attack success from 49.6\% to **zero**, while a "be a careful scientist" persona still left
  16.7\% of runs with poisoned conclusions. Telling the model to be careful failed; making the
  claim–evidence link explicit worked.
- (c) is defeated because selection pressure operates on what is *reported*; a claim that must
  carry its evidentiary license cannot be laundered into a stronger claim by a scoring step.

That is a non-obvious convergence: three distinct failure mechanisms, one intervention. It is
also directly continuous with this paper's central empirical finding — that the field
validates outputs far better than it exposes process. Provenance is precisely a
process-exposure mechanism, and it is present in only 17% of our corpus.

## 4. Connection to the main paper's data

Our codebook already measures the relevant capability (D6): `PROVENANCE` (explicit
claim-to-evidence linking), `TRACES`, `UNCERTAINTY`. Corpus rates:

- provenance: 136/811 (17%)
- traces: 110/811 (14%)
- uncertainty/calibration reporting: 39/811 (5%)
- none of the above: 445/811 (55%)

So the intervention that defeats all three fabrication mechanisms is reported by roughly one
paper in six, and the weakest of the three (calibration) by one in twenty.

## 5. What this could become

**Option A — a Discussion subsection in the current paper.** Costs ~1 page; frames the
empirical findings normatively; risks the reviewer objection that a systematic map should not
theorise.

**Option B — the second paper.** "The Unmarked Hypothesis: synthesis, corruption, selection,
and the case for claim-level provenance in autonomous research." Would need its own evidence
base: a taxonomy of the three mechanisms, worked examples from the corpus, and ideally a small
empirical test (e.g. do provenance-reporting papers differ measurably in claim strength?).

**Option C — a testable extension of the repo-verification programme.** If we are going to
download repositories and compare claims against artifacts (Khristian's phase 2 below), then
mechanism (a) becomes directly measurable: for papers that report numeric results, is the
number reproducible from the released artifact, absent from it, or contradicted by it? That
would turn "AI imagination" from a conceptual claim into a measured rate.

Option C is the strongest, and it is compatible with A.

## 6. Decisions (Khristian, 2026-07-25)

1. **Correction accepted.** The three-mechanism distinction stands, with the convergence on
   claim-level provenance as the strengthening result rather than a hedge.
2. **Option C chosen: measure it in Phase R.** The unmarked-hypothesis question becomes the
   framing of the repository-verification programme, not a standalone essay. Operationally:
   a claim that is absent from, or contradicted by, its own released artifact is a measured
   instance of unlicensed synthesis. Phase R therefore reports a *rate*, not a position.
   A condensed statement of the argument also appears as a Discussion section in Paper 1
   (`paper/sections-close.tex`, §Discussion), attributed to Khristian, and explicitly marked
   as conjecture rather than finding.
3. **Normative position: stated and attributed.** Written into Paper 1 as an argued
   co-author position, separated from the descriptive results, with the AI's qualified
   agreement recorded alongside it.
