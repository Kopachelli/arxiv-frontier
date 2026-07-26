"""Phase V: build blinded verification batches and score the results.

  python code/phase_v.py build <outdir>     # export Arm 1 + Arm 2 batches and key files
  python code/phase_v.py score <resultsdir> # score both arms

Blinding is enforced here: exported batches carry no model names, no provenance, and no
reference to the study. The item -> producing-model mapping and the corruption ledger live
in key files that are never exported to a verifier.
"""

import csv
import json
import random
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DATA = ROOT / "data"
VDIR = DATA / "phase-v"
SEED = 20260726
N_ARM1 = 150          # papers re-screened + re-coded from scratch by each model
N_ARM2 = 200          # decisions audited by each model
CORRUPT_RATE = 0.10

CODE_ALT = {
    "D1": ["SYSTEM", "BENCHMARK", "FRAMEWORK", "POSITION", "SURVEY", "CASE_STUDY"],
    "D2": ["L0_ASSISTIVE", "L1_STAGE", "L2_PIPELINE", "L3_CLOSED_LOOP", "L4_FULL"],
    "D8": ["DISCOVERY", "CAPABILITY", "METHOD", "CONCEPTUAL"],
}


def load():
    cand = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "candidates.csv", encoding="utf-8"))}
    cand.update(json.loads((DATA / "expert-identified-meta.json").read_text(encoding="utf-8")))
    l1 = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "screening-decisions.csv", encoding="utf-8"))}
    fin = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "screening-final.csv", encoding="utf-8"))}
    coded = {r["arxiv_id"]: r for r in csv.DictReader(open(DATA / "coded-corpus.csv", encoding="utf-8"))}
    return cand, l1, fin, coded


