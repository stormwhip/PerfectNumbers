#!/usr/bin/env python3
"""Crash-safe worker driver bridging FrontierLedgerV2, DiskProofStore, and ProofTreeV21Frontier."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import threading
import time
from typing import Optional

from FrontierLedgerV2 import DiskProofStore, FrontierLedgerV2, LeaseLost


def _start_lease_renewer(
    ledger_path: Path,
    run_fingerprint: str,
    task_id: str,
    attempt: str,
    ttl: int,
    stop_event: threading.Event,
    lease_lost_flag: threading.Event,
) -> threading.Thread:
    interval = max(1.0, ttl / 3.0)

    def _loop() -> None:
        conn = FrontierLedgerV2(ledger_path, run_fingerprint)
        try:
            while not stop_event.wait(interval):
                try:
                    conn.renew(task_id, attempt, int(time.time()), ttl)
                except LeaseLost:
                    lease_lost_flag.set()
                    return
        finally:
            conn.close()

    t = threading.Thread(target=_loop, daemon=True)
    t.start()
    return t


def run_split_step(
    binary: Path,
    bound_exp: int,
    ledger_path: Path,
    proof_store: DiskProofStore,
    run_fingerprint: str,
    ttl: int = 120,
    no_db: bool = False,
) -> str:
    """Claim one PENDING task and perform a deterministic single-level C++ shallow split."""
    ledger = FrontierLedgerV2(ledger_path, run_fingerprint)
    try:
        claimed = ledger.claim(int(time.time()), ttl)
        if claimed is None:
            return "IDLE"
        task_id, attempt, state_bytes = claimed

        stop_ev = threading.Event()
        lost_ev = threading.Event()
        renewer = _start_lease_renewer(
            ledger_path, run_fingerprint, task_id, attempt, ttl, stop_ev, lost_ev
        )

        try:
            with tempfile.TemporaryDirectory(prefix="opn-split-") as tmp:
                in_bin = Path(tmp) / "in.bin"
                out_prefix = Path(tmp) / "child"
                in_bin.write_bytes(state_bytes)

                cmd = [str(binary), "split-state", str(bound_exp), str(in_bin), str(out_prefix)]
                if no_db:
                    cmd.append("--no-db")
                proc = subprocess.run(cmd, text=True, capture_output=True, check=False)

                if lost_ev.is_set():
                    return "LEASE_LOST"
                if proc.returncode == 10:
                    # SPLIT_ALL_CLOSED: must NOT submit empty split; caller must solve & emit leaf proof
                    return "ALL_CLOSED_NEEDS_PROOF"
                if proc.returncode != 0:
                    return f"SPLIT_ERROR_{proc.returncode}"

                meta_path = Path(f"{out_prefix}_meta.json")
                meta = json.loads(meta_path.read_text(encoding="utf-8"))
                split_meta_digest = proof_store.put_json(meta)

                edge_records = []
                for edge in meta["edges"]:
                    if edge["status"] == "OPEN":
                        edge_bytes = Path(edge["state_file"]).read_bytes()
                        edge_records.append(("OPEN", edge_bytes))
                    elif edge["status"] == "CLOSED":
                        # Record explicit unaudited closed-edge metadata until C++ emits full leaf DAG
                        closed_digest = proof_store.put_json({
                            "kind": "UNAUDITED_CPP_CLOSED_EDGE",
                            "branch_prime": meta["branch_prime"],
                            "edge": edge,
                        })
                        edge_records.append(("CLOSED", closed_digest))
                    else:
                        raise RuntimeError(f"unknown edge status: {edge}")

                ledger.split_with_evidence(
                    task_id, attempt, int(time.time()),
                    split_proof_sha256=split_meta_digest,
                    edge_records=edge_records,
                )
                return f"SPLIT_COMMITTED_OPEN_{meta['open_count']}"
        finally:
            stop_ev.set()
            renewer.join(timeout=5.0)
    finally:
        ledger.close()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--binary", type=Path, required=True)
    parser.add_argument("--bound-exp", type=int, default=2400)
    parser.add_argument("--ledger", type=Path, required=True)
    parser.add_argument("--proof-store", type=Path, required=True)
    parser.add_argument("--run-fingerprint", type=str, required=True)
    parser.add_argument("--ttl", type=int, default=120)
    parser.add_argument("--no-db", action="store_true")
    parser.add_argument("--max-splits", type=int, default=1)
    args = parser.parse_args()

    store = DiskProofStore(args.proof_store)
    for step in range(args.max_splits):
        res = run_split_step(
            binary=args.binary,
            bound_exp=args.bound_exp,
            ledger_path=args.ledger,
            proof_store=store,
            run_fingerprint=args.run_fingerprint,
            ttl=args.ttl,
            no_db=args.no_db,
        )
        print(f"DRIVER_STEP step={step} result={res}", flush=True)
        if res == "IDLE":
            break
    return 0


if __name__ == "__main__":
    sys.exit(main())
