#!/usr/bin/env python3
"""Exhaustive 3,072-task (or 3,058-task) independent audit runner and report aggregator.

Never trusts bare solver `PROVEN` strings or unverified SQLite `RESULT` records.
Every accepted shard must pass IndependentVerifierV2 from an externally pinned RootTaskPin.
"""

from __future__ import annotations

import argparse
import datetime
import hashlib
import json
from pathlib import Path
import sys
import time
from typing import Dict, List, Optional, Tuple

from FrontierLedgerV2 import DiskProofStore, FrontierLedgerV2
from IndependentVerifierV2 import (
    DEFAULT_CIRC_ORDER,
    ORIGINAL_ROOTS,
    REPLACEMENT_ROOTS,
    RootTaskPin,
    VerificationError,
    sha256_hex,
    strict_json_loads,
    verify_root_task_bundle,
    verify_terminal_and_manifest,
)
import VerifyRootExponentCoverage


REPLACEMENT_CIRC_ORDER: Tuple[int, ...] = (23, 7, 11, 31, 13, 3, 5, 17)


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        while True:
            chunk = stream.read(4 * 1024 * 1024)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()


import sqlite3
from IndependentVerifierV2 import (
    DEFAULT_CIRC_ORDER,
    ORIGINAL_ROOTS,
    REPLACEMENT_ROOTS,
    RootTaskPin,
    VerificationError,
    canonical_json_bytes,
    parse_state_dict,
    strict_json_loads,
    verify_root_task_bundle,
    verify_terminal_and_manifest,
)


def _open_ledger_readonly(db_path: Path, expected_fingerprint: str) -> sqlite3.Connection:
    """Open SQLite ledger in strict read-only mode; never creates or mutates files."""
    uri = f"file:{db_path.resolve()}?mode=ro"
    try:
        conn = sqlite3.connect(uri, uri=True)
    except sqlite3.Error as exc:
        raise VerificationError(f"cannot open ledger read-only {db_path.name}: {exc}") from exc
    conn.row_factory = sqlite3.Row
    try:
        row = conn.execute("SELECT fingerprint FROM run WHERE singleton=1").fetchone()
    except sqlite3.Error as exc:
        conn.close()
        raise VerificationError(f"corrupted or uninitialized ledger {db_path.name}: {exc}") from exc
    if row is None or row["fingerprint"] != expected_fingerprint:
        conn.close()
        raise VerificationError(
            f"ledger {db_path.name} run_fingerprint mismatch "
            f"(expected {expected_fingerprint!r}, got {row['fingerprint'] if row else None!r})"
        )
    return conn


def _merge_dag_nodes(target_by_hash: Dict[str, Tuple[bytes, dict]], nodes: object, source_label: str) -> None:
    """Validate nodes list and deduplicate byte-identical DAG nodes; reject conflicting duplicates."""
    if not isinstance(nodes, list):
        raise VerificationError(f"{source_label}: expected 'nodes' to be a list")
    for node in nodes:
        if not isinstance(node, dict) or "state" not in node:
            raise VerificationError(f"{source_label}: node missing 'state'")
        h = parse_state_dict(node["state"]).state_hash()
        raw = canonical_json_bytes(node)
        existing = target_by_hash.get(h)
        if existing is None:
            target_by_hash[h] = (raw, node)
        elif existing[0] != raw:
            raise VerificationError(
                f"{source_label}: conflicting duplicate proof node for state hash {h}"
            )


