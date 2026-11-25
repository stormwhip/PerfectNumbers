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
             '19x274-QFine19_274.json.gz', '19x86-HDir19_86.json.gz', '13x76-QFine13_76.json.gz',
             '19x102-CacheD19_102.json.gz', '13x418-CacheD13_418.json.gz',
             '31x396-CacheD31_396.json.gz', '13x42-CacheD13_42.json.gz',
             '13x38-NoExtra13_38.json.gz', '13x54-QFine13_54.json.gz', '13x68-NoExtra13_68.json.gz',
             '13x84-QFine13_84.json.gz', '19x68-QFine19_68.json.gz', '19x84-QFine19_84.json.gz',
             '19x98-QFine19_98.json.gz',
             '13x34-CacheD13_34.json.gz', '13x44-QFine13_44.json.gz', '13x48-CacheD13_48.json.gz',
             '13x50-NoExtra13_50.json.gz', '13x56-NoExtra13_56.json.gz', '13x74-NoExtra13_74.json.gz',
             '19x50-CacheD19_50.json.gz', '19x64-CacheD19_64.json.gz', '19x74-CacheD19_74.json.gz',
             '19x104-QFine19_104.json.gz', '19x120-QFine19_120.json.gz', '19x124-QFine19_124.json.gz',
             '31x26-CacheD31_26.json.gz', '31x32-Long231_32.json.gz',
             'seven/best-11x220-1.pack.json.gz', 'seven/best-7x234-1.pack.json.gz',
             'seven/best-11x132-1.pack.json.gz', 'seven/best-7x252-1.pack.json.gz',
             'seven/best-11x66-1.pack.json.gz', 'seven/best-11x214-1.pack.json.gz',
             'seven/best-7x412-1.pack.json.gz', 'seven/best-7x162-1.pack.json.gz',
             'seven/best-7x108-1.pack.json.gz', 'seven/best-11x46-1.pack.json.gz',
             'candidate-13x100-refine1.pack.json.gz', 'candidate-31x486-refine1.pack.json.gz',
             'candidate-19x148-refine1.pack.json.gz', 'candidate-19x598-refine1.pack.json.gz',
             'candidate-31x438-ecm-refine.pack.json.gz', 'candidate-19x360-refine1.pack.json.gz',
             'seven/best-11x646-1.pack.json.gz')
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
