"""Check that every custom macro used in the paper is defined in paper/numbers.tex.

An undefined macro is the most likely way a data-driven paper breaks, and it fails
silently in some LaTeX configurations. Run before any build or submission.

Usage: python code/check_macros.py
"""

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "paper"

# macros provided by LaTeX/packages rather than by us
KNOWN = {
    "documentclass", "usepackage", "newcommand", "input", "title", "author", "date",
    "thanks", "maketitle", "begin", "end", "section", "subsection", "subsubsection",
    "paragraph", "label", "ref", "cite", "citep", "citet", "textbf", "textit", "emph",
    "texttt", "url", "includegraphics", "caption", "centering", "item", "itemsep",
    "bibliographystyle", "bibliography", "noindent", "large", "normalsize", "normalfont",
    "bfseries", "titleformat", "thesection", "thesubsection", "kappa", "geometry",
    "hspace", "vspace", "textwidth", "linewidth", "footnote", "quad", "qquad", "\\",
    "emph", "mathrm", "text", "times", "leq", "geq", "approx", "sim", "%", "&", "#",
    "_", "$", "{", "}", "toprule", "midrule", "bottomrule", "multicolumn", "hline",
    "subsection*", "section*", "protect", "ldots", "dots", "and", "e", "colon",
    "definecolor", "color", "textcolor", "hidelinks", "natbib", ",",
}


def main():
    defined = set()
    numbers = PAPER / "numbers.tex"
    if numbers.exists():
        defined = set(re.findall(r"\\newcommand\{\\(\w+)\}", numbers.read_text(encoding="utf-8")))

    used = {}
    for tex in sorted(PAPER.glob("*.tex")):
        if tex.name == "numbers.tex":
            continue
        text = tex.read_text(encoding="utf-8")
        text = re.sub(r"(?m)^\s*%.*$", "", text)
        for m in re.finditer(r"\\([A-Za-z]+)", text):
            used.setdefault(m.group(1), set()).add(tex.name)
        defined |= set(re.findall(r"\\newcommand\{\\(\w+)\}", text))

    missing = {k: v for k, v in used.items() if k not in defined and k not in KNOWN}
    unused = defined - set(used) - {"nExpert"}

    print(f"{len(defined)} macros defined, {len(used)} command names used")
    if missing:
        print(f"\nUNDEFINED ({len(missing)}):")
        for k, files in sorted(missing.items()):
            print(f"  \\{k}  <- {', '.join(sorted(files))}")
    if unused:
        print(f"\ndefined but unused ({len(unused)}): {', '.join(sorted(unused))}")
    if missing:
        sys.exit(1)
    print("\nall macros resolve")


if __name__ == "__main__":
    main()
