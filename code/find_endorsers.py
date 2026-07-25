"""Check candidate arXiv endorsers: which categories they actually publish in, and their
stated corresponding-author email.

arXiv endorsement is category-specific, so an author must be active in the target category
to endorse for it. Emails are read from the papers' own PDFs (authors publish them for
correspondence); nothing is guessed.

Usage: python code/find_endorsers.py
"""

import io
import re
import time
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET

NS = {"atom": "http://www.w3.org/2005/Atom",
      "arxiv": "http://arxiv.org/schemas/atom"}

CANDIDATES = {
    "2607.09195": "Takahara & Mizoguchi — Toward Auditable AI Scientists",
    "2607.17100": "Ning et al. — Auto Research for Materials",
    "2606.31273": "Li — The Calibration Turn",
    "2607.05682": "Wang — FirstResearch",
    "2606.02184": "Brzozowski & Chung — The Ghost Couple",
    "2607.10712": "Gyevnar, Kasirzadeh & Shah — Distributed Denial of Science",
    "2605.08192": "Vishwarupe et al. — NeurIPS reproducibility standards",
}
EMAIL = re.compile(r"[\w.\-+]+@[\w\-]+\.[\w.\-]+")


def meta(arxiv_id):
    url = "http://export.arxiv.org/api/query?" + urllib.parse.urlencode(
        {"id_list": arxiv_id, "max_results": 1})
    with urllib.request.urlopen(url, timeout=60) as r:
        root = ET.fromstring(r.read())
    e = root.find("atom:entry", NS)
    prim = e.find("arxiv:primary_category", NS)
    cats = [c.get("term") for c in e.findall("atom:category", NS)]
    authors = [a.findtext("atom:name", "", NS) for a in e.findall("atom:author", NS)]
    return prim.get("term"), cats, authors


def emails(arxiv_id):
    req = urllib.request.Request(f"https://arxiv.org/pdf/{arxiv_id}",
                                 headers={"User-Agent": "arxiv-frontier-endorser-check"})
    try:
        with urllib.request.urlopen(req, timeout=90) as r:
            raw = r.read()
        from pypdf import PdfReader
        reader = PdfReader(io.BytesIO(raw))
        # correspondence addresses are on the first page or in the last-page contact block
        pages = list(reader.pages)
        text = ""
        for p in pages[:2] + pages[-1:]:
            try:
                text += (p.extract_text() or "") + "\n"
            except Exception:
                pass
        found = []
        for m in EMAIL.finditer(text):
            a = m.group(0).rstrip(".,;)")
            if a not in found and "arxiv" not in a.lower():
                found.append(a)
        return found[:6]
    except Exception as e:
        return [f"(error: {type(e).__name__})"]


def main():
    for pid, label in CANDIDATES.items():
        prim, cats, authors = meta(pid)
        has_dl = "cs.DL" in cats
        print(f"\n{pid}  {label}")
        print(f"  authors : {', '.join(authors[:6])}{' ...' if len(authors) > 6 else ''}")
        print(f"  primary : {prim}   all: {', '.join(cats)}")
        print(f"  cs.DL   : {'YES — can endorse for cs.DL' if has_dl else 'no'}")
        print(f"  emails  : {', '.join(emails(pid)) or '(none found in PDF)'}")
        time.sleep(3)


if __name__ == "__main__":
    main()
