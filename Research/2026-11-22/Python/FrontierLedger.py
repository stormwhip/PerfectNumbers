"""Transactional frontier storage. Coverage and leaf proofs are checked separately."""

from contextlib import contextmanager
import hashlib
import sqlite3
import uuid


class LeaseLost(RuntimeError):
    pass


class FrontierLedger:
    def __init__(self, path, run_fingerprint):
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
                id TEXT PRIMARY KEY, parent TEXT REFERENCES task(id),
                ordinal INTEGER NOT NULL, state BLOB NOT NULL,
                status TEXT NOT NULL CHECK(status IN ('PENDING','CLAIMED','SPLIT','RESULT')),
                attempt TEXT, lease_until INTEGER,
                proof_sha256 TEXT
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

    def close(self):
        self.db.close()

    def task_id(self, parent, ordinal):
        raw = self.fingerprint.encode("utf-8")
        identity = ((parent or "ROOT") + ":" + str(ordinal)).encode("ascii")
        return hashlib.sha256(len(raw).to_bytes(8, "big") + raw + identity).hexdigest()

    def insert_task(self, parent, ordinal, state):
        identifier = self.task_id(parent, ordinal)
        self.db.execute(
            "INSERT INTO task(id,parent,ordinal,state,status) VALUES (?,?,?,?,'PENDING')",
            (identifier, parent, ordinal, state),
        )
        return identifier

    def seed(self, states):
        states = tuple(states)
        if not states:
            raise ValueError("expected at least one root task")
        with self.transaction():
            if self.db.execute("SELECT 1 FROM task LIMIT 1").fetchone():
                raise ValueError("frontier is already seeded")
            return [self.insert_task(None, index, state) for index, state in enumerate(states)]

    def claim(self, now, ttl):
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
            self.db.execute("""
                UPDATE task SET status='CLAIMED',attempt=?,lease_until=? WHERE id=?
            """, (attempt, now + ttl, row["id"]))
            return row["id"], attempt, row["state"]

    def renew(self, task_id, attempt, now, ttl):
        if ttl <= 0:
            raise ValueError("lease duration must be positive")
        with self.transaction():
            result = self.db.execute("""
                UPDATE task SET lease_until=MAX(lease_until,?)
                WHERE id=? AND status='CLAIMED' AND attempt=? AND lease_until>?
            """, (now + ttl, task_id, attempt, now))
            if result.rowcount != 1:
                raise LeaseLost(task_id)

    def update_claim(self, task_id, attempt, now, status, proof=None):
        result = self.db.execute("""
            UPDATE task SET status=?, attempt=NULL, lease_until=NULL, proof_sha256=?
            WHERE id=? AND status='CLAIMED' AND attempt=? AND lease_until>?
        """, (status, proof, task_id, attempt, now))
        if result.rowcount != 1:
            raise LeaseLost(task_id)

    def split(self, task_id, attempt, now, child_states):
        """Commit a complete, ordered frontier transfer or roll the entire update back."""
        child_states = tuple(child_states)
        if not child_states:
            raise ValueError("empty split needs a leaf witness")
        with self.transaction():
            self.update_claim(task_id, attempt, now, "SPLIT")
            return [self.insert_task(task_id, index, state)
                    for index, state in enumerate(child_states)]

    def finish(self, task_id, attempt, now, proof_sha256):
        """Record a candidate proof digest, without treating it as verified."""
        if len(proof_sha256) != 64 or any(c not in "0123456789abcdef" for c in proof_sha256):
            raise ValueError("expected a lowercase SHA-256 digest")
        with self.transaction():
            self.update_claim(task_id, attempt, now, "RESULT", proof_sha256)
