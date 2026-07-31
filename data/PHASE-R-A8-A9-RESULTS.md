# Phase R — Areas 8 and 9, and the cross-area pattern at four areas

Cycle 1 (Linear SOFTWR-205). Two areas verified together:

- **A8 scholarly record** (24 papers) — systems that consume and evaluate the scholarly
  record: automated literature review, survey generation, automated peer review, novelty
  assessment. 168 claims.
- **A9 research infrastructure** (16 papers) — tooling that supports research without
  performing a stage: protocol representation, scientific coding agents, retrosynthesis
  planners, proof assistants, figure generation. 111 claims.

Ledgers: `data/phase-r-ledger-A8_scholarly_record.csv`,
`data/phase-r-ledger-A9_research_infrastructure.csv`.

---

## A8 scholarly record

| verdict | share | | claim type | n | supported | not located |
|---|---|---|---|---|---|---|
| `SUPPORTED` | 44.6% | | ARTIFACT_RELEASE | 25 | 72% | 8% |
| `UNVERIFIABLE` | 28.0% | | METHOD_COMPONENT | 64 | 61% | 5% |
| `NOT_LOCATED` | 14.3% | | DATASET | 24 | 42% | 17% |
| `DIVERGENT` | 13.1% | | NUMERIC_RESULT | 37 | **22%** | **38%** |
| `CONTRADICTED` | 0 | | EXTERNAL_VALIDATION | 18 | 0% | 6% |

External validation at 0% supported is expected rather than alarming: these systems are
evaluated by human judges or by correlation with human reviewer scores, and neither is the
kind of thing a code repository can evidence. Those claims are overwhelmingly `UNVERIFIABLE`.

## A9 research infrastructure

| verdict | share | | claim type | n | supported | not located |
|---|---|---|---|---|---|---|
| `SUPPORTED` | 49.5% | | METHOD_COMPONENT | 44 | 68% | 5% |
| `UNVERIFIABLE` | 23.4% | | ARTIFACT_RELEASE | 18 | 67% | 0% |
| `NOT_LOCATED` | 14.4% | | DATASET | 11 | 36% | 18% |
| `DIVERGENT` | 12.6% | | NUMERIC_RESULT | 28 | **25%** | **43%** |
| `CONTRADICTED` | 0 | | EXTERNAL_VALIDATION | 10 | 20% | 0% |

---

## The pattern now holds across four independent areas

121 papers, 886 claims, four areas that share no papers and differ in subject matter, all
verified with the same pipeline and the same evidence requirement.

| area | method component supported | numeric result supported | ratio |
|---|---|---|---|
| A1 discovery | 62% (n=60) | 36% (n=103) | 1.7× |
| A2 auditability | 53% (n=58) | 33% (n=51) | 1.6× |
| A8 scholarly record | 61% (n=64) | 22% (n=37) | 2.8× |
| A9 research infrastructure | 68% (n=44) | 25% (n=28) | 2.7× |
| **pooled** | **61% (n=226)** | **32% (n=219)** | **1.9×** |

**A described method is roughly twice as likely to be locatable in a paper's own repository
as a reported number.** The direction is identical in all four areas; only the magnitude
varies. This is no longer a property of one subfield.

What happens to the numbers that are not supported:

| area | supported | divergent | not located | unverifiable |
|---|---|---|---|---|
| A1 | 36% | 10% | 29% | 25% |
| A2 | 33% | 4% | 31% | 31% |
| A8 | 22% | 14% | 38% | 27% |
| A9 | 25% | 7% | 43% | 25% |
| **pooled** | **32%** | **9%** | **33%** | **27%** |

A third of all reported numeric results could not be located in the artifact that is supposed
to contain them, and a further 9% diverge from it.

## Pooled, by claim type

| claim type | n | supported | divergent | not located | unverifiable |
|---|---|---|---|---|---|
| ARTIFACT_RELEASE | 129 | 67% | 10% | 7% | 15% |
| MECHANISM_IMPLEMENTED | 117 | 62% | 7% | 6% | 26% |
| METHOD_COMPONENT | 226 | 61% | 18% | 8% | 13% |
| DATASET | 88 | 44% | 10% | 23% | 23% |
| SELF_APPLICATION | 49 | 43% | 18% | 22% | 16% |
| **NUMERIC_RESULT** | **219** | **32%** | **9%** | **33%** | **27%** |
| EXTERNAL_VALIDATION | 58 | 12% | 5% | 17% | 66% |

The ordering is stable and interpretable. Claims about *what exists* — released artifacts,
implemented mechanisms, described components — are well supported. Claims about *what was
measured* are not. Claims about *what happened in the world* are mostly outside what a
repository can settle, and are marked as such rather than counted against the paper.

## Verification depth

`R2` (file contents inspected) on **81%** of claims; `R1` 11%; `R0` 8%. No code was executed
anywhere in the programme so far, and every claim records the level actually reached.

## Interpretation, stated carefully

This does not establish that any reported number was invented. The likeliest explanation for
a missing result remains mundane: repositories hold code far more often than they hold
outputs, logs, or the scripts that turn one into the other.

What it does establish, now across four areas: **the quantities on which this literature's
claims rest are the part a reader is least able to check, and they are markedly less
checkable than the machinery that produced them.** Five areas remain, and each is an
opportunity for the pattern to break.
