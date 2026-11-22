"""Tests for AuditRunner2400: root-set binding, unaudited PROVEN rejection, and full closure."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

from AuditRunner2400 import render_markdown_report, run_full_audit
from FrontierLedgerV2 import DiskProofStore, FrontierLedgerV2
from IndependentVerifierV2 import DEFAULT_CIRC_ORDER, VerificationError, canonical_json_bytes
from VerifierV2Tests import build_valid_1e8_bundle


def main() -> None:
    cert_dir = Path(__file__).resolve().parent.parent / "Certificates"
    orig_cert = cert_dir / "TerminalOriginal.json.gz"
    repl_cert = cert_dir / "TerminalReplacement.json.gz"
    if not orig_cert.is_file() or not repl_cert.is_file():
        raise RuntimeError("Archived terminal certificates missing; extract handoff first")

    fp = "sha256:audit-runner-test-v1"
    bundle = build_valid_1e8_bundle()
    root_bytes = canonical_json_bytes(bundle["nodes"][0]["state"])

    with tempfile.TemporaryDirectory(prefix="opn-audit-test-") as tmp:
        root_tmp = Path(tmp)
        manifest_path = root_tmp / "Manifest.json"
        ledger_dir = root_tmp / "Ledgers"
        proof_dir = root_tmp / "Proofs"
        legacy_dir = root_tmp / "LegacyStates"
        ledger_dir.mkdir()
        proof_dir.mkdir()
        legacy_dir.mkdir()

        task_0 = {
            "root": 19,
            "index": 0,
            "count": 1,
            "exponent": 2,
            "exact": False,
            "id": "P19_I00000",
        }
        manifest_path.write_text(
            json.dumps({
                "target_exponent": 8,
                "root_order": list(DEFAULT_CIRC_ORDER),
                "tasks": [task_0],
            }),
            encoding="utf-8",
        )

        # Test 1: Pairing TerminalReplacement.json.gz with original root manifest MUST FAIL
        try:
            run_full_audit(
                manifest_path, repl_cert, ledger_dir, proof_dir, fp,
                root_set_name="original", override_upper_bound_N=10**8,
            )
            raise RuntimeError("mismatched terminal certificate was wrongly accepted")
        except VerificationError:
            print("[PASS] Test 1: mismatched root set between terminal cert and manifest rejected")

        # Test 2: Legacy PROVEN record without proof DAG MUST NOT close theorem
        (legacy_dir / "P19_I00000.json").write_text(
            json.dumps({"task": task_0, "status": "PROVEN", "exit_code": 0}),
            encoding="utf-8",
        )
        s_legacy = run_full_audit(
            manifest_path, orig_cert, ledger_dir, proof_dir, fp,
            root_set_name="original", legacy_states_dir=legacy_dir, override_upper_bound_N=10**8,
        )
        if (
            s_legacy["final_theorem_status"] != "INCOMPLETE_FRONTIER"
            or s_legacy["verified_closed_tasks"] != 0
            or s_legacy["counts_by_status"].get("PROGRAM_PROVEN_UNAUDITED") != 1
        ):
            raise RuntimeError(f"legacy PROVEN mishandled: {s_legacy}")
        print("[PASS] Test 2: legacy PROVEN flagged as PROGRAM_PROVEN_UNAUDITED (0 verified)")

        # Test 3: Seed ledger + finish with valid disk proof -> UNCONDITIONALLY_VERIFIED
        store = DiskProofStore(proof_dir)
        ledger = FrontierLedgerV2(ledger_dir / "P19_I00000.sqlite", fp)
        (rid,) = ledger.seed([root_bytes])
        tid, tok, _ = ledger.claim(now=0, ttl=30)
        digest = store.put_json(bundle)
        ledger.finish(tid, tok, now=1, proof_sha256=digest)
        ledger.close()

        s_ok = run_full_audit(
            manifest_path, orig_cert, ledger_dir, proof_dir, fp,
            root_set_name="original", legacy_states_dir=legacy_dir, override_upper_bound_N=10**8,
        )
        if s_ok["final_theorem_status"] != "UNCONDITIONALLY_VERIFIED" or s_ok["verified_closed_tasks"] != 1:
            raise RuntimeError(f"valid verified closure rejected: {s_ok}")
        md = render_markdown_report(s_ok)
        if "UNCONDITIONALLY_VERIFIED" not in md:
            raise RuntimeError("markdown report missing verdict")
        print("[PASS] Test 3: full terminal + ledger + IndependentVerifierV2 closure accepted")

    print("AuditRunnerTests: ALL TESTS PASSED")


if __name__ == "__main__":
    main()
