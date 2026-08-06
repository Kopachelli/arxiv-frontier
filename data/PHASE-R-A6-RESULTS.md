# Phase R — Area 6 (deep research), and the pattern at seven areas

Cycle 3 (Linear SOFTWR-207). **A6 deep research**: 79 papers, 545 claims, 71 with a readable
repository tree. Agents performing multi-step information seeking, evidence synthesis and
report generation, plus the evaluation suites built for them.
Ledger: `data/phase-r-ledger-A6_deep_research.csv`.

This is the area Khristian Kopachelli's override brought into scope. In Paper 1 the AI
recommended excluding general-purpose deep-research agents as out of scope (boundary rule
BR7); the human overruled it, moving 183 papers into the corpus. Verifying the area closes
that loop, and the result bears on whether the override was right.

---

## The most extreme dissociation in the programme

| verdict | share |
|---|---|
| `SUPPORTED` | 58.2% |
| `NOT_LOCATED` | 18.5% |
| `UNVERIFIABLE` | 14.9% |
| `DIVERGENT` | 8.4% |
| `CONTRADICTED` | 0 |

| claim type | n | supported | not located |
|---|---|---|---|
| **ARTIFACT_RELEASE** | 103 | **82%** | 2% |
| **METHOD_COMPONENT** | 216 | **77%** | 7% |
| DATASET | 85 | 46% | 21% |
| EXTERNAL_VALIDATION | 20 | 35% | 10% |
| **NUMERIC_RESULT** | 121 | **17%** | **53%** |

Deep-research papers are simultaneously **the best in the corpus at shipping what they
describe and the worst at making their reported numbers locatable.** Both extremes are
records: 82% artifact-release support and 77% method-component support are the highest
figures we have measured anywhere, and 17% numeric support with 53% not located are the
lowest and highest respectively.

The gap matters because of what these numbers are. Deep-research papers report scores on
public benchmarks --- BrowseComp, GAIA, HLE, WideSearch, xbench-DS, DeepResearch Bench. These
are computed quantities, produced by running released code against a public dataset. Unlike a
wet-lab assay (A4) or a human novelty rating (A7), **there is no reason in principle why a
repository could not hold them**: a results file, an evaluation log, a set of generated
reports, a leaderboard entry. Verifiers were told explicitly to look for exactly those before
concluding anything. In 53% of cases they were not there.

So the area with the strongest engineering culture in the corpus has the weakest
result-provenance. The systems are real, the code is released, the components exist --- and
the numbers those systems produced mostly are not.

## On the override

The human's reversal admitted the most artifact-rich part of the corpus. Had it stood, the
review would have excluded the papers with the highest release rates we have measured, and
would have reported a field that looked *less* well-engineered than it is. It would also have
missed the sharpest instance of the programme's central finding. On both counts the override
was correct, and the AI's original recommendation would have produced a worse map.

## The pattern at seven areas

288 papers, 2,038 claims.

| area | method component | numeric result | ratio |
|---|---|---|---|
| A2 auditability | 53% (n=58) | 33% (n=51) | 1.6× |
| A1 discovery | 62% (n=60) | 36% (n=103) | 1.7× |
| A4 physical & life sciences | 71% (n=120) | 29% (n=84) | 2.5× |
| A9 research infrastructure | 68% (n=44) | 25% (n=28) | 2.7× |
| A8 scholarly record | 61% (n=64) | 22% (n=37) | 2.8× |
| A7 ideation | 65% (n=92) | 15% (n=61) | 4.4× |
| **A6 deep research** | **77% (n=216)** | **17% (n=121)** | **4.7×** |
| **pooled** | **69% (n=654)** | **25% (n=485)** | **2.7×** |

**Seven areas, same direction, no exceptions.** The ratio ranges 1.6× to 4.7×. Pooled, a
described method component is 2.7 times more likely to be locatable in a paper's own
repository than a reported number.

Pooled fate of the 485 numeric claims: 25% supported, 7% divergent, **42% not located**, 26%
unverifiable.

## Why this is not simply "repositories hold code, not outputs"

That explanation is true and insufficient. If it were the whole story, the not-located rate
would be roughly constant across areas, because all these repositories are code repositories.
It is not: 29% in discovery, 53% in deep research. The variation tracks something else ---
plausibly how much of the reported number depends on a run that costs money to reproduce.
Deep-research evaluations involve thousands of live web queries and paid model calls, so the
result of a run is precisely the artifact most worth preserving and least likely to be
regenerable by a reader. That is a hypothesis this programme can test in the trend and
synthesis papers, not a conclusion.

## Limits

- 8 of 79 papers had no readable repository tree.
- Two subagents ran while the safety classifier was unavailable; their outputs were reviewed
  and show the same evidence discipline as the rest, with file paths on every positive verdict.
- Verification reflects repository state at retrieval. No code was executed; every claim
  records the level actually reached.
