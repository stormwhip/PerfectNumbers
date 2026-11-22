#!/usr/bin/env python3
"""Mixed OPEN + CLOSED split_with_evidence() + AuditRunner2400 closure test (fixes B-5 / G-4)."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

from AuditRunner2400 import run_full_audit
from FrontierLedgerV2 import DiskProofStore, FrontierLedgerV2
from IndependentVerifierV2 import (
    DEFAULT_CIRC_ORDER,
    canonical_json_bytes,
)


def build_1e12_mixed_split_fixtures():
    """Exact N <= 10^12 arithmetic fixtures with 2 child edges: edge 0 CLOSED, edge 1 OPEN."""
    root_state = {
        "branched": [{"p": 19, "exp": 2, "exact": False}],
        "unbranched": [],
        "forbidden": [],
        "has_special": False,
        "composites": [],
        "source_v_bounds": [],
        "source_v2_bounds": [],
    }
    child_e2 = {
        "branched": [
            {"p": 19, "exp": 2, "exact": False},
            {"p": 127, "exp": 2, "exact": True},
        ],
        "unbranched": [3],
        "forbidden": [],
        "has_special": False,
        "composites": [],
        "source_v_bounds": [
            {"q": 3, "sources": [{"p": 19, "v": 1}]},
            {"q": 127, "sources": [{"p": 19, "v": 1}]},
        ],
        "source_v2_bounds": [{"p": 19, "v2": 0}],
    }
    child_e4 = {
        "branched": [
            {"p": 19, "exp": 2, "exact": False},
            {"p": 127, "exp": 4, "exact": True},
        ],
        "unbranched": [3],
        "forbidden": [],
        "has_special": False,
        "composites": [],
        "source_v_bounds": [
            {"q": 3, "sources": [{"p": 19, "v": 1}]},
            {"q": 127, "sources": [{"p": 19, "v": 1}]},
        ],
        "source_v2_bounds": [{"p": 19, "v2": 0}],
    }
    split_node = {
        "kind": "SPLIT",
        "state": root_state,
        "deductions": [
            {
                "source_p": 19,
                "d": 2,
                "v2": 0,
                "factors": [
                    {"q": 3, "e": 1, "cert": {"method": "TRIAL_DIV", "max_divisor": 2}},
                    {"q": 127, "e": 1, "cert": {"method": "TRIAL_DIV", "max_divisor": 11}},
                ],
            }
        ],
        "split_rule": {
            "type": "UNBRANCHED_EXPONENT_EXHAUSTION",
            "branch_prime": 127,
            "prime_cert": {"method": "TRIAL_DIV", "max_divisor": 11},
            "size_cutoff_ge": 6,  # 19^2 * 3^2 * 127^6 > 1.36e16 > 10^12
        },
        "children": [
            {"edge": {"exp": 2, "exact": True}, "state": child_e2},
            {"edge": {"exp": 4, "exact": True}, "state": child_e4},
        ],
    }
    # Edge 0 (CLOSED immediately at split time): sigma(127^2) = 3 * 5419 -> size > 1.53e15 > 10^12
    leaf_e2 = {
        "kind": "LEAF",
        "state": child_e2,
        "witness": {
            "reason": "SIZE_EXCEEDS_BOUND",
            "deductions": [
                {
                    "source_p": 127,
                    "d": 2,
                    "v2": 0,
                    "factors": [
                        {"q": 3, "e": 1, "cert": {"method": "TRIAL_DIV", "max_divisor": 2}},
                        {"q": 5419, "e": 1, "cert": {"method": "TRIAL_DIV", "max_divisor": 73}},
                    ],
                }
            ],
            "claimed_min_size": 1538847046315881,
        },
    }
    # Edge 1 (OPEN child finished later): sigma(127^4) = 262209281 kept as odd composite_rem
    # lcm(19^2 * 3^2 * 127^4, 262209281) = 221,621,891,173,371,599,529 > 10^12
    leaf_e4 = {
        "kind": "LEAF",
        "state": child_e4,
        "witness": {
            "reason": "SIZE_EXCEEDS_BOUND",
            "deductions": [
                {
                    "source_p": 127,
                    "d": 4,
                    "v2": 0,
                    "factors": [],
                    "composite_rem": 262209281,
                    "composite_min_prime": 3,
                }
            ],
            "claimed_min_size": 845209938609 * 262209281,
        },
    }
    return root_state, child_e4, split_node, leaf_e2, leaf_e4


def main() -> None:
    cert_path = Path(__file__).resolve().parent.parent / "Certificates" / "TerminalOriginal.json.gz"
    if not cert_path.is_file():
        raise RuntimeError("TerminalOriginal.json.gz missing; extract handoff first")

    root_state, child_e4, split_node, leaf_e2, leaf_e4 = build_1e12_mixed_split_fixtures()
    fp = "sha256:mixed-edge-regression-v1"
    task_0 = {
        "root": 19,
        "index": 0,
        "count": 1,
        "exponent": 2,
        "exact": False,
        "id": "P19_I00000",
    }

    with tempfile.TemporaryDirectory(prefix="opn-mixed-edge-") as tmp:
        root_tmp = Path(tmp)
        manifest_path = root_tmp / "Manifest.json"
        ledger_dir = root_tmp / "Ledgers"
        proof_dir = root_tmp / "Proofs"
        ledger_dir.mkdir()
        proof_dir.mkdir()

        manifest_path.write_text(
            json.dumps({
                "target_exponent": 12,
                "root_order": list(DEFAULT_CIRC_ORDER),
                "tasks": [task_0],
            }),
            encoding="utf-8",
        )

        store = DiskProofStore(proof_dir)
        ledger = FrontierLedgerV2(ledger_dir / "P19_I00000.sqlite", fp)
        ledger.seed([canonical_json_bytes(root_state)])
        tid, tok, _ = ledger.claim(now=0, ttl=60)

        # Persist split proof + CLOSED edge 0 proof, submit mixed [CLOSED, OPEN] atomically
        split_digest = store.put_json(split_node)
        closed_e2_digest = store.put_json({"nodes": [leaf_e2]})
        (open_e4_id,) = ledger.split_with_evidence(
            tid, tok, now=5,
            split_proof_sha256=split_digest,
            edge_records=[
                ("CLOSED", closed_e2_digest),
                ("OPEN", canonical_json_bytes(child_e4)),
            ],
        )
        ledger.close()

        # While edge 1 is still PENDING, audit MUST report OPEN_FRONTIER
        s_mid = run_full_audit(
            manifest_path, cert_path, ledger_dir, proof_dir, fp,
            root_set_name="original", override_upper_bound_N=10**12,
        )
        if s_mid["final_theorem_status"] != "INCOMPLETE_FRONTIER" or s_mid["total_open_frontier_tasks"] != 1:
            raise RuntimeError(f"mixed split with open edge mishandled: {s_mid}")
        print("[PASS] Mixed [CLOSED, OPEN] split accurately reports OPEN_FRONTIER before child finishes")

        # Claim and finish edge 1
        ledger = FrontierLedgerV2(ledger_dir / "P19_I00000.sqlite", fp)
        ctid, ctok, _ = ledger.claim(now=10, ttl=60)
        if ctid != open_e4_id:
            raise RuntimeError("claimed unexpected task id")
        leaf_e4_digest = store.put_json({"nodes": [leaf_e4]})
        ledger.finish(ctid, ctok, now=15, proof_sha256=leaf_e4_digest)
        ledger.close()

        # Full read-only audit MUST now verify both CLOSED edge 0 and RESULT edge 1
        s_done = run_full_audit(
            manifest_path, cert_path, ledger_dir, proof_dir, fp,
            root_set_name="original", override_upper_bound_N=10**12,
        )
        if s_done["final_theorem_status"] != "UNCONDITIONALLY_VERIFIED" or s_done["verified_closed_tasks"] != 1:
            raise RuntimeError(f"mixed split closure failed audit: {s_done}")
        print("[PASS] Mixed [CLOSED, OPEN] split + child RESULT closed cleanly as UNCONDITIONALLY_VERIFIED")

    print("FrontierV2MixedEdgeTests: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
