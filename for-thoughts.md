# For thoughts — Khristian's inbox

Drop anything here between sessions: half-formed ideas, objections, critiques from others,
things that felt wrong, questions, papers worth a look. No structure required. Claude reads
this file at the start of every session and answers each item in writing, including where it
disagrees.

**How items leave this file.** Nothing is deleted. When an item is dealt with it moves to
Resolved with a note saying where it ended up, so the reasoning stays findable.

| destination | when |
|---|---|
| `protocol/amendments.md` | it changes a rule already in force |
| `protocol/*.md` | it changes how we work going forward |
| `notes/*.md` | a concept worth developing, not yet a decision |
| the paper | an argument or a finding |
| Linear | a unit of work |
| stays here, answered | a question — the answer is the artifact |

---

## Open

*(empty — add anything, in any form)*

---

## Resolved

### 2026-07-31 — External critique of paper v2 → **v3 published**

A detailed outside reading of v2. Seven substantive points, all acted on. This was the first
substantive error in the project found from **outside**, and the most valuable single input
the paper has received.

| # | point | outcome |
|---|---|---|
| 1 | Headline dissociation overstated for $n=58$ — auditability and code-release intervals contain the corpus rate | **Accepted, corrected.** Claim is now "audits *no better*, validates far better". Wilson intervals throughout; Table 1 caption states which comparisons hold and why. `errors.md` #14 |
| 2 | Redundancy is on screening, but *coding* produces every headline number | **Accepted.** Double-coding reliability study is the next task |
| 3 | Sensitivity analysis available but not run | **Done.** Three corpus definitions; nothing moves >4pp, auditability <1pp. Limitation → demonstrated robustness |
| 4 | §6 reads as AI deference to the human co-author | **Accepted.** Explicit caution added asking readers to weigh the arguments, not the convergence; "settles the question" softened |
| 5 | Corpus-count inconsistencies (807 vs 811, artifact-check totals) | **Fixed.** Counts reconciled explicitly in method |
| 6 | Missing PRISMA / evidence-synthesis lineage | **Fixed.** PRISMA 2020 cited; method positioned as adapted, with AI-specific departures marked |
| 7 | Abstract oversells rater independence | **Fixed.** "Two models from the same family — not independent raters, and we do not treat them as such" |
| — | v1 metadata (811 papers) already circulating via aggregators | **Noted in §10.** Concept DOI resolves to current version |
| — | No arXiv ID — is it the endorsement barrier? | **Yes.** Two endorsement drafts sit unsent in Gmail (Takahara & Mizoguchi; Ning et al.), both cite the live DOI. Sending is Khristian's call |

**The critic's framing was right on the thing that mattered most:** we committed, in our own
headline, the exact failure the paper charges the literature with — evidence not matched to
the strength of the claim it was asked to carry — while the data to catch it sat released in
the repository. A reader could recompute, and did. That is the release policy working.

*Not yet acted on:* the suggestion to split the unmarked-imagination conjecture into its own
paper. It is already the organising frame of the Phase R programme
(`notes/unmarked-hypothesis.md` §5, option C), so it will get its own treatment there with
evidence attached. Revisit once Phase R's cross-cutting papers exist.
