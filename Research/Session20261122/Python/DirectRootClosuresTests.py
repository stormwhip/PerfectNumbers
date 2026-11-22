#!/usr/bin/env python3
"""Regression tests: direct certified leaves and full-audit fast path."""
from __future__ import annotations

import tempfile
from pathlib import Path

from AuditRunner2400 import audit_single_shard
from DirectRootClosures2400 import direct_root_bundle, independently_check_direct_roots
from FrontierLedgerV2 import DiskProofStore
from IndependentVerifierV2 import DEFAULT_CIRC_ORDER, ORIGINAL_ROOTS, RootTaskPin, verify_root_task_bundle


def run() -> None:
    result = independently_check_direct_roots(DEFAULT_CIRC_ORDER)
    expected = {19: 0, 7: 2, 11: 1, 31: 1, 13: 1, 3: 5, 5: 3, 17: 1}
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
    print("DirectRootClosuresTests: PASS (3072 tasks, 14 certified direct leaves, audit integration)")


if __name__ == "__main__":
    run()
