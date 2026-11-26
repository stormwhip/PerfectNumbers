"""Exact support and valuation partition at the inherited 110-bit pivot."""
from functools import cache
from math import gcd, prod
from pathlib import Path
import gzip, json, sys

REPO = Path(__file__).resolve().parents[3]
R = REPO / 'Research'
sys.path[:0] = [str(R / 'Session20261126'), str(R / 'FinalSprint')]
from PivotCheck import C, B, floor10

ORDER = (19, 7, 11, 31, 13, 3, 5, 17)
P, E, Q = 19, 316, 1255900817071954721881883552067931
A = C.sigma(P, E)


def inputs():
    old = json.loads(gzip.decompress((R / 'FinalSprint/Support/Pivot316.json.gz').read_bytes()))
    source = json.loads((R / 'Session20261126/OpenSupport.json').read_bytes())
    assert source['order'] == list(ORDER)
    all_masks = source['rows']['19:316']
    assert all_masks == sorted(set(all_masks)) and len(all_masks) == 57
    assert len(old['masks']) == 36 and set(old['masks']) <= set(all_masks)
    return old, all_masks, sorted(set(all_masks) - set(old['masks']))


def groups(m):
    assert type(m) is int and 0 < m < 256 and m & 1
    return tuple(z for i, z in enumerate(ORDER[1:], 1) if m >> i & 1), tuple(z for i, z in enumerate(ORDER[1:], 1) if not m >> i & 1)


@cache
def feasible(f):
    rows = [(P, E), (Q, f)]
    x = P**E * Q**f
    z = A * C.sigma(Q, f)
    t = z // (1 + f % 2)
    d = t // gcd(t, x)
    return rows, x, z, t, d


def branches(m):
    """Return exact first-valuation obligations (ignoring forced presence), and first omitted valuation."""
    _, absent = groups(m)
    ban = prod(absent)
    c = C.valuation(A, Q)
    f = c
    todo = []
    while P**E * (A // Q**c) * Q**f <= B:
        if f % 2 == 0 or Q % 4 == f % 4 == 1:
            _, x, z, t, d = feasible(f)
            if gcd(t * Q, ban) == gcd(d, x) == 1 and x * d <= B and z <= 2 * x:
                todo.append(f)
        f += 1
    return todo, f


def prime_chain(z, table):
    assert type(z) is int and z > 2
    n = z
    if n >= 2**64:
        rows = table[str(z)]
        assert rows
        for row in rows:
            assert row[0] == n
            n = C.pc.level(*row)
    assert C.pc.prime64(n)
    return True


if __name__ == '__main__':
    assert __debug__
    old, _, missing = inputs()
    assert prime_chain(Q, old['ecpp']) and A % Q == 0
    known = {row['f'] for row in old['rows']}
    for m in missing:
        fs, tail = branches(m)
        print(m, groups(m), fs, 'uncovered', sorted(set(fs)-known), 'tail', tail)
    print('prefixes', [(f, floor10(x*d)) for f in range(2, 25, 2) for _, x, _, _, d in [feasible(f)]])