def audit_single_shard(
    task: dict,
    pin: RootTaskPin,
    ledger_dir: Path,
    proof_store: DiskProofStore,
    run_fingerprint: str,
    legacy_states_dir: Optional[Path] = None,
) -> dict:
    """Independently audit one top-level shard (strictly read-only on SQLite and disk proofs)."""
    tid = task["id"]
    db_path = ledger_dir / f"{tid}.sqlite"
    t0 = time.monotonic()

    if not db_path.is_file():
        if legacy_states_dir is not None:
            legacy_file = legacy_states_dir / f"{tid}.json"
            if legacy_file.is_file():
                try:
                    rec = strict_json_loads(legacy_file.read_text(encoding="utf-8"))
                    if isinstance(rec, dict) and rec.get("task") == task:
                        legacy_status = rec.get("status")
                        if legacy_status == "PROVEN":
                            return {
                                "id": tid,
                                "root": task["root"],
                                "index": task["index"],
                                "status": "PROGRAM_PROVEN_UNAUDITED",
                                "open_tasks": 1,
                                "verify_seconds": time.monotonic() - t0,
                                "detail": "legacy V21 PROVEN record has no independent proof DAG",
                            }
                        if legacy_status in ("TIMEOUT", "UNRESOLVED", "INTERRUPTED"):
                            return {
                                "id": tid,
                                "root": task["root"],
                                "index": task["index"],
                                "status": legacy_status,
                                "open_tasks": 1,
                                "verify_seconds": time.monotonic() - t0,
                                "detail": f"legacy V21 ended with {legacy_status}",
                            }
                except (OSError, VerificationError):
                    return {
                        "id": tid,
                        "root": task["root"],
                        "index": task["index"],
                        "status": "FAILED",
                        "open_tasks": 1,
                        "verify_seconds": time.monotonic() - t0,
                        "detail": f"corrupted legacy state file {legacy_file.name}",
                    }
        return {
            "id": tid,
            "root": task["root"],
            "index": task["index"],
            "status": "UNSTARTED",
            "open_tasks": 1,
            "verify_seconds": time.monotonic() - t0,
            "detail": f"missing ledger {db_path.name}",
        }

    conn = None
    try:
        conn = _open_ledger_readonly(db_path, run_fingerprint)
        rows = conn.execute(
            "SELECT id, parent, status, proof_sha256, total_edges FROM task"
        ).fetchall()
        if not rows:
            raise VerificationError("empty SQLite ledger")

        open_rows = [r for r in rows if r["status"] not in ("SPLIT", "RESULT")]
        if open_rows:
            return {
                "id": tid,
                "root": task["root"],
                "index": task["index"],
                "status": "OPEN_FRONTIER",
                "open_tasks": len(open_rows),
                "total_ledger_tasks": len(rows),
                "verify_seconds": time.monotonic() - t0,
                "detail": f"{len(open_rows)}/{len(rows)} tasks still PENDING/CLAIMED",
            }

        task_parents = {r["id"]: r["parent"] for r in rows}
        merged_nodes: Dict[str, Tuple[bytes, dict]] = {}

        for row in rows:
            if row["status"] == "RESULT":
                payload = proof_store.get_verified_json(row["proof_sha256"])
                _merge_dag_nodes(merged_nodes, payload.get("nodes"), f"RESULT:{row['id']}")
            elif row["status"] == "SPLIT":
                split_payload = proof_store.get_verified_json(row["proof_sha256"])
                _merge_dag_nodes(merged_nodes, [split_payload], f"SPLIT:{row['id']}")
                edges = conn.execute(
                    "SELECT edge_ordinal, edge_kind, child_task_id, edge_proof_sha256 "
                    "FROM split_edge WHERE parent_id=? ORDER BY edge_ordinal",
                    (row["id"],),
                ).fetchall()
                if len(edges) != row["total_edges"]:
                    raise VerificationError(f"split edge count mismatch on {row['id']}")
                for expected_ord, e in enumerate(edges):
                    if e["edge_ordinal"] != expected_ord:
                        raise VerificationError(f"non-contiguous edge ordinal on {row['id']}")
                    if e["edge_kind"] == "OPEN":
                        cid = e["child_task_id"]
                        if cid not in task_parents or task_parents[cid] != row["id"]:
                            raise VerificationError(
                                f"OPEN edge {expected_ord} references missing or mismatched child {cid}"
                            )
                    elif e["edge_kind"] == "CLOSED":
                        closed_payload = proof_store.get_verified_json(e["edge_proof_sha256"])
                        _merge_dag_nodes(
                            merged_nodes, closed_payload.get("nodes"), f"CLOSED:{row['id']}:{expected_ord}"
                        )
                    else:
                        raise VerificationError(f"unknown split_edge kind {e['edge_kind']!r}")

        deduped_nodes = [node for _, node in merged_nodes.values()]
        verdict = verify_root_task_bundle(pin, {"nodes": deduped_nodes})
        if verdict.get("status") != "TREE_ACCEPTED":
            raise VerificationError(f"unexpected verifier verdict: {verdict}")

        return {
            "id": tid,
            "root": task["root"],
            "index": task["index"],
            "status": "VERIFIED_CLOSED",
            "open_tasks": 0,
            "splits_verified": verdict["splits_verified"],
            "leaves_verified": verdict["leaves_verified"],
            "verified_primes_count": verdict["verified_primes_count"],
            "root_hash": verdict["root_hash"],
            "verify_seconds": time.monotonic() - t0,
        }
    except (VerificationError, ValueError, OSError, sqlite3.Error) as exc:
        return {
            "id": tid,
            "root": task["root"],
            "index": task["index"],
            "status": "FAILED",
            "open_tasks": 1,
            "verify_seconds": time.monotonic() - t0,
            "detail": str(exc),
        }
    finally:
        if conn is not None:
            conn.close()


