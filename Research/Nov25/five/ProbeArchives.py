"""Discovery only. Read nominated private forests; test exact isolated bound routines."""
from pathlib import Path
import argparse
import hashlib
import json
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH/'NightFive'))
from WeightedReplay import proof, verify, I, B
from WeightedSecond import second


def lookup(src):
    d = json.loads((RESEARCH/'RootFiveNext/RootFiveCertificate.json').read_text())['ecpp']
    for r in sorted(src/'Witnesses' for _ in [0]):
        if not r.is_dir(): raise ValueError('missing historical witness directory')
    return d


def pack(src, e):
    d = lookup(src)
    h = src/f'ForestCyc25_{e}.json'
    n = json.loads(h.read_bytes())
    owners = dict(n['owners'])
    vertices = set(n['P']) | set(owners)
    cert = {}
    usable = set()
    for p in vertices:
        if p < 2**64:
            usable.add(p)
            continue
        k = hashlib.sha256(str(p).encode()).hexdigest()[:24]
        v = d.get(k)
        if v is None:
            paths = [src/'Witnesses'/f'{k}.json', src.parents[2]/'NightCache'/'ecpp-local'/f'{k}.json']
            f = next((path for path in paths if path.is_file()), None)
            if f is None:
                continue
            v = json.loads(f.read_bytes())
        usable.add(p)
        cert[str(p)] = v
    roots = set(n['P']) & usable
    kept = set(roots)
    todo = list(roots)
    while todo:
        r = todo.pop()
        for p, q in owners.items():
            if q == r and p in usable and p not in kept:
                todo.append(p)
                kept.add(p)
    return dict(p=5, e=e, roots=sorted(roots), owners=[(p,q) for p,q in owners.items() if p in kept], head=n['head']), {str(p): cert[str(p)] for p in kept if p >= 2**64}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('exponents', type=int, nargs='+')
    ap.add_argument('--archive', type=Path, default=RESEARCH.parents[1]/'overnight/Research/NightFive')
    a = ap.parse_args()
    for e in a.exponents:
        row, cert = pack(a.archive, e)
        raw = proof(row, cert)
        T = 50011
        scores = []
        for mu in (1500, 2500, 3500, 4500, 5500, 6500, 8000, 10000):
            d = dict(row, T=T, mu=mu)
            scores.append((verify(d)//I.LN10_HI, mu))
        hi, mu = max(scores)
        b = second(dict(row, T=T, mu=mu))//I.LN10_HI
        print(e, 'raw', [(str(q),len(str(v))-1) for q,v in raw.items()], 'weighted', hi, mu, b, flush=True)


if __name__ == '__main__':
    main()
