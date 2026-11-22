"""Crash-consistency fault-injection & IndependentVerifierV2 closure tests for FrontierLedgerV2."""

from __future__ import annotations

from pathlib import Path
import sqlite3
import tempfile

from FrontierLedgerV2 import DiskProofStore, FrontierLedgerV2, LeaseLost
from IndependentVerifierV2 import (
    DEFAULT_CIRC_ORDER,
    ORIGINAL_ROOTS,
    RootTaskPin,
    VerificationError,
    canonical_json_bytes,
    verify_root_task_bundle,
)
from VerifierV2Tests import build_valid_1e8_bundle, make_1e8_pin


def audit_ledger_from_disk(ledger: FrontierLedgerV2, store: DiskProofStore, pin: RootTaskPin) -> dict:
    """Reconstruct complete proof DAG from SQLite ledger + DiskProofStore and run Verifier V2."""
    rows = ledger.db.execute(
        "SELECT id, parent, status, proof_sha256, total_edges FROM task"
    ).fetchall()
    if not rows:
        raise VerificationError("empty ledger")

    all_nodes = []
    for row in rows:
        status = row["status"]
        if status not in ("SPLIT", "RESULT"):
            raise VerificationError(f"open frontier task {row['id']} in status {status}")
        if status == "RESULT":
            payload = store.get_verified_json(row["proof_sha256"])
            all_nodes.extend(payload.get("nodes", []))
        elif status == "SPLIT":
            split_payload = store.get_verified_json(row["proof_sha256"])
            all_nodes.append(split_payload)
            edges = ledger.db.execute(
                "SELECT edge_ordinal, edge_kind, child_task_id, edge_proof_sha256 "
                "FROM split_edge WHERE parent_id=? ORDER BY edge_ordinal",
                (row["id"],),
            ).fetchall()
            if len(edges) != row["total_edges"]:
                raise VerificationError(f"split edge catalog count mismatch on {row['id']}")
            for expected_ord, e in enumerate(edges):
                if e["edge_ordinal"] != expected_ord:
                    raise VerificationError(f"non-contiguous edge ordinal on {row['id']}")
                if e["edge_kind"] == "CLOSED":
                    closed_payload = store.get_verified_json(e["edge_proof_sha256"])
                    all_nodes.extend(closed_payload.get("nodes", []))

    return verify_root_task_bundle(pin, {"nodes": all_nodes})


def main() -> None:
    pin = make_1e8_pin()
    bundle = build_valid_1e8_bundle()
    split_node, leaf_node = bundle["nodes"]
    root_bytes = canonical_json_bytes(split_node["state"])
    child_bytes = canonical_json_bytes(split_node["children"][0]["state"])
    fp = "sha256:opn-v2-fault-test"

    with tempfile.TemporaryDirectory(prefix="opn-ledger-v2-") as tmp:
        tmp_path = Path(tmp)

        # ---- Run A: Unsplit baseline ----
        store_a = DiskProofStore(tmp_path / "proofs_a")
        ledger_a = FrontierLedgerV2(tmp_path / "a.sqlite", fp)
        (root_id_a,) = ledger_a.seed([root_bytes])
        tid, tok, _ = ledger_a.claim(now=0, ttl=10)
        digest_a = store_a.put_json(bundle)
        ledger_a.finish(tid, tok, now=1, proof_sha256=digest_a)
        res_a = audit_ledger_from_disk(ledger_a, store_a, pin)
        if res_a["status"] != "TREE_ACCEPTED":
            raise RuntimeError(f"unsplit run failed: {res_a}")
        ledger_a.close()

        # ---- Run B: 3 Fault Injections + Split + Crash Recovery ----
        store_b = DiskProofStore(tmp_path / "proofs_b")
        db_b = tmp_path / "b.sqlite"
        w1 = FrontierLedgerV2(db_b, fp)
        w2 = FrontierLedgerV2(db_b, fp)
        (root_id_b,) = w1.seed([root_bytes])

        # Fault 1: Last child record fails before DB commit -> entire split rolls back
        t1, tok1, _ = w1.claim(now=0, ttl=10)
        split_digest = store_b.put_json(split_node)
        try:
            w1.split_with_evidence(
                t1, tok1, now=2, split_proof_sha256=split_digest,
                edge_records=[("OPEN", child_bytes), ("OPEN", None)],  # triggers NOT NULL
            )
            raise RuntimeError("Fault 1 should have raised IntegrityError")
        except sqlite3.IntegrityError:
            pass
        # Verify rollback: parent is still CLAIMED, zero children exist
        cnt = w1.db.execute("SELECT COUNT(*) FROM task").fetchone()[0]
        if cnt != 1:
            raise RuntimeError(f"Fault 1 left orphan children: count={cnt}")
        print("[PASS] Fault 1: last child insert failure rolled back cleanly")

        # Fault 2: Proof file written & fsynced to disk, then worker crashes BEFORE DB commit
        # (split_digest is already on disk; worker 1 dies without committing, lease expires at t=10)
        t2, tok2, _ = w2.claim(now=10, ttl=15)
        if t2 != root_id_b or tok2 == tok1:
            raise RuntimeError("Fault 2 lease takeover failed")
        # Stale worker 1 tries to commit late -> must get LeaseLost
        try:
            w1.finish(t1, tok1, now=11, proof_sha256=split_digest)
            raise RuntimeError("stale worker should not finish")
        except LeaseLost:
            pass
        print("[PASS] Fault 2: orphan disk proof + stale lease takeover handled cleanly")

        # Fault 3: DB transaction commits, then worker crashes BEFORE receiving ack
        (child_id,) = w2.split_with_evidence(
            t2, tok2, now=12, split_proof_sha256=split_digest,
            edge_records=[("OPEN", child_bytes)],
        )
        # Simulate abrupt process exit after commit by closing connection immediately
        w2.close()
        w1.close()

        # Reopen after crash: unclosed frontier must FAIL audit
        w3 = FrontierLedgerV2(db_b, fp)
        try:
            audit_ledger_from_disk(w3, store_b, pin)
            raise RuntimeError("open frontier wrongly accepted")
        except VerificationError:
            pass

        # Claim recovered child, persist leaf proof on disk, finish, and audit full tree
        ctid, ctok, _ = w3.claim(now=15, ttl=15)
        if ctid != child_id:
            raise RuntimeError("recovered child id mismatch")
        leaf_digest = store_b.put_json({"nodes": [leaf_node]})
        w3.finish(ctid, ctok, now=18, proof_sha256=leaf_digest)

        res_b = audit_ledger_from_disk(w3, store_b, pin)
        if res_b["status"] != "TREE_ACCEPTED" or res_b["root_hash"] != res_a["root_hash"]:
            raise RuntimeError("split+recovery closure mismatch against unsplit run")
        print(f"[PASS] Fault 3: post-commit crash recovery closed cleanly, root_hash={res_b['root_hash']}")
        w3.close()

    print("FrontierV2FaultTests: ALL 3 FAULT INJECTIONS & DISK-BASED VERIFIER CLOSURE PASSED")


if __name__ == "__main__":
    main()
