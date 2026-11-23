"""Replay the indicator-capacity audit, then apply Teichmueller valuation pricing
to the open shards of roots 19, 7, 11, 31 and 13."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
sys.path.insert(0, str(RESEARCH / "IndicatorCapacity"))

from VerifyTeichmullerValuation2400 import ROOTS, Profile, check_lemmas, verify_shard


def load_baseline(replay):
    path = RESEARCH / "IndicatorCapacity" / "Audit2400.json"
    stored = json.loads(path.read_text(encoding="utf-8"))
    if replay:
        from AuditIndicatorCapacity2400 import run as replay_indicator
        # Compare after a JSON round trip, which turns integer keys into strings.
        if json.loads(json.dumps(replay_indicator())) != stored:
            raise ValueError("Indicator-capacity baseline changed; regenerate this audit")
    return stored


def run(replay=True):
    previous = load_baseline(replay)
    tasks = previous["open_manifest"]
    proofs = {}
    for p in ROOTS:
        check_lemmas(p)
        prof = Profile(p)
        for t in tasks:
            if t["root"] != p:
                continue
            ok, detail = verify_shard(p, t["exponent"], t["exact"], prof)
            if ok:
                proofs[t["id"]] = [dict(exponent=e, rule=r) for e, r in detail]
    additions = [t for t in tasks if t["id"] in proofs]
    remaining = [t for t in tasks if t["id"] not in proofs]
    counts = Counter(t["root"] for t in additions)
    by_root = {
        p: dict(verified=row["verified"] + counts[int(p)],
                open=row["open"] - counts[int(p)], added=counts[int(p)])
        for p, row in previous["by_root"].items()
    }
    return dict(
        theorem_status="INCOMPLETE_FRONTIER" if remaining else "UNCONDITIONALLY_VERIFIED",
        total=previous["total"], previous_closed=previous["closed"],
        closed=previous["closed"] + len(additions), open=len(remaining),
        by_root=by_root,
        additions=[dict(t, proof=proofs[t["id"]]) for t in additions],
        open_manifest=remaining,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--no-replay", action="store_true",
                        help="trust the checked-in indicator-capacity audit")
    args = parser.parse_args()
    result = run(replay=not args.no_replay)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("additions", "open_manifest")}, indent=2))


if __name__ == "__main__":
    main()
