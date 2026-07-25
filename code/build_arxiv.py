"""Assemble an arXiv-ready submission directory.

arXiv compiles from a flat directory, so figure paths must not contain '../'. This copies
the LaTeX sources and figures into paper/arxiv-submission/ and rewrites the include paths.
The result is what would be uploaded; nothing is uploaded by this script.

Usage: python code/build_arxiv.py
"""

import re
import shutil
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "paper"
FIGS = ROOT / "figures"
OUT = PAPER / "arxiv-submission"

TEX = ["main.tex", "numbers.tex", "references.bib",
       "sections-intro.tex", "sections-method.tex", "sections-results.tex",
       "sections-reflexive.tex", "sections-close.tex"]


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    used = set()
    for name in TEX:
        src = PAPER / name
        text = src.read_text(encoding="utf-8")
        for m in re.finditer(r"\\includegraphics(?:\[[^\]]*\])?\{\.\./figures/([^}]+)\}", text):
            used.add(m.group(1))
        text = re.sub(r"(\\includegraphics(?:\[[^\]]*\])?\{)\.\./figures/", r"\1", text)
        (OUT / name).write_text(text, encoding="utf-8")

    missing = []
    for fig in sorted(used):
        cands = [FIGS / fig, FIGS / f"{fig}.pdf"]
        src = next((c for c in cands if c.exists()), None)
        if src is None:
            missing.append(fig)
            continue
        shutil.copy2(src, OUT / src.name)

    # arXiv needs the .bbl, since it does not run bibtex
    bbl = PAPER / "main.bbl"
    if bbl.exists():
        shutil.copy2(bbl, OUT / "main.bbl")
    else:
        missing.append("main.bbl (run bibtex first)")

    print(f"arXiv package -> {OUT}")
    for f in sorted(p.name for p in OUT.iterdir()):
        print("  ", f)
    if missing:
        print("\nMISSING:", ", ".join(missing))
    else:
        print("\ncomplete")


if __name__ == "__main__":
    main()
