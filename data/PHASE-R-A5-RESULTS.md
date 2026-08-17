# Phase R — Area 5 (benchmark), and the pattern at eight areas

Cycle 4 (Linear SOFTWR-208). **A5 benchmark**: 116 papers, 805 claims — the largest area in
the programme and the most mechanically checkable. Benchmarks, datasets and evaluation
methodologies for autonomous AI research systems.
Ledger: `data/phase-r-ledger-A5_benchmark.csv`.

A5 was designed as the sharpest test of the programme's central finding. Elsewhere a paper can
fairly say its numbers are not the kind of thing a repository holds: a wet-lab assay (A4) is a
physical measurement, a novelty rating (A7) lives in a human judge's head. **A benchmark's task
count has no such excuse.** If a paper says the benchmark has 500 tasks, the released files
either contain 500 records or they do not, and a reader can count them.

---

## Benchmarks are the best-evidenced area in the corpus

| verdict | share |
|---|---|
| `SUPPORTED` | 67.5% |
| `NOT_LOCATED` | 12.9% |
| `DIVERGENT` | 11.4% |
| `UNVERIFIABLE` | 8.1% |
| `CONTRADICTED` | 0.1% (1 claim) |

| claim type | n | supported | not located | divergent |
|---|---|---|---|---|
| **METHOD_COMPONENT** | 205 | **84%** | 5% | 8% |
| **ARTIFACT_RELEASE** | 119 | **84%** | 2% | 7% |
| **DATASET** | 276 | **74%** | 7% | **16%** |
| **NUMERIC_RESULT** | 167 | **40%** | 43% | 12% |
| EXTERNAL_VALIDATION | 38 | 5% | 3% | 5% |

Four records at once: the highest overall support rate (67.5%), the highest method-component
support (84%), the highest artifact-release support (84%, tied with A6's 82% within noise), and
the highest dataset support (74%) in the programme — the previous best was 52%.

**Benchmarks ship their data.** That is the plainest positive finding the programme has
produced, and it is worth stating as prominently as any failure: the area whose entire
contribution *is* a dataset overwhelmingly releases one, and the released files overwhelmingly
match what the paper describes.

## The pattern holds — and A5 bounds it

| area | method component | numeric result | ratio |
|---|---|---|---|
| A2 auditability | 53% (n=58) | 33% (n=51) | 1.6× |
| A1 discovery | 62% (n=60) | 36% (n=103) | 1.7× |
| **A5 benchmark** | **84% (n=205)** | **40% (n=167)** | **2.1×** |
| A4 physical & life sciences | 71% (n=120) | 29% (n=84) | 2.5× |
| A9 research infrastructure | 68% (n=44) | 25% (n=28) | 2.7× |
| A8 scholarly record | 61% (n=64) | 22% (n=37) | 2.8× |
| A7 ideation | 65% (n=92) | 15% (n=61) | 4.4× |
| A6 deep research | 77% (n=216) | 17% (n=121) | 4.7× |
| **pooled** | **72% (n=859)** | **29% (n=652)** | **2.5×** |

**Eight areas, same direction, no exceptions.** A5 was the area most likely to break the
pattern and it does not. What it does is bound it from below: 40% numeric support is the
highest we have measured, and 2.1× the narrowest gap. Benchmarks are the best in the corpus at
making their reported numbers locatable — and a described method is still more than twice as
likely to be found in their repositories as a reported number.

That result is more informative than a uniform finding would have been. It rules out the
reading that the gap is an artifact of areas whose numbers are intrinsically unrecordable.
Here they are recordable, the repositories are unusually complete, and the gap persists at
half its pooled size. **Even where checking is easiest, results are the least-preserved part of
the record.**

Of A5's 167 numeric claims, 43% were not located — a rate close to the corpus-wide 42%,
despite this area's much better release behaviour. What benchmarks preserve is the *input* to
evaluation, not its *output*: the task set is released, the baseline table that scored models
against it is usually not.

## Divergence is a symptom of checkability, not of sloppiness

A5 has the programme's highest `DIVERGENT` rate (11.4% overall, **16% of dataset claims**), and
this must be read carefully, because the naive reading is exactly backwards.

**You can only disagree with a number you can find.** In areas where the artifact is absent the
verdict is `NOT_LOCATED` — no mismatch can be recorded, because nothing was there to mismatch.
A5's divergence rate is high *because* its release rate is high. A rising divergence count is
what a field looks like when it becomes auditable, not when it becomes careless.

Four examples, each a deterministic count rather than an impression:

| paper | claim | what the files hold |
|---|---|---|
| arXiv:2604.09251 | 268 human-validated questions across five domains | 255 records across the five JSONL files (34/68/59/…) |
| arXiv:2604.15411 | five physics subfields | six distinct `subfield` values over 100 records; `amo` is the extra |
| arXiv:2602.02905 | 40 fully executed tasks | 35 task directories under `benchmark/papers/` |
| arXiv:2607.16848 | full paper corpora released | 39 of 81 full-text files present in the HF dataset tree |

These are small, mundane discrepancies of exactly the kind a reader would find in an afternoon,
and none of them implies anything about the research. They are reported because the programme's
standard is correspondence between text and artifact, and because a review that recorded only
absences would systematically under-report the areas that release most.

## The single CONTRADICTED verdict

One claim in 805, and it is a licence mismatch: arXiv:2605.16616 states in its ethics section
that the dataset and evaluation suite are released under CC-BY-4.0; the repository's top-level
`LICENSE` is Apache-2.0 and the GitHub API reports `license.spdx_id = "Apache-2.0"`. The README
notes that subsystems carry their own licences, so a CC-BY-4.0 file may well exist deeper in
the tree.

We record it as `CONTRADICTED` because the top-level evidence conflicts with the stated claim,
which is the bar the protocol sets. It is a documentation inconsistency with practical
consequences for a reuser, not a finding about the research, and it is precisely the sort of
thing the authors would likely fix in an afternoon if told. That is what cycle 6's right of
reply is for.

## Method notes

- **Counting worked.** Verifiers were instructed to count records deterministically rather than
  accept a summary — the lesson from `errors.md` #12 and from the A7 near-miss where a summary
  reported 72 records against an exact count of 100. Every divergence above cites a count.
- **Hugging Face pointers were treated as legitimate release evidence** where the pointer was
  verified, and verifiers were required to say whether they checked the pointer or the data.
  Several went further and counted the HF tree itself.
- **Zero verdicts were discarded** for missing evidence at merge — the first area with a clean
  sweep. 85% of verdicts reached R2 (contents inspected); 6% stopped at R0.
- **The session-limit interruption cost nothing.** The run stopped at 37 of 116 agents; the
  partial ledger was committed to git, and the workflow resumed from cache. The 38-paper
  partial reported 68% support and 78% dataset support against final figures of 67.5% and 74% —
  close, but we did not report them as findings at the time, and were right not to: the partial
  numeric-result figure would have been read against a smaller n than the claim needed.

## Limits

- 116 papers, 805 claims; every paper in the area, no sampling.
- `EXTERNAL_VALIDATION` at 5% supported (n=38) is expected, not a finding: expert quality
  review of a benchmark is not something the benchmark's repository can settle. 70% of such
  claims corpus-wide are `UNVERIFIABLE`.
- Verification reflects repository state at retrieval. No code was executed; every claim records
  the level actually reached.
- Divergences are correspondence findings between a paper and its own artifact at one point in
  time. Repositories change; papers do not. No author has been contacted — that happens once,
  for everyone, in cycle 6.
