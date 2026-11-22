#!/usr/bin/env python3
"""Exact subset-DP optimization of immediately certified root contradictions.

This optimizes both one-node FORBIDDEN_FACTOR and SIGMA_DIVISOR_SIZE certificates.
It is not a prediction of proof-tree size or total 72-hour runtime.
"""
from __future__ import annotations

from itertools import permutations
import json

from DirectRootClosures2400 import divides_sigma_mod, sigma_divisor_size_exceeds
from IndependentVerifierV2 import DEFAULT_CIRC_ORDER, ORIGINAL_ROOTS, REPLACEMENT_ROOTS
from VerifyRootExponentCoverage import canonical_tasks


def evaluate_root_set(roots: tuple[int, ...], baseline: tuple[int, ...]) -> dict:
    primes = tuple(sorted(roots))
    if tuple(sorted(baseline)) != primes:
        raise ValueError("baseline order must permute its root set")
    n = len(primes)
    full = (1 << n) - 1
    bit_of = {p: 1 << i for i, p in enumerate(primes)}
    task_masks = {p: [] for p in primes}
    size_by_root = {p: 0 for p in primes}

    # Root exponent manifest is independent of how the root primes are ordered.
    tasks = list(canonical_tasks(primes))
    for task in tasks:
        p, d = task["root"], task["exponent"]
        if sigma_divisor_size_exceeds(p, d, 10**2400):
            size_by_root[p] += 1
            continue
        hit_mask = 0
        for q in primes:
            if q != p and divides_sigma_mod(p, d, q):
                hit_mask |= bit_of[q]
        task_masks[p].append(hit_mask)

    size_total = sum(size_by_root.values())
    gain = {
        (p, subset): sum((hit & subset) != 0 for hit in task_masks[p])
        for p in primes for subset in range(1 << n)
    }

    def score(order: tuple[int, ...]) -> tuple[int, dict[int, int]]:
        subset = 0
        per_root = {}
        for p in order:
            per_root[p] = gain[p, subset]
            subset |= bit_of[p]
        if subset != full:
            raise ValueError("incomplete root order")
        return size_total + sum(per_root.values()), per_root

    # Bellman recurrence: choose the next root p given precisely the forbidden prefix.
    dp = {0: (size_total, ())}
    for subset in range(1 << n):
        if subset not in dp:
            continue
        old_score, old_order = dp[subset]
        for p in primes:
            if subset & bit_of[p]:
                continue
            nxt = subset | bit_of[p]
            candidate = (old_score + gain[p, subset], old_order + (p,))
            if nxt not in dp or candidate[0] > dp[nxt][0]:
                dp[nxt] = candidate
    best_score, best_order = dp[full]
    baseline_score, baseline_by_root = score(baseline)

    # Independent exhaustive permutation oracle: 8! = 40,320 arrangements.
    exhaustive_max = -1
    ties = 0
    for order in permutations(primes):
        val, _ = score(order)
        if val > exhaustive_max:
            exhaustive_max = val
            ties = 1
        elif val == exhaustive_max:
            ties += 1
    if best_score != exhaustive_max or score(best_order)[0] != best_score:
        raise RuntimeError("subset DP disagrees with independent full permutation census")

    return {
        "root_set": primes,
        "total_tasks": len(tasks),
        "baseline_order": baseline,
        "baseline_direct_closures": baseline_score,
        "sigma_size_closures": size_total,
        "baseline_forbidden_factor_closures": baseline_score - size_total,
        "baseline_by_root": baseline_by_root,
        "optimal_order": best_order,
        "optimal_direct_closures": best_score,
        "optimal_forbidden_factor_closures": best_score - size_total,
        "optimal_order_count": ties,
        "exhaustive_permutations": 40320,
    }


def main() -> None:
    original = evaluate_root_set(ORIGINAL_ROOTS, DEFAULT_CIRC_ORDER)
    replacement = evaluate_root_set(
        REPLACEMENT_ROOTS, (23, 7, 11, 31, 13, 3, 5, 17)
    )
    if (original["total_tasks"], original["baseline_direct_closures"],
            original["optimal_direct_closures"]) != (3072, 1396, 1397):
        raise RuntimeError(f"unexpected original-root baseline: {original}")
    if (replacement["total_tasks"], replacement["baseline_direct_closures"],
            replacement["optimal_direct_closures"]) != (3058, 1390, 1393):
        raise RuntimeError(f"unexpected replacement-root baseline: {replacement}")
    print(json.dumps({"original": original, "replacement": replacement},
                     indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
