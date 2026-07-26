# Area paper template (Phase R, papers 1–9)

Every area paper follows this structure, so that nine papers by the same programme are
comparable and the cross-cutting papers can aggregate them without re-reading prose. Fixed
before the first area's results were known.

---

## Title pattern

*Do the Artifacts Support the Claims? Repository Verification of \<AREA\> in Autonomous AI
Research (2024–2026)*

## Standing sections

**1. What this paper checks, and what it does not.** States up front that this is a
correspondence check between a paper's claims and its own released artifact — not an
assessment of whether the research is good, novel, or correct, and not an investigation of
authors. Names the verdict vocabulary and states that `NOT_LOCATED` never means fabrication.

**2. The area.** Definition, inclusion rule, n, and how the area sits in the partition. Notes
which papers fall in adjacent areas and why.

**3. Method.** The R0–R3 ladder, the archetype router (which levels were possible for which
repositories), the evidence requirement per verdict type, and the discard rule for verdicts
lacking evidence. Reports how many verdicts were discarded — a paper that never discards any
is not applying its own rule.

**4. Results.**
  4.1 Availability (R0) and archetype distribution (R1) for the area.
  4.2 Claim ledger: verdicts overall and by claim type.
  4.3 The four standing cross-cuts, identical in every area paper: by **domain (B)**, by
      **cohort (D)**, by **lineage (F)**, by **institution type (H, aggregate only)**.
  4.4 Notable individual cases, named, with the evidence that settled each.

**5. What we could not check.** Every area has claims the artifact could not evidence — a
wet-lab assay, a human study, a closed dataset. Stated as a proportion, not buried.

**6. Threats to validity.** At minimum: our own extraction defects (Paper 1 logged one that
inflated a dead-link rate by a third against other researchers, `errors.md` #12); the
possibility that our search was inadequate for any `NOT_LOCATED`; branch and time drift
between publication and verification; and the fact that verification was AI-conducted with
the correlated-error bound Phase V measured directly.

**7. Right of reply.** Which authors were contacted, how many responded, and their responses
published unedited. Corrections we accepted are marked in the ledger, not silently applied.

**8. Data availability.** The area's full claim ledger, with every verdict, its evidence, and
the level of verification actually reached.

## Standing tables (identical schema across all nine papers)

| table | content |
|---|---|
| T1 | area composition: n, archetype distribution, verification levels reached |
| T2 | verdicts × claim type |
| T3 | verdicts × cohort (feeds the trend paper) |
| T4 | verdicts × lineage (feeds the lineage paper) |
| T5 | verdicts × institution type, aggregate only, cells < 5 suppressed |
| T6 | discarded verdicts, by reason |

## Rules that bind every area paper

1. **No verdict without its evidence.** A file path for `SUPPORTED`/`DIVERGENT`/
   `CONTRADICTED`; the exact search performed for `NOT_LOCATED`.
2. **No stronger check implied than was performed.** Every claim records the level reached;
   no paper may describe a result as reproduced unless R3 was actually run.
3. **Neutral vocabulary, always.** No output of this programme characterises any author's
   conduct or uses the language of misconduct.
4. **Authors get right of reply before publication**, and responses are published unedited.
5. **We are in the ledger too.** Paper 1 of the programme is verified by the same procedure
   and reported with the same prominence.
6. **Our own defects are reported as ours.** Where a failure to locate an artifact turns out
   to be a defect in our tooling, it is corrected and logged as our error, not counted against
   the paper.
