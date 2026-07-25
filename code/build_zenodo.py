"""Assemble the Zenodo deposit bundle and its metadata.

Produces paper/zenodo/ containing everything to upload, plus zenodo-metadata.json in the
shape Zenodo's deposition API expects. Nothing is uploaded by this script; depositing
requires the human author's own account and must be done by him.

Usage: python code/build_zenodo.py
"""

import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "paper" / "zenodo"

DESCRIPTION = """
<p><strong>A systematic map of 811 papers on autonomous AI research systems (January 2024 –
July 2026), conducted by a frontier language model, with its own research process logged and
analysed as data.</strong></p>

<p><em>Authorship.</em> This work was jointly produced by a human researcher and an AI system.
Claude Fable 5 (Anthropic) proposed the research direction, wrote the review protocol and
codebook, wrote all software, executed the search, screening, coding and analysis, generated
the figures, and drafted the manuscript. Khristian Kopachelli framed the project, made the
scope decisions, overruled the AI's judgment where he disagreed (one such reversal changed the
corpus by 183 papers), contributed the two conceptual arguments in the Discussion, and takes
responsibility for the published work. This record lists both as creators. The companion
arXiv version lists only the human author, because arXiv policy does not permit AI systems to
be named as authors; the two records cross-reference each other and describe the same
collaboration.</p>

<p><em>Findings.</em> Quarterly output in this literature grew roughly fortyfold in nine
quarters. 71% of papers report benchmark metrics, but only 5% re-test a result outside the
loop that produced it, 55% provide no auditability mechanism of any kind, and 71% never state
what humans did. Conditioning on claim strength reveals a dissociation: papers claiming the AI
produced new scientific knowledge validate their <em>results</em> better than average (50%
report external validation versus 11% corpus-wide) while exposing their <em>process</em> worse
(64% provide no auditability mechanism versus 55%). This field validates outputs better than
it exposes process, and the gap is widest where its claims are strongest.</p>

<p><em>Reflexive component.</em> Because the review was conducted by the class of system it
studies, the process was logged rather than smoothed. Two frontier models screening the same
corpus under the same protocol agreed on 83.3% of decisions (Cohen's kappa 0.71), with
disagreements clustering on seven boundary classes where the field has not settled what counts
as an AI scientist — forcing a documented protocol amendment mid-review. Six AI failures are
reported with measured rates, including a workflow that reported success having performed no
work, silent item-dropping in structured extraction at 0.4–0.5%, a pipeline defect that fed
empty inputs to a reasoning step, and a draft thesis contradicted by the authors' own data.</p>

<p><em>Contents.</em> Paper (PDF), full candidate corpus and both layers of screening
decisions with per-paper justifications, the coded corpus, mechanical full-text
artifact-verification results for all 811 papers, all analysis and figure code, the review
protocol with amendments, and the three contemporaneous process logs.</p>

<p><em>A note on provenance.</em> Brzozowski &amp; Chung (arXiv:2606.02184) document 1,655
Zenodo records bearing real DOIs, fabricated authors, and backdated timestamps. This deposit
is intended as the inverse in every respect: an accountable human author, an AI contributor
named as exactly what it is, unmanipulated timestamps, released underlying data, and a
complete log of how the work was produced including its failures.</p>
"""

METADATA = {
    "metadata": {
        "upload_type": "publication",
        "publication_type": "preprint",
        "title": ("When the Instrument Studies Itself: A Systematic Map of Autonomous AI "
                  "Research Systems (2024-2026), Conducted by a Frontier Language Model"),
        "creators": [
            {"name": "Kopachelli, Khristian", "affiliation": "Independent researcher"},
            {"name": "Claude Fable 5", "affiliation": "Anthropic"},
        ],
        "description": DESCRIPTION.strip(),
        "access_right": "open",
        "license": "cc-by-4.0",
        "keywords": [
            "AI scientist", "autonomous research agents", "systematic review",
            "research integrity", "auditability", "reproducibility", "meta-research",
            "scientometrics", "human-AI collaboration", "large language models",
        ],
        "notes": ("Code is released under the MIT License; data, text and figures under "
                  "CC BY 4.0. See LICENSE in the accompanying repository."),
        "related_identifiers": [
            {"relation": "isSupplementedBy",
             "identifier": "https://github.com/Kopachelli/arxiv-frontier",
             "resource_type": "software"},
        ],
    }
}

BUNDLE = [
    ("paper/main.pdf", "when-the-instrument-studies-itself.pdf"),
    ("README.md", "README.md"),
    ("LICENSE", "LICENSE"),
]
ZIP_DIRS = ["data", "code", "protocol", "process-log", "figures", "notes"]


def main():
    if OUT.exists():
        shutil.rmtree(OUT)
    OUT.mkdir(parents=True)

    missing = []
    for src, dst in BUNDLE:
        p = ROOT / src
        if p.exists():
            shutil.copy2(p, OUT / dst)
        else:
            missing.append(src)

    zpath = OUT / "arxiv-frontier-artifacts.zip"
    with zipfile.ZipFile(zpath, "w", zipfile.ZIP_DEFLATED) as z:
        for d in ZIP_DIRS:
            base = ROOT / d
            if not base.exists():
                missing.append(d)
                continue
            for f in sorted(base.rglob("*")):
                if f.is_file() and "__pycache__" not in f.parts:
                    z.write(f, f.relative_to(ROOT).as_posix())

    (OUT / "zenodo-metadata.json").write_text(
        json.dumps(METADATA, indent=2), encoding="utf-8")

    print(f"Zenodo bundle -> {OUT}")
    for f in sorted(OUT.iterdir()):
        print(f"   {f.name}  ({f.stat().st_size / 1024:.0f} KB)")
    if missing:
        print("\nMISSING:", ", ".join(missing))


if __name__ == "__main__":
    main()
