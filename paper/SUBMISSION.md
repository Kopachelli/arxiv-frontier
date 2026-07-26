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

**Category — CORRECTED 2026-07-26.** Primary **`cs.AI`**; cross-list `cs.DL` and `cs.CY`.

The original plan named `cs.DL` primary. That was wrong on a dimension the AI had not
checked: **arXiv endorsement is category-specific**, and none of the candidate endorsers whose
work this paper most directly extends publish in cs.DL. Verified with
`code/find_endorsers.py`:

| candidate | categories | can endorse cs.DL? |
|---|---|---|
| Takahara & Mizoguchi (2607.09195) | cs.AI, cond-mat.mtrl-sci | no |
| Ning et al. (2607.17100) | cs.MA, cs.AI, cs.SE | no |
| Li (2606.31273) | cs.LG | no |
| Wang (2607.05682) | cs.AI | no |
| Brzozowski & Chung (2606.02184) | **cs.DL**, cs.LG | yes |
| Gyevnár, Kasirzadeh & Shah (2607.10712) | cs.CR, cs.AI, **cs.DL** | yes |

Choosing cs.AI primary is defensible on the merits, not merely on convenience: the object of
the study is AI systems and their evidentiary practices, and cs.AI is where the mapped
literature lives and where the audience that should act on the findings reads. Cross-listing
to cs.DL preserves reach into scientometrics and meta-research.

**Endorsement (cs.AI).** Two drafts prepared in Gmail on 2026-07-26, not sent:
1. **Takahara & Mizoguchi** (`kougen@iis.u-tokyo.ac.jp`, `teru@iis.u-tokyo.ac.jp`) — closest
   intellectual neighbours; our results are the field-scale evidence for their argument.
2. **Jingjie Ning et al.** (`jening@cs.cmu.edu`, cc `kegl@dp.tech`) — their held-out-transfer
   method is one of the positive exemplars in our findings.

Addresses were read from the papers' own PDFs (`code/find_endorsers.py`), not guessed.

A third option worth considering if both decline: **Nihar B. Shah** (CMU), co-author of
arXiv:2607.10712, is prominent in peer-review and meta-science and is cs.DL-active — which
would also make a cs.DL primary submission viable. No email appears in that PDF, so his
address would need to be looked up rather than inferred.

If no cs.AI endorsement materialises, the fallback is cs.DL primary with Brzozowski & Chung or
Shah as endorser; the Zenodo DOI means the work is public and citable either way.

**Authorship compliance.** arXiv does not permit AI systems as authors. Khristian is the sole
listed author; the AI's role is disclosed in the title-page footnote, §8 Contribution
Statement, and the abstract. This is compliant, and we state in §8 that if listing tracked
contribution rather than accountability, the AI would be a co-author.

**Files to submit.** `main.tex`, `sections-*.tex`, `numbers.tex`, `references.bib`, and the
five figure PDFs. Note: figure paths use `../figures/`; for arXiv the figures must be copied
into the submission directory and the paths flattened. Not yet done.

## Zenodo deposit (companion record) -- PUBLISHED

- v1: 10.5281/zenodo.21577093 (2026-07-25)
- **v2: 10.5281/zenodo.21579505 (2026-07-26)** -- corpus corrected to 807 papers
- **Concept DOI (always latest): 10.5281/zenodo.21577092**


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
