# Phase R — Area 3 (end-to-end), and the completed pattern at nine areas

Cycle 5 (Linear SOFTWR-209). **A3 end-to-end**: 86 papers, 595 claims, 80 with a readable
repository tree. Systems claiming to carry out a complete research cycle — generate a
hypothesis, design and run an experiment, analyse the result, write it up — with little or no
human intervention. This area contains the field's best-known papers.
Ledger: `data/phase-r-ledger-A3_end_to_end.csv`.

**This area asks a question the others do not.** Elsewhere the test is whether a described
component exists. Here the claim is that *the loop closed* — that the system ran the whole way
through and produced research autonomously. Code that could in principle produce an output is
not the output, so verifiers were told plainly: a pipeline that exists is not a pipeline that
ran. Orchestration code, agent-role definitions and prompt templates are `METHOD_COMPONENT`
evidence. Evidence that the loop closed is the **residue of a run** — generated papers, run
directories, trajectories, hypothesis maps, result JSONs. Every paper required at least one
`SELF_APPLICATION` claim addressing this directly.

---

## Half of end-to-end systems evidence a completed run

| `SELF_APPLICATION` (n=98) | share |
|---|---|
| `SUPPORTED` — run residue found and cited | **51%** |
| `NOT_LOCATED` | 33% |
| `UNVERIFIABLE` | 14% |
| `DIVERGENT` | 2% |

This is the number the area existed to produce, and it deserves to be read in both directions.
**Half of the systems claiming autonomous research release the evidence that they performed
it** — not a description of a run, but its artefacts. Some of what verifiers found is
substantial:

- 24 complete submission directories, each with three files, in one repository's git tree
- a single 7.59 MB end-to-end trace, 161,663 lines, containing 272 `>>>[IdeaAgent]` and 362
  `>>>[CodeAgent]` turns
- a released run directory holding `IDEA.md` and a `.hypothesis_map.json` recording three
  hypotheses with outcomes, two of them **refuted**
- a 200-run trajectory dataset on Hugging Face with query, loop count, trajectory and report

A system that releases the trace of a run where its own hypotheses were refuted is doing
something the rest of this programme has been asking the field to do. That is worth stating as
plainly as any deficit.

The other half is a real gap, and the honest framing is that we could not locate the residue —
33% `NOT_LOCATED` on exactly the claim these papers are built on. Several READMEs state that
run outputs are generated at runtime and deliberately not committed, which is a legitimate
engineering choice with a real evidential cost.

## A3's numbers are the best-preserved in the corpus

| claim type | n | supported | not located |
|---|---|---|---|
| ARTIFACT_RELEASE | 89 | 78% | 2% |
| METHOD_COMPONENT | 194 | 74% | 6% |
| DATASET | 62 | 53% | 10% |
| NUMERIC_RESULT | 122 | **37%** | **25%** |
| SELF_APPLICATION | 98 | 51% | 33% |
| EXTERNAL_VALIDATION | 30 | 20% | 10% |

**25% not-located on numeric results is the lowest rate in the programme** — against a pooled
39%, and against 53% in deep research. The reason is structural and worth naming: a system that
releases the residue of its runs thereby releases the numbers those runs produced. Provenance
comes free with the trace. A3 did not set out to preserve its results better than other areas;
it preserved them as a side effect of releasing what it did.

That is a mechanism, not just a correlation, and it is the most actionable finding in this
cycle: **the cheapest route to result-provenance is to ship the run directory.**

## The pattern, complete: nine areas of nine

490 papers, 3,438 claims.

| area | method component | numeric result | ratio |
|---|---|---|---|
| A2 auditability | 53% (n=58) | 33% (n=51) | 1.6× |
| A1 discovery | 62% (n=60) | 36% (n=103) | 1.7× |
| **A3 end-to-end** | **74% (n=194)** | **37% (n=122)** | **2.0×** |
| A5 benchmark | 84% (n=205) | 40% (n=167) | 2.1× |
| A4 physical & life sciences | 71% (n=120) | 29% (n=84) | 2.5× |
| A9 research infrastructure | 68% (n=44) | 25% (n=28) | 2.7× |
| A8 scholarly record | 61% (n=64) | 22% (n=37) | 2.8× |
| A7 ideation | 65% (n=92) | 15% (n=61) | 4.4× |
| A6 deep research | 77% (n=216) | 17% (n=121) | 4.7× |
| **pooled** | **73% (n=1,053)** | **30% (n=774)** | **2.4×** |

