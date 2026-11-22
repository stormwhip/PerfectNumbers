#!/usr/bin/env python3
"""Regression tests: direct certified leaves and full-audit fast path."""
from __future__ import annotations

import tempfile
from pathlib import Path

from AuditRunner2400 import audit_single_shard
from DirectRootClosures2400 import direct_root_bundle, independently_check_direct_roots
from FrontierLedgerV2 import DiskProofStore
from IndependentVerifierV2 import DEFAULT_CIRC_ORDER, ORIGINAL_ROOTS, RootTaskPin, VerificationError, verify_leaf_node, verify_root_task_bundle


def run() -> None:
    result = independently_check_direct_roots(DEFAULT_CIRC_ORDER)
    expected = {19: 130, 7: 191, 11: 154, 31: 116, 13: 146, 3: 311, 5: 217, 17: 134}
    if result["total_tasks"] != 3072 or result["by_root"] != expected:
        raise RuntimeError(f"wrong independent closure census: {result}")

    root = 7
    d = 2
    pin = RootTaskPin(
        upper_bound_N=10**2400,
        root_set=ORIGINAL_ROOTS,
        root_order=DEFAULT_CIRC_ORDER,
        circ_order=DEFAULT_CIRC_ORDER,
        root_prime=root,
        root_exp=d,
        root_exact=True,
    )
    proof = direct_root_bundle(pin)
    if proof is None or verify_root_task_bundle(pin, proof)["status"] != "TREE_ACCEPTED":
        raise RuntimeError("root 7 exponent 2 must have a valid independent certificate")

    task = {"root": root, "index": 0, "exponent": d,
            "exact": True, "id": "P7_I00000"}
    with tempfile.TemporaryDirectory(prefix="opn-direct-root-") as temp:
        dest = Path(temp)
        outcome = audit_single_shard(
            task=task,
            pin=pin,
            ledger_dir=dest / "AbsentLedgers",
            proof_store=DiskProofStore(dest / "Proofs"),
            run_fingerprint="sha256:direct-root-test",
        )
        if (outcome["status"] != "VERIFIED_CLOSED"
                or outcome.get("certificate_source") != "DIRECT_ROOT_FORBIDDEN_FACTOR"
                or outcome["open_tasks"] != 0):
            raise RuntimeError(f"valid direct certificate not counted: {outcome}")

    # High root exponent: certified directly by p^d * odd(sigma(p^d)) > 10^2400.
    size_pin = RootTaskPin(
        upper_bound_N=10**2400,
        root_set=ORIGINAL_ROOTS,
        root_order=DEFAULT_CIRC_ORDER,
        circ_order=DEFAULT_CIRC_ORDER,
        root_prime=19,
        root_exp=940,
        root_exact=False,
    )
    size_proof = direct_root_bundle(size_pin)
    if (size_proof is None
            or size_proof["nodes"][0]["witness"]["reason"] != "SIGMA_DIVISOR_SIZE"
            or verify_root_task_bundle(size_pin, size_proof)["status"] != "TREE_ACCEPTED"):
        raise RuntimeError("root 19 exponent 940 must be independently certified by sigma size")

    # Strict inequality: equality with the exact forced divisor must remain OPEN.
    boundary_pin = RootTaskPin(
        upper_bound_N=19**2 * ((19**3 - 1) // 18),
        root_set=ORIGINAL_ROOTS,
        root_order=DEFAULT_CIRC_ORDER,
        circ_order=DEFAULT_CIRC_ORDER,
        root_prime=19,
        root_exp=2,
        root_exact=False,
    )
    initial = boundary_pin.build_initial_state(set())
    size_leaf = {"kind": "LEAF", "witness": {
        "reason": "SIGMA_DIVISOR_SIZE", "source_p": 19, "d": 2
    }}
    try:
        verify_leaf_node(initial, size_leaf, boundary_pin.upper_bound_N, set())
    except VerificationError:
        pass
    else:
        raise RuntimeError("sigma-size equality was wrongly treated as strict closure")
    if verify_leaf_node(initial, size_leaf, boundary_pin.upper_bound_N - 1, set()) != "LEAF_ACCEPTED":
        raise RuntimeError("sigma-size strict positive margin was wrongly rejected")

    no_direct = RootTaskPin(
        upper_bound_N=10**2400,
        root_set=ORIGINAL_ROOTS,
        root_order=DEFAULT_CIRC_ORDER,
        circ_order=DEFAULT_CIRC_ORDER,
        root_prime=19,
        root_exp=2,
        root_exact=False,
    )
    if direct_root_bundle(no_direct) is not None:
        raise RuntimeError("first root incorrectly certified as forbidden-factor closure")
    print("DirectRootClosuresTests: PASS (3072 tasks, 1399 independently checked leaves, audit integration)")


if __name__ == "__main__":
    run()
