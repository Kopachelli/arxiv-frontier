# When the Instrument Studies Itself

A systematic map of **811 papers** on autonomous AI research systems (January 2024 – July
2026), conducted by a frontier language model, with its own process logged as data.

**Authors.** Khristian Kopachelli (independent researcher) · Claude Fable 5 (Anthropic).
The AI proposed the research direction, wrote the protocol and all software, executed the
search, screening, coding and analysis, and drafted the manuscript. The human framed the
project, made the scope decisions, overruled the AI where he disagreed, and takes
responsibility for the published work. See §8 of the paper for the precise division.

## What we found

| | |
|---|---|
| Corpus growth | 6 papers in 2024-Q1 → 241 in 2026-Q2 (~40×) |
| Report benchmark metrics | 71% |
| Test a result **outside** the loop that produced it | 5% |
| Provide **no** auditability mechanism | 55% |
| Never state what the humans did | 71% |
| Claim the AI produced new knowledge | 58 papers |
| …of those, provide no auditability mechanism | 64% |

The central result is a **dissociation**: papers making discovery claims validate their
*results* far better than average (50% report external validation vs 11% corpus-wide) while
exposing their *process* worse (36% provide any auditability mechanism vs 45%). This field
validates outputs better than it exposes process, and the gap is widest where its claims are
strongest.

We also report our own failures, with rates — a workflow that reported success having done
nothing, silent item-dropping at 0.4–0.5% in structured extraction, a pipeline defect that fed
empty inputs to a reasoning step, and a draft thesis contradicted by our own data. Every one
was caught by a cheap mechanical check.

## Layout

```
paper/         LaTeX source, generated numbers, verified bibliography, SUBMISSION.md
protocol/      Review protocol, codebook, screening prompts, amendments A1–A2
code/          Harvest, screening, coding, analysis, figures, artifact + citation verification
data/          Candidates, both screening layers, coded corpus, artifact verification, results
figures/       Generated figures
process-log/   Timeline, AI error log, human-intervention log  (the reflexive case-study data)
notes/         Programme roadmap, concept notes
```

## Reproduce

```bash
pip install -r code/requirements.txt
python code/harvest.py            # rebuild data/candidates.csv from the arXiv API
python code/screen.py  ...        # screening batch prep / merge / adjudication
python code/code_corpus.py ...    # coding batch prep / merge
python code/verify_artifacts.py   # mechanical full-text check of artifact release
python code/analyze.py            # all statistics -> data/RESULTS.md + paper/numbers.tex
python code/figures.py            # figures/
python code/gen_bib.py            # references.bib from live metadata
python code/verify_bib.py         # fail loudly on any unverifiable citation
python code/check_macros.py       # fail loudly on any undefined number in the paper
```

Screening and coding themselves ran as LLM agent batches; the prompts are in `protocol/` and
every per-paper decision with its justification is in `data/`.

## Integrity commitments

No fabricated data. Every reported number is generated from a released CSV by
`code/analyze.py` — none is transcribed by hand. Every citation is machine-verified against
live arXiv/Crossref metadata (17/17). Every AI failure encountered is recorded in
`process-log/errors.md` and reported in the paper. The AI's role is disclosed in the abstract,
a title-page footnote, and a dedicated contribution statement.

**Known limitation, stated up front:** no human independently validated any screening decision.
This follows from a deliberate minimal-intervention design (paper §3.6) and is a real cost, not
a technicality. The audit worksheet is in `data/screening-audit-worksheet.md` for anyone who
wants to perform it.

## Status

Paper 1 of a planned programme (`notes/roadmap.md`): next is blind cross-model verification of
this work, then a repository-verification programme checking whether papers' claims are
supported by the artifacts they release.
