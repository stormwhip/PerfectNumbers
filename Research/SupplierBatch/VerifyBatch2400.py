"""Replay the batch addition against the original 3,072-shard partition."""

import argparse
from collections import Counter
import json
from pathlib import Path
import sys

BATCH_DIR = Path(__file__).resolve().parent
RESEARCH_DIR = BATCH_DIR.parent
BASELINE_DIR = RESEARCH_DIR / "Session20261122"
sys.path.insert(0, str(BASELINE_DIR / "Python"))
sys.path.insert(0, str(RESEARCH_DIR / "FermatRootValuation"))

from AuditRootClass2400 import audit, read_certificate
from CyclotomicValuationDual2400 import TRIAL, replay
from PrimeValuationClosure2400 import contradicts
from RoadblockDual import log_bounds
from RootClassCertificate2400 import ORDER, TARGET
from TerminalCertificate import DYADIC

from SupplierProduct2400 import verify_exponent
from Verify import covers, forbids, tables

CERT_DIR = BASELINE_DIR / "Certificates"
CLOSED_BASELINE = 1805


def exterior_certificates(certificates, terminal):
    divisor = DYADIC * log_bounds(2)[1]
    special_gain = log_bounds(1000001,1000000)[1]
    data = []
    max_named = max(TRIAL, *(edge[2] for edge in terminal["edges"]))
    for cert in certificates:
        if cert["mode"] != "ordinary" or cert["branch"] != 0:
            raise ValueError("wrong exterior LP domain")
        bounds, (tail, named) = replay(cert, terminal, special_gain, return_prices=True)
        price = tail, tuple((r,*exponents) for r,exponents in named.items())
        data.append((cert["root"], cert.get("unit",1), bounds, price))
    return data, divisor, max_named


def supplier_witness(p, e, scan, outer_index, joint_index, exterior):
    data, divisor, max_named = exterior
    if type(scan) is not int or not 1 <= scan <= 100000:
        raise ValueError("invalid shared-divisor scan cutoff")

    def bound(index, weighted):
        if index is None:
            return 0, 1, (0, ())
        if type(index) is not int or not 0 <= index < len(data):
            raise ValueError("invalid referenced dual")
        root, unit, bounds, prices = data[index]
        if root != p or weighted != (unit > 1) or e+1 not in bounds:
            raise ValueError("exterior dual does not cover this actual exponent")
        return max(0,bounds[e+1]//divisor), unit, prices

    plain, _, prices = bound(outer_index,False)
    weighted, unit, _ = bound(joint_index,True)
    return verify_exponent(p,e,scan,plain,unit,weighted,max_named,prices)


def run(bank_path):
    if not __debug__:
        raise RuntimeError("run without -O")
    terminal_path = CERT_DIR / "TerminalOriginal.json.gz"
    baseline = audit(terminal_path, CERT_DIR / "RootClassDuals2400.json.gz")
    if baseline["total_tasks"] != 3072 or baseline["closed_tasks"] != CLOSED_BASELINE:
        raise ValueError("unexpected original audit baseline")
    bundle = read_certificate(bank_path)
    terminal = read_certificate(terminal_path)
    exterior = exterior_certificates(bundle["duals"],terminal)
    tasks = baseline["open_manifest"]
    open_tasks = {t["id"]:t for t in tasks}
    _, actual = tables()
    live = {(p,e) for p,e,label,_ in actual if label=="OPEN"}
    new_exact = {}
    for row in bundle["supplier"]:
        p,e,scan,outer,joint,expected = row
        key = p,e
        if key not in live or key in new_exact:
            raise ValueError(f"invalid or duplicate actual exponent {key}")
        reason = supplier_witness(p,e,scan,outer,joint,exterior)
        if not reason or reason != expected:
            raise ValueError(f"supplier proof failed for {key}")
        new_exact[key] = reason

    residual = live - new_exact.keys()
    additions = {}
    for t in tasks:
        p,d,exact = t["root"],t["exponent"],t["exact"]
        if p in (3,5) and not any(q==p and covers(e,d,exact) for q,e in residual):
            if not any(q==p and covers(e,d,exact) for q,e in new_exact):
                raise ValueError(f"missing supplier evidence for {t['id']}")
            additions[t["id"]] = "ALL_ACTUAL_EXPONENTS"

    factor_replay = {}
    for task_id, primes, expected in bundle["factors"]:
        if task_id not in open_tasks or task_id in factor_replay:
            raise ValueError(f"invalid or duplicate factor task {task_id}")
        t = open_tasks[task_id]
        p = t["root"]
        reason = contradicts(p,t["exponent"],t["exact"],tuple(sorted(forbids(p))),
                             10**TARGET,node_budget=140,known_primes=tuple(primes))
        if reason != expected or not reason:
            raise ValueError(f"factor tree failed for {task_id}")
        factor_replay[task_id] = reason
        additions.setdefault(task_id,reason)

    remaining = [t for t in tasks if t["id"] not in additions]
    by_root = {p:dict(verified=baseline["by_root"][p]["verified"],
                     open=baseline["by_root"][p]["open"],added=0) for p in ORDER}
    for task_id in additions:
        p = open_tasks[task_id]["root"]
        by_root[p]["open"] -= 1
        by_root[p]["verified"] += 1
        by_root[p]["added"] += 1
    return dict(theorem_status="INCOMPLETE_FRONTIER" if remaining else "UNCONDITIONALLY_VERIFIED",
                total=baseline["total_tasks"],previous_closed=CLOSED_BASELINE,
                closed=CLOSED_BASELINE+len(additions),open=len(remaining),
                by_root=by_root,by_rule=dict(Counter(additions.values())),
                additions=[{**t,"proof":additions[t["id"]]} for t in tasks
                           if t["id"] in additions],
                exact_exponents=[dict(root=p,exponent=e,reason=reason)
                                 for (p,e),reason in sorted(new_exact.items())],
                open_manifest=remaining)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--bank",type=Path,default=BATCH_DIR/"BatchSupplierProofs2400.json.gz")
    parser.add_argument("--output",type=Path)
    args=parser.parse_args()
    result=run(args.bank)
    if args.output:
        args.output.write_text(json.dumps(result,indent=2)+"\n")
    print(json.dumps({k:v for k,v in result.items()
                      if k not in ("additions","exact_exponents","open_manifest")},indent=2))


if __name__ == "__main__":
    main()
