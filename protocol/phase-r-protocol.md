# Phase R protocol — repository verification programme

Draft 2026-07-26, written before any repository was cloned or any claim assessed. The
naming policy (`protocol/phase-r-naming-policy.md`) was fixed earlier and separately, also
before any results existed. Specification by Khristian Kopachelli; design by Claude Fable 5.

---

## 1. Question

Paper 1 measured what this literature *reports*. Phase R measures whether the reports are
*supported by the artifacts the papers themselves release*.

- **RQ-R1 (availability).** Of the repositories papers link to, how many exist, are public,
  and contain anything?
- **RQ-R2 (correspondence).** For a paper's checkable claims, is the supporting evidence
  present in its own released artifact?
- **RQ-R3 (unlicensed synthesis).** How often is a stated result absent from, or contradicted
  by, the artifact that is supposed to contain it? This operationalises the
  unmarked-hypothesis argument (`notes/unmarked-hypothesis.md`) as a measured rate rather
  than a conjecture.
- **RQ-R4 (does provenance help?).** Do papers that report provenance, traces, or
  reproduction artifacts (codebook D6) show different correspondence rates than those that do
  not? This turns the remedy claim into a falsifiable prediction.

## 2. Sampling frame

The 491 papers in Paper 1's corpus with at least one repository URL extracted mechanically
from their full text (`data/artifact-verification.csv`): 812 GitHub URLs, 155 Hugging Face,
11 anonymous.4open.science, 4 GitLab.

## 3. Ladder of evidence — what "verification" means here

Each step is strictly cheaper than the next and is reported separately. We do not claim to
have done a step we did not do.

| level | what is checked | method |
|---|---|---|
| **R0 availability** | does the URL resolve, is it public, is it non-empty | host API, mechanical, no judgement |
| **R1 presence** | do the files the paper implies exist (code, data, configs, prompts) | file listing, pattern match |
| **R2 correspondence** | is each checkable claim evidenced in the artifact | model-assisted, quote-required |
| **R3 execution** | does the code run and reproduce a reported number | attempted only on a documented subset |

Most papers will be assessed to R2. R3 is expensive and environment-dependent; where it is
not attempted we say so per paper rather than implying a stronger check than we performed.

## 4. Claim classification (fixed vocabulary, from the naming policy)

`SUPPORTED` · `DIVERGENT` · `NOT_LOCATED` · `CONTRADICTED` · `UNVERIFIABLE`

`NOT_LOCATED` never means fabrication, and no output of this programme will say otherwise.
Every `NOT_LOCATED` verdict must record the specific search performed.

## 5. Evidence requirement (from Phase V's lesson)

Phase V established that a second model's judgement adds almost nothing against correlated
error (zero corruptions were caught by exactly one model), while a mechanical check of a
stated invariant found real violations deterministically. Phase R is designed accordingly:

1. **Mechanical wherever possible.** R0 and R1 involve no model judgement.
2. **Quote-required at R2.** Every verdict must cite a verbatim path or line from the
   artifact, or record the exact search that failed. A verdict without locatable evidence is
   discarded, not averaged in.
3. **No second-model rubber stamp.** We do not run a second model to "confirm" R2 verdicts
   and report the agreement as quality. Where a second check is applied, it is a different
   *kind* of check, not a different model doing the same thing.
4. **Invariant checks on our own outputs**, as in `code/check_consistency.py`.

## 6. Areas

The corpus is to be partitioned into 7–10 areas, each yielding one paper, plus a synthesis.
The partition is a scope decision reserved for the human co-author; candidate schemes and
their sizes are in `notes/phase-r-partition-options.md`. No area work begins before the
partition is fixed and recorded.

## 7. Ethics and load

- Only public repositories are accessed. Nothing is bypassed and no authentication wall is
  circumvented; a private or deleted repository is recorded as `UNVERIFIABLE`.
- Cloning is rate-limited and shallow. Repository contents are **not redistributed**; we
  publish claim ledgers and file listings, not copies of other people's code.
- Licences are recorded per repository, and any excerpt quoted in a ledger is short and
  attributed.
- Authors of named papers are notified with a right of reply before publication, per the
  naming policy.

## 8. We go first

Paper 1 is verified by this same procedure and appears as the first entry in the ledger. Its
repository is public at <https://github.com/Kopachelli/arxiv-frontier> and its deposit at
<https://doi.org/10.5281/zenodo.21577093>. If our own claims are not locatable in our own
artifacts, that is published with the same prominence as anyone else's — and Phase V has
already produced one such finding (18 internal-consistency violations, `errors.md` #10).
