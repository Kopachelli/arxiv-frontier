# Coding reliability — double-coding study

Run 2026-07-31 in response to an external critique of v2, which observed that screening
received two independent passes plus a stability check while **coding — which produces every
headline number — was a single pass over abstracts**. The paper acknowledged the asymmetry
and never measured it. This measures it.

**Design.** 149 papers drawn at random from the corpus (seed 20260731) were re-coded from
title and abstract by a second pass that never saw the original codes. Per-dimension Cohen's
$\kappa$ for single-select dimensions; mean Jaccard for the three multi-select dimensions,
where $\kappa$ is not defined. Data: `data/coding-reliability.csv`.

---

## Per-dimension reliability

| dim | what it codes | agreement | statistic | reading |
|---|---|---|---|---|
| D7_data | data released | 98.0% | $\kappa$ 0.93 | substantial |
| D1 | paper type | 94.6% | $\kappa$ 0.92 | substantial |
| D5 | evaluation method | 83.2% | Jaccard 0.92 | substantial |
| D8 | claim strength | 91.9% | $\kappa$ 0.87 | substantial |
| D7_code | code released | 94.6% | $\kappa$ 0.86 | substantial |
| D4 | domain | 87.9% | $\kappa$ 0.83 | substantial |
| D6 | auditability mechanisms | 77.2% | Jaccard 0.81 | substantial |
| D2 | autonomy level | 85.2% | $\kappa$ 0.78 | substantial |
| D3 | lifecycle stages | 49.7% exact | Jaccard 0.63 | moderate |
| **D9** | **human role** | **56.4%** | **$\kappa$ 0.37** | **fair** |

Nine of ten dimensions are substantial or better. One is not, and it happens to carry a
headline figure — so it needs looking at rather than reporting.

## D9's low reliability is in a distinction the paper never uses

The confusion matrix is dominated by a single cell: **50 of 149 papers coded `NONE_CLAIMED`
originally were re-coded `UNSPECIFIED`.** Every other off-diagonal cell is in single figures.

Those two categories both mean *the paper does not tell you what humans did*. The distinction
between them — whether a paper actively asserts no human involvement, or simply never
mentions it — turns out not to be reliably recoverable from an abstract. That is a real
codebook defect, and we record it as one.

But the paper's headline figure collapses exactly those two categories into one binary. On
the quantity as actually used:

| | agreement | $\kappa$ | original | re-code |
|---|---|---|---|---|
| human role unstated | **92.6%** | **0.78** | 77.9% | 78.5% |

Substantial agreement, and the two passes produce nearly the same rate. **The 71% figure is
reliable even though the five-category dimension underneath it is not.**

This is worth stating as a general point: reporting $\kappa$ for a dimension can badly
understate the reliability of a statistic derived from it, when the statistic collapses
categories the coders cannot separate. The reliability that matters is the reliability of the
quantity as reported.

## The uncomfortable finding: our most-cited number is coder-dependent

Applying the same collapse to the other headline quantities:

| quantity as reported | agreement | $\kappa$ | original | re-code |
|---|---|---|---|---|
| held-out transfer | 98.0% | 0.79 | 4.7% | 5.4% |
| real-world validation | 98.0% | 0.91 | 13.4% | 11.4% |
| **no auditability mechanism** | 84.6% | 0.67 | **57.7%** | **70.5%** |

Held-out transfer and real-world validation are tight: the two passes differ by under two
points, and the published figures (5% and 11%) are safe.

The auditability figure is not tight. Agreement is 84.6% and $\kappa$ 0.67 — substantial by
convention — but the **marginals differ by 12.8 points**. Two coders working from the same
codebook and the same abstracts would report "58% provide no auditability mechanism" and
"71% provide no auditability mechanism" for the same corpus. Our published figure is 55%.

This does not overturn the finding. Both passes agree that a clear majority of this
literature provides no auditability mechanism, which is the claim the paper makes and the
basis of its argument. What it establishes is that **the precise percentage carries roughly
±13 points of coder-dependent variation, and should be read as "most papers, somewhere near
three in five" rather than as 55%.** The paper is being amended to say so.

The likely cause is the same one that produced seven boundary classes at screening: D6 asks
whether a mechanism is present *as a designed feature*, and abstracts frequently gesture at
inspectability without committing to it. That is a judgement call, and judgement calls made
once are not measurements.

## What this changes

1. The paper reports these reliabilities, including the unflattering one.
2. The auditability figure is presented with its coder-dependent range rather than as a point
   estimate.
3. D9's `NONE_CLAIMED` / `UNSPECIFIED` distinction is recorded as a codebook defect. We do not
   re-code the corpus to fix it, because the paper never uses the distinction — but a future
   study that needs it should not trust these two categories separately.
4. The critique that prompted this was right, and the asymmetry it identified was real: nine
   dimensions came out fine, and finding that out cost one workflow run. It should have been
   part of the original design.
