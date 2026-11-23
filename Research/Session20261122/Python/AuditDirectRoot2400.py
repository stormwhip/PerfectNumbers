#!/usr/bin/env python3
"""End-to-end independent 2400 audit of direct root leaves with empty ledgers.

Rechecks the certified original coprime class, constructs the canonical 3072
manifest, then runs the ordinary AuditRunner2400 with absent ledger/proof files.
Only integer-certified contradictions, including fully enumerated finite quotients, may become VERIFIED_CLOSED.
"""
from __future__ import annotations

import json
from pathlib import Path
import tempfile

from AuditRunner2400 import run_full_audit
from IndependentVerifierV2 import DEFAULT_CIRC_ORDER
from VerifyRootExponentCoverage import canonical_tasks


def main() -> None:
    base = Path(__file__).resolve().parent.parent
    terminal = base / "Certificates" / "TerminalOriginal.json.gz"
    if not terminal.is_file():
        raise RuntimeError(f"missing archived coprime certificate: {terminal}")

    with tempfile.TemporaryDirectory(prefix="opn-root-audit-") as folder:
        temp = Path(folder)
        manifest = temp / "Manifest.json"
        manifest.write_text(json.dumps({
            "target_exponent": 2400,
            "root_order": list(DEFAULT_CIRC_ORDER),
            "tasks": list(canonical_tasks(DEFAULT_CIRC_ORDER)),
        }) + "\n", encoding="utf-8")
        summary = run_full_audit(
            manifest_path=manifest,
            terminal_cert_path=terminal,
            ledger_dir=temp / "MissingLedgers",
            proof_store_dir=temp / "EmptyProofs",
            run_fingerprint="sha256:direct-root-audit-v1",
            root_set_name="original",
        )
        expected = {
            "VERIFIED_CLOSED": 1448,
            "UNSTARTED": 1624,
        }
        if (summary["total_tasks"] != 3072
                or summary["counts_by_status"] != expected
                or summary["verified_closed_tasks"] != 1448
                or summary["total_open_frontier_tasks"] != 1624
                or summary["final_theorem_status"] != "INCOMPLETE_FRONTIER"):
            raise RuntimeError(f"unexpected rigorous audit summary: {summary}")
        print(json.dumps({
            "terminal_status": summary["terminal_certificate"]["status"],
            "proof_status": summary["final_theorem_status"],
            "total_tasks": summary["total_tasks"],
            "counts_by_status": summary["counts_by_status"],
            "independent_verified_leaves": summary["verified_closed_tasks"],
            "remaining_open_top_level_tasks": summary["total_open_frontier_tasks"],
        }, indent=2))
        print("AuditDirectRoot2400: PASS")


if __name__ == "__main__":
    main()
