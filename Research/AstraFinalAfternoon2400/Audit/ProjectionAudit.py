"""Independent projection audit; never attest mathematical coverage from a ledger label."""
import argparse
from collections import Counter
import json
from math import isqrt
from pathlib import Path
import re
import subprocess

BASE = '495c59f55456a70994ce7848487e0c4e262c1984'
B = 10**2400
ROOTS = (19, 7, 11, 31, 13, 3, 5, 17)
HERE = Path(__file__).resolve().parent.parent


def frozen(name):
    return json.loads(subprocess.check_output(['git', 'show', f'{BASE}:Research/{name}'], cwd=HERE))


def reconstruct():
    # Generate all representative positions and tag each legal actual exponent independently.
    composite = set()
    for q in range(2, isqrt(5031) + 1):
        if q not in composite:
            composite.update(range(q*q, 5032, q))
    representatives = {}
    all_by_root = {}
    for p in ROOTS:
        powers = [1]
        while powers[-1]*p <= B:
            powers.append(powers[-1]*p)
        cap = len(powers)-1
        reps = [(1, True)] if p % 4 == 1 else []
        low = {3: [(2, True), (4, True), (8, False), (14, False), (24, False)],
               7: [(2, True), (8, False)]}.get(p, [])
        reps.extend(low)
        reps.extend((ell-1, False) for ell in range({3: 7, 7: 5}.get(p, 3), cap+2, 2)
                    if ell not in composite)
        legal = {e for e in range(1, cap+1) if e % 2 == 0 or p % 4 == e % 4 == 1}
        covered = set()
        for i, (a, exact) in enumerate(reps):
            members = {a} & legal if exact else {e for e in legal if divmod(e+1, a+1)[1] == 0}
            representatives[f'P{p}_I{i:05d}'] = {(p, e) for e in members}
            covered |= members
        assert covered == legal
        all_by_root[p] = len(reps)
    assert len(representatives) == 3072
    return representatives, all_by_root


def sets(shards):
    result = {name: {tuple(k) for k in keys} for name, keys in shards.items()}
    assert all(len(result[name]) == len(keys) > 0 for name, keys in shards.items())
    return result


def invert(shards):
    return {(p, e): {s for s in shards if (p, e) in shards[s]}
            for p, e in set().union(*shards.values())}


def subtract(shards, complete):
    return {s: survivors for s, old in shards.items() if (survivors := old.difference(complete))}


def parse_key(raw):
    p, e = map(int, raw.split(','))
    return p, e


def test_projection(before):
    # Pick an actual one-to-many key; removing it must touch *all* incidences, not
    # necessarily closing a shard. An empty full set must leave everything intact.
    reverse = invert(before)
    k = next(k for k in sorted(reverse) if len(reverse[k]) > 1)
    simulated = subtract(before, {k})
    assert {s for s in before if simulated.get(s, set()) != before[s]} == reverse[k]
    assert set(before) - set(simulated) == {s for s in reverse[k] if before[s] == {k}}
    assert k not in invert(simulated) and subtract(before, set()) == before
    return k, tuple(sorted(reverse[k]))


def main():
    assert __debug__, 'must not run under -O'
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--accepted-full', action='append', default=[], type=parse_key,
                    help='supply each exact key already accepted on exhaustive mathematical evidence')
    args = ap.parse_args()
    allowed = set(args.accepted_full)
    assert len(allowed) == len(args.accepted_full)
    reps, total_by_root = reconstruct()
    legacy = sets(frozen('GeminiFrontier/ShardToKeys.json'))
    old_reverse = {parse_key(k): set(v) for k, v in frozen('GeminiFrontier/KeyToShards.json').items()}
    assert invert(legacy) == old_reverse
    prior = frozen('FinalNight2400/Results.json')
    prior_full = [tuple(r['Key']) for r in prior if r['Status'] == 'VERIFIED_FULL']
    assert len(prior_full) == len(set(prior_full)) == 25 and set(prior_full) <= old_reverse.keys()
    before = sets(frozen('FinalNight2400/OpenFrontier.json')['ShardRemainders'])
    assert before == subtract(legacy, set(prior_full))
    for data in (legacy, before):
        assert all(keys <= reps[s] for s, keys in data.items())
    assert (len(before), len(invert(before)), sum(map(len, before.values()))) == (43, 53, 57)
    assert sum(len(ks) == 1 for ks in before.values()) == 35
    control_key, control_shards = test_projection(before)
    ledger = json.loads((HERE / 'Results.json').read_bytes())
    assert ledger['BaselineCommit'] == BASE
    known=invert(before)
    for row in ledger['Entries']:
        assert tuple(row['Key']) in known
    full = [tuple(row['Key']) for row in ledger['Entries'] if row['Status'] == 'VERIFIED_FULL']
    assert len(full) == len(set(full)) and set(full) == allowed, ('unapproved full-key label or missing full-key record', full, allowed)
    after = subtract(before, allowed)
    actual = json.loads((HERE / 'OpenFrontier.json').read_bytes())
    assert actual['BaselineCommit'] == BASE
    got = sets(actual['ShardRemainders'])
    reverse = invert(after)
    assert got == after
    assert {parse_key(k): set(v) for k, v in actual['KeyToShards'].items()} == reverse
    assert {tuple(k) for k in actual['NewFullKeys']} == allowed
    assert len(actual['NewFullKeys']) == len(allowed)
    assert set(actual['NewClosedShards']) == before.keys()-after.keys()
    assert len(actual['NewClosedShards']) == len(before)-len(after)
    assert actual['TotalShards'] == len(reps)
    assert (actual['ClosedShards'], actual['OpenShards'], actual['DistinctKeys'], actual['SingletonShards']) == (
        len(reps)-len(after), len(after), len(reverse), sum(len(ks) == 1 for ks in after.values()))
    assert actual['GlobalStatus'] == ('INCOMPLETE_FRONTIER' if after else 'FRONTIER_EMPTY_AUDIT_REQUIRED')
    open_by_root = Counter(int(re.match(r'P(\d+)_I\d+$', s)[1]) for s in after)
    for p in ROOTS:
        row = actual['ByRoot'][str(p)]
        assert (row['Closed'], row['Open'], row['Keys']) == (total_by_root[p]-open_by_root[p], open_by_root[p],
                                                          sorted(e for q, e in reverse if q == p))
    print(f'PASS complete representatives {len(reps)}, independent set difference {len(allowed)} accepted full keys, '
          f'{actual["ClosedShards"]} closed / {len(after)} open / {len(reverse)} keys / {actual["SingletonShards"]} singleton')
    print('Negative control for single-incidence subtraction:', control_key, 'appears in', control_shards)


if __name__ == '__main__':
    main()
