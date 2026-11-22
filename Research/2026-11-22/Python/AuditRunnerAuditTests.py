"""Audit regression tests covering P3-1 through P3-4 fixes for AuditRunner2400."""

from __future__ import annotations

import json
from pathlib import Path
import tempfile

from AuditRunner2400 import run_full_audit
from FrontierLedgerV2 import DiskProofStore, FrontierLedgerV2
from IndependentVerifierV2 import (
    DEFAULT_CIRC_ORDER,
    ORIGINAL_ROOTS,
    REPLACEMENT_ROOTS,
    VerificationError,
    canonical_json_bytes,
)
import VerifyRootExponentCoverage
from VerifierV2Tests import build_valid_1e8_bundle


def main() -> None:
    cert_dir = Path(__file__).resolve().parent.parent / "Certificates"
    orig_cert = cert_dir / "TerminalOriginal.json.gz"
    repl_cert = cert_dir / "TerminalReplacement.json.gz"
    if not orig_cert.is_file() or not repl_cert.is_file():
        raise RuntimeError("Archived terminal certificates missing; extract handoff first")

    fp = "sha256:audit-p3-regression-v1"
    bundle = build_valid_1e8_bundle()
    split_node, leaf_node = bundle["nodes"]
    root_bytes = canonical_json_bytes(split_node["state"])
    child_bytes = canonical_json_bytes(split_node["children"][0]["state"])

    task_0 = {
        "root": 19,
        "index": 0,
        "count": 1,
        "exponent": 2,
        "exact": False,
        "id": "P19_I00000",
    }

    with tempfile.TemporaryDirectory(prefix="opn-p3-audit-") as tmp:
        root_tmp = Path(tmp)
        manifest_path = root_tmp / "Manifest.json"
        ledger_dir = root_tmp / "Ledgers"
        proof_dir = root_tmp / "Proofs"
        legacy_dir = root_tmp / "LegacyStates"
        ledger_dir.mkdir()
        proof_dir.mkdir()
        legacy_dir.mkdir()

        manifest_path.write_text(
            json.dumps({
                "target_exponent": 8,
                "root_order": list(DEFAULT_CIRC_ORDER),
                "tasks": [task_0],
            }),
            encoding="utf-8",
        )

        # P3-1: 0-byte corrupted ledger file must NOT be mutated by audit and must report FAILED
        bad_db = ledger_dir / "P19_I00000.sqlite"
        bad_db.write_bytes(b"")
        s_bad_db = run_full_audit(
            manifest_path, orig_cert, ledger_dir, proof_dir, fp,
            root_set_name="original", override_upper_bound_N=10**8,
        )
        if s_bad_db["counts_by_status"].get("FAILED") != 1 or bad_db.stat().st_size != 0:
            raise RuntimeError(f"P3-1 failed: audit mutated or mishandled 0-byte db: {s_bad_db}")
        bad_db.unlink()
        print("[PASS] P3-1: read-only audit rejected 0-byte ledger without mutating file")

        # P3-2A: Legacy TIMEOUT / UNRESOLVED must preserve status (not fall back to UNSTARTED)
        for st_name in ("TIMEOUT", "UNRESOLVED"):
            (legacy_dir / "P19_I00000.json").write_text(
                json.dumps({"task": task_0, "status": st_name, "exit_code": None}),
                encoding="utf-8",
            )
            s_leg = run_full_audit(
                manifest_path, orig_cert, ledger_dir, proof_dir, fp,
                root_set_name="original", legacy_states_dir=legacy_dir, override_upper_bound_N=10**8,
            )
            if s_leg["counts_by_status"].get(st_name) != 1:
                raise RuntimeError(f"P3-2A failed for {st_name}: {s_leg}")
        print("[PASS] P3-2A: legacy TIMEOUT and UNRESOLVED classifications preserved")

        # P3-3A: SPLIT with unclosed PENDING child -> OPEN_FRONTIER (not verified)
        store = DiskProofStore(proof_dir)
        ledger = FrontierLedgerV2(ledger_dir / "P19_I00000.sqlite", fp)
        (rid,) = ledger.seed([root_bytes])
        tid, tok, _ = ledger.claim(now=0, ttl=30)
        split_digest = store.put_json(split_node)
        (cid,) = ledger.split_with_evidence(
            tid, tok, now=1, split_proof_sha256=split_digest,
            edge_records=[("OPEN", child_bytes)],
        )
        ledger.close()

        s_open = run_full_audit(
            manifest_path, orig_cert, ledger_dir, proof_dir, fp,
            root_set_name="original", override_upper_bound_N=10**8,
        )
        if (
            s_open["final_theorem_status"] != "INCOMPLETE_FRONTIER"
            or s_open["counts_by_status"].get("OPEN_FRONTIER") != 1
            or s_open["total_open_frontier_tasks"] != 1
        ):
            raise RuntimeError(f"P3-3A OPEN_FRONTIER mishandled: {s_open}")
        print("[PASS] P3-3A: SPLIT with PENDING child accurately reported as OPEN_FRONTIER")

        # P3-3B: Finish child with valid disk proof -> SPLIT + RESULT closes cleanly
        ledger = FrontierLedgerV2(ledger_dir / "P19_I00000.sqlite", fp)
        ctid, ctok, _ = ledger.claim(now=2, ttl=30)
        if ctid != cid:
            raise RuntimeError("expected child task claim")
        leaf_digest = store.put_json({"nodes": [leaf_node]})
        ledger.finish(ctid, ctok, now=3, proof_sha256=leaf_digest)
        ledger.close()

        s_closed = run_full_audit(
            manifest_path, orig_cert, ledger_dir, proof_dir, fp,
            root_set_name="original", override_upper_bound_N=10**8,
        )
        if s_closed["final_theorem_status"] != "UNCONDITIONALLY_VERIFIED":
            raise RuntimeError(f"P3-3B valid SPLIT+RESULT closure rejected: {s_closed}")
        print("[PASS] P3-3B: SPLIT + RESULT full disk-based closure accepted")

        # P3-3C: Tamper disk proof file after finish() -> must fail audit
        tampered_file = proof_dir / leaf_digest[:2] / f"{leaf_digest}.json"
        tampered_file.write_text('{"tampered": true}', encoding="utf-8")
        s_tamper = run_full_audit(
            manifest_path, orig_cert, ledger_dir, proof_dir, fp,
            root_set_name="original", override_upper_bound_N=10**8,
        )
        if (
            s_tamper["final_theorem_status"] != "INCOMPLETE_FRONTIER"
            or s_tamper["counts_by_status"].get("FAILED") != 1
        ):
            raise RuntimeError(f"P3-3C tampered proof file wrongly accepted: {s_tamper}")
        print("[PASS] P3-3C: post-finish disk proof tampering rejected as FAILED")

        # P3-4: Production 10^2400 manifest validation (3,072 original & 3,058 replacement)
        for name, cert_p, roots in (
            ("original", orig_cert, ORIGINAL_ROOTS),
            ("replacement", repl_cert, REPLACEMENT_ROOTS),
        ):
            m_prod = root_tmp / f"Manifest_{name}.json"
            tasks_prod = list(VerifyRootExponentCoverage.canonical_tasks(sorted(roots)))
            m_prod.write_text(
                json.dumps({"target_exponent": 2400, "root_order": sorted(roots), "tasks": tasks_prod}),
                encoding="utf-8",
            )
            empty_ledgers = root_tmp / f"EmptyLedgers_{name}"
            empty_ledgers.mkdir()
            s_prod = run_full_audit(
                m_prod, cert_p, empty_ledgers, proof_dir, fp, root_set_name=name,
            )
            if s_prod["total_tasks"] != len(tasks_prod) or s_prod["verified_closed_tasks"] != 0:
                raise RuntimeError(f"P3-4 production manifest audit mismatch for {name}: {s_prod}")
            print(f"[PASS] P3-4: production 10^2400 {name} manifest ({len(tasks_prod)} tasks) + terminal cert verified")

        # P3-4B: Missing task in production manifest must raise VerificationError (not raw ValueError)
        m_broken = root_tmp / "Manifest_broken.json"
        broken_tasks = list(VerifyRootExponentCoverage.canonical_tasks(sorted(ORIGINAL_ROOTS)))[:-1]
        m_broken.write_text(
            json.dumps({"target_exponent": 2400, "root_order": sorted(ORIGINAL_ROOTS), "tasks": broken_tasks}),
            encoding="utf-8",
        )
        try:
            run_full_audit(m_broken, orig_cert, ledger_dir, proof_dir, fp, root_set_name="original")
            raise RuntimeError("broken 3,071-task manifest was wrongly accepted")
        except VerificationError:
            print("[PASS] P3-4B: truncated 3,071-task production manifest rejected with VerificationError")

    print("AuditRunnerAuditTests: ALL P3-1..P3-4 REGRESSION TESTS PASSED")


if __name__ == "__main__":
    main()
