# Phase R cycles — one line each

The authoritative progress table. Mirrors the Linear project
[arXiv Frontier — Phase R verification](https://linear.app/kopachelli/project/arxiv-frontier-phase-r-verification-eb87d5f458b6).
Update the status column as each cycle completes; this file plus the committed ledgers are
the whole of the programme's durable state.

**No sampling. Every area verified in full before any area paper is written.**

| cycle | Linear | areas | papers | est. tokens | status |
|---|---|---|---|---|---|
| — | — | A1 discovery | 32 | 2.87M actual | ✅ **done** — 255 claims |
| — | — | A2 auditability | 49 | 3.98M actual | ✅ **done** — 352 claims |
| **1** | SOFTWR-205 | A8 scholarly record + A9 research infrastructure | 24 + 16 | 3.21M actual | ✅ **done** — 279 claims |
| **2** | SOFTWR-206 | A4 physical & life sciences + A7 ideation | 49 + 39 | 7.85M actual | ✅ **done** — 607 claims |
| **3** | SOFTWR-207 | A6 deep research | 79 | ~6.7M | ⬜ pending |
| **4** | SOFTWR-208 | A5 benchmark | 116 | ~9.9M | ⬜ pending |
| **5** | SOFTWR-209 | A3 end-to-end | 86 | ~7.3M | ⬜ pending |
| **6** | SOFTWR-210 | cross-cutting papers + author right of reply | — | — | ⬜ blocked by 1–5 |

**Total: 490 papers across nine areas.** 209 verified (1,493 claims), 281 remaining.

## How to run a cycle

Open a fresh session in `C:\github\arxiv-frontier` and paste the prompt from
`SESSION-START.md`. It orients itself from disk and picks the next cycle.

Start a **new session per cycle** — see the reasoning at the bottom of `SESSION-START.md`.

## Rules that bind every cycle

1. Every verdict carries its evidence; verdicts without it are discarded, not averaged.
2. `NOT_LOCATED` never means fabrication. A false accusation is worse than a missed one.
3. Establish *why* an artifact is missing before reporting that it is (see `errors.md` #12).
4. No author is contacted until cycle 6. Right of reply happens once, for everyone.
5. Commit the ledger the moment a cycle completes. Progress lives in git, not in context.
6. Our own tooling defects are logged as ours and never counted against a paper.

## If a cycle is interrupted

Commit what is finished, record exactly where it stopped in the table above, and start a new
session. Nothing is lost: ledgers are per-area CSVs and the next session rebuilds orientation
from this file.
