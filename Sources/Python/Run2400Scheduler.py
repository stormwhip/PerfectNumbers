#!/usr/bin/env python3
"""Restartable 2400 exponent-root partition runner for V21.

This orchestrates eight root-prime case partitions, which assume earlier
root primes are absent. Each listed exponent option is a distinct task.
Completion is a program status, NOT an audited proof of an unconditional theorem.
"""
import argparse
import concurrent.futures
import datetime
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

ROOTS = (19, 7, 11, 31, 13, 3, 5, 17)
INPUTS = (
    "ProofTreeV21", "facts.idx", "facts.dat", "PrimeCutoffProduct.bin",
    "PrefixDualBounds.csv", "PrefixDualVariableGains.csv",
    "PrefixDualForcedGains.csv",
)
SHARD_RE = re.compile(r"^SHARD root=(\d+) index=(\d+) exponent=(\d+) exact=([01])$", re.M)
COUNT_RE = re.compile(r"^SHARD_COUNT root=(\d+) count=(\d+)$", re.M)


def digest(path):
    h = hashlib.sha256()
    with open(path, "rb") as stream:
        while True:
            block = stream.read(8 * 1024 * 1024)
            if not block:
                break
            h.update(block)
    return h.hexdigest()


def atomic_json(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(path.name + ".tmp")
    with temporary.open("w", encoding="utf-8") as out:
        json.dump(value, out, indent=2, ensure_ascii=False)
        out.write("\n")
    os.replace(temporary, path)


def load_manifest(base, out):
    p = out / "Manifest.json"
    if not p.exists():
        raise RuntimeError(f"Missing {p}; execute 'prepare' first")
    manifest = json.loads(p.read_text(encoding="utf-8"))
    for name, expected in manifest["sha256"].items():
        current = digest(base / name)
        if current != expected:
            raise RuntimeError(f"Changed input {name}: manifest hash mismatch")
    return manifest


def prepare(base, out, root_order):
    inputs = {f: digest(base / f) for f in INPUTS}
    manifest_path = out / "Manifest.json"
    if manifest_path.exists():
        current = load_manifest(base, out)
        if tuple(current["root_order"]) != tuple(root_order):
            raise RuntimeError("Existing manifest uses a different root order")
        print(f"ALREADY_PREPARED tasks={len(current['tasks'])} manifest={manifest_path}")
        return
    tasks = []
    env = dict(os.environ)
    env["OMP_NUM_THREADS"] = "1"
    env["OPN_ROOT_ORDER"] = ",".join(map(str, root_order))
    for root in root_order:
        result = subprocess.run(
            ["./ProofTreeV21", "2400", str(root), "list"],
            cwd=base, env=env, text=True, capture_output=True, timeout=120,
            check=True,
        )
        counts = COUNT_RE.findall(result.stdout)
        entries = SHARD_RE.findall(result.stdout)
        if len(counts) != 1 or int(counts[0][0]) != root or len(entries) != int(counts[0][1]):
            raise RuntimeError(f"Bad root manifest: {root}, {result.stdout[-1500:]}")
        for expected_index, (found_root, found_index, exponent, exact) in enumerate(entries):
            if int(found_root) != root or int(found_index) != expected_index:
                raise RuntimeError(f"Non-contiguous or incorrect shard entry for {root}")
            tasks.append({
                "root": root, "index": expected_index,
                "count": len(entries), "exponent": int(exponent),
                "exact": bool(int(exact)),
                "id": f"P{root}_I{expected_index:05d}",
            })
        print(f"MANIFEST_ROOT p={root} options={len(entries)}", flush=True)
    atomic_json(manifest_path, {
        "target_exponent": 2400,
        "root_order": list(root_order),
        "created_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "sha256": inputs,
        "tasks": tasks,
        "proof_status": "UNVERIFIED_PROGRAM_OUTPUT",
    })
    print(f"MANIFEST_COMPLETE tasks={len(tasks)} path={manifest_path}", flush=True)


def task_file(out, task):
    return out / "States" / (task["id"] + ".json")


def accepted(out, task):
    p = task_file(out, task)
    if not p.exists():
        return False
    try:
        data = json.loads(p.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return False
    return data.get("status") == "PROVEN" and data.get("task") == task


def run_task(base, out, task, deadline, threads, root_order):
    if accepted(out, task):
        return "PROVEN"
    remaining = deadline - time.monotonic()
    if remaining <= 1:
        return "UNSTARTED"
    log = out / "Logs" / (task["id"] + ".log")
    log.parent.mkdir(parents=True, exist_ok=True)
    env = dict(os.environ)
    env["OMP_NUM_THREADS"] = str(threads)
    env["OPN_ROOT_ORDER"] = ",".join(map(str, root_order))
    command = ["./ProofTreeV21", "2400", str(task["root"]), str(task["index"])]
    start = time.monotonic()
    return_code = None
    timed_out = False
    with log.open("wb") as output:
        try:
            completed = subprocess.run(
                command, cwd=base, stdout=output, stderr=subprocess.STDOUT,
                timeout=max(1, deadline - time.monotonic()), env=env,
                check=False,
            )
            return_code = completed.returncode
        except subprocess.TimeoutExpired:
            timed_out = True
    elapsed = time.monotonic() - start
    content = log.read_text(encoding="utf-8", errors="replace")
    expected = (
        f"Forbid p={task['root']} branch={task['index']}/{task['count']} "
        "-> PROVEN"
    )
    status = "PROVEN" if return_code == 0 and expected in content and re.search(
        r"failed_rb=0", content[content.find(expected):content.find(expected)+300]
    ) else ("TIMEOUT" if timed_out else "UNRESOLVED")
    record = {
        "task": task, "status": status, "exit_code": return_code,
        "elapsed_seconds": elapsed, "log_sha256": digest(log),
        "finished_utc": datetime.datetime.now(datetime.timezone.utc).isoformat(),
    }
    atomic_json(task_file(out, task), record)
    print(f"SHARD_RESULT id={task['id']} status={status} "
          f"elapsed={elapsed:.3f}s", flush=True)
    return status


def status(out, manifest):
    tasks = manifest["tasks"]
    done = sum(accepted(out, task) for task in tasks)
    unresolved = []
    for task in tasks:
        p = task_file(out, task)
        if p.exists() and not accepted(out, task):
            unresolved.append(task["id"])
    print(f"TREE_PROGRESS proven={done} total={len(tasks)} "
          f"pending={len(tasks)-done} unresolved={len(unresolved)}")
    if done == len(tasks):
        print("TREE_SEARCH_COMPLETE_UNAUDITED: LP, primality and arithmetic audits remain")
    return done == len(tasks)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("prepare", "run", "status", "verify"))
    parser.add_argument("--base", type=Path, default=Path("Build"))
    parser.add_argument("--out", type=Path, default=Path("Build/TaskResults"))
    parser.add_argument("--jobs", type=int, default=4)
    parser.add_argument("--threads-per-job", type=int, default=2)
    parser.add_argument("--max-hours", type=float, default=72.0)
    parser.add_argument("--root-order", type=str, default=None,
                        help="Comma-separated eight-prime permutation; frozen into manifest")
    args = parser.parse_args()
    base = args.base.resolve()
    out = args.out.resolve()
    desired_order = tuple(int(q) for q in args.root_order.split(",")) if args.root_order else None
    if desired_order is not None and sorted(desired_order) != sorted(ROOTS):
        parser.error("--root-order must permute exactly the eight canonical root primes")
    if args.mode == "prepare":
        prepare(base, out, desired_order or ROOTS)
        return 0
    manifest = load_manifest(base, out)
    if desired_order is not None and tuple(manifest["root_order"]) != desired_order:
        raise RuntimeError("Requested root order differs from saved manifest")
    root_order = tuple(manifest["root_order"])
    if sorted(root_order) != sorted(ROOTS):
        raise RuntimeError("Saved root order is not an eight-prime permutation")
    if args.mode in ("status", "verify"):
        done = status(out, manifest)
        return 0 if args.mode == "status" or done else 1
    if not (1 <= args.jobs <= 64 and 1 <= args.threads_per_job <= 64
            and 0 < args.max_hours <= 72):
        parser.error("jobs and threads must be 1..64; max-hours must be in (0,72]")
    deadline = time.monotonic() + args.max_hours * 3600.0
    pending = [task for task in manifest["tasks"] if not accepted(out, task)]
    print(f"START jobs={args.jobs} threads_per_job={args.threads_per_job} "
          f"remaining_tasks={len(pending)} max_hours={args.max_hours}", flush=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [
            pool.submit(run_task, base, out, task, deadline,
                        args.threads_per_job, root_order)
            for task in pending
        ]
        for f in concurrent.futures.as_completed(futures):
            f.result()
    return 0 if status(out, manifest) else 2


if __name__ == "__main__":
    try:
        sys.exit(main())
    except (OSError, RuntimeError, subprocess.CalledProcessError) as exc:
        print(f"SCHEDULER_ERROR: {exc}", file=sys.stderr)
        sys.exit(2)
