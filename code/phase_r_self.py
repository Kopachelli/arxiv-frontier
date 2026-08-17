"""Phase R, "we go first": prepare Paper 1 for verification by the same procedure.

  python code/phase_r_self.py <outdir>

Naming policy §5 requires that Paper 1 of this programme be verified by the procedure it
applies to everyone else, and appear as the first entry in the ledger. This builds the same
input package the area verifiers received — paper text plus a complete repository listing —
so the only difference between how we treat ourselves and how we treat others is the subject.

Two departures from `phase_r_area.py prepare`, both forced and both recorded:

1. The paper has no arXiv ID yet (endorsement pending), so its text comes from the local
   LaTeX sources rather than a fetched PDF. The sources are what the released artifact
   contains, so this is if anything the stricter input.
2. The repository is this one. It cannot be blinded — it carries the author's name — so
   independence is sought by adversarial instruction and multiple verifiers instead.
"""

import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PAPER = ROOT / "paper"
REPO_URL = "https://github.com/Kopachelli/arxiv-frontier"

SECTIONS = ["main.tex", "sections-intro.tex", "sections-method.tex",
            "sections-results.tex", "sections-reflexive.tex", "sections-close.tex"]


def tracked_files():
    """Exactly what is released: git's own index, not a filesystem walk."""
    out = subprocess.run(["git", "ls-files"], cwd=ROOT, capture_output=True,
                         text=True, check=True).stdout
    return sorted(p for p in out.splitlines() if p.strip())


def main(outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)

    text = []
    for name in SECTIONS:
        p = PAPER / name
        if p.exists():
            text.append(f"%%%%% ===== {name} ===== %%%%%\n"
                        + p.read_text(encoding="utf-8", errors="replace"))
    numbers = (PAPER / "numbers.tex").read_text(encoding="utf-8", errors="replace")

    files = tracked_files()
    head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=ROOT,
                          capture_output=True, text=True, check=True).stdout.strip()

    pkg = {
        "arxiv_id": "PAPER-1-SELF",
        "title": "When the Instrument Studies Itself",
        "archetype": "FULL_PIPELINE",
        "paper_text": "\n\n".join(text),
        "numbers_tex": numbers,
        "repository": {
            "owner": "Kopachelli", "repo": "arxiv-frontier", "url": REPO_URL,
            "commit": head, "n_files": len(files), "files": files,
            "readme": (ROOT / "README.md").read_text(encoding="utf-8", errors="replace")[:20000],
        },
    }
    (out / "SELF-000.json").write_text(json.dumps(pkg, indent=1), encoding="utf-8")
    print(f"Paper 1 prepared: {len(files)} tracked files at {head[:9]}")
    print(f"  paper text {len(pkg['paper_text']):,} chars, numbers.tex {len(numbers):,} chars")
    print(f"  -> {out / 'SELF-000.json'}")


if __name__ == "__main__":
    main(sys.argv[1])
