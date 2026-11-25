"""Rebuild the Nov25 delta from verified exact-exponent proof adapters."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
BASE = HERE.parent / 'NightMerge/Audit.json'
BASE_COMMIT = 'e89dffd5a74debad80f695d6177f3d785e6268e8'
BASE_SHA256_LF = '3efc593b3950340cee799f0be02ee19be4c1c1caf1b8f501eefb3021dcb5d902'
BASE_BLOB = '80148583dcdf88d1c77b6493267e05425e9c36b0'


def load_baseline():
    data = BASE.read_bytes().replace(b'\r\n', b'\n')
    blob = hashlib.sha1(b'blob ' + str(len(data)).encode('ascii') + b'\0' + data)
    if blob.hexdigest() != BASE_BLOB or hashlib.sha256(data).hexdigest() != BASE_SHA256_LF:
        raise ValueError('wrong NightMerge audit blob')
    audit = json.loads(data)
    shards = audit['remaining_shards']
    if (audit['closed'], audit['open'], len(shards)) != (2646, 426, 426):
        raise ValueError('incorrect baseline shard totals')
    if len({s['id'] for s in shards}) != len(shards) or any(
        not s['remaining_actuals'] or len(set(s['remaining_actuals'])) != len(s['remaining_actuals'])
        for s in shards
    ):
        raise ValueError('invalid baseline obligations')
    if len(obligations(shards)) != 562:
        raise ValueError('incorrect baseline exact-exponent total')
    return audit


def obligations(shards):
    return {(s['root'], e) for s in shards for e in s['remaining_actuals']}


def aggregate(audit, verified_batches):
    original = audit['remaining_shards']
    pending = obligations(original)
    proofs = set()
    for label, verified in verified_batches:
        keys = set(verified)
        if not keys or not keys <= pending:
            raise ValueError(f'{label}: empty or out-of-scope proof batch')
        proofs.update(keys)
    closed, left = [], []
    for s in original:
        todo = [e for e in s['remaining_actuals'] if (s['root'], e) not in proofs]
        if todo:
            left.append(dict(s, remaining_actuals=todo))
        else:
            closed.append(s)
    if obligations(left) != pending - proofs:
        raise ValueError('lost remaining obligations')
    counts = lambda roots: dict(sorted(Counter(roots).items()))
    return dict(baseline_commit=BASE_COMMIT, baseline_audit_blob=BASE_BLOB,
                status='INCOMPLETE_FRONTIER' if left else 'REQUIRES_GLOBAL_REPLAY',
                baseline_closed=audit['closed'], baseline_open=audit['open'],
                baseline_actuals=len(pending), new_actuals=sorted(proofs),
                new_actuals_by_root=counts(p for p, _ in proofs),
                new_shards=len(closed), new_shards_by_root=counts(s['root'] for s in closed),
                closed=audit['closed'] + len(closed), open=len(left),
                remaining_actuals=len(obligations(left)),
                remaining_actuals_by_root=counts(p for p, _ in obligations(left)),
                remaining_shards_by_root=counts(s['root'] for s in left),
                closed_shards=closed, remaining_shards=left)


def verified_batches(workers=1):
    # Only explicit, fail-closed adapters go here; no discovery results.
    import sys
    from concurrent.futures import ProcessPoolExecutor
    sys.path.insert(0, str(HERE))
    from ProofJobs import verify_job
    names = ('five148', 'five520',
             'P19x274QFine19x274.json.gz', 'P19x86HDir19x86.json.gz', 'P13x76QFine13x76.json.gz',
             'P19x102CacheD19x102.json.gz', 'P13x418CacheD13x418.json.gz',
             'P31x396CacheD31x396.json.gz', 'P13x42CacheD13x42.json.gz',
             'P13x38NoExtra13x38.json.gz', 'P13x54QFine13x54.json.gz', 'P13x68NoExtra13x68.json.gz',
             'P13x84QFine13x84.json.gz', 'P19x68QFine19x68.json.gz', 'P19x84QFine19x84.json.gz',
             'P19x98QFine19x98.json.gz',
             'P13x34CacheD13x34.json.gz', 'P13x44QFine13x44.json.gz', 'P13x48CacheD13x48.json.gz',
             'P13x50NoExtra13x50.json.gz', 'P13x56NoExtra13x56.json.gz', 'P13x74NoExtra13x74.json.gz',
             'P19x50CacheD19x50.json.gz', 'P19x64CacheD19x64.json.gz', 'P19x74CacheD19x74.json.gz',
             'P19x104QFine19x104.json.gz', 'P19x120QFine19x120.json.gz', 'P19x124QFine19x124.json.gz',
             'P31x26CacheD31x26.json.gz', 'P31x32Long231x32.json.gz',
             'Seven/Best11x2201.pack.json.gz', 'Seven/Best7x2341.pack.json.gz',
             'Seven/Best11x1321.pack.json.gz', 'Seven/Best7x2521.pack.json.gz',
             'Seven/Best11x661.pack.json.gz', 'Seven/Best11x2141.pack.json.gz',
             'Seven/Best7x4121.pack.json.gz', 'Seven/Best7x1621.pack.json.gz',
             'Seven/Best7x1081.pack.json.gz', 'Seven/Best11x461.pack.json.gz',
             'Candidate13x100Refine1.pack.json.gz', 'Candidate31x486Refine1.pack.json.gz',
             'Candidate19x148Refine1.pack.json.gz', 'Candidate19x598Refine1.pack.json.gz',
             'Candidate31x438EcmRefine.pack.json.gz', 'Candidate19x360Refine1.pack.json.gz',
             'Seven/Best11x6461.pack.json.gz', 'Candidate13x58Refine1.pack.json.gz',
             'Candidate13x690EcmRefine.pack.json.gz', 'Best19x646Finalecm.pack.json.gz',
             'Candidate19x576Finalecm2.pack.json.gz')
    if workers == 1:
        return tuple(map(verify_job, names))
    with ProcessPoolExecutor(workers) as executor:
        return tuple(executor.map(verify_job, names))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument('--write', type=Path)
    group.add_argument('--check', type=Path)
    parser.add_argument('--workers', type=int, default=1)
    args = parser.parse_args()
    if not 1<=args.workers<=12:parser.error('--workers must be in 1..12')
    result = aggregate(load_baseline(), verified_batches(args.workers))
    text = json.dumps(result, indent=1) + '\n'
    if args.write:
        args.write.write_text(text, encoding='utf-8', newline='\n')
    if args.check and json.loads(args.check.read_bytes()) != json.loads(text):
        raise ValueError('stored ledger differs from fresh replay')
    print(f"{len(result['new_actuals'])} verified exact exponents; {result['new_shards']} new closed shards; "
          f"{result['open']} remaining shards, {result['remaining_actuals']} remaining exact exponents")


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('replay requires assertions; do not use -O')
    main()
