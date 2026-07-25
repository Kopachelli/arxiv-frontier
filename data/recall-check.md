# Recall Cross-Check (2026-07-25)

Method: (a) membership test of 15 landmark in-scope papers known to the team (from initial
scouting + field knowledge) against the harvested pool; (b) keyword searches on OpenAlex and
Semantic Scholar compared against the pool.

## Known-set membership (before supplementary queries)

13/15 present. Misses:
- 2606.02184 (Ghost Couple) — vocabulary outlier ("ghost-authored records").
- 2605.28102 (Training Stratigraphy) — autoethnographic vocabulary.
Both added via the expert-identified route (`data/expert-identified.csv`), reported in the
PRISMA flow as "records identified through other methods". Supplementary integrity-vocabulary
queries were also added (paper mills, scientific fraud, research misconduct, AI-generated
scientific) — these broaden coverage of that subliterature generally, though they do not
catch these two specific papers.

## Supplementary queries added before screening

Recall probing surfaced field vocabulary the v1 query set under-covered, most importantly
**"deep research"** (343 in-window hits; the 2025–26 term for autonomous research agents),
plus science agent, AI research assistant, autonomous discovery, closed-loop discovery,
automated literature review, research idea generation, and four integrity terms. All counts
in `data/HARVEST_MANIFEST.md` after the final run.

## Cross-source finding (for Limitations)

OpenAlex sampling shows flagship bio-domain autonomous-science systems (e.g., Biomni,
SpatialAgent) publish on **bioRxiv**, not arXiv — outside our primary source. The review's
corpus is therefore best interpreted as mapping the arXiv-visible (CS-centric) field;
domain-venue systems (esp. biology wet-lab agents) are under-represented. Reported honestly
in the paper's Limitations.

Semantic Scholar API returned empty for our queries at check time (possible rate limiting);
OpenAlex relevance ranking was noisy for phrase-less queries. The known-set membership test
is the stronger recall signal.
