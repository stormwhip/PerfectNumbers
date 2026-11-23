"""Audit the original partition together with replayable root-class certificates."""

import argparse
from collections import Counter, defaultdict
import gzip
import json
from pathlib import Path

from DirectRootClosures2400 import independently_check_direct_roots
from IndependentVerifierV2 import strict_json_loads
from PrimeValuationClosure2400 import contradicts
from RootClassCertificate2400 import ORDER, TARGET, accepted_shards
from TerminalCertificate import verify as verify_terminal
from VerifyRootExponentCoverage import canonical_tasks


def read_certificate(path):
    return strict_json_loads(gzip.decompress(path.read_bytes()).decode("ascii"))


def audit(terminal_path, bank_path):
    terminal = read_certificate(terminal_path)
    if tuple(terminal["roots"]) != tuple(sorted(ORDER)) or not verify_terminal(terminal):
        raise ValueError("original coprime class rejected")
    tasks = list(canonical_tasks(ORDER))
    direct = independently_check_direct_roots(ORDER)
    if direct["total_tasks"] != len(tasks):
        raise ValueError("root task count mismatch")
    closed = {t["id"]: "BASELINE_INTEGER" for t in direct["witnesses"]}
    conditional = defaultdict(set)

    for cert in read_certificate(bank_path):
        branch = cert.get("branch")
        if branch is None:
            ids = accepted_shards(cert, terminal)
            source = "CYCLOTOMIC_RESIDUAL_DUAL" if cert["residual"] else "ROOT_CLASS_DUAL"
            for task_id in ids:
                closed.setdefault(task_id, source)
        else:
            ids = accepted_shards(cert, terminal, branch_only=True)
            conditional[cert["root"], branch[0], branch[1]].update(ids)
    for root, prime in {(root, prime) for root, prime, _ in conditional}:
        for task_id in conditional[root, prime, False] & conditional[root, prime, True]:
            closed.setdefault(task_id, "COMPLEMENTARY_PRIME_SPLIT_DUAL")

    for t in tasks:
        task_id, root = t["id"], t["root"]
        if task_id in closed:
            continue
        forbidden = tuple(sorted(ORDER[:ORDER.index(root)]))
        reason = contradicts(root, t["exponent"], t["exact"], forbidden,
                             10**TARGET, node_budget=120)
        if reason is not None:
            closed[task_id] = reason

    opened = [t for t in tasks if t["id"] not in closed]
    open_by_root = Counter(t["root"] for t in opened)
    by_root = {p: {"verified": sum(t["root"] == p and t["id"] in closed for t in tasks),
                   "open": open_by_root[p]} for p in ORDER}
    return dict(
        theorem_status="INCOMPLETE_FRONTIER" if opened else "UNCONDITIONALLY_VERIFIED",
        total_tasks=len(tasks), closed_tasks=len(closed), open_tasks=len(opened),
        by_root=by_root, by_source=dict(Counter(closed.values())),
        partial_branch_coverage=[
            dict(root=root, prime=prime, present=present,
                 still_open_top_level=len(ids - closed.keys()),
                 open_task_ids=sorted(ids - closed.keys()))
            for (root, prime, present), ids in sorted(conditional.items())
            if ids - closed.keys()
        ],
        open_manifest=opened,
    )


def main():
    certificate_dir = Path(__file__).resolve().parents[1] / "Certificates"
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--terminal", type=Path, default=certificate_dir / "TerminalOriginal.json.gz")
    parser.add_argument("--bank", type=Path, default=certificate_dir / "RootClassDuals2400.json.gz")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    result = audit(args.terminal, args.bank)
    if args.output:
        args.output.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    del result["open_manifest"]
    for branch in result["partial_branch_coverage"]:
        del branch["open_task_ids"]
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
