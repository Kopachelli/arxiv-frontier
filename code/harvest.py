"""arXiv metadata harvest for the systematic review corpus.

Normative record of the search strategy (protocol section 3). Rebuilds
data/candidates.csv and data/HARVEST_MANIFEST.md from the public arXiv API.

Usage: python code/harvest.py
"""

import csv
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone
from pathlib import Path

API = "http://export.arxiv.org/api/query"
NS = {
    "atom": "http://www.w3.org/2005/Atom",
    "opensearch": "http://a9.com/-/spec/opensearch/1.1/",
    "arxiv": "http://arxiv.org/schemas/atom",
}

CATEGORIES = ["cs.AI", "cs.CL", "cs.LG", "cs.MA", "cs.DL", "cs.CY", "cs.SE", "cs.HC"]
CAT_CLAUSE = "(" + " OR ".join(f"cat:{c}" for c in CATEGORIES) + ")"
DATE_CLAUSE = "submittedDate:[202201010000 TO 202607312359]"

def phrase(p):
    return f'(ti:"{p}" OR abs:"{p}")'

def conj(a, b):
    return f'(abs:"{a}" AND ({" OR ".join(f_abs(x) for x in b)}))'

def f_abs(x):
    return f'abs:"{x}"' if " " in x else f"abs:{x}"

AGENT_TERMS = ["agent", "agentic", "language model", "LLM"]

# Query families (protocol section 3). Keys appear in candidates.csv:matched_queries.
QUERIES = {
    # QF1 - system identity terms
    "qf1_ai_scientist": phrase("AI scientist"),
    "qf1_ai_scientists": phrase("AI scientists"),
    "qf1_co_scientist": phrase("co-scientist"),
    "qf1_auto_research_agent": phrase("autonomous research agent"),
    "qf1_research_agent": phrase("research agent"),
    "qf1_research_agents": phrase("research agents"),
    "qf1_auto_sci_discovery": phrase("autonomous scientific discovery"),
    "qf1_automated_sci_discovery": phrase("automated scientific discovery"),
    "qf1_agentic_sci_discovery": phrase("agentic scientific discovery"),
    "qf1_autonomous_experimentation": phrase("autonomous experimentation"),
    "qf1_self_driving_lab": phrase("self-driving lab"),
    "qf1_self_driving_laboratory": phrase("self-driving laboratory"),
    "qf1_autonomous_research": phrase("autonomous research"),
    "qf1_automated_research": phrase("automated research"),
    "qf1_research_automation": phrase("research automation"),
    "qf1_autonomous_scientist": phrase("autonomous scientist"),
    "qf1_agent_laboratory": phrase("agent laboratory"),
    # Supplementary (added after recall cross-check, before screening; see
    # process-log/timeline.md session 1 and data/recall-check.md):
    "qf1_deep_research": phrase("deep research"),
    "qf1_science_agent": phrase("science agent"),
    "qf1_ai_research_assistant": phrase("AI research assistant"),
    "qf1_autonomous_discovery": phrase("autonomous discovery"),
    "qf1_closed_loop_discovery": phrase("closed-loop discovery"),
    # QF2 - lifecycle-stage terms conditioned on agent/LLM vocabulary
    "qf2_hypothesis_generation": conj("hypothesis generation", AGENT_TERMS),
    "qf2_research_ideation": phrase("research ideation"),
    "qf2_scientific_ideation": phrase("scientific ideation"),
    "qf2_idea_generation_sci": conj("scientific idea generation", AGENT_TERMS),
    "qf2_automated_ideation": phrase("automated ideation"),
    "qf2_paper_generation": conj("paper generation", AGENT_TERMS),
    "qf2_scientific_writing_agent": conj("scientific writing", AGENT_TERMS),
    "qf2_experiment_design_agent": conj("experiment design", AGENT_TERMS),
    "qf2_automated_peer_review": phrase("automated peer review"),
    "qf2_automated_lit_review": phrase("automated literature review"),
    "qf2_research_idea_generation": phrase("research idea generation"),
    # QF3 - audit & integrity terms scoped to AI research
    "qf3_ai_generated_research": phrase("AI-generated research"),
    "qf3_ai_generated_papers": phrase("AI-generated papers"),
    "qf3_research_integrity_ai": conj("research integrity", AGENT_TERMS + ["artificial intelligence", "generative AI"]),
    # NB: an earlier version used conj("auditable", AGENT_TERMS); arXiv stems "auditable"
    # to audit*, exploding the query to 2,336 mostly-irrelevant hits (see
    # process-log/errors.md #1). Replaced with precise phrases:
    "qf3_auditable_ai_scientist": phrase("auditable AI scientist"),
    "qf3_auditable_agent_phrase": phrase("auditable agent"),
    "qf3_auditable_research": phrase("auditable research"),
    "qf3_ai4science_agent": conj("AI4Science", AGENT_TERMS),
    "qf3_scientific_fraud": phrase("scientific fraud"),
    "qf3_paper_mills": phrase("paper mills"),
    "qf3_research_misconduct": phrase("research misconduct"),
    "qf3_ai_generated_scientific": phrase("AI-generated scientific"),
}

