#!/usr/bin/env python3
"""Independently certified direct root-factor exclusions for the 10^2400 search.

For an exact root exponent e=d or a standard branch with (d+1)|(e+1),
sigma(p^d) divides sigma(p^e). An odd prime q dividing sigma(p^d)
must divide the hypothetical odd perfect N. A prior forbidden root q
therefore gives a complete one-node certificate.

This module is deliberately independent of the C++ solver's PROVEN status.
"""
from __future__ import annotations

import argparse
import copy
import json
from math import isqrt
from pathlib import Path
from typing import Optional

from IndependentVerifierV2 import (
    DEFAULT_CIRC_ORDER,
    ORIGINAL_ROOTS,
    REPLACEMENT_ROOTS,
    RootTaskPin,
    VerificationError,
    verify_root_task_bundle,
)
from VerifyRootExponentCoverage import canonical_tasks


def divides_sigma_mod(p: int, d: int, q: int) -> bool:
    """Exact modular criterion, with p == 1 (mod q) handled explicitly."""
    if p == q:
        return False
    if p % q == 1:
        return (d + 1) % q == 0
    return pow(p, d + 1, q) == 1


def direct_root_bundle(pin: RootTaskPin) -> Optional[dict]:
    """Return a minimal independent-verifier DAG only for a direct contradiction."""
    idx = pin.root_order.index(pin.root_prime)
    q = next(
        (r for r in pin.root_order[:idx]
         if divides_sigma_mod(pin.root_prime, pin.root_exp, r)),
        None,
    )
    if q is None:
        return None

    # The trusted root state and excluded roots are rebuilt from the external pin.
    root_state = pin.build_initial_state(set())
    return {
        "nodes": [{
            "kind": "LEAF",
            "state": root_state.canonical_dict(),
            "witness": {
                "reason": "FORBIDDEN_FACTOR",
                "forbidden_lemma": {
                    "source_p": pin.root_prime,
                    "d": pin.root_exp,
                    "forbidden_q": q,
                    "cert": {"method": "TRIAL_DIV", "max_divisor": isqrt(q)},
                },
            },
        }],
    }


def independently_check_direct_roots(root_order: tuple[int, ...], emit_dir: Optional[Path] = None) -> dict:
    """Check every manifest entry and every generated certificate, including tampering."""
    root_set = tuple(sorted(root_order))
    original = tuple(sorted(ORIGINAL_ROOTS))
    replacement = tuple(sorted(REPLACEMENT_ROOTS))
    if root_set not in (original, replacement):
        raise VerificationError("unsupported root set")
    circ_order = DEFAULT_CIRC_ORDER if root_set == original else (23, 7, 11, 31, 13, 3, 5, 17)
    if emit_dir is not None:
        emit_dir.mkdir(parents=True, exist_ok=True)

    counts = {p: 0 for p in root_order}
    witnesses = []
    tasks = list(canonical_tasks(root_order))
    for task in tasks:
        pin = RootTaskPin(
            upper_bound_N=10**2400,
            root_set=root_set,
            root_order=root_order,
            circ_order=circ_order,
            root_prime=task["root"],
            root_exp=task["exponent"],
            root_exact=task["exact"],
        )
        bundle = direct_root_bundle(pin)
        if bundle is None:
            continue
        if verify_root_task_bundle(pin, bundle)["status"] != "TREE_ACCEPTED":
            raise VerificationError(f"unverified direct certificate: {task['id']}")

        witness = bundle["nodes"][0]["witness"]["forbidden_lemma"]
        q = witness["forbidden_q"]
        # Independent big-integer check; modular detection is never trusted on its own.
        sigma = (pow(pin.root_prime, pin.root_exp + 1) - 1) // (pin.root_prime - 1)
        if sigma % q != 0:
            raise VerificationError(f"incorrect modular divisibility for {task['id']}")
        malformed = copy.deepcopy(bundle)
        malformed["nodes"][0]["witness"]["forbidden_lemma"]["forbidden_q"] = pin.root_prime
        try:
            verify_root_task_bundle(pin, malformed)
        except VerificationError:
            pass
        else:
            raise VerificationError(f"tampered certificate accepted for {task['id']}")

        if emit_dir is not None:
            dest = emit_dir / (task["id"] + ".json")
            dest.write_text(
                json.dumps(bundle, sort_keys=True, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
        counts[task["root"]] += 1
        witnesses.append({
            "id": task["id"],
            "root": task["root"],
            "exponent": task["exponent"],
            "exact": task["exact"],
            "forbidden_q": q,
        })
    return {
        "root_order": root_order,
        "total_tasks": len(tasks),
        "verified_direct_closures": len(witnesses),
        "by_root": counts,
        "witnesses": witnesses,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-set", choices=("original", "replacement"), default="original")
    parser.add_argument("--emit-dir", type=Path)
    args = parser.parse_args()
    order = DEFAULT_CIRC_ORDER if args.root_set == "original" else (23, 7, 11, 31, 13, 3, 5, 17)
    result = independently_check_direct_roots(order, args.emit_dir)
    if args.root_set == "original" and result["verified_direct_closures"] != 14:
        raise VerificationError("original-root baseline closure count changed unexpectedly")
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
