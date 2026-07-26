# Phase R naming policy — decided 2026-07-25, before any verification was run

**Why this exists.** The policy on identifying papers whose claims are not supported by their
own artifacts was fixed *before* we looked at a single repository, so that it could not be
shaped by what we found or by who the authors turned out to be. This document is timestamped
in git history for that reason.

**Decision (Khristian Kopachelli, with the AI's recommendation): papers are named, with
protections.**

## 1. Papers are identified

Each verified paper appears in a public ledger by title and arXiv ID, with its per-claim
classification. Aggregate-only reporting was rejected: it would make our findings
unfalsifiable, since no reader could check whether we judged correctly — which contradicts
the argument this entire programme makes.

## 2. Vocabulary is neutral and describes what we observed, not what we infer

The classification vocabulary is fixed here and may not be replaced by stronger language:

| code | meaning |
|---|---|
| `SUPPORTED` | the claim is reproducible from, or directly evidenced by, the artifact |
| `DIVERGENT` | the artifact addresses the claim but yields a materially different value |
| `NOT_LOCATED` | we could not locate evidence for the claim in the artifact |
| `CONTRADICTED` | the artifact contains evidence inconsistent with the claim |
| `UNVERIFIABLE` | repository missing, private, empty, or non-executable in our environment |

**`NOT_LOCATED` never means fabrication.** The overwhelmingly likely explanations are mundane:
a repository moved, a script rotted, a config was undocumented, a result lives in a branch or
a notebook we did not find, or our own procedure was inadequate. We will say this every time
the number is reported, and no press-style framing ("papers caught fabricating") is permitted
in any output of this programme.

## 3. Authors are notified with a right of reply before publication

Every named paper's corresponding author is contacted with our per-claim findings and given a
reasonable period to respond. Responses are published alongside our results, unedited. Where
an author demonstrates our verification was wrong, we correct the ledger and record the
correction rather than quietly amending it.

**Timing — decided 2026-07-26 (Khristian).** Authors are contacted **once, after all nine
areas are verified**, not area by area. Reasons, recorded now so the choice is not
re-litigated later:

- A paper may appear in only one area, but our verification method will have improved across
  the programme. Contacting everyone at the same maturity level treats all authors alike.
- Per-area contact would leak partial findings before the cross-cutting analyses exist, and
  an author would be replying to a claim whose context is not yet written.
- It concentrates the correction window: replies arrive together, are adjudicated together,
  and every ledger is updated once rather than drifting.

The cost is that the interval between verification and notification is longer, and a
repository may change in between. We therefore record the verification date and the commit
or retrieval timestamp for every paper, and re-check any claim an author disputes against
the state at the time we looked *and* the state at reply.

## 4. Our own method is on the record

The verification procedure, scripts, environment, and full claim ledger are released, so that
our verdicts are as checkable as we are asking theirs to be. Any claim we mark `NOT_LOCATED`
must be accompanied by the specific search we performed.

## 5. We go first

**Paper 1 of this programme is verified by the same procedure and appears as the first entry
in the ledger.** If our own claims are not locatable in our own released artifacts, that is
published with the same prominence as anyone else's. We are not in a position to ask a field
to accept verification we have not accepted ourselves.

## 6. Scope limit

This programme verifies correspondence between claims and released artifacts. It does not
investigate authors, assess intent, or make findings of misconduct, and no output of this
programme will characterise any author's conduct.
