"""Small deterministic experiment, not a certificate adapter for the delta ledger."""
import argparse
from collections import Counter
import gzip
from itertools import product
import json
from math import gcd, isqrt
from pathlib import Path
import sys

H = Path(__file__).resolve().parent
R = H.parent
sys.path.insert(0, str(H))
from Ledger import load_baseline, obligations
from SizePilot import Tree, coprime_parts, I, B

DEFAULT = ((7,330), (7,1018), (11,646), (11,718), (13,330), (13,738),
           (19,646), (19,676), (31,486), (3,1162), (5,520))


def rows(p):
    return json.loads(p.read_bytes()) if p.suffix != '.gz' else json.loads(gzip.decompress(p.read_bytes()))


def trial_bank():
    """Only release data, including prime subjects from their tracked ECPP files.

    Experiment accepts MR64 primes and archived certificate subjects as *hints*;
    any positive candidate needs a separate actual primality replay.
    """
    pool = set(I.SMALL)
    for prefix in ('NightOrder', 'EveningTree', 'NightMerge'):
        folder = R / prefix
        for f in folder.glob('Batch*.json'):
            packet = rows(f)
            if isinstance(packet, list):
                for row in packet:
                    if isinstance(row, dict):
                        pool.update(row.get('fs', []))
        for f in (folder / 'ECPP').glob('*.json*'):
            chain = rows(f)
            pool.add(chain[0][0])
    for f in ('OrderSupplyNext/Accepted.json', 'EveningTree/Verified.json'):
        for row in rows(R/f):
            pool.update(row.get('rs', []))
            pool.update(row.get('fs', []))
    return tuple(sorted(q for q in pool if type(q) is int and q > 2))


def selftest():
    for a,b,c in product(range(1,30), repeat=3):
        v = coprime_parts((a,b,c))
        if any(gcd(x,y)!=1 for i,x in enumerate(v) for y in v[:i]) or a*b*c != I.prod(v):
            raise AssertionError((a,b,c,v))
    coprime_parts.cache_clear()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--case', nargs=2, type=int, action='append')
    ap.add_argument('--nodes', type=int, default=150)
    ap.add_argument('--depth', type=int, default=6)
    ap.add_argument('--cap', type=int, default=20001)
    args = ap.parse_args()
    if not __debug__ or not 5000 <= args.cap <= 1000000:
        raise SystemExit('Require assertions and cap in [5000, 1000000]')
    selftest()
    eligible = obligations(load_baseline()['remaining_shards'])
    pool = trial_bank()
    cases = DEFAULT if args.case is None else tuple(map(tuple, args.case))
    if not set(cases) <= eligible:
        raise ValueError('out-of-snapshot target')
    for p,e in cases:
        A=I.sigma(p,e)
        fs=[q for q in pool if q not in I.SMALL and A%q==0]
        for tag,cap in [('control',None),('parity',args.cap)]:
            T=Tree(p,e,fs,args.depth,args.nodes,cap,p not in (3,5))
            ok=T.prove()
            print(json.dumps(dict(p=p,e=e,mode=tag,closed_candidate=ok,root_factors=len(fs),
                                  stats=T.stats,first=T.first)),flush=True)


if __name__ == '__main__':
    main()
