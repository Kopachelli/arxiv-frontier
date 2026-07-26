# Phase R — Area 1 (discovery claims): claim-versus-artifact results

32 papers whose headline claim is a **discovery** — an assertion that an AI system produced
new knowledge about the world, not merely that a system performs well. 255 claims assessed
against the papers' own released repositories. Full ledger with every verdict and its
evidence: `data/phase-r-ledger-A1_discovery.csv`.

**These are not findings about authors.** This is a correspondence check between what a paper
states and what its own artifact contains. `NOT_LOCATED` never means fabrication; the
overwhelmingly likely explanations are mundane — the result lives in a branch or notebook we
did not find, the repository holds code but not outputs, a configuration was undocumented, or
our search was inadequate. Nothing here is published until the authors of named papers have
had a right of reply.

---

## Overall verdicts

| verdict | n | share |
|---|---|---|
| `SUPPORTED` | 114 | 44.7% |
| `UNVERIFIABLE` | 58 | 22.7% |
| `NOT_LOCATED` | 54 | 21.2% |
| `DIVERGENT` | 28 | 11.0% |
| `CONTRADICTED` | 1 | 0.4% |

Verification depth: **R2 (file contents inspected) on 223 of 255 claims (87%)**; R1 on 16;
R0 on 16. No claim was assessed at R3 — no code was executed, and the ledger says so per
claim rather than implying otherwise.

## The result: implementations are present, evidence for numbers is not

| claim type | n | `SUPPORTED` | `NOT_LOCATED` | `DIVERGENT` | `UNVERIFIABLE` |
|---|---|---|---|---|---|
| **METHOD_COMPONENT** | 60 | **62%** | 8% | 15% | 15% |
| ARTIFACT_RELEASE | 39 | 59% | 10% | 18% | 10% |
| DATASET | 23 | 52% | 26% | 4% | 17% |
| **NUMERIC_RESULT** | 103 | **36%** | 29% | 10% | 25% |
| EXTERNAL_VALIDATION | 30 | 17% | 30% | 3% | 50% |

The gap between `METHOD_COMPONENT` (62% supported) and `NUMERIC_RESULT` (36% supported) is
the finding. **If a paper in this area describes a module, you can usually find it. If it
reports a number, more often than not you cannot confirm it from the artifact.** Repositories
in this literature carry implementations; they carry the evidence for reported results much
less often.

`EXTERNAL_VALIDATION` behaves exactly as it should: half of those claims are `UNVERIFIABLE`,
because a wet-lab assay or clinical outcome is not the kind of thing a code repository can
evidence. That is expected and is not a criticism — and the verifiers' willingness to use
`UNVERIFIABLE` rather than reach for an accusatory verdict is evidence the calibration held.

## What `DIVERGENT` looks like in practice

The 28 divergences are specific and checkable, not impressions. Representative cases, each
with the path that settled it:

- **Hyperparameter mismatch.** A paper states LoRA scaling α = 16; `train.py` sets
  `lora_alpha=32`. *(Independently re-verified by the authors of this report by fetching the
  file directly — the verdict, path and values were all correct.)*
- **Probability mismatch.** A paper states genetic-programming operator probabilities of
  0.75 / 0.2 / 0.05; `selector.py` defines 0.8 / 0.15 / 0.05.
- **Scope mismatch.** A paper reports five autonomously produced papers; `assets/cases/`
  contains three, and the other two are absent from the checkout.
- **Task-count mismatch.** A paper evaluates on ten named tasks; `tasks/` contains nine
  directories, four of which map to the paper's list.
- **Identical "different" methods.** Two domain-specific "top-performing methods" for
  different scientific problems are byte-identical files (`diff` reports no differences).
- **Range overreach.** A claim about behaviour "beyond 80 residues" where the study's own
  configuration caps the length grid at 80.

The single `CONTRADICTED` verdict runs in the *safer* direction: a paper's ethics statement
undertakes not to open-source a particular module, and the module is in fact present in the
repository. Worth recording precisely because it shows the check is not merely finding
absences.

## What this means for the programme's central question

The unmarked-hypothesis argument (`notes/unmarked-hypothesis.md`) predicts that where a
system cannot obtain a value it may synthesise a plausible one, and that the defect is the
missing epistemic marker rather than the generative act. Area 1 gives that a first
measurement: **39% of reported numeric results in discovery papers are either not locatable
in the artifact (29%) or diverge from it (10%)**, against 8% and 15% for described method
components.

This does not establish that any number was invented — a missing result file is the far more
likely explanation, and we say so. What it establishes is narrower and still substantial: in
the area of this literature that makes the strongest claims, **the reported quantities are
the part a reader is least able to check**, and they are markedly less checkable than the
machinery that supposedly produced them.

## Method notes and limits

- Verifiers received the full paper text, the complete repository file listing, and the
  README, and could fetch individual files. They were not shown Paper 1's codes or any prior
  verdict, so their assessments are not anchored on ours.
- Every verdict required evidence of a type fixed in advance — a file path for
  `SUPPORTED`/`DIVERGENT`/`CONTRADICTED`, the exact search performed for `NOT_LOCATED`.
  Verdicts lacking it are discarded rather than averaged in; none were discarded in this area.
- 2 of 32 papers had no readable repository tree and contribute only `UNVERIFIABLE` claims.
- Verification reflects repository state at the time of checking; branches, later commits and
  large-file storage may hold material we did not see. Any single `NOT_LOCATED` should be read
  as a statement about our search.
- The verification was AI-conducted, with the correlated-error bound Phase V measured
  directly: a second frontier model checking the same records caught nothing the first
  missed. A second model is therefore not a safeguard here; the evidence requirement and the
  reader's ability to re-open the same file are.
