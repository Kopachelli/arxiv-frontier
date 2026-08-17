# Divergence rates measure checkability, not carelessness

A note for the cross-cutting papers, written when A5 completed (cycle 4). It records a
confound that will otherwise be re-derived — or worse, missed — when the area papers are
drafted.

## The trap

A5 benchmark has the programme's highest `DIVERGENT` rate: 11.4% of all claims, 16% of dataset
claims. The obvious reading is that benchmark papers are the least accurate in the corpus.

That reading is backwards.

**A divergence requires a located artifact.** To record that a paper says 268 and the files
hold 255, you must first find the files and count them. Where nothing is released, no
mismatch can be recorded — the verdict is `NOT_LOCATED`, and the paper's numbers pass through
the review unchallenged.

So `DIVERGENT` is conditional on release. A5 has the highest divergence rate because it has
the highest release rate (74% dataset support against a previous best of 52%). The areas that
release least look cleanest on this metric, purely because there was nothing to check.

## The correction reverses the ranking

Computed both ways over all eight areas (2,843 claims), where *located* means the artifact was
found and assessed — `SUPPORTED` + `DIVERGENT` + `CONTRADICTED`:

| area | divergence / all claims | divergence / located claims | located n |
|---|---|---|---|
| A6 deep research | 8.4% | **12.7%** | 363 |
| A7 ideation | 8.7% | 16.9% | 136 |
| A4 physical & life sciences | 9.6% | 15.2% | 217 |
| A2 auditability | 10.8% | 16.8% | 226 |
| **A5 benchmark** | **11.4%** (2nd highest) | **14.5%** (2nd lowest) | 636 |
| A1 discovery | 11.0% | 19.6% | 143 |
| A9 research infrastructure | 12.6% | 20.3% | 69 |
| A8 scholarly record | 13.1% (highest) | 22.7% (highest) | 97 |
| **pooled** | **10.4%** | **15.7%** | 1,887 |

A5 moves from second-worst to second-best, and sits below the pooled rate on the corrected
metric while sitting above it on the raw one. Same ledger, opposite conclusion. A1 discovery
moves the other way, from middling to fourth-worst.

The two metrics are only weakly related (A8 is worst on both; A5 and A1 swap ends), which is
what makes the raw figure actively misleading rather than merely noisy: a reader cannot mentally
correct for it, because the correction is not monotone.

## Why it matters for the area papers

Any table that ranks areas by divergence rate ranks them, in part, by how auditable they are.
Presented without this caveat it would reward opacity — the exact inversion the programme
exists to expose. It is also the same failure the review charges the literature with: a number
whose evidential meaning does not match the claim it is asked to carry.

**Rule for the area papers and the synthesis:** report divergence as a share of *located*
claims, not of all claims, and state the denominator. A divergence rate over all claims is a
composite of two different things — how much a field releases, and how well what it releases
matches what it says. Only the second is what the reader thinks they are being told.

## The same structure appears elsewhere

- `CONTRADICTED` is conditional on release for the same reason, and more sharply: one
  contradiction in 805 A5 claims, zero in most areas, and the areas with zero are not thereby
  vindicated.
- `NOT_LOCATED` versus `UNVERIFIABLE` is the distinction we already draw carefully (A4's
  numbers are absent though recordable; A7's are unrecordable in principle). This is the same
  discipline applied one level up: **before comparing a rate across areas, ask what had to be
  true for that rate to be nonzero at all.**

## Open question for the trend paper

If divergence is conditional on release, then a field that improves its release practices will
show a *rising* divergence rate while getting better, not worse. Whether that shows in the
2024–2026 time series is testable with the data we now hold, and would be a clean result: an
apparent decline in accuracy that is actually an increase in auditability.

Related: [[unmarked-hypothesis]].
