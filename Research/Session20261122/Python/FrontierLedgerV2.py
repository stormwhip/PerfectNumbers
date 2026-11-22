"""Transactional frontier ledger (V2) with durable split-evidence & disk proof store."""

from __future__ import annotations

from contextlib import contextmanager
import hashlib
import os
from pathlib import Path
import sqlite3
import tempfile
from typing import Callable, Dict, Iterable, List, Optional, Sequence, Tuple
import uuid

from IndependentVerifierV2 import (
    VerificationError,
    canonical_json_bytes,
    sha256_hex,
    strict_json_loads,
)


class LeaseLost(RuntimeError):
    pass


def _is_valid_sha256(digest: object) -> bool:
    return (
        isinstance(digest, str)
        and len(digest) == 64
        and all(c in "0123456789abcdef" for c in digest)
    )


def _fsync_dir(directory: Path) -> None:
    if os.name != "posix":
        return
    fd = os.open(str(directory), os.O_RDONLY)
    try:
        os.fsync(fd)
    finally:
        os.close(fd)


class DiskProofStore:
    """Crash-consistent content-addressed JSON proof store on local filesystem."""

    def __init__(self, root_dir: Path):
        self.root = Path(root_dir).resolve()
        self.root.mkdir(parents=True, exist_ok=True)

    def _path_for(self, digest: str) -> Path:
        if not _is_valid_sha256(digest):
            raise ValueError(f"invalid sha256 digest: {digest!r}")
        return self.root / digest[:2] / f"{digest}.json"

    def put_json(self, obj: dict) -> str:
        raw = canonical_json_bytes(obj)
        digest = sha256_hex(raw)
        dest = self._path_for(digest)
        dest.parent.mkdir(parents=True, exist_ok=True)
        if dest.exists():
            if sha256_hex(dest.read_bytes()) == digest:
                return digest
            raise VerificationError(f"corrupted existing proof file at {dest}")

        fd, tmp_name = tempfile.mkstemp(prefix=".tmp_", dir=str(dest.parent))
        tmp_path = Path(tmp_name)
        try:
            with os.fdopen(fd, "wb") as stream:
                stream.write(raw)
                stream.flush()
                os.fsync(stream.fileno())
            os.replace(tmp_path, dest)
            _fsync_dir(dest.parent)
        except BaseException:
            if tmp_path.exists():
                tmp_path.unlink(missing_ok=True)
            raise
        return digest

    def get_verified_json(self, expected_digest: str) -> dict:
        dest = self._path_for(expected_digest)
        if not dest.is_file():
            raise VerificationError(f"missing proof file on disk for digest {expected_digest}")
        raw = dest.read_bytes()
        actual = sha256_hex(raw)
        if actual != expected_digest:
            raise VerificationError(
                f"disk proof digest mismatch: expected {expected_digest}, got {actual}"
            )
        parsed = strict_json_loads(raw.decode("utf-8"))
        if not isinstance(parsed, dict):
            raise VerificationError("proof payload must be a JSON object")
        return parsed


