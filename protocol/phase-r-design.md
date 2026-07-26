# Phase R — combined design (fixed 2026-07-26, before any area work)

Partition decided by Khristian Kopachelli, who chose to combine schemes A, B, D, E, F and H
rather than pick one. This document turns that choice into an executable design. It is fixed
before any repository is assessed.

---

## 1. The key structural point

The six chosen schemes are not six partitions. Treating them as such would give an
unmanageable product of cells. They occupy three distinct roles:

| role | schemes | meaning |
|---|---|---|
| **Partition** — defines an area, and therefore a paper | **A** (what the repository is supposed to support) | one area = one paper |
| **Method router** — decides *which checks are even possible* | **E** (artifact archetype) | not a grouping; a branch in the pipeline |
| **Cross-cutting dimensions** — recorded on every paper, reported in every area | **B** (domain), **D** (time), **F** (lineage), **H** (institution type) | enable within-area breakdowns and their own cross-area papers |

This gives one collection effort and many analyses, instead of six incompatible cuts.

## 2. One shared ledger

Every verified paper produces one row in a single schema. Area papers are slices of it;
cross-cutting papers are different slices of the same rows. Nothing is collected twice.

```
arxiv_id · area(A) · domain(B) · cohort(D) · archetype(E) · lineage(F) · institution(H)
        · repo_url · R0_availability · R1_presence · claim_id · claim_text
        · verdict{SUPPORTED|DIVERGENT|NOT_LOCATED|CONTRADICTED|UNVERIFIABLE}
        · evidence_path_or_search · verification_level_reached{R0|R1|R2|R3}
```

## 3. Partition A — the eight areas (one paper each)

Assignment is **first match wins**, in this order, so areas are disjoint:

| # | area | rule | ~n (repo-bearing) |
|---|---|---|---|
| 1 | Discovery claims | D8 = DISCOVERY | 32 |
| 2 | Auditability & integrity tooling | screened IC3 | ~70 |
| 3 | End-to-end autonomous systems | D2 ∈ {L3, L4} | ~113 |
| 4 | Autonomous experimentation / self-driving labs | D3 ∋ EXECUTION ∧ D4 ∈ {MATERIALS, CHEMISTRY, PHYSICS} | ~45 |
| 5 | Benchmarks & evaluation | D1 = BENCHMARK | ~141 |
| 6 | Deep research agents | entered via BR7 | ~120 |
| 7 | Ideation & hypothesis generation | D3 ∋ IDEATION, single-stage | ~60 |
| 8 | Biomedical systems | D4 = BIOMED | ~56 |

Areas 1 and 2 run first: area 1 carries the programme's central question at the smallest
size, and area 2 is the reflexive one — do papers *proposing* auditability tools ship them?

## 4. Method router E — artifact archetype decides what can be checked

Assigned mechanically from the repository's file listing, before any claim is assessed. The
archetype determines the verification track, and every verdict records the level reached, so
we never imply a stronger check than we performed.

| archetype | detection | verification track |
|---|---|---|
| `FULL_PIPELINE` | code + data + config/env + entry point | R0→R3, execution attempted |
| `CODE_ONLY` | code, no data | R0→R2, plus dependency/entry-point audit |
| `DATA_ONLY` | data/results, no runnable code | R0→R2 against reported numbers |
| `PROMPTS_ONLY` | prompt/config files, no implementation | R0→R2, prompt-to-claim correspondence |
| `DEMO_APP` | app/notebook/UI, no reproducible pipeline | R0→R2, feature-presence only |
| `STUB` | README or placeholder only | R0→R1, recorded as such |
| `DEAD` | URL does not resolve | R0 only, `UNVERIFIABLE` |

This makes E the honest backbone of the whole programme: it prevents a `PROMPTS_ONLY`
repository from being scored as if execution had been attempted.

## 5. Cross-cutting dimensions — recorded on every row

- **B — domain.** Already coded (D4). Reported within every area, and used to route papers to
  domain-expert review, which is Khristian's stated reason for including it: experts should be
  able to contribute to the areas they know.
- **D — cohort.** Half-year bins by first submission (2024-H1 … 2026-H2). Reported within every
  area and aggregated into the trend paper. This is the dimension that answers *"is the field
  getting better or worse at releasing verifiable work?"* — currently unknown.
- **F — lineage.** Which seed system a paper builds on (AI Scientist, Agent Laboratory,
  co-scientist, ChemCrow, self-driving-lab stacks, none). Detected from citations, GitHub fork
  relationships, and explicit "built on" statements. Asks whether verifiability propagates
  through derivative work.
- **H — institution type.** Industry lab / academic / hospital or national lab / independent /
  mixed, from author affiliations. See §7 for the constraint this carries.

## 6. Papers

| paper | content |
|---|---|
| **1–8** | one per area of partition A, each reporting its own B/D/E/H breakdowns |
| **9 — Lineage** | F across all areas: does verifiability propagate from seed systems to derivatives? |
| **10 — Trend** | D across all areas: is artifact quality improving or degrading, 2024→2026? |
| **11 — Synthesis** | field-level rates; tests whether papers reporting provenance mechanisms (codebook D6) differ measurably in claim support, turning the remedy claim in `notes/unmarked-hypothesis.md` into a falsifiable prediction |

Paper 1 of the programme (the systematic map) is verified by this same procedure and appears
as the first entry in the ledger.

## 7. Constraint on dimension H

Institution-type analysis is standard scientometrics, but it invites institutional comparison
in a way the other dimensions do not. The naming policy is therefore extended for H
specifically:

- **H is reported only in aggregate by institution *type*.** No output ranks, names, or
  compares individual institutions, laboratories, or groups.
- Individual papers remain named under the existing policy (that is about artifacts, not
  affiliations), but no output juxtaposes a named paper with an institutional judgement.
- If the H analysis cannot be conducted without effectively identifying a small number of
  institutions — for example if a cell has fewer than five papers — that cell is merged or
  suppressed rather than reported.

This is fixed now, before we know which direction the H result points.

## 8. Order of work

1. Build the dimension extractors (E, F, H) — mechanical, and required before any area starts.
2. Area 1 (discovery claims) end to end, to prove the R0–R3 pipeline at small scale.
3. Area 2 (auditability tooling).
4. Remaining areas, then the three cross-cutting papers.
