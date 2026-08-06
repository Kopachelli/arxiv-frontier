"""Double-code a random sample of the corpus and report per-dimension reliability.

Written 2026-07-31 in response to an external critique: screening received two independent
passes plus a stability check, while CODING — which produces every headline number — was a
single pass by one model over abstracts. That asymmetry was acknowledged in the paper but
never measured. This measures it.

  python code/coding_reliability.py sample <outdir>   # export a random sample for re-coding
  python code/coding_reliability.py score <resultsdir>

Per-dimension Cohen's kappa tells us which of the ten dimensions are load-bearing and which
are noise. A dimension with low kappa is one whose reported percentage carries measurement
error we cannot currently quantify — and saying so is more useful than not knowing.
"""

import csv
import json
import math
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
SEED = 20260731
N_SAMPLE = 150
SINGLE = ["D1", "D2", "D4", "D7_code", "D7_data", "D8", "D9"]
MULTI = ["D3", "D5", "D6"]


def cohens_kappa(pairs):
    n = len(pairs)
    if not n:
        return float("nan")
    cats = sorted({c for p in pairs for c in p})
    obs = sum(1 for a, b in pairs if a == b) / n
    m1, m2 = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    exp = sum((m1[c] / n) * (m2[c] / n) for c in cats)
    return (obs - exp) / (1 - exp) if exp != 1 else float("nan")


def jaccard(a, b):
    sa, sb = set(x for x in a.split(";") if x), set(x for x in b.split(";") if x)
    if not sa and not sb:
        return 1.0
    return len(sa & sb) / len(sa | sb) if (sa | sb) else 1.0


def sample(outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    coded = list(csv.DictReader(open(DATA / "coded-corpus.csv", encoding="utf-8")))
    cand = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "candidates.csv", encoding="utf-8"))}
    cand.update(json.loads((DATA / "expert-identified-meta.json").read_text(encoding="utf-8")))
    pick = random.Random(SEED).sample(coded, min(N_SAMPLE, len(coded)))
    papers = [{"arxiv_id": r["arxiv_id"], "title": r["title"],
               "abstract": cand[r["arxiv_id"]]["abstract"]} for r in pick]
    size = 12
    for i in range(0, len(papers), size):
        (out / f"rel-{i // size:03d}.json").write_text(
            json.dumps(papers[i:i + size], indent=1), encoding="utf-8")
    print(f"{len(papers)} papers -> {(len(papers) + size - 1) // size} batches (seed {SEED})")
    print("NOTE: the re-coder sees title+abstract only — never the original codes.")


def score(resultsdir):
    orig = {r["arxiv_id"]: r for r in csv.DictReader(
        open(DATA / "coded-corpus.csv", encoding="utf-8"))}
    redo = {}
    for f in sorted(Path(resultsdir).glob("rel-*.json")):
        try:
            for it in json.loads(f.read_text(encoding="utf-8")):
                redo[it["arxiv_id"]] = it
        except json.JSONDecodeError as e:
            print(f"  unparseable {f.name}: {e}")
    both = [(orig[p], redo[p]) for p in redo if p in orig]
    print(f"double-coded: {len(both)} papers\n")

    rows = []
    print(f'{"dimension":12s}{"agreement":>11s}{"kappa":>9s}   interpretation')
    print("-" * 68)
    for d in SINGLE:
        pairs = [(a[d], str(b.get(d, "")).upper()) for a, b in both]
        agree = sum(1 for x, y in pairs if x == y) / len(pairs)
        k = cohens_kappa(pairs)
        tag = ("substantial" if k >= 0.61 else "moderate" if k >= 0.41
               else "fair" if k >= 0.21 else "poor")
        print(f"{d:12s}{agree:>10.1%}{k:>9.2f}   {tag}")
        rows.append({"dimension": d, "type": "single", "agreement": round(agree, 3),
                     "kappa": round(k, 3), "interpretation": tag})
    for d in MULTI:
        sims = [jaccard(a[d], str(b.get(d, "")).upper()) for a, b in both]
        exact = sum(1 for a, b in both if set(a[d].split(";")) == set(
            str(b.get(d, "")).upper().split(";"))) / len(both)
        mean_j = sum(sims) / len(sims)
        tag = ("substantial" if mean_j >= 0.7 else "moderate" if mean_j >= 0.5 else "poor")
        print(f"{d:12s}{exact:>10.1%}{mean_j:>9.2f}   {tag} (multi-select: Jaccard, not kappa)")
        rows.append({"dimension": d, "type": "multi", "agreement": round(exact, 3),
                     "kappa": round(mean_j, 3), "interpretation": tag})

    with open(DATA / "coding-reliability.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["dimension", "type", "agreement", "kappa",
                                          "interpretation"])
        w.writeheader()
        w.writerows(rows)

    print("\nDIMENSIONS CARRYING HEADLINE NUMBERS:")
    for d, what in [("D6", "the 55% no-auditability figure"),
                    ("D5", "the 5% held-out and 11% real-world figures"),
                    ("D9", "the 71% human-role-unstated figure"),
                    ("D8", "the discovery/capability split")]:
        r = next(x for x in rows if x["dimension"] == d)
        print(f"  {d} -> {what}: {r['kappa']:.2f} ({r['interpretation']})")
    print("\nwrote data/coding-reliability.csv")


if __name__ == "__main__":
    {"sample": sample, "score": score}[sys.argv[1]](sys.argv[2])