class FrontierLedgerV2:
    """SQLite WAL ledger binding parent split evidence, ordered edge catalog, and child tasks."""

    def __init__(self, path: Path, run_fingerprint: str):
        self.db = sqlite3.connect(path, isolation_level=None)
        self.db.row_factory = sqlite3.Row
        self.db.execute("PRAGMA journal_mode=WAL")
        self.db.execute("PRAGMA synchronous=FULL")
        self.db.execute("PRAGMA foreign_keys=ON")
        self.db.executescript("""
            CREATE TABLE IF NOT EXISTS run (
                singleton INTEGER PRIMARY KEY CHECK (singleton=1),
                fingerprint TEXT NOT NULL
            );
            CREATE TABLE IF NOT EXISTS task (
                id TEXT PRIMARY KEY,
                parent TEXT REFERENCES task(id),
                ordinal INTEGER NOT NULL,
                state BLOB NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('PENDING','CLAIMED','SPLIT','RESULT')),
                attempt TEXT,
                lease_until INTEGER,
                proof_sha256 TEXT,
                total_edges INTEGER
            );
            CREATE TABLE IF NOT EXISTS split_edge (
                parent_id TEXT NOT NULL REFERENCES task(id),
                edge_ordinal INTEGER NOT NULL,
                edge_kind TEXT NOT NULL CHECK(edge_kind IN ('OPEN','CLOSED')),
                child_task_id TEXT REFERENCES task(id),
                edge_proof_sha256 TEXT,
                PRIMARY KEY (parent_id, edge_ordinal),
                CHECK (
                    (edge_kind='OPEN' AND child_task_id IS NOT NULL AND edge_proof_sha256 IS NULL)
                    OR (edge_kind='CLOSED' AND child_task_id IS NULL AND edge_proof_sha256 IS NOT NULL)
                )
            );
            CREATE UNIQUE INDEX IF NOT EXISTS task_child ON task(parent, ordinal);
            CREATE UNIQUE INDEX IF NOT EXISTS task_root ON task(ordinal) WHERE parent IS NULL;
        """)
        try:
            with self.transaction():
                self.db.execute("INSERT OR IGNORE INTO run VALUES (1, ?)", (run_fingerprint,))
                row = self.db.execute("SELECT fingerprint FROM run").fetchone()
                if row[0] != run_fingerprint:
                    raise ValueError("frontier run fingerprint mismatch")
        except BaseException:
            self.db.close()
            raise
        self.fingerprint = run_fingerprint

    @contextmanager
    def transaction(self):
        self.db.execute("BEGIN IMMEDIATE")
        try:
            yield
            self.db.commit()
        except BaseException:
            self.db.rollback()
            raise

    def close(self) -> None:
        self.db.close()

    def task_id(self, parent: Optional[str], ordinal: int) -> str:
        raw = self.fingerprint.encode("utf-8")
        identity = ((parent or "ROOT") + ":" + str(ordinal)).encode("ascii")
        return hashlib.sha256(len(raw).to_bytes(8, "big") + raw + identity).hexdigest()

    def _insert_task(self, parent: Optional[str], ordinal: int, state: bytes) -> str:
        identifier = self.task_id(parent, ordinal)
        self.db.execute(
            "INSERT INTO task(id,parent,ordinal,state,status) VALUES (?,?,?,?,'PENDING')",
            (identifier, parent, ordinal, state),
        )
        return identifier

    def seed(self, states: Sequence[bytes]) -> List[str]:
        states = tuple(states)
        if not states:
            raise ValueError("expected at least one root task")
        with self.transaction():
            if self.db.execute("SELECT 1 FROM task LIMIT 1").fetchone():
                raise ValueError("frontier is already seeded")
            return [self._insert_task(None, idx, st) for idx, st in enumerate(states)]

    def claim(self, now: int, ttl: int) -> Optional[Tuple[str, str, bytes]]:
        if ttl <= 0:
            raise ValueError("lease duration must be positive")
        with self.transaction():
            row = self.db.execute("""
                SELECT id,state FROM task
                WHERE status='PENDING' OR (status='CLAIMED' AND lease_until<=?)
                ORDER BY CASE WHEN status='PENDING' THEN 0 ELSE 1 END, rowid LIMIT 1
            """, (now,)).fetchone()
            if row is None:
                return None
            attempt = uuid.uuid4().hex
            self.db.execute(
                "UPDATE task SET status='CLAIMED', attempt=?, lease_until=? WHERE id=?",
                (attempt, now + ttl, row["id"]),
            )
            return row["id"], attempt, row["state"]

    def renew(self, task_id: str, attempt: str, now: int, ttl: int) -> None:
        if ttl <= 0:
            raise ValueError("lease duration must be positive")
        with self.transaction():
            res = self.db.execute("""
                UPDATE task SET lease_until=MAX(lease_until, ?)
                WHERE id=? AND status='CLAIMED' AND attempt=? AND lease_until>?
            """, (now + ttl, task_id, attempt, now))
            if res.rowcount != 1:
                raise LeaseLost(task_id)

    def _update_claim(
        self,
        task_id: str,
        attempt: str,
        now: int,
        status: str,
        proof_sha256: str,
        total_edges: Optional[int] = None,
    ) -> None:
        res = self.db.execute("""
            UPDATE task
            SET status=?, attempt=NULL, lease_until=NULL, proof_sha256=?, total_edges=?
            WHERE id=? AND status='CLAIMED' AND attempt=? AND lease_until>?
        """, (status, proof_sha256, total_edges, task_id, attempt, now))
        if res.rowcount != 1:
            raise LeaseLost(task_id)

    def split_with_evidence(
        self,
        task_id: str,
        attempt: str,
        now: int,
        split_proof_sha256: str,
        edge_records: Sequence[Tuple[str, object]],
        fault_hook: Optional[Callable[[int], None]] = None,
    ) -> List[str]:
        """Atomically record parent split proof, full ordered edge catalog, and all OPEN children.

        edge_records: ordered sequence of:
          - ("OPEN", child_state_bytes)
          - ("CLOSED", closed_subtree_proof_sha256)
        Forbids empty splits or all-CLOSED splits (use finish() when entire parent is closed).
        """
        if not _is_valid_sha256(split_proof_sha256):
            raise ValueError("split_proof_sha256 must be lowercase 64-hex SHA-256")
        records = tuple(edge_records)
        if not records:
            raise ValueError("empty split is forbidden; submit a leaf witness via finish()")
        if not any(kind == "OPEN" for kind, _ in records):
            raise ValueError("all edges are CLOSED; submit complete subtree via finish()")

        open_child_ids: List[str] = []
        with self.transaction():
            self._update_claim(task_id, attempt, now, "SPLIT", split_proof_sha256, len(records))
            for edge_ord, (kind, payload) in enumerate(records):
                if fault_hook is not None:
                    fault_hook(edge_ord)
                if kind == "OPEN":
                    cid = self._insert_task(task_id, edge_ord, payload)  # type: ignore[arg-type]
                    self.db.execute(
                        "INSERT INTO split_edge(parent_id,edge_ordinal,edge_kind,child_task_id) "
                        "VALUES (?,?,'OPEN',?)",
                        (task_id, edge_ord, cid),
                    )
                    open_child_ids.append(cid)
                elif kind == "CLOSED":
                    if not _is_valid_sha256(payload):
                        raise ValueError(f"invalid closed edge proof digest at ordinal {edge_ord}")
                    self.db.execute(
                        "INSERT INTO split_edge(parent_id,edge_ordinal,edge_kind,edge_proof_sha256) "
                        "VALUES (?,?,'CLOSED',?)",
                        (task_id, edge_ord, payload),
                    )
                else:
                    raise ValueError(f"unknown edge kind: {kind!r}")
        return open_child_ids

    def finish(self, task_id: str, attempt: str, now: int, proof_sha256: str) -> None:
        if not _is_valid_sha256(proof_sha256):
            raise ValueError("expected a lowercase SHA-256 digest")
        with self.transaction():
            self._update_claim(task_id, attempt, now, "RESULT", proof_sha256, None)
