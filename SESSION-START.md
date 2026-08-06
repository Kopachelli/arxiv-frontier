# Session start — paste this to begin any Phase R session

Copy everything in the box below into a fresh Claude Code session opened in
`C:\github\arxiv-frontier`. It is deliberately universal: it works at any point in the
programme, figures out where things stand from disk rather than from memory, and picks the
next cycle itself.

---

```
Read for-thoughts.md FIRST and answer anything in its Open section in writing, including
where you disagree. Then read notes/roadmap.md, notes/PHASE-R-CYCLES.md,
protocol/phase-r-design.md, protocol/phase-r-naming-policy.md and process-log/errors.md.

Then work out where we actually are, from disk rather than from anything you assume:
  - ls data/phase-r-ledger-*.csv          -> which areas are already verified
  - git log --oneline -12                 -> what happened most recently
  - python code/check_consistency.py      -> is the corpus still internally consistent

Tell me, briefly:
  1. which cycle is next, and why
  2. anything that looks unfinished or inconsistent
  3. any decision you need from me before starting

Then run that cycle end to end without asking permission for the routine parts:
prepare the area(s), run the verification workflow, merge the ledger, generate the figure,
write the results markdown, and commit and push. Keep going until the cycle is done.

Rules that always apply:
  - Every verdict needs its evidence. A repository file path for SUPPORTED / DIVERGENT /
    CONTRADICTED, the exact search performed for NOT_LOCATED. Discard verdicts that lack it
    rather than averaging them in.
  - NOT_LOCATED never means fabrication. A false accusation is a worse error than a missed
    one. Calibrate against over-claiming, not against being thorough.
  - Before reporting that someone else's artifact is missing, establish why it is missing.
    Our own extraction defects have been misattributed to other researchers once already
    (errors.md #12) and that must not happen again.
  - Log any failure of yours to process-log/errors.md as it happens, with how it was caught.
  - Do not contact any author. Right of reply happens once, in cycle 6, after all nine areas.
  - Commit the ledger as soon as the cycle completes. Progress must live in git, never only
    in context.

If the context window runs short mid-cycle, commit whatever is finished, write down exactly
where you stopped in notes/PHASE-R-CYCLES.md, and tell me to start a new session.
```

---

## Should you start a new session for each cycle?

**Yes — a fresh session per cycle, rather than continuing through compactions.** Three
reasons:

1. **Each cycle needs the budget.** A5 alone is ~9.9M tokens. A fresh session starts with a
   full window; a continued one may not have room to finish, and stopping halfway through an
   area is worse than not starting it.
2. **Compaction loses detail that this work depends on** — the exact wording of verdicts,
   which files were already checked, which anomalies were noticed but not yet chased.
   Re-reading four files from disk reconstructs the state better than a summary of them does.
3. **Nothing is lost by restarting**, because the design already assumes it: every ledger is
   committed the moment its area completes, the roadmap carries the cycle table, and the
   prompt above rebuilds orientation in about a minute.

The one exception: if a cycle finishes early and plenty of context remains, continuing
straight into a small follow-up task is fine. Do not start a *new area* on a partly-used
window.