def run_full_audit(
    manifest_path: Path,
    terminal_cert_path: Path,
    ledger_dir: Path,
    proof_store_dir: Path,
    run_fingerprint: str,
    root_set_name: str = "original",
    legacy_states_dir: Optional[Path] = None,
    override_upper_bound_N: Optional[int] = None,
    override_circ_order: Optional[Tuple[int, ...]] = None,
) -> dict:
    """Execute full partition + terminal + per-shard independent verification."""
    t_start = time.monotonic()
    if root_set_name == "original":
        expected_roots = ORIGINAL_ROOTS
        circ_order = override_circ_order or DEFAULT_CIRC_ORDER
    elif root_set_name == "replacement":
        expected_roots = REPLACEMENT_ROOTS
        circ_order = override_circ_order or REPLACEMENT_CIRC_ORDER
    else:
        raise VerificationError(f"unknown root_set_name: {root_set_name!r}")

    if tuple(sorted(circ_order)) != tuple(sorted(expected_roots)):
        raise VerificationError(f"circ_order {circ_order} does not match root_set {expected_roots}")

    terminal_info = verify_terminal_and_manifest(
        terminal_cert_path=terminal_cert_path,
        expected_root_set=expected_roots,
        manifest_path=None,
    )

    manifest = strict_json_loads(manifest_path.read_text(encoding="utf-8"))
    if not isinstance(manifest, dict):
        raise VerificationError("manifest must be a JSON object")

    root_order = tuple(manifest.get("root_order", ()))
    if tuple(sorted(root_order)) != tuple(sorted(expected_roots)):
        raise VerificationError(
            f"manifest root_order {root_order} does not match terminal certificate roots {expected_roots}"
        )

    if override_upper_bound_N is None:
        try:
            VerifyRootExponentCoverage.verify_manifest(manifest)
        except (ValueError, KeyError, TypeError) as exc:
            raise VerificationError(f"manifest coverage verification failed: {exc}") from exc
        upper_bound_N = 10**2400
    else:
        upper_bound_N = override_upper_bound_N

    tasks = manifest.get("tasks")
    if not isinstance(tasks, list) or not tasks:
        raise VerificationError("manifest has empty or invalid tasks list")

    store = DiskProofStore(proof_store_dir)
    results: List[dict] = []
    counts_by_status: Dict[str, int] = {}
    per_root_summary: Dict[int, Dict[str, int]] = {}
    total_open_tasks = 0

    for task in tasks:
        pin = RootTaskPin(
            upper_bound_N=upper_bound_N,
            root_set=expected_roots,
            root_order=root_order,
            circ_order=circ_order,
            root_prime=task["root"],
            root_exp=task["exponent"],
            root_exact=task["exact"],
        )
        res = audit_single_shard(
            task=task,
            pin=pin,
            ledger_dir=ledger_dir,
            proof_store=store,
            run_fingerprint=run_fingerprint,
            legacy_states_dir=legacy_states_dir,
        )
        results.append(res)
        st = res["status"]
        counts_by_status[st] = counts_by_status.get(st, 0) + 1
        total_open_tasks += res.get("open_tasks", 0)
        rsum = per_root_summary.setdefault(task["root"], {"total": 0, "verified_closed": 0})
        rsum["total"] += 1
        if st == "VERIFIED_CLOSED":
            rsum["verified_closed"] += 1

    verified_count = counts_by_status.get("VERIFIED_CLOSED", 0)
    all_closed = (
        verified_count == len(tasks)
        and total_open_tasks == 0
        and counts_by_status.get("FAILED", 0) == 0
    )

    return {
        "audit_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "final_theorem_status": "UNCONDITIONALLY_VERIFIED" if all_closed else "INCOMPLETE_FRONTIER",
        "root_set_name": root_set_name,
        "root_set": list(expected_roots),
        "root_order": list(root_order),
        "circ_order": list(circ_order),
        "target_upper_bound_digits": len(str(upper_bound_N)) - 1,
        "terminal_certificate": terminal_info,
        "manifest_sha256": file_sha256(manifest_path),
        "total_tasks": len(tasks),
        "verified_closed_tasks": verified_count,
        "total_open_frontier_tasks": total_open_tasks,
        "counts_by_status": counts_by_status,
        "per_root_summary": {str(k): v for k, v in sorted(per_root_summary.items())},
        "verify_wall_seconds": time.monotonic() - t_start,
        "non_closed_samples": [r for r in results if r["status"] != "VERIFIED_CLOSED"][:50],
    }