**Nine areas. Same direction. No exceptions.** Ratios run 1.6× to 4.7×; pooled, a described
method component is 2.4 times more likely to be locatable in a paper's own repository than a
reported number. The corpus-wide fate of 774 numeric claims: 30% supported, 9% divergent, **39%
not located**, 21% unverifiable.

The two areas at the extremes now have an interpretable mechanism between them. A6 deep
research releases the most code and preserves the fewest numbers (4.7×); A3 releases run
residue and preserves the most (2.0×). The difference is not how much a field releases but
**what kind of thing it releases** — and only one kind carries results with it.

## Divergence, on the corrected denominator

A3 diverges on 10% of all claims and **15% of located claims** (n=410), against a pooled 16%.
As established when A5 completed, the raw rate is conditional on release and cannot be compared
across areas; see `notes/divergence-and-checkability.md`.

## The two CONTRADICTED verdicts

Seven contradictions in 3,438 claims across the whole programme; two are here. Both are
recorded because top-level released evidence conflicts with a stated claim, which is the bar
the protocol sets. Neither is a finding about any author's conduct — §6 of the naming policy
puts that expressly out of scope — and both authors will receive these findings with a right of
reply in cycle 6, before anything is published.

**arXiv:2411.11910 (Baby-AIGS).** Footnote 1 states "Code is released at
`github.com/AgentForceTeamOfficial/Baby-AIGS`". The repository resolves and is public; its
recursive git tree returns exactly three entries and its own README says "Please stay tuned for
code release!". This is the ordinary and entirely common case of a placeholder repository
created ahead of a release that did not follow.

**arXiv:2509.21553 (AutoClimDS).** The paper states: *"Data discovery and acquisition proceeded
via natural language instructions only: no datasets, numerical values, or coefficients are
provided."* The released prompt for the run its own README maps to the corresponding figure
(`case_studies/npcc_fig6_good/npcc_fig6_nasa.txt`) instructs the agent to "Adopt VLM = −1.5
mm/yr (subsidence)", supplies the conversion `s = (+1.5 / 304.8) ft/yr`, and states the
expected diagnostic `VLM slope check (~0.004921 ft/yr)`. The −1.5 mm/yr figure the paper
reports the system as recovering appears in the prompt as a given.

**This one was checked directly by the AI lead, not accepted from a subagent**, per the rule in
`errors.md` #12 that a negative finding must be established at source. The prompt file was
fetched and read in full.

The fairest counter-reading, which we state because the authors are entitled to it: the
sentence is scoped to *data discovery and acquisition*, and one could read "no numerical values
are provided" as meaning no *data* values — the agent did have to locate the NOAA sea-level
record itself, and the log shows that it did. On that reading the VLM figure is a modelling
parameter rather than data. We record `CONTRADICTED` nonetheless because the sentence lists
"coefficients" explicitly, and −1.5 mm/yr is supplied as one.

**Two things must be said alongside it.** First, this paper's other verdicts are strong: its
`SELF_APPLICATION` claim is `SUPPORTED` — ten completed run directories, the loop demonstrably
closed — and its central knowledge-graph dataset claim reproduces exactly (1,482,552 nodes and
5,815,623 edges against the paper's ~1.48M and ~5.8M). Second, and more important:
**this discrepancy is findable only because the authors released the prompt logs.** A paper
that shipped code without traces would have produced a `NOT_LOCATED` and passed through this
review unchallenged. The most transparent papers absorb the most scrutiny — the central
asymmetry recorded in `notes/divergence-and-checkability.md`, here in its sharpest form.

## Limits

- 86 papers, no sampling. 7 repositories dead and 3 stubs at retrieval; `UNVERIFIABLE` is the
  correct verdict for those and no findings were manufactured from empty trees.
- `SELF_APPLICATION` at 51% measures *whether run residue is locatable*, not whether the
  research it produced is good. A released trace is evidence a loop closed, not that it closed
  usefully.
- Autonomy claims were only marked `DIVERGENT` where the repository itself documents a required
  human step. A human in the loop was never inferred from absence of evidence.
- Verification reflects repository state at retrieval. No code was executed; 85% of verdicts
  across the programme reached R2 (contents inspected).
