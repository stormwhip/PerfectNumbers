"""Replay the supplier baseline and indicator-capacity additions."""
import argparse
from collections import Counter
import json
from pathlib import Path
import sys

from VerifyIndicatorCapacity2400 import load_duals, sieve_primes, verify_exponent

RESEARCH = Path(__file__).resolve().parents[1]
SUPPLIER = RESEARCH / "SupplierBatch"
sys.path.insert(0, str(SUPPLIER))
from VerifyBatch2400 import run as replay_supplier_batch
from Verify import covers, tables


def run():
    previous = replay_supplier_batch(SUPPLIER / "BatchSupplierProofs2400.json.gz")
    if json.dumps(previous, indent=2) + "\n" != (SUPPLIER / "BatchAudit2400.json").read_text():
        raise ValueError("Supplier baseline changed; regenerate the merged audit")

    tasks = previous["open_manifest"]
    prior_exclusions = {(row["root"], row["exponent"]) for row in previous["exact_exponents"]}
    _, actual_rows = tables()
    live = {
        (p, e) for p, e, label, _ in actual_rows
        if p in (3, 5) and label == "OPEN" and (p, e) not in prior_exclusions
    }
    candidates_by_shard = {
        t["id"]: {(p, e) for p, e in live
                  if p == t["root"] and covers(e, t["exponent"], t["exact"])}
        for t in tasks if t["root"] in (3, 5)
    }
    if any(not group for group in candidates_by_shard.values()):
        raise ValueError("An open shard has no live exponent")

    primes = sieve_primes(500_000)
    duals = load_duals(primes)
    proved = {}
    for p, e in sorted(set().union(*candidates_by_shard.values())):
        passed, rule = verify_exponent(p, e, duals[p], primes)
        if passed:
            proved[p, e] = rule

    additions = [t for t in tasks if t["id"] in candidates_by_shard
                 and candidates_by_shard[t["id"]] <= proved.keys()]
    newly_closed = {t["id"] for t in additions}
    remaining = [t for t in tasks if t["id"] not in newly_closed]
    counts = Counter(t["root"] for t in additions)
    by_root = {
        p: dict(verified=row["verified"] + counts[p], open=row["open"] - counts[p],
                added=counts[p])
        for p, row in previous["by_root"].items()
    }
    return dict(
        theorem_status="INCOMPLETE_FRONTIER" if remaining else "UNCONDITIONALLY_VERIFIED",
        total=previous["total"], previous_closed=previous["closed"],
        closed=previous["closed"] + len(additions), open=len(remaining),
        by_root=by_root,
        additions=additions,
        exact_exponents=[dict(root=p, exponent=e, rule=rule)
                         for (p, e), rule in sorted(proved.items())],
        open_manifest=remaining,
    )


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = run()
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items()
                      if k not in ("additions", "exact_exponents", "open_manifest")}, indent=2))
    print(f"New actual-exponent exclusions: {len(result['exact_exponents'])}")


if __name__ == "__main__":
    main()
