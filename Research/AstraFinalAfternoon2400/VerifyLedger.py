"""Verify frozen incidence and project registered full proofs; not a proof replay."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha1
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parent
BASE = '495c59f55456a70994ce7848487e0c4e262c1984'
ROOTS = (19, 7, 11, 31, 13, 3, 5, 17)
TOTAL_BY_ROOT = dict(zip(ROOTS, (287, 412, 341, 253, 325, 676, 481, 297)))
PIN = {
    'FinalNight2400/OpenFrontier.json': '6dd4c8d3ca351811807c5ec078f7e4bcb1538575',
    'FinalNight2400/Results.json': '198b7c0c0e3d58fc97f314de722b7a8f5d5f2f5d',
    'GeminiFrontier/November28/Results.json': 'df8b6061f938010d54945c81e729a73cc4b7f08d',
    'GeminiFrontier/ShardToKeys.json': 'de821605b9bb0c124ff8ca4a576f85ced96afaa2',
    'GeminiFrontier/KeyToShards.json': 'efad9522397f1b9a79aaf27c4ab90e65d58d1683',
}


def load(path):
    return json.loads(path.read_bytes())


def pinned(name):
    b = (RESEARCH / name).read_bytes().replace(b'\r\n', b'\n')
    assert sha1(b'blob %d\0' % len(b) + b).hexdigest() == PIN[name], name
    return json.loads(b)


def incidence(by_shard):
    inv = defaultdict(list)
    for shard, keys in by_shard.items():
        root = int(shard.split('_')[0][1:])
        assert len(keys) == len(set(map(tuple, keys))) > 0
        for p, e in keys:
            assert p == root and p in ROOTS and (e > 0 and (e % 2 == 0 or p % 4 == e % 4 == 1))
            inv[f'{p},{e}'].append(shard)
    return dict(inv)


def frozen_frontier():
    frozen = pinned('FinalNight2400/OpenFrontier.json')
    historical_shards = pinned('GeminiFrontier/ShardToKeys.json')
    hist_inverse = incidence(historical_shards)
    assert hist_inverse == pinned('GeminiFrontier/KeyToShards.json')
    history = pinned('FinalNight2400/Results.json')
    counts = Counter(r['Status'] for r in history)
    assert counts == {'VERIFIED_FULL': 25, 'VERIFIED_CONDITIONAL': 77}
    full = {tuple(r['Key']) for r in history if r['Status'] == 'VERIFIED_FULL'}
    assert len(full) == 25 and all(f'{p},{e}' in hist_inverse for p, e in full)
    projected = {s: [k for k in keys if tuple(k) not in full] for s, keys in historical_shards.items()}
    assert {s: ks for s, ks in projected.items() if ks} == frozen['ShardRemainders']
    assert len(historical_shards) - len(frozen['ShardRemainders']) == 25
    shards = frozen['ShardRemainders']
    inv = incidence(shards)
    assert (len(shards), len(inv), sum(len(v) == 1 for v in shards.values())) == (43, 53, 35)
    assert sum(map(len, inv.values())) == 57
    supplement = pinned('GeminiFrontier/November28/Results.json')
    assert supplement['AcceptedLocalExclusions'] == 143 and supplement['NewCompleteKeys'] == supplement['NewClosedShards'] == 0
    return shards, inv


def project(shards, inv, results):
    full, conditional = set(), set()
    verified_ids = set()
    assert results['BaselineCommit'] == BASE and isinstance(results['Entries'], list)
    for r in results['Entries']:
        p, e = r['Key']
        assert f'{p},{e}' in inv
        assert r['Status'] in ('VERIFIED_FULL', 'VERIFIED_CONDITIONAL', 'OPEN')
        assert r['Id'] and r['Id'] not in verified_ids
        verified_ids.add(r['Id'])
        if r['Status'] == 'OPEN':
            continue
        for attr in ('Proof', 'Certificate', 'Verifier', 'IndependentReview'):
            f = (HERE / r[attr]).resolve()
            assert f.is_relative_to(HERE) and f.is_file(), (r['Id'], attr)
        if r['Status'] == 'VERIFIED_FULL':
            assert (p, e) not in full
            full.add((p, e))
        else:
            assert isinstance(r['Conditions'], dict) and r['Conditions']
            condition = (p, e, json.dumps(r['Conditions'], sort_keys=True))
            assert condition not in conditional
            conditional.add(condition)
    now = {s: [k for k in ks if tuple(k) not in full] for s, ks in shards.items()}
    emptied = sorted(s for s, ks in now.items() if not ks)
    now = {s: ks for s, ks in now.items() if ks}
    remaining = incidence(now)
    roots = defaultdict(list)
    for k in remaining:
        p, e = map(int, k.split(','))
        roots[p].append(e)
    open_by_root = Counter(int(s.split('_')[0][1:]) for s in now)
    assert sum(TOTAL_BY_ROOT.values()) == 3072
    return dict(BaselineCommit=BASE, GlobalStatus='INCOMPLETE_FRONTIER' if now else 'FRONTIER_EMPTY_AUDIT_REQUIRED',
                TotalShards=3072, ClosedShards=3072-len(now), OpenShards=len(now), DistinctKeys=len(remaining),
                SingletonShards=sum(len(ks) == 1 for ks in now.values()),
                NewFullKeys=sorted(full), NewClosedShards=emptied, RegisteredConditionalEntries=len(conditional),
                ByRoot={p: dict(Closed=TOTAL_BY_ROOT[p]-open_by_root[p], Open=open_by_root[p], Keys=sorted(roots[p])) for p in ROOTS},
                ShardRemainders=now, KeyToShards=dict(sorted(remaining.items())))


if __name__ == '__main__':
    assert __debug__, 'do not run with -O'
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='regenerate the derived projection')
    args = parser.parse_args()
    data = project(*frozen_frontier(), load(HERE / 'Results.json'))
    dest = HERE / 'OpenFrontier.json'
    encoded = json.dumps(data, indent=2) + '\n'
    if args.write:
        dest.write_text(encoded, encoding='utf-8', newline='\n')
    else:
        assert dest.read_text(encoding='utf-8') == encoded
    print('PASS frozen forward/reverse incidence and exact-key projection:',
          {k: data[k] for k in ('ClosedShards', 'OpenShards', 'DistinctKeys', 'SingletonShards', 'NewFullKeys', 'NewClosedShards', 'RegisteredConditionalEntries')})
