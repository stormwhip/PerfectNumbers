import sqlite3
import tempfile
from pathlib import Path

from FrontierLedger import FrontierLedger, LeaseLost


def reject(kind, action):
    try:
        action()
    except kind:
        return
    raise AssertionError(f"expected {kind.__name__}")


with tempfile.TemporaryDirectory() as directory:
    path = Path(directory, "queue.sqlite")
    a = FrontierLedger(path, "sha256:run-A")
    b = FrontierLedger(path, "sha256:run-A")
    root, = a.seed([b"root state"])
    _, expired, _ = a.claim(0, 5)
    current_id, current, body = b.claim(5, 10)
    assert current_id == root and body == b"root state" and expired != current
    reject(LeaseLost, lambda: a.finish(root, expired, 6, "0" * 64))
    reject(LeaseLost, lambda: a.split(root, expired, 6, [b"stale"]))
    reject(LeaseLost, lambda: a.renew(root, expired, 6, 20))
    b.renew(root, current, 6, 20)
    reject(ValueError, lambda: b.split(root, current, 6, iter(())))
    # NOT NULL failure after the first insertion must roll back the whole split.
    reject(sqlite3.IntegrityError, lambda: b.split(root, current, 6, [b"left", None]))
    assert a.claim(6, 1) is None
    left, right = b.split(root, current, 6, [b"left", b"right"])
    assert len({root, left, right}) == 3
    b.close()
    b = FrontierLedger(path, "sha256:run-A")
    assert b.claim(7, 10)[::2] == (left, b"left")
    task, attempt, state = a.claim(7, 10)
    assert (task, state) == (right, b"right")
    a.finish(task, attempt, 8, "1" * 64)
    reject(LeaseLost, lambda: a.finish(task, attempt, 8, "1" * 64))
    reject(ValueError, lambda: FrontierLedger(path, "sha256:run-B"))
    b.close()
    a.close()
print("FrontierLedgerTests: atomic split rollback, crash recovery, and stale lease rejection pass")
