#!/usr/bin/env python3
"""Generate independently checkable one-node root certificates for 10^2400.

Two exact-integer rules:
- FORBIDDEN_FACTOR: an earlier excluded root divides sigma(p^d).
- SIGMA_DIVISOR_SIZE: p^d * odd(sigma(p^d)) exceeds the target bound.

For exact exponents e=d or standard branches with d+1 dividing e+1,
sigma(p^d) divides sigma(p^e). No factorization of sigma(p^d) is needed.
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
    """Exact modular criterion; handle the non-invertible p == 1 (mod q) case."""
    if p == q:
        return False
    if p % q == 1:
        return (d + 1) % q == 0
    return pow(p, d + 1, q) == 1


def odd_sigma_prime_power(p: int, d: int) -> int:
    sigma = (pow(p, d + 1) - 1) // (p - 1)
    return sigma // (sigma & -sigma)


def sigma_divisor_size_exceeds(p: int, d: int, bound: int) -> bool:
    # The bit-length lower bound avoids allocating enormous powers.
    if (p.bit_length() - 1) * d > bound.bit_length():
        return True
    return pow(p, d) * odd_sigma_prime_power(p, d) > bound


def direct_root_bundle(pin: RootTaskPin) -> Optional[dict]:
    """Construct one verifier LEAF from the external trusted task pin."""
    idx = pin.root_order.index(pin.root_prime)
    q = next(
        (r for r in pin.root_order[:idx]
         if divides_sigma_mod(pin.root_prime, pin.root_exp, r)),
        None,
    )
    if q is not None:
        witness = {
            "reason": "FORBIDDEN_FACTOR",
            "forbidden_lemma": {
                "source_p": pin.root_prime,
                "d": pin.root_exp,
                "forbidden_q": q,
                "cert": {"method": "TRIAL_DIV", "max_divisor": isqrt(q)},
            },
        }
    elif sigma_divisor_size_exceeds(pin.root_prime, pin.root_exp, pin.upper_bound_N):
        witness = {
            "reason": "SIGMA_DIVISOR_SIZE",
            "source_p": pin.root_prime,
            "d": pin.root_exp,
        }
    elif (pin.root_order == DEFAULT_CIRC_ORDER and
          pin.upper_bound_N == 10**2400 and not pin.root_exact and
          (pin.root_prime, pin.root_exp) in ((19, 936), (11, 1150), (11, 1152))):
        witness = {
            "reason": "FINITE_QUOTIENT_CYCLOTOMIC",
            "source_p": pin.root_prime,
            "d": pin.root_exp,
        }
    else:
        return None

    root_state = pin.build_initial_state(set())
    return {"nodes": [{
        "kind": "LEAF",
        "state": root_state.canonical_dict(),
        "witness": witness,
    }]}


def independently_check_direct_roots(root_order: tuple[int, ...], emit_dir: Optional[Path] = None) -> dict:
    """Enumerate the canonical manifest; verify proofs and rejected mutations."""
    root_set = tuple(sorted(root_order))
    original = tuple(sorted(ORIGINAL_ROOTS))
    replacement = tuple(sorted(REPLACEMENT_ROOTS))
    if root_set not in (original, replacement):
        raise VerificationError("unsupported root set")
    circ_order = DEFAULT_CIRC_ORDER if root_set == original else (23, 7, 11, 31, 13, 3, 5, 17)
    if emit_dir is not None:
        emit_dir.mkdir(parents=True, exist_ok=True)

    counts = {p: 0 for p in root_order}
    reasons = {"FORBIDDEN_FACTOR": 0, "SIGMA_DIVISOR_SIZE": 0, "FINITE_QUOTIENT_CYCLOTOMIC": 0}
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
            raise VerificationError(f"independent checker rejected: {task['id']}")

        witness = bundle["nodes"][0]["witness"]
        reason = witness["reason"]
        sigma = (pow(pin.root_prime, pin.root_exp + 1) - 1) // (pin.root_prime - 1)
        if reason == "FORBIDDEN_FACTOR":
            q = witness["forbidden_lemma"]["forbidden_q"]
            if sigma % q != 0:
                raise VerificationError(f"modular detection incorrect at {task['id']}")
        elif reason == "SIGMA_DIVISOR_SIZE":
            odd_sigma = sigma // (sigma & -sigma)
            if pow(pin.root_prime, pin.root_exp) * odd_sigma <= pin.upper_bound_N:
                raise VerificationError(f"size proof incorrect at {task['id']}")
        elif reason == "FINITE_QUOTIENT_CYCLOTOMIC":
            if (pin.root_prime, pin.root_exp) not in ((19, 936), (11, 1150), (11, 1152)):
                raise VerificationError("unexpected finite quotient witness")
        else:
            raise VerificationError(f"unknown direct root reason {reason}")

        # The verifier must reject a forged claimed source exponent or root.
        malformed = copy.deepcopy(bundle)
        if reason == "FORBIDDEN_FACTOR":
            malformed["nodes"][0]["witness"]["forbidden_lemma"]["forbidden_q"] = pin.root_prime
        else:
            malformed["nodes"][0]["witness"]["d"] += 1
        try:
            verify_root_task_bundle(pin, malformed)
        except VerificationError:
            pass
        else:
            raise VerificationError(f"tampered proof accepted: {task['id']}")

        if emit_dir is not None:
            (emit_dir / (task["id"] + ".json")).write_text(
                json.dumps(bundle, sort_keys=True, separators=(",", ":")) + "\n",
                encoding="utf-8",
            )
        counts[task["root"]] += 1
        reasons[reason] += 1
        witnesses.append({
            "id": task["id"], "root": task["root"],
            "exponent": task["exponent"], "exact": task["exact"],
            "reason": reason,
        })
    return {
        "root_order": root_order,
        "total_tasks": len(tasks),
        "verified_direct_closures": len(witnesses),
        "by_root": counts,
        "by_reason": reasons,
        "witnesses": witnesses,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root-set", choices=("original", "replacement"), default="original")
    parser.add_argument("--emit-dir", type=Path)
    args = parser.parse_args()
    order = DEFAULT_CIRC_ORDER if args.root_set == "original" else (23, 7, 11, 31, 13, 3, 5, 17)
    result = independently_check_direct_roots(order, args.emit_dir)
    if args.root_set == "original":
        if (result["verified_direct_closures"], result["by_reason"]) != (
            1399, {"FORBIDDEN_FACTOR": 14, "SIGMA_DIVISOR_SIZE": 1382,
                   "FINITE_QUOTIENT_CYCLOTOMIC": 3}
        ):
            raise VerificationError("original-root certificate census changed unexpectedly")
    print(json.dumps(
        {**{k: v for k, v in result.items() if k != "witnesses"},
         "first_witnesses": result["witnesses"][:20]},
        ensure_ascii=False, indent=2,
    ))


if __name__ == "__main__":
    main()