def build(outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    VDIR.mkdir(parents=True, exist_ok=True)
    cand, l1, fin, coded = load()
    rng = random.Random(SEED)

    # ---------- Arm 1: independent re-doing ----------
    # Provenance = which Layer-1 pass the paper's original decision came from. We use papers
    # where the two passes AGREED, so "the original decision" is unambiguous, and we attribute
    # each item to a producing model by alternating assignment (recorded in the key).
    agreed = [p for p, r in l1.items() if r["agreement"] == "agree" and p in fin]
    arm1_ids = rng.sample(sorted(agreed), min(N_ARM1, len(agreed)))
    arm1_key = []
    arm1_items = []
    for i, pid in enumerate(arm1_ids):
        producer = "fable" if i % 2 == 0 else "opus"
        orig = l1[pid][f"pass{'A' if producer == 'fable' else 'B'}_decision"]
        arm1_key.append({"arxiv_id": pid, "producer": producer,
                         "original_decision": orig,
                         "original_reason": l1[pid][f"pass{'A' if producer == 'fable' else 'B'}_reason"],
                         "final_decision": fin[pid]["final_decision"]})
        arm1_items.append({"item_id": f"a1-{i:04d}", "arxiv_id": pid,
                           "title": cand[pid]["title"], "abstract": cand[pid]["abstract"]})
    _write_batches(out, "arm1", arm1_items, 15)
    (VDIR / "arm1-key.csv").write_text(_csv(arm1_key), encoding="utf-8")

    # ---------- Arm 2: audit, with mechanically corrupted ground truth ----------
    pool = [p for p in coded if p in fin]
    arm2_ids = rng.sample(sorted(pool), min(N_ARM2, len(pool)))
    n_corrupt = int(round(len(arm2_ids) * CORRUPT_RATE))
    corrupt_ids = set(rng.sample(arm2_ids, n_corrupt))

    arm2_key, arm2_items = [], []
    for i, pid in enumerate(arm2_ids):
        f, c = fin[pid], coded[pid]
        decision, reason = f["final_decision"], f["final_reason"]
        d1, d2, d8 = c["D1"], c["D2"], c["D8"]
        kind = "none"
        if pid in corrupt_ids:
            kind = rng.choice(["FLIP", "REASON_SWAP", "CODE_DRIFT"])
            if kind == "FLIP":
                decision = "exclude" if decision == "include" else "include"
            elif kind == "REASON_SWAP":
                reason = rng.choice([r for r in
                                     ["IC1", "IC2", "IC3", "EC1", "EC2", "EC6_ASSISTIVE",
                                      "EC7_HUMAN_AI_USE", "EC8_GENERIC_ANALYSIS"]
                                     if r != reason])
            else:
                dim = rng.choice(["D1", "D2", "D8"])
                cur = {"D1": d1, "D2": d2, "D8": d8}[dim]
                alt = rng.choice([v for v in CODE_ALT[dim] if v != cur])
                if dim == "D1":
                    d1 = alt
                elif dim == "D2":
                    d2 = alt
                else:
                    d8 = alt
        arm2_key.append({"item_id": f"a2-{i:04d}", "arxiv_id": pid, "corruption": kind})
        arm2_items.append({
            "item_id": f"a2-{i:04d}", "arxiv_id": pid,
            "title": cand[pid]["title"], "abstract": cand[pid]["abstract"],
            "recorded_decision": decision, "recorded_reason": reason,
            "recorded_paper_type": d1, "recorded_autonomy": d2, "recorded_claim_strength": d8,
        })
    _write_batches(out, "arm2", arm2_items, 20)
    (VDIR / "arm2-key.csv").write_text(_csv(arm2_key), encoding="utf-8")

    print(f"Arm 1: {len(arm1_items)} items ({len(arm1_items)//15 + 1} batches)")
    print(f"Arm 2: {len(arm2_items)} items, {n_corrupt} corrupted "
          f"({dict(Counter(k['corruption'] for k in arm2_key if k['corruption'] != 'none'))})")
    print(f"keys -> {VDIR} (never exported to verifiers)")


def _write_batches(out, tag, items, size):
    for i in range(0, len(items), size):
        (out / f"{tag}-{i // size:03d}.json").write_text(
            json.dumps(items[i:i + size], indent=1), encoding="utf-8")


def _csv(rows):
    if not rows:
        return ""
    import io
    buf = io.StringIO()
    w = csv.DictWriter(buf, fieldnames=list(rows[0].keys()), lineterminator="\n")
    w.writeheader()
    w.writerows(rows)
    return buf.getvalue()


def cohens_kappa(pairs):
    n = len(pairs)
    if not n:
        return float("nan")
    cats = sorted({c for p in pairs for c in p})
    obs = sum(1 for a, b in pairs if a == b) / n
    m1, m2 = Counter(a for a, _ in pairs), Counter(b for _, b in pairs)
    exp = sum((m1[c] / n) * (m2[c] / n) for c in cats)
    return (obs - exp) / (1 - exp) if exp != 1 else float("nan")


def score(resultsdir):
    res = Path(resultsdir)
    arm1_key = {r["arxiv_id"]: r for r in csv.DictReader(open(VDIR / "arm1-key.csv", encoding="utf-8"))}
    arm2_key = {r["item_id"]: r for r in csv.DictReader(open(VDIR / "arm2-key.csv", encoding="utf-8"))}

    # ---- Arm 1 ----
    print("\n=== ARM 1: independent re-doing ===")
    rows = []
    for f in sorted(res.glob("arm1-*-*.json")):
        verifier = f.stem.split("-")[-1]          # arm1-000-fable.json
        for it in json.loads(f.read_text(encoding="utf-8")):
            k = arm1_key.get(it.get("arxiv_id"))
            if not k:
                continue
            rows.append({"arxiv_id": it["arxiv_id"], "verifier": verifier,
                         "producer": k["producer"], "redone": it.get("decision", ""),
                         "original": k["original_decision"],
                         "self": int(verifier == k["producer"]),
                         "agree": int(it.get("decision", "") == k["original_decision"]),
                         "guessed_self": it.get("authored_by_you", "")})
    if rows:
        for cond in [(v, p) for v in ("fable", "opus") for p in ("fable", "opus")]:
            sub = [r for r in rows if (r["verifier"], r["producer"]) == cond]
            if sub:
                agree = sum(r["agree"] for r in sub) / len(sub)
                k = cohens_kappa([(r["redone"], r["original"]) for r in sub])
                tag = "SELF " if cond[0] == cond[1] else "cross"
                print(f"  {tag} verifier={cond[0]:6s} producer={cond[1]:6s} "
                      f"n={len(sub):3d}  agreement={agree:.3f}  kappa={k:.3f}")
        selfr = [r for r in rows if r["self"]]
        crossr = [r for r in rows if not r["self"]]
        if selfr and crossr:
            d = (sum(r["agree"] for r in selfr) / len(selfr)
                 - sum(r["agree"] for r in crossr) / len(crossr))
            print(f"  self-preference (self - cross agreement): {d:+.3f}")
        # authorship-identification probe: only responses that committed to yes/no count
        def guess_bit(v):
            s = str(v).strip().lower()
            if s in ("yes", "true", "1"):
                return 1
            if s in ("no", "false", "0"):
                return 0
            return None

        committed = [(guess_bit(r["guessed_self"]), r["self"]) for r in rows]
        committed = [(g, s) for g, s in committed if g is not None]
        abstained = len(rows) - len(committed)
        print(f"  authorship probe: {len(committed)}/{len(rows)} committed to a guess "
              f"({abstained} answered 'unknown')")
        if committed:
            acc = sum(1 for g, s in committed if g == s) / len(committed)
            said_yes = sum(g for g, _ in committed) / len(committed)
            print(f"    accuracy={acc:.3f} vs 0.500 chance;  said-'yes' rate={said_yes:.3f}")
        (DATA / "phase-v-arm1.csv").write_text(_csv(rows), encoding="utf-8")

    # ---- Arm 2 ----
    print("\n=== ARM 2: audit against corrupted ground truth ===")
    a2 = []
    for f in sorted(res.glob("arm2-*-*.json")):
        verifier = f.stem.split("-")[-1]
        for it in json.loads(f.read_text(encoding="utf-8")):
            k = arm2_key.get(it.get("item_id"))
            if not k:
                continue
            flagged = str(it.get("flag_incorrect", "")).lower() in ("true", "yes", "1")
            a2.append({"item_id": k["item_id"], "arxiv_id": k["arxiv_id"],
                       "verifier": verifier, "corruption": k["corruption"],
                       "flagged": int(flagged), "note": str(it.get("note", ""))[:300]})
    if a2:
        for v in sorted({r["verifier"] for r in a2}):
            sub = [r for r in a2 if r["verifier"] == v]
            corrupted = [r for r in sub if r["corruption"] != "none"]
            clean = [r for r in sub if r["corruption"] == "none"]
            sens = sum(r["flagged"] for r in corrupted) / len(corrupted) if corrupted else float("nan")
            fpr = sum(r["flagged"] for r in clean) / len(clean) if clean else float("nan")
            print(f"  {v:6s} n={len(sub):3d}  sensitivity={sens:.3f} "
                  f"({sum(r['flagged'] for r in corrupted)}/{len(corrupted)})  "
                  f"flag-rate on uncorrupted={fpr:.3f}")
            by_kind = Counter(r["corruption"] for r in corrupted if r["flagged"])
            print(f"         detected by kind: {dict(by_kind)}")
        (DATA / "phase-v-arm2.csv").write_text(_csv(a2), encoding="utf-8")

        # --- the question the two-model design exists to answer ---
        by_item = {}
        for r in a2:
            by_item.setdefault(r["item_id"], {})[r["verifier"]] = r
        both = {i: d for i, d in by_item.items() if len(d) == 2}
        if both:
            vs = sorted({r["verifier"] for r in a2})
            same = sum(1 for d in both.values()
                       if d[vs[0]]["flagged"] == d[vs[1]]["flagged"])
            print(f"\n  INTER-MODEL AGREEMENT on flag/no-flag: {same}/{len(both)} "
                  f"= {same / len(both):.3f}")
            kp = cohens_kappa([(str(d[vs[0]]["flagged"]), str(d[vs[1]]["flagged"]))
                               for d in both.values()])
            print(f"  Cohen's kappa between the two auditors: {kp:.3f}")

            missed_both, missed_one, caught_both = [], [], []
            for i, d in both.items():
                if d[vs[0]]["corruption"] == "none":
                    continue
                f0, f1 = d[vs[0]]["flagged"], d[vs[1]]["flagged"]
                (caught_both if f0 and f1 else missed_both if not f0 and not f1
                 else missed_one).append((i, d[vs[0]]["corruption"], d[vs[0]]["arxiv_id"]))
            print(f"\n  corrupted items caught by BOTH: {len(caught_both)}")
            print(f"  caught by exactly ONE:            {len(missed_one)}  {[m[1] for m in missed_one]}")
            print(f"  MISSED BY BOTH (shared blind spot): {len(missed_both)}")
            for i, kind, pid in missed_both:
                print(f"     {i}  {kind}  arXiv:{pid}")
            print("\n  A shared blind spot is the result that matters: it is invisible to a "
                  "second-model check, which is exactly the redundancy strategy this review used.")
        print("\n  NOTE: flags on uncorrupted items are disagreements, not yet false "
              "positives; they require adjudication before being counted as errors.")


if __name__ == "__main__":
    {"build": build, "score": score}[sys.argv[1]](sys.argv[2])
