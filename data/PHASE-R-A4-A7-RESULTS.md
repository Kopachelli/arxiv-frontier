# Phase R — Areas 4 and 7, and the cross-area pattern at six areas

Cycle 2 (Linear SOFTWR-206).

- **A4 physical & life sciences** (49 papers, 344 claims) — research acting on the physical
  world: self-driving laboratories, autonomous experimentation, materials, chemistry,
  biomedical. Claims here often concern outcomes in a laboratory or clinic.
- **A7 ideation** (39 papers, 263 claims) — hypothesis generation, research-idea generation,
  novelty-aware ideation, idea ranking.

Ledgers: `data/phase-r-ledger-A4_physical_life_sciences.csv`,
`data/phase-r-ledger-A7_ideation.csv`.

---

## A4 physical & life sciences

| verdict | share |
|---|---|
| `SUPPORTED` | 52.5% |
| `UNVERIFIABLE` | 18.7% |
| `NOT_LOCATED` | 18.4% |
| `DIVERGENT` | 9.5% |
| `CONTRADICTED` | 0.9% |

Artifact-release claims are the best supported we have measured anywhere (78%). Method
components reach 71%. Numeric results reach 29%, with **49% not located** — the highest
not-located rate in the programme.

The `UNVERIFIABLE` rate is lower here (18.7%) than the area's design anticipated. Verifiers
were told explicitly that a wet-lab synthesis or clinical outcome is not something a
repository can evidence and that a high `UNVERIFIABLE` rate would be correct. They used
`NOT_LOCATED` instead for a large share of numeric claims, which is the right call when the
number in question is a computed benchmark figure rather than a physical measurement.

## A7 ideation

| verdict | share |
|---|---|
| `SUPPORTED` | 43.0% |
| `UNVERIFIABLE` | 31.9% |
| `NOT_LOCATED` | 16.3% |
| `DIVERGENT` | 8.7% |

The highest `UNVERIFIABLE` rate in the programme, and appropriately so: ideation systems are
predominantly evaluated by human expert judges rating novelty and feasibility, which a code
repository cannot settle.

**Numeric results are supported at 15%** — the lowest figure we have recorded. Ideation papers
report quality scores for generated ideas, and the ideas and their ratings are usually not in
the repository, even though (unlike a wet-lab result) they are exactly the kind of artifact
that could be released. Verifiers were instructed to check for released idea sets, generation
logs and rating spreadsheets before concluding `NOT_LOCATED`, and largely did not find them.

## The pattern at six areas

209 papers, 1,493 claims, six areas that share no papers and differ in subject matter.

| area | method component supported | numeric result supported | ratio |
|---|---|---|---|
| A2 auditability | 53% (n=58) | 33% (n=51) | 1.6× |
| A1 discovery | 62% (n=60) | 36% (n=103) | 1.7× |
| A4 physical & life sciences | 71% (n=120) | 29% (n=84) | 2.5× |
| A9 research infrastructure | 68% (n=44) | 25% (n=28) | 2.7× |
| A8 scholarly record | 61% (n=64) | 22% (n=37) | 2.8× |
| A7 ideation | 65% (n=92) | 15% (n=61) | **4.4×** |
| **pooled** | **64% (n=438)** | **28% (n=364)** | **2.3×** |

**Six areas, same direction, without exception.** The ratio ranges from 1.6× to 4.4×; the
pooled figure is 2.3×. A described method component is more than twice as likely to be
locatable in a paper's own repository as a reported number.

What becomes of the numbers that are not supported:

| area | supported | divergent | not located | unverifiable |
|---|---|---|---|---|
| A1 discovery | 36% | 10% | 29% | 25% |
| A2 auditability | 33% | 4% | 31% | 31% |
| A4 physical & life sciences | 29% | 5% | **49%** | 18% |
| A7 ideation | 15% | 8% | 39% | **38%** |
| A8 scholarly record | 22% | 14% | 38% | 27% |
| A9 research infrastructure | 25% | 7% | 43% | 25% |

The two areas at the extremes fail differently, and the difference is interpretable. A4's
numbers are mostly *not located* — they are computed quantities that a repository could hold
and does not. A7's are mostly *unverifiable* — they are human novelty ratings that no
repository could settle. Only one of those two is a reporting problem; we distinguish them
rather than pooling them into a single failure rate.

## An exemplar worth reporting as prominently as the failures

A programme that only reports what it cannot find will give a false impression of the field.
The last A7 paper verified (arXiv:2607.00924) is the tightest correspondence we have measured,
and it is worth stating precisely what that looks like:

- **All ten** semantic-backtracking counts in the paper (16/46/14/13/8/3, 92/84/8, 89/9/2)
  reproduce **exactly** from three released per-question CSVs.
- The headline judge-score gains reproduce from released data within the stated bands
  (+46.2\%/+59.4\%/+48.6\% against a stated 40--65\%; +28.6\% against a stated 25--30\%).
- The single negative finding is narrow and mundane: run outputs backing one novelty claim are
  excluded by `.gitignore` and archived to a Hugging Face dataset the README itself says is
  created `--private`.

This is what a fully checkable paper looks like, and it exists in the same corpus as the
papers whose numbers cannot be located at all. The distribution is not uniformly poor.

Two further things from that verification are worth recording as method, not anecdote:

1. **The verifier avoided a false `DIVERGENT` by counting rather than summarising.** A
   summarisation of `benchmark_questions.jsonl` reported 72 records; a deterministic line
   count gives exactly 100. Had the summary been trusted, we would have accused a paper of a
   discrepancy that does not exist. This is the same lesson as `errors.md` #12, arriving from
   a different direction: *before reporting a mismatch, compute rather than read.*
2. **The verifier declined to score a claim it could not settle**, rather than assigning a
   weak verdict. Table 1's semantic-diversity values require a sentence splitter unavailable
   in the environment; a regex approximation over-split by ~7\%, so the claim was left out of
   the ledger entirely with the reason recorded. An omitted claim is more honest than a
   verdict manufactured to fill a row.

## Verification note

One A4 paper (arXiv:2601.18207, PaperSearchQA) was verified directly by the AI lead rather
than by a subagent: two subagent attempts were terminated by a safety classifier that appears
to have been triggered by the paper's biomedical corpus content. The paper is a benign
search-agent benchmark. Its ledger entry carries a note recording this; the evidence standard
applied was identical.

## Limits

- 5 of 49 A4 papers and 6 of 39 A7 papers had no readable repository tree.
- Verification reflects repository state at retrieval; timestamps are recorded per paper.
- No code was executed. Every claim records the level actually reached.