def render_markdown_report(summary: dict) -> str:
    lines = [
        "# PerfectNumbers 全量独立验收汇总报告",
        "",
        f"- **验收时间 (UTC)**：{summary['audit_utc']}",
        f"- **最终定理状态**：`{summary['final_theorem_status']}`",
        f"- **根集与顺序**：`{summary['root_set_name']}` / `root_order={summary['root_order']}`",
        f"- **互素证书核验**：`{summary['terminal_certificate']['status']}` (`sha256={summary['terminal_certificate']['terminal_sha256']}`)",
        f"- **顶层任务闭合度**：`{summary['verified_closed_tasks']} / {summary['total_tasks']}`（开放前沿任务数：`{summary['total_open_frontier_tasks']}`）",
        f"- **独立复核墙钟耗时**：`{summary['verify_wall_seconds']:.3f}s`",
        "",
        "## 按根素数闭合统计",
        "",
        "| 根素数 | 顶层任务总数 | 已独立验证闭合 | 剩余未闭合 |",
        "| ---: | ---: | ---: | ---: |",
    ]
    for root_str, st in summary["per_root_summary"].items():
        rem = st["total"] - st["verified_closed"]
        lines.append(f"| {root_str} | {st['total']} | {st['verified_closed']} | {rem} |")
    lines.extend([
        "",
        "## 按状态分类计数",
        "",
        "```json",
        json.dumps(summary["counts_by_status"], indent=2, ensure_ascii=False),
        "```",
    ])
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--terminal-cert", type=Path, required=True)
    parser.add_argument("--ledger-dir", type=Path, required=True)
    parser.add_argument("--proof-store", type=Path, required=True)
    parser.add_argument("--run-fingerprint", type=str, required=True)
    parser.add_argument("--root-set", choices=("original", "replacement"), default="original")
    parser.add_argument("--legacy-states-dir", type=Path, default=None)
    parser.add_argument("--out-json", type=Path, default=Path("AuditSummary.json"))
    parser.add_argument("--out-md", type=Path, default=Path("AuditSummary.md"))
    args = parser.parse_args()

    summary = run_full_audit(
        manifest_path=args.manifest,
        terminal_cert_path=args.terminal_cert,
        ledger_dir=args.ledger_dir,
        proof_store_dir=args.proof_store,
        run_fingerprint=args.run_fingerprint,
        root_set_name=args.root_set,
        legacy_states_dir=args.legacy_states_dir,
    )
    args.out_json.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    args.out_md.write_text(render_markdown_report(summary), encoding="utf-8")
    print(
        f"AUDIT_COMPLETE status={summary['final_theorem_status']} "
        f"verified={summary['verified_closed_tasks']}/{summary['total_tasks']} "
        f"wall={summary['verify_wall_seconds']:.3f}s"
    )
    return 0 if summary["final_theorem_status"] == "UNCONDITIONALLY_VERIFIED" else 1


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (VerificationError, OSError, ValueError) as exc:
        print(f"AUDIT_ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
