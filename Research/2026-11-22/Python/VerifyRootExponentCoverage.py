"""Independently audit top-level exponent coverage for a 2400 shard manifest."""

import argparse
import json
from math import isqrt
from pathlib import Path

ROOT_SETS = (
    frozenset((3, 5, 7, 11, 13, 17, 19, 31)),
    frozenset((3, 5, 7, 11, 13, 17, 23, 31)),
)


def exponent_ceiling(root, target):
    cap, power = 0, 1
    while power <= target // root:
        power *= root
        cap += 1
    return cap


def option_list(root, cap):
    options = []
    if root % 4 == 1:
        options.append((1, True))
    first = 3
    if root == 3:
        options.extend(((2, True), (4, True), (8, False), (14, False), (24, False)))
        first = 7
    elif root == 7:
        options.extend(((2, True), (8, False)))
        first = 5
    for candidate in range(first, cap + 2, 2):
        if all(candidate % q for q in range(3, isqrt(candidate) + 1, 2)):
            options.append((candidate - 1, False))
    return [(e, exact) for e, exact in options if e <= cap]


def check_exponent_coverage(root, cap, options):
    # Include the Euler class even when exact and standard options overlap.
    legal = set(range(2, cap + 1, 2))
    if root % 4 == 1:
        legal.update(range(1, cap + 1, 4))
    for d, exact in options:
        if exact:
            legal.discard(d)
        else:
            legal.difference_update(range(d, cap + 1, d + 1))
    if legal:
        raise ValueError(f"root {root} has uncovered exponents: {sorted(legal)[:8]}")


def canonical_tasks(order, exponent=2400):
    if frozenset(order) not in ROOT_SETS or len(order) != 8:
        raise ValueError("expected a permutation of one of the two certified root sets")
    target = 10**exponent
    for root in order:
        cap = exponent_ceiling(root, target)
        options = option_list(root, cap)
        check_exponent_coverage(root, cap, options)
        for i, (d, exact) in enumerate(options):
            yield {"root": root, "index": i, "count": len(options),
                   "exponent": d, "exact": exact, "id": f"P{root}_I{i:05d}"}


def verify_manifest(manifest):
    if manifest["target_exponent"] != 2400:
        raise ValueError("target exponent must be 2400")
    tasks = list(canonical_tasks(manifest["root_order"]))
    given = manifest["tasks"]
    if len(given) != len(tasks):
        raise ValueError(f"expected {len(tasks)} top-level shards, got {len(given)}")
    for i, (actual, expected) in enumerate(zip(given, tasks)):
        if actual != expected or type(actual.get("exact")) is not bool:
            raise ValueError(f"unexpected top-level shard at position {i}: expected {expected}")
    return len(tasks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", type=Path, nargs="?")
    args = parser.parse_args()
    if args.manifest is None:
        for roots in ROOT_SETS:
            tasks = list(canonical_tasks(sorted(roots)))
            counts = {t["root"]: t["count"] for t in tasks}
            assert verify_manifest({"target_exponent": 2400, "root_order": sorted(roots),
                                    "tasks": tasks}) == len(tasks)
            print(f"REFERENCE_SHARDS total={len(tasks)} roots={counts}")
    else:
        manifest = json.loads(args.manifest.read_text(encoding="utf-8"))
        print(f"ROOT_EXPONENT_COVERAGE_OK tasks={verify_manifest(manifest)}")


if __name__ == "__main__":
    main()
