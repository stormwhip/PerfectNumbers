"""Replay this sprint only, then project against the pinned pre-sprint obligations.
Run with -I -S -B; does not replay the inherited proofs. No third-party imports.
"""
from hashlib import sha256
from pathlib import Path
import argparse, json, sys


HERE = Path(__file__).resolve().parent
OLD = HERE.parent / 'Session20261126'
sys.path[:0] = [str(HERE), str(OLD)]
import TreeCheck


def pinned():
    raw = (OLD / 'Delta.json').read_bytes().replace(b'\r\n', b'\n')
    if sha256(raw).hexdigest() != 'ff47c354d6e5c47f6daff26bdd37b3b2922ff1cfcc0ce6af91487432f9a0c4e2':
        raise ValueError('wrong pre-sprint proof ledger')
    return json.loads(raw)


def project():
    old = pinned()
    rows = old['remaining_shards']
    live = {(s['root'], e) for s in rows for e in s['remaining_actuals']}
    assert len(live) == 110 and len(rows) == 98 and old['closed'] == 2974
    proofs = []
    hits = set()
    for path in sorted(HERE.glob('Tree*.json.gz')):
        p, e, stats = TreeCheck.verify(path)
        assert (p, e) in live - hits and path.name == f'Tree{p}x{e}.json.gz'
        hits.add((p, e))  # exact only: no lifting to a multiple of e+1
        proofs.append(dict(actual=[p, e], packet=path.name, sha256=sha256(path.read_bytes()).hexdigest(),
                           forest_leaves=stats[0], split_nodes=stats[1], direct_cases=stats[2]))
    from JointTree import verify as joint_verify
    for path in sorted(HERE.glob('JointTree*.json.gz')):
        p, e, stats, prices = joint_verify(path)
        assert (p, e) in live - hits and path.name == f'JointTree{p}x{e}.json.gz'
        hits.add((p, e))
        proofs.append(dict(actual=[p,e], packet=path.name, sha256=sha256(path.read_bytes()).hexdigest(),
                           forest_leaves=stats[0], split_nodes=stats[1], direct_cases=stats[2],
                           price_leaves=stats[3], prices=json.loads(json.dumps(prices))))
    remaining = []; closed = []
    for s in rows:
        left = [e for e in s['remaining_actuals'] if (s['root'], e) not in hits]
        if left:
            remaining.append(dict(s, remaining_actuals=left))
        else:
            closed.append(s['id'])
    keys = {(s['root'], e) for s in remaining for e in s['remaining_actuals']}
    assert keys == live - hits
    return dict(baseline='2b53c830dd903b460a315df04fa3a4a410fb8357', total=3072,
                closed=old['closed'] + len(closed), open=len(remaining), open_actuals=len(keys),
                singleton_shards=sum(len(s['remaining_actuals']) == 1 for s in remaining),
                new_actuals=sorted(map(list, hits)), new_shards=closed, proofs=proofs,
                remaining_shards=remaining)


if __name__ == '__main__':
    if not __debug__: raise SystemExit('assertions required')
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true')
    args = parser.parse_args()
    result = project(); path = HERE / 'Delta.json'
    if args.write:
        path.write_text(json.dumps(result, indent=1) + '\n', encoding='utf-8', newline='\n')
    elif json.loads(path.read_bytes()) != result:
        raise SystemExit('proof/ledger mismatch')
    print('PASS | closed, open, remaining actuals:', result['closed'], result['open'], result['open_actuals'])