PER_QUERY_CAP = 2500   # hard cap per query; truncation is reported, never silent
PAGE = 100             # arXiv API max page size
SLEEP = 3.0            # arXiv API politeness delay (seconds)

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"


def fetch(query, start):
    q = f"{query} AND {CAT_CLAUSE} AND {DATE_CLAUSE}"
    url = API + "?" + urllib.parse.urlencode({
        "search_query": q,
        "start": start,
        "max_results": PAGE,
        "sortBy": "submittedDate",
        "sortOrder": "descending",
    })
    for attempt in range(4):
        try:
            with urllib.request.urlopen(url, timeout=60) as r:
                return ET.fromstring(r.read())
        except Exception as e:
            if attempt == 3:
                raise
            print(f"    retry {attempt + 1} after error: {e}")
            time.sleep(10 * (attempt + 1))


def canonical_id(raw):
    # http://arxiv.org/abs/2607.12345v2 -> 2607.12345
    m = re.search(r"abs/([^v]+(?:v\d+)?)$", raw)
    ident = m.group(1) if m else raw
    return re.sub(r"v\d+$", "", ident)


def parse_entries(root):
    out = []
    for e in root.findall("atom:entry", NS):
        raw_id = e.findtext("atom:id", "", NS)
        title = re.sub(r"\s+", " ", e.findtext("atom:title", "", NS)).strip()
        abstract = re.sub(r"\s+", " ", e.findtext("atom:summary", "", NS)).strip()
        published = e.findtext("atom:published", "", NS)[:10]
        updated = e.findtext("atom:updated", "", NS)[:10]
        authors = "|".join(a.findtext("atom:name", "", NS) for a in e.findall("atom:author", NS))
        prim = e.find("arxiv:primary_category", NS)
        primary = prim.get("term") if prim is not None else ""
        cats = ";".join(c.get("term") for c in e.findall("atom:category", NS))
        out.append({
            "arxiv_id": canonical_id(raw_id),
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "primary_category": primary,
            "categories": cats,
            "first_submitted": published,
            "last_updated": updated,
        })
    total = root.findtext("opensearch:totalResults", "0", NS)
    return out, int(total)


def main():
    DATA.mkdir(exist_ok=True)
    papers = {}          # id -> record
    stats = []           # per-query manifest rows
    t0 = datetime.now(timezone.utc)

    for key, query in QUERIES.items():
        got, total, start = 0, None, 0
        while True:
            root = fetch(query, start)
            entries, total = parse_entries(root)
            for rec in entries:
                pid = rec["arxiv_id"]
                if pid in papers:
                    papers[pid]["matched_queries"] += f";{key}"
                else:
                    rec["matched_queries"] = key
                    papers[pid] = rec
            got += len(entries)
            start += PAGE
            time.sleep(SLEEP)
            if not entries or got >= min(total, PER_QUERY_CAP):
                break
        truncated = total > PER_QUERY_CAP
        stats.append((key, total, got, truncated))
        print(f"{key}: total={total} fetched={got}{' TRUNCATED' if truncated else ''}")

    rows = sorted(papers.values(), key=lambda r: r["first_submitted"])
    fields = ["arxiv_id", "title", "abstract", "authors", "primary_category",
              "categories", "first_submitted", "last_updated", "matched_queries"]
    with open(DATA / "candidates.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)

    with open(DATA / "HARVEST_MANIFEST.md", "w", encoding="utf-8") as f:
        f.write("# Harvest Manifest\n\n")
        f.write(f"Harvest run (UTC): {t0.isoformat()}\n\n")
        f.write(f"Window: 2022-01-01 to 2026-07-31 (submittedDate)\n\n")
        f.write(f"Categories: {', '.join(CATEGORIES)}\n\n")
        f.write(f"Unique papers after dedup: **{len(rows)}**\n\n")
        f.write("| query | api_total | fetched | truncated |\n|---|---|---|---|\n")
        for key, total, got, tr in stats:
            f.write(f"| {key} | {total} | {got} | {'YES' if tr else ''} |\n")
        f.write("\nExact query strings are defined in `code/harvest.py` (normative).\n")

    print(f"\nDone: {len(rows)} unique candidates -> data/candidates.csv")


if __name__ == "__main__":
    main()
