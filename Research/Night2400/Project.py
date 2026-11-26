"""Project distinct independently verified exact keys onto the frozen open frontier."""
import argparse
from collections import Counter, defaultdict
from hashlib import sha256
import json
from pathlib import Path

BASELINE_SHA = '49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec'
LEDGER_SHA256 = 'ba1775dc1848c11b06395247d9d09a3c121f126514d552ea9dd3582bc1cd40dc'


def encode(mapping):
    return json.dumps(mapping, indent=2, ensure_ascii=True) + '\n'


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('baseline', type=Path)
    parser.add_argument('--out', type=Path, required=True)
    parser.add_argument('--verified', type=Path, help='JSON array of [root, exponent] pairs, after independent acceptance')
    args = parser.parse_args()
    if not __debug__:
        raise RuntimeError('assertions required')
    raw = args.baseline.read_bytes().replace(b'\r\n', b'\n')
    if sha256(raw).hexdigest() != LEDGER_SHA256:
        raise ValueError('input is not the frozen FinalSprint ledger')
    base = json.loads(raw)
    before, after = {}, {}
    keys = defaultdict(list)
    for row in base['remaining_shards']:
        p, shard = row['root'], row['id']
        exps = row['remaining_actuals']
        assert shard not in before and exps and len(set(exps)) == len(exps), row
        before[shard] = [(p, e) for e in exps]
        for key in before[shard]:
            keys[key].append(shard)
    assert (len(before), len(keys), sum(len(v)==1 for v in before.values())) == (base['open'], base['open_actuals'], base['singleton_shards'])
    assert base['total'] - base['closed'] == len(before)
    verified = set(map(tuple, json.loads(args.verified.read_text(encoding='utf-8')))) if args.verified else set()
    if verified - keys.keys():
        raise ValueError(f'keys absent from frozen ledger: {sorted(verified - keys.keys())}')
    new_closed, roots = [], Counter({p: 0 for p in (19, 7, 11, 31, 13, 3, 5, 17)})
    for shard, old in before.items():
        residual = [key for key in old if key not in verified]
        if residual:
            after[shard] = residual
            roots[old[0][0]] += 1
        else:
            new_closed.append(shard)
    args.out.mkdir(parents=True, exist_ok=True)
    args.out.joinpath('KeyToShards.json').write_text(encode({f'{p},{e}': [s for s in rows if s in after] for (p,e),rows in sorted(keys.items()) if (p,e) not in verified}), encoding='utf-8')
    args.out.joinpath('ShardToKeys.json').write_text(encode(after), encoding='utf-8')
    assert {key for values in after.values() for key in values} == keys.keys() - verified
    by_root_keys = Counter({p: 0 for p in roots})
    by_root_keys.update(p for p,e in keys.keys() - verified)
    summary = dict(baseline_sha=BASELINE_SHA, baseline_ledger_sha256=LEDGER_SHA256,
                   total=base['total'], closed=base['closed']+len(new_closed), open=len(after),
                   distinct_keys=len(keys)-len(verified), singleton_shards=sum(len(v)==1 for v in after.values()),
                   new_closed=new_closed, new_keys=sorted(verified), open_by_root=dict(roots),
                   distinct_keys_by_root=dict(by_root_keys))
    args.out.joinpath('Delta.json').write_text(encode(summary), encoding='utf-8')
    print(encode(summary), end='')


if __name__ == '__main__':
    main()
