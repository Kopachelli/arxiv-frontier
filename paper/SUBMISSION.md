# Publication package — status and checklist

Nothing in this file has been executed. Every outward-facing action requires Khristian's
explicit per-item approval (protocol §8a.4).

---

## Build state

- `paper/main.pdf` — 19 pages, compiles clean (pdflatex ×2 + bibtex + ×2).
- All numbers generated into `paper/numbers.tex` by `code/analyze.py`; none hand-typed.
- All 17 citations verified against live arXiv/Crossref metadata (`code/verify_bib.py`, 17/17).
- All macros resolve (`code/check_macros.py`).
- Figures regenerate from released CSVs (`code/figures.py`).

## arXiv submission

**Category.** Primary `cs.DL` (Digital Libraries) — the paper is a bibliometric/systematic
map of a literature, which is squarely cs.DL. Cross-list `cs.AI` and `cs.CY`.
Rationale for not making cs.AI primary: the contribution is about the literature's evidentiary
practices, not a new AI method; cs.DL moderation is also a more natural fit and historically a
more accessible endorsement path for a first-time submitter.

**Endorsement.** Khristian is a first-time arXiv submitter, so cs.DL will require endorsement
by an established author in that category. Options, in order of likely success:
1. Ask a corresponding author of a paper we cite whose work we engage substantively — the
   auditability thread (Takahara & Mizoguchi; Li; Ning et al.) is the natural approach, since
   our results directly extend their argument.
2. Ask a cs.DL-active researcher in scientometrics/meta-science.
3. Post to Zenodo first (no endorsement required), then request endorsement citing the DOI.

**Authorship compliance.** arXiv does not permit AI systems as authors. Khristian is the sole
listed author; the AI's role is disclosed in the title-page footnote, §8 Contribution
Statement, and the abstract. This is compliant, and we state in §8 that if listing tracked
contribution rather than accountability, the AI would be a co-author.

**Files to submit.** `main.tex`, `sections-*.tex`, `numbers.tex`, `references.bib`, and the
five figure PDFs. Note: figure paths use `../figures/`; for arXiv the figures must be copied
into the submission directory and the paths flattened. Not yet done.

## Zenodo deposit (companion record)

Purpose: a citable record carrying the explicit joint-authorship statement that arXiv policy
does not permit, plus archived data and code.

- Creators: Khristian Kopachelli; Claude Fable 5 (Anthropic) — listed as a contributor of type
  `Other` if the schema rejects a non-human creator, with the joint-authorship statement in the
  description.
- Upload: paper PDF, `data/*.csv`, `code/*.py`, `protocol/*.md`, `process-log/*.md`.
- Description must cross-reference the arXiv ID once assigned, and vice versa.
- **Deliberate contrast with the failure mode we cite.** \citet{brzozowski2026ghost} documents
  1,655 Zenodo records with real DOIs, fabricated authors, and backdated timestamps. Our
  deposit should be the inverse in every respect: a real accountable human author, an AI
  contributor named as what it is, real timestamps, and a full process log. Worth stating in
  the deposit description.

## GitHub repository

Remote already configured: `https://github.com/Kopachelli/arxiv-frontier` (branch `dev`,
7 commits unpushed). Public release makes the repository the reproducibility artifact the
paper claims it is.

Before pushing publicly, confirm:
- [x] No secrets (gitleaks clean on every commit).
- [x] No redistributed third-party content — we release metadata, decisions, and our own code
      only; no harvested PDFs or paper full text are stored in the repo.
- [ ] `README.md` updated with the final numbers and a citation block.
- [ ] License chosen (suggest CC-BY-4.0 for data/text, MIT for code).
- [ ] Khristian's approval to make it public.

## Open decisions requiring Khristian

1. Approve public push of the GitHub repository.
2. Approve Zenodo deposit (needs his account; the AI cannot and should not authenticate as him).
3. Approve arXiv submission and choose the endorsement route.
4. Choose licenses.
5. Decide the Phase R naming policy **before** Phase R begins (see `notes/roadmap.md`).
