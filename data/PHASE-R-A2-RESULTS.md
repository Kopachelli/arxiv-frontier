# Phase R — Area 2 (auditability and integrity tooling): results

49 papers proposing auditability mechanisms for AI-conducted research — inspectable traces,
claim-to-evidence provenance, hypothesis-evolution protocols, calibration and claim-licensing
frameworks, reproduction standards, governance norms. 352 claims assessed against the papers'
own repositories. Full ledger: `data/phase-r-ledger-A2_auditability.csv`.

This area supports a question no other area can ask: **do papers advocating a standard meet
it themselves?** That question is easy to ask unfairly, so the verification prompt carried an
explicit instruction that scoring a paper harshly for advocating a standard it does not meet
is a bias rather than rigour, that position papers with nothing to implement are correctly
`UNVERIFIABLE`, and that a `NOT_LOCATED` is a statement about our search and never a charge
of hypocrisy.

---

## Overall verdicts

| verdict | n | share |
|---|---|---|
| `SUPPORTED` | 188 | 53.4% |
| `UNVERIFIABLE` | 72 | 20.5% |
| `NOT_LOCATED` | 54 | 15.3% |
| `DIVERGENT` | 38 | 10.8% |
| `CONTRADICTED` | 0 | 0.0% |

## The good news, stated first because it is the larger finding

**The mechanisms these papers propose largely exist.**

| claim type | n | `SUPPORTED` | `NOT_LOCATED` |
|---|---|---|---|
| ARTIFACT_RELEASE | 47 | **72%** | 6% |
| **MECHANISM_IMPLEMENTED** | 117 | **62%** | **6%** |
| METHOD_COMPONENT | 58 | 53% | 16% |
| SELF_APPLICATION | 49 | 43% | 22% |
| DATASET | 30 | 43% | 27% |
| NUMERIC_RESULT | 51 | 33% | 31% |

Of 117 claims about a proposed auditability mechanism, 62% were located in the artifact and
only 6% could not be found. This subfield ships what it designs, and releases what it says it
releases (72% on artifact-release claims, the highest rate we have measured anywhere). If the
expected story was that auditability researchers merely theorise, the data does not support
it.

## Self-application: about half meet their own standard

| verdict | n |
|---|---|
| `SUPPORTED` | 21 |
| `NOT_LOCATED` | 11 |
| `DIVERGENT` | 9 |
| `UNVERIFIABLE` | 8 (position papers with nothing to implement) |

Excluding the 8 where the check was impossible, **21 of 41 (51%) visibly meet the standard
they advocate**.

Examples of papers that do, with the evidence:

- A paper arguing that literature-based discovery is hard to replicate ships
  `requirements.txt` with ~116 pinned versions and a SHA256-pinned model URL.
- A survey demanding "verifiable citations" ships a project table with a populated URL column
  for every row.
- A paper advocating transparent, reproducible AI-assisted research ships both the
  data-generating notebook and the resulting cohort data.

And papers where we could not find it — recorded as searches, not accusations:

- A paper arguing scientific knowledge must be machine-readable and traceable releases a
  ~1,100-row journal title/URL list; we found no traceability layer in the two content files.
- A paper whose central position is that research is credible only with executable
  implementation has an 8-file repository (README, CONTRIBUTING, LICENSE, four images) with no
  script or notebook.
- A paper criticising deep-research systems for "obscuring intermediate decisions" — we
  searched its full repository tree and did not locate released traces.

We report these as measured facts about our search of a public artifact. Several have obvious
innocent explanations, including that the artifact is a curated index rather than a system,
and the right of reply exists precisely for this.

## The finding that replicates across areas

Area 1 (discovery papers) and Area 2 (auditability papers) share no papers, differ in subject
matter, and were verified independently. The numeric-result pattern is nearly identical:

| claim type | A1 supported | A2 supported |
|---|---|---|
| ARTIFACT_RELEASE | 59% (n=39) | 72% (n=47) |
| METHOD_COMPONENT | 62% (n=60) | 53% (n=58) |
| DATASET | 52% (n=23) | 43% (n=30) |
| **NUMERIC_RESULT** | **36%** (n=103) | **33%** (n=51) |
| NUMERIC_RESULT `NOT_LOCATED` | 29% | 31% |

**Reported numbers are the least locatable class of claim in both areas, at almost the same
rate.** Descriptions of machinery are found roughly twice as often as the quantities that
machinery supposedly produced. Two independent areas is not proof of a field-wide law, but it
is the first evidence that this is a property of the literature rather than of one subfield —
and it is the pattern the remaining seven areas will either confirm or break.

## Limits

- 7 of 49 papers had no readable repository tree and contribute mainly `UNVERIFIABLE` claims.
- `SELF_APPLICATION` requires interpreting what a paper advocates, which is the most
  judgement-laden verdict in the programme. Each one records the standard it applied in the
  claim text, so a reader can disagree with the reading and not merely the finding.
- Verification reflects repository state at retrieval; timestamps are recorded per paper and
  disputed claims will be re-checked against both states at reply.
- No code was executed. Every claim records the level actually reached.
