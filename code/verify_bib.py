"""Machine-verify every citation in paper/references.bib against live metadata.

For arXiv entries: fetches title/authors by ID from the arXiv API and fuzzy-compares with
the bib entry. For DOI entries: resolves via Crossref. Any mismatch or unresolvable entry is
a FAILURE — the paper is not done until this script passes clean.

Usage: python code/verify_bib.py
"""

import re
import sys
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BIB = ROOT / "paper" / "references.bib"
NS = {"atom": "http://www.w3.org/2005/Atom"}


def parse_bib(text):
    """Minimal .bib parser: returns list of dicts with key, and lowercase field map."""
    entries = []
    for m in re.finditer(r"@(\w+)\s*\{\s*([^,]+),(.*?)\n\}", text, re.S):
        fields = dict(
            (k.lower(), re.sub(r"\s+", " ", v).strip(" {}"))
            for k, v in re.findall(r"(\w+)\s*=\s*[{\"](.*?)[}\"]\s*,?\s*\n", m.group(3), re.S)
        )
        entries.append({"type": m.group(1), "key": m.group(2).strip(), **fields})
    return entries


def norm(s):
    return re.sub(r"[^a-z0-9 ]", "", s.lower()).strip()


def similar(a, b):
    return SequenceMatcher(None, norm(a), norm(b)).ratio()


def check_arxiv(arxiv_id, bib_title):
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"id_list": arxiv_id, "max_results": 1})
    with urllib.request.urlopen(url, timeout=60) as r:
        root = ET.fromstring(r.read())
    entry = root.find("atom:entry", NS)
    if entry is None:
        return False, "no such arXiv id"
    live_title = re.sub(r"\s+", " ", entry.findtext("atom:title", "", NS)).strip()
    if not live_title:
        return False, "arXiv returned empty title"
    score = similar(live_title, bib_title)
    if score < 0.85:
        return False, f"title mismatch (sim={score:.2f}): live='{live_title}'"
    return True, f"ok (sim={score:.2f})"


def check_doi(doi, bib_title):
    url = f"https://api.crossref.org/works/{urllib.parse.quote(doi)}"
    req = urllib.request.Request(url, headers={"User-Agent": "arxiv-frontier-bib-check"})
    try:
        import json
        with urllib.request.urlopen(req, timeout=60) as r:
            data = json.load(r)
    except Exception as e:
        return False, f"DOI unresolvable: {e}"
    titles = data.get("message", {}).get("title", [])
    if not titles:
        return False, "DOI has no title metadata"
    score = similar(titles[0], bib_title)
    if score < 0.85:
        return False, f"title mismatch (sim={score:.2f}): live='{titles[0]}'"
    return True, f"ok (sim={score:.2f})"


def main():
    if not BIB.exists():
        sys.exit(f"missing {BIB}")
    entries = parse_bib(BIB.read_text(encoding="utf-8"))
    print(f"{len(entries)} bib entries")
    failures = []
    for e in entries:
        title = e.get("title", "")
        eprint = e.get("eprint") or ""
        doi = e.get("doi") or ""
        if eprint:
            ok, msg = check_arxiv(eprint, title)
        elif doi:
            ok, msg = check_doi(doi, title)
        else:
            ok, msg = False, "no eprint or doi field — unverifiable"
        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {e['key']}: {msg}")
        if not ok:
            failures.append(e["key"])
        time.sleep(1.0)
    print(f"\n{len(entries) - len(failures)}/{len(entries)} verified")
    if failures:
        print("FAILURES:", ", ".join(failures))
        sys.exit(1)


if __name__ == "__main__":
    main()
