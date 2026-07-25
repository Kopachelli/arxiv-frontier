# arxiv-frontier

**When the Instrument Studies Itself: A Systematic Map of Autonomous AI Research Systems
(2024–2026), Conducted by a Frontier AI** — working repository.

A human–AI research collaboration: Khristian Kopachelli (independent researcher) and Claude
Fable 5 (Anthropic). The AI conducts a PRISMA-style systematic review and bibliometric
analysis of the "AI scientist" / autonomous-research literature; the process is itself
documented as a reflexive case study, with all AI errors and human interventions logged.

## Layout

```
protocol/     Review protocol, codebook, amendments (normative methodology)
code/         Harvest, screening, analysis, figure, and bib-verification scripts (Python)
data/         Candidate corpus, screening decisions, coded corpus, reliability sample (CSV)
figures/      Generated figures
paper/        LaTeX source (arXiv version + Zenodo title-page variant)
process-log/  Contemporaneous timeline, AI error log, human-intervention log (RQ4 data)
```

## Reproduction

```
pip install -r code/requirements.txt
python code/harvest.py        # rebuild data/candidates.csv from the arXiv API
python code/analyze.py        # recompute all statistics from data/*.csv
python code/figures.py        # regenerate figures/
python code/verify_bib.py     # validate every paper citation against live metadata
```

## Integrity commitments

No fabricated data; every reported count traceable to a CSV; every citation
machine-verified; complete disclosure of the AI's role; all AI failures logged in
`process-log/errors.md` and reported in the paper.
