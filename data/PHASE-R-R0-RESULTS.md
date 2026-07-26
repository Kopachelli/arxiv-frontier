# Phase R — R0 and R1 results (availability and artifact archetype)

Mechanical measurements over the 490 repo-bearing papers in the corrected (v2) corpus.
No model judgement is involved in any number on this page: every figure comes from host APIs
and file listings, and is reproducible from the released scripts.

---

## R0 — does the linked repository exist?

| | |
|---|---|
| repository URLs checked | 982 (812 GitHub · 155 Hugging Face · 15 other) |
| GitHub URLs resolving | 745 |
| **GitHub URLs dead (corrected)** | **50 / 812 = 6.2%** |
| papers with ≥1 resolvable repository | 451 / 491 = 91.9% |
| **papers where no linked repository resolves** | **40 / 491 = 8.1%** |
| live repositories that are empty | 3 |
| archived | 11 |

**A correction to our own measurement.** The uncorrected figures were 8.3% and 9.4%. Seventeen
"dead" links were an artifact of our extractor: PDF text extraction breaks long URLs across
lines, so the regex captured prefixes of real repository names, and a trailing `.git` was not
stripped. Those seventeen working repositories had been counted as other researchers' dead
links. Repairs are listed individually in `data/phase-r-url-repairs.csv`; the incident is
`process-log/errors.md` #12.

## Why the dead links are dead

A 404 is returned both for a deleted repository and for one that never existed. Two checks
separate the cases:

- **Owner accounts: 67 of 67 dead links (100%) have a live owner account.** No dead link is
  explained by a deleted or fictitious account.
- **Renames are excluded**: the GitHub API follows rename redirects, so a renamed repository
  would have returned 200.

What remains for the 50 genuinely dead links is that the owner is real and the specific
repository is absent — never created, or made private after publication. From a reader's
position those are the same failure.

## The temporal signal points the wrong way for link rot

| cohort | papers | dead-link rate | `FULL_PIPELINE` share |
|---|---|---|---|
| 2024-H1 | 13 | 0.0% | 69.2% |
| 2024-H2 | 24 | 20.8% | 66.7% |
| 2025-H1 | 61 | 8.2% | 63.9% |
| 2025-H2 | 120 | 6.7% | 65.8% |
| 2026-H1 | 250 | 15.6% | 62.0% |
| 2026-H2 | 22 (July only) | 27.3% | 63.6% |

*(rates before URL repair; the repaired series is recomputed in the trend paper)*

Link rot predicts that **older** papers suffer most: repositories are deleted, accounts lapse,
projects are abandoned. The observed pattern is the opposite — the oldest cohort has the
lowest dead rate and the recent cohorts the highest — and no dead link is explained by a lost
account. The hypothesis this supports, to be tested rather than asserted in the trend paper,
is that recent papers increasingly cite repositories that **do not exist yet at publication**.

Meanwhile the completeness of repositories that *do* exist is close to flat (69% → 64%
`FULL_PIPELINE`). If that holds under the repaired series, the finding is a specific one:
this field is not getting sloppier about what it puts in a repository; it is getting worse at
making the repository exist at all.

## R1 — artifact archetype (dimension E, the method router)

| archetype | n | share | verification track |
|---|---|---|---|
| `FULL_PIPELINE` (code + data + config) | 312 | 63.7% | R0→R3, execution attempted |
| `CODE_ONLY` | 89 | 18.2% | R0→R2 + dependency audit |
| `DEAD` | 63 | 12.9% | R0 only, `UNVERIFIABLE` |
| `STUB` (README/placeholder only) | 16 | 3.3% | R0→R1 |
| `DEMO_APP` | 7 | 1.4% | R0→R2, feature presence |
| `DATA_ONLY` | 3 | 0.6% | R0→R2 against reported numbers |

Nearly two thirds of repositories carry code, data and a configuration or environment file
together — the combination that makes an execution attempt meaningful. That is a considerably
better baseline than the abstract-level reading in Paper 1 suggested, and it means the
expensive R3 track is worth building.

## Areas (partition A), with archetype

| area | n | `FULL_PIPELINE` | `DEAD` |
|---|---|---|---|
| A1 discovery | 32 | 21 | 2 |
| A2 auditability | 49 | 28 | 7 |
| A3 end-to-end | 86 | 64 | 7 |
| A4 self-driving lab | 10 | 6 | 0 |
| A5 benchmark | 132 | 80 | 23 |
| A6 deep research | 82 | 54 | 8 |
| A7 ideation | 51 | 32 | 9 |
| A8 biomedical | 8 | 3 | 2 |
| A9 other | 40 | 24 | 5 |

Two areas are too small to carry a paper (A4 = 10, A8 = 8) and A9 is a residual rather than a
defined area. Both need a decision before area work proceeds; see the note in
`notes/phase-r-partition-options.md`.
