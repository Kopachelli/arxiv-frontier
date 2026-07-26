# Phase V results — blind cross-model verification

Run 2026-07-26 under `protocol/phase-v-protocol.md`, which was written and committed before
any verification was executed. All per-item data in `data/phase-v-arm1.csv`,
`data/phase-v-arm2.csv`; ground-truth keys in `data/phase-v/`.

40 agent runs, 0 failures. Verifiers: Claude Fable 5 and Claude Opus 5, blinded to
provenance, to the study, and to each other.

---

## Arm 1 — independent re-doing (n = 150 papers × 2 models)

| verifier | producer | condition | agreement with original | Cohen's κ |
|---|---|---|---|---|
| Fable 5 | Fable 5 | **self** | 0.867 | 0.701 |
| Fable 5 | Opus 5 | cross | 0.880 | 0.743 |
| Opus 5 | Fable 5 | cross | 0.853 | 0.668 |
| Opus 5 | Opus 5 | **self** | 0.880 | 0.743 |

**Self-preference: +0.007** (self minus cross agreement). Effectively zero. Blinded to
provenance, neither model treated its own prior decisions more favourably than the other
model's.

**Authorship-identification probe: 0 of 300 responses committed to a guess.** Every response
was "unknown". Whether this reflects an absence of stylistic self-recognition or an unwillingness
to speculate cannot be separated by this design; either way, no evidence of self-identification
was found, which strengthens the self-preference null (the blind was not defeated).

Re-screening reproduced the original decision 85–88% of the time (κ ≈ 0.67–0.74) — close to
Paper 1's own Layer-1 figure of 83.3% / κ 0.71, on a different sample under the amended
criteria.

## Arm 2 — audit against injected ground truth (n = 200 records × 2 models, 20 corrupted)

| model | sensitivity | flags on uncorrupted |
|---|---|---|
| Fable 5 | **0.850** (17/20) | 0.094 |
| Opus 5 | **0.850** (17/20) | 0.094 |

By corruption type, **both models were identical**:

| corruption | injected | caught |
|---|---|---|
| `FLIP` (decision reversed) | 3 | 3 (100%) |
| `REASON_SWAP` (incompatible reason code) | 10 | 10 (100%) |
| `CODE_DRIFT` (dimension changed) | 7 | 4 (57%) |

### The result that matters

- **Inter-model agreement on flag/no-flag: 194/200 = 0.970, κ = 0.894.**
- **Corrupted items caught by exactly one model: 0.**

Every corruption one model missed, the other missed too. **Running a second frontier model as
a check detected nothing the first model would not have detected.** Redundancy across
Claude-family models bought zero additional error detection on this sample. This is the
concern \citet{bowkis2026automated} raise theoretically — correlated error under shared
training — measured directly, and it applies to Paper 1's own dual-model screening design.

### The shared blind spot is narrower than it looks

All three missed corruptions were `CODE_DRIFT`, and inspecting them shows the corrupted value
was **still defensible**:

| item | field corrupted | published → corrupted | assessment |
|---|---|---|---|
| a2-0012 (2605.25964) | claim strength | METHOD → CAPABILITY | both readings defensible |
| a2-0120 (2604.16982) | autonomy | NA → L1_STAGE | judgement call on a framework paper |
| a2-0183 (2510.16082) | paper type | SYSTEM → FRAMEWORK | the paper is *titled* "…Framework"; the corruption is arguably more correct than our published code |

On corruptions that were unambiguously wrong (`FLIP`, `REASON_SWAP`), detection was **13/13 =
100%** for both models. The `CODE_DRIFT` misses do not show auditor incompetence; they show
that the codebook underdetermines these fine-grained distinctions — the same failure that
produced Paper 1's seven boundary classes, reappearing one layer down at coding rather than
screening.

## What the audit flagged that was not corrupted — and what that was worth

14 of 180 uncorrupted records (7.8%) were flagged as wrong by **both** models with
substantively identical reasoning. Adjudication found:

- **Most were false alarms caused by a defect in our own audit prompt.** The prompt paraphrased
  the codebook's autonomy rule as "NA if the paper presents no system", where the codebook says
  autonomy applies *only* to `SYSTEM` and `CASE_STUDY` papers and is `NA` for all others. Both
  auditors therefore flagged correctly-coded `FRAMEWORK` papers. Logged as error #9.
- **One flag was correct and revealed a real class of error** (a2-0162, ChatBCI): a paper coded
  `L0_ASSISTIVE` was included, which contradicts amendment A1's boundary rule BR1, under which
  assistive tools are excluded as `EC6_ASSISTIVE`.

That single true positive prompted a mechanical consistency check
(`code/check_consistency.py`) over the whole corpus, which found:

| rule | violations |
|---|---|
| **C1** included but coded `L0_ASSISTIVE` (contradicts BR1) | **15** |
| C5 `POSITION`/`SURVEY` paper credited with lifecycle stages | 3 |
| C2 `SYSTEM`/`CASE_STUDY` with `NA` autonomy | 0 |
| C3 non-system with an autonomy level | 0 |
| C4 `UNCLEAR` code without a full-text flag | 0 |

**18 of 811 records (2.2%) violate rules the protocol already implied.** Full list in
`data/consistency-violations.csv`.

## The methodological finding

The LLM audit's value was **not** as a detector. It found one genuine problem and fourteen
false alarms, and its misses were perfectly correlated with the other model's. Its value was
as a *prompt to write a mechanical checker* — and that checker then found 18 violations
deterministically, exhaustively, with no false positives, in milliseconds, over a corpus
forty times larger than the audited sample.

This is the same lesson as \citet{gyevnar2026ddos}'s persona-versus-provenance contrast, and
the same lesson as every failure in Paper 1's own error log: **judgement-based checking of
judgement-based work has correlated blind spots; mechanical checks of stated invariants do
not.** The practical recommendation that follows is not "have a second model review it" — we
measured that and it added nothing — but "state your invariants and check them by script."

## Bound on these results, stated in advance and unchanged

Both verifiers are Claude-family models. This measures cross-model, not independent,
agreement, and a systematic error shared across the family is invisible to the entire design.
The Arm 2 result — zero uniquely-caught corruptions — is direct evidence that this bound is
not hypothetical.

It also means Phase V does not substitute for the human screening audit that Paper 1 records
as its principal limitation. If anything it strengthens the case for one: the redundancy that
was actually used in Paper 1 (two frontier models) is now measured to add approximately
nothing against correlated error.
