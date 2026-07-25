# Publication steps — what Khristian does, in order

Sequencing decided 2026-07-25: **Zenodo → DOI → endorsement → arXiv → repository public.**
Everything the AI can prepare is prepared. The remaining actions require your accounts, so
they are yours to perform.

---

## Step 1 — Zenodo deposit ✅ DONE 2026-07-26

**Published: <https://doi.org/10.5281/zenodo.21577093>**

Both authors listed as creators (Kopachelli, Khristian · Claude Fable 5 (Anthropic)),
CC BY 4.0, four files, repository link, joint-authorship statement in the description.
Verified independently after publication. The paper PDF carries this DOI in §9.

*Original instructions retained below for the record.*

## Step 1 (original) — Zenodo deposit

Everything to upload is in `paper/zenodo/`:

| file | what it is |
|---|---|
| `when-the-instrument-studies-itself.pdf` | the paper, 19 pages |
| `arxiv-frontier-artifacts.zip` | data, code, protocol, process logs, figures, notes (1.5 MB) |
| `README.md`, `LICENSE` | context and licensing |
| `zenodo-metadata.json` | the metadata, ready to paste field by field |

1. Sign in at <https://zenodo.org> → **New upload**.
2. Upload the four files (not the JSON — that is your reference for filling the form).
3. Fill the form from `zenodo-metadata.json`:
   - Upload type: **Publication → Preprint**
   - Title, description, keywords: copy verbatim
   - **Creators: both of us** — "Kopachelli, Khristian" (Independent researcher) and
     "Claude Fable 5" (Anthropic). This is the whole point of the Zenodo record: it carries
     the joint authorship that arXiv's policy does not allow.
   - License: **CC BY 4.0**
   - Related identifier: the GitHub URL, relation *is supplemented by*
4. Publish. **Copy the DOI.**

Once you have the DOI, tell me and I will insert it into the paper's availability section and
rebuild before anything goes to arXiv.

## Step 2 — Endorsement request (you; draft ready)

`paper/endorsement-request.md` has the candidate endorsers, why each was chosen, and a draft
message. Read it before sending — it discloses the AI's role up front, deliberately, and you
should be comfortable with that framing since it is your name on the request.

Ask one person at a time. If two weeks pass without a reply, move to the next.

## Step 3 — arXiv submission (you, once endorsed; package ready)

`paper/arxiv-submission/` compiles standalone (verified: 19 pages, flat figure paths,
pre-built `main.bbl` since arXiv does not run bibtex). Upload the whole directory contents.

- Primary category: **cs.DL**; cross-list **cs.AI**, **cs.CY**
- The abstract for the web form is in `main.tex`; paste the plain-text version
- Licence: CC BY 4.0, matching the Zenodo record

## Step 4 — Make the repository public (me, on your word)

The repo is currently **private**. Say the word once arXiv is live and I will flip it, so the
links in both records resolve.

---

## Before any of this: things worth your eyes

1. **Read §3.5 and §6.** §3.5 is the minimal-intervention condition — I rewrote it after your
   explanation, and you should check that it represents your reasoning accurately rather than
   my paraphrase of it. §6 puts two arguments in your name; make sure you actually hold them
   as stated.
2. **The contribution statement (§8)** describes what each of us did. If anything there is
   wrong or overstated in either direction, it needs fixing before submission — it is the part
   of the paper most likely to be quoted.
3. **You are the accountable author.** The AI wrote the software, ran the analysis, and drafted
   the text; a mistake anywhere in that chain is published under your name. The verification
   layers exist to make that risk small and inspectable, not zero.
