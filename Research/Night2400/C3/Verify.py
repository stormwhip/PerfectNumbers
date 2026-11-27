"""Replay the two exact conditional fibers of (7,430), not a shard cover."""
import gzip
import json
from math import prod
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
R = HERE.parents[1]
sys.path[:0] = [str(R / 'FinalSprint'), str(R / 'Session20261126')]
from JointValuation import excludes
from PivotCheck import B, C, exact_leaf, floor10

ROOT = (7, 430)
Q = 3602407438103418087310110702859943140744217508967


def verify():
    assert __debug__
    d = json.loads(gzip.decompress((HERE / 'Fibers7x430.json.gz').read_bytes()))
    assert set(d) == {'p', 'e', 'pivot', 'cases', 'ecpp'}
    assert (d['p'], d['e']) == ROOT and d['pivot'] == Q
    used = set()

    def prime(q):
        assert type(q) is int and q > 2
        x = q
        if q >= 2**64:
            used.add(str(q))
            for row in d['ecpp'][str(q)]:
                assert row[0] == x and x >= 2**64
                x = C.pc.level(*row)
        assert C.pc.prime64(x)
        return True

    assert prime(ROOT[0]) and prime(Q) and Q.bit_length() == 162 and Q % 4 == 3
    s = C.State([ROOT])
    assert not s.conflict and C.valuation(s.D, Q) == 1
    scale, f = s.base // Q, 1
    domain, direct, incompatible = [], [], []
    while scale * Q**f <= B:
        if not s.possible(Q, f, 1):
            incompatible.append(f)
        else:
            t = C.State([ROOT, (Q, f)])
            dead = t.conflict or t.base > B or prod(C.sigma(p, e) for p, e in t.rows.items()) > 2*t.X
            (direct if dead else domain).append(f)
        f += 1
    assert (domain, direct, incompatible, f) == (list(range(2, 17, 2)), list(range(18, 35, 2)), list(range(1, 36, 2)), 36)
    print('DOMAIN P7_I00082', domain, 'DIRECT', direct, 'TAIL >=', f, flush=True)
    assert set(d['cases']) == {'14', '16'}
    P = [ROOT, (Q, 14)]
    t = C.State(P)
    forest = d['cases']['14']
    roots, owners, head = forest['roots'], forest['owners'], forest['head']
    assert set(forest) == {'type', 'roots', 'owners', 'head'} and forest['type'] == 'forest'
    assert head == 2 and not owners
    C.validate_forest(t, roots, owners, head, prime)
    a, b = C.Forest(t, roots, owners, head).lower()[0], exact_leaf(P, roots, owners, head)
    assert a > B and b > B
    print('PASS 14: dual forest floors', floor10(a), floor10(b), flush=True)
    P = [ROOT, (Q, 16)]
    assert d['cases']['16'] == {'type': 'price', 'targets': [0, 1]}
    receipt = excludes(P, C.State(P).bad, [0, 1])
    assert receipt == (19, [6378, 518, 0])
    assert used == set(d['ecpp'])
    print('PASS 16:', receipt, 'OPEN: 2, 4, 6, 8, 10, 12', flush=True)


if __name__ == '__main__':
    verify()
