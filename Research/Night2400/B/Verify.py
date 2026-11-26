"""Cold replay of exact secondary-cell exclusions. No factor bank or discovery dependencies."""
import gzip
import json
import sys
from collections import Counter
from functools import cache
from hashlib import sha256
from math import prod
from pathlib import Path

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path.insert(0, str(RESEARCH / 'Session20261126'))
import PivotCheck as PC

C = PC.C
B = PC.B
Q = 797161
PIVOTS = {1: 398581, 2: 22996651, 66: 5897}


def viable(state):
    return (not state.conflict and state.base <= B
            and prod(C.sigma(q, h) for q, h in state.rows.items()) <= 2 * state.X)


def domain(prefix, q):
    state = C.State(prefix)
    assert viable(state) and q not in state.rows and q not in state.bad and state.D % q == 0
    c = C.valuation(state.D, q)
    base = state.base // q**c
    cases = {}
    h = c
    while base * q**h <= B:
        if state.possible(q, h, c):
            child = prefix + [(q, h)]
            if viable(C.State(child)):
                cases[str(h)] = child
        h += 1
    assert base * q**h > B and (h == c or base * q**(h-1) <= B)
    return cases, h


def verify(path):
    assert __debug__
    raw = path.read_bytes()
    data = json.loads(gzip.decompress(raw))
    assert set(data) == {'f', 'tree', 'ecpp'}
    cert = data['ecpp']
    used = set()
    stats = Counter()
    lowest = None

    @cache
    def prime(q):
        assert type(q) is int and q > 2
        u = q
        if q >= 2**64:
            chain = cert[str(q)]
            for row in chain:
                assert row[0] == u
                u = C.pc.level(*row)
            used.add(str(q))
        assert C.pc.prime64(u)
        return True

    def walk(prefix, row):
        nonlocal lowest
        if row['type'] == 'split':
            assert set(row) == {'type', 'q', 'cases'} and prime(row['q'])
            children, _ = domain(prefix, row['q'])
            assert set(children) == set(row['cases']), ('incomplete inner split', prefix)
            stats['splits'] += 1
            for h, child in children.items():
                walk(child, row['cases'][h])
            return
        assert row['type'] == 'forest' and set(row) == {'type', 'roots', 'owners', 'head'}
        state = C.State(prefix)
        k, o, h = row['roots'], row['owners'], row['head']
        C.validate_forest(state, k, o, h, prime)
        lower = min(C.Forest(state, k, o, h).lower()[0], PC.exact_leaf(prefix, k, o, h))
        assert lower > B, ('underpriced', prefix, PC.floor10(lower))
        floor = PC.floor10(lower)
        lowest = floor if lowest is None else min(lowest, floor)
        stats['forests'] += 1

    assert set(C.ORDER[:C.ORDER.index(3)]) == {19, 7, 11, 31, 13}
    assert prime(3) and prime(Q) and C.sigma(3, 12) == Q
    f = data['f']
    assert type(f) is int and f in PIVOTS
    piv, _ = domain([(3, 12)], Q)
    prefix = piv[str(f)]
    row = data['tree']
    assert set(row) == {'type', 'q', 'cases'} and row['type'] == 'split' and row['q'] == PIVOTS[f]
    assert prime(row['q'])
    children, tail = domain(prefix, row['q'])
    assert row['cases'] and set(row['cases']) <= set(children)
    for h, sub in row['cases'].items():
        walk(children[h], sub)
    assert used == set(cert)
    remains = sorted(map(int, set(children) - set(row['cases'])))
    result = dict(root=[3, 12], primary=[Q, f], secondary=row['q'],
                  covered=len(row['cases']), domain=len(children), tail=tail, unresolved=remains,
                  full_fiber=not remains, stats=dict(stats), minimum_floor=lowest,
                  ecpp=len(used), sha256=sha256(raw).hexdigest())
    print('PASS', json.dumps(result), flush=True)
    return result


if __name__ == '__main__':
    if not __debug__ or len(sys.argv) < 2:
        raise SystemExit('run with assertions enabled: Verify.py PACKET [...]')
    paths = list(map(Path, sys.argv[1:]))
    for path in paths:
        verify(path)
