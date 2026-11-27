"""Offline exact conditional replay for the fixed (7,36), P7_I00011 task.

An explicit open leaf is a scope restriction, not an exclusion. The verifier
returns all such paths, and checks all siblings and size tails of every split.
"""
from functools import cache
from hashlib import sha256
from math import prod
from pathlib import Path
import gzip
import json
import sys

H = Path(__file__).resolve().parent
R = H.parents[1]
sys.path[:0] = [str(R / 'Session20261126'), str(R / 'FinalSprint')]
from PivotCheck import C, B, exact_leaf, floor10
from JointValuation import excludes

PIVOT = 4805345109492315767981401
FIBERS = {1,2,4,5,6,9,10,12,13,14,16,18,20,21,22,24,25,28,29,30,32,33,34,36,37,38,40,41,42,45,46}


def replay(x):
    assert __debug__
    assert set(x) == {'p', 'e', 'tree', 'ecpp'} and (x['p'], x['e']) == (7, 36)
    tree = x['tree']
    assert tree['type'] == 'split' and tree['q'] == PIVOT
    assert set(tree['cases']) == {str(f) for f in FIBERS}
    used, open_paths, terminals, splits = set(), [], [], []

    @cache
    def prime(z):
        assert type(z) is int and z > 2
        n = z
        if n >= 2**64:
            key = str(n)
            used.add(key)
            chain = x['ecpp'][key]
            assert type(chain) is list and chain
            for row in chain:
                assert row[0] == n
                n = C.pc.level(*row)
        assert C.pc.prime64(n)
        return True

    def direct(s):
        return s.conflict or s.base > B or prod(C.sigma(z, f) for z, f in s.rows.items()) > 2*s.X

    def walk(parts, node):
        s = C.State(parts)
        assert not direct(s)
        kind = node['type']
        if kind == 'open':
            assert set(node) == {'type'}
            open_paths.append(parts[1:])
            return
        if kind == 'forest':
            assert set(node) == {'type', 'roots', 'owners', 'head'}
            k, o, h = node['roots'], node['owners'], node['head']
            C.validate_forest(s, k, o, h, prime)
            a, b = C.Forest(s, k, o, h).lower()[0], exact_leaf(parts, k, o, h)
            assert min(a, b) > B, ('forest open', parts, floor10(min(a,b)))
            terminals.append((parts[1:], kind, floor10(min(a, b))))
            return
        if kind == 'price':
            assert set(node) in ({'type'}, {'type', 'targets'}) and all(prime(z) for z, _ in parts)
            receipt = excludes(parts, s.bad, node.get('targets'))
            terminals.append((parts[1:], kind, receipt))
            return
        assert kind == 'split' and set(node) == {'type', 'q', 'cases'}
        q = node['q']
        assert prime(q) and q not in s.rows and q not in s.bad and s.D % q == 0
        h = C.valuation(s.D, q)
        scale = s.base // q**h
        f, size = h, s.base
        rejected, trivial, children = [], [], {}
        while size <= B:
            if not s.possible(q, f, h):
                rejected.append(f)
            else:
                sub = parts + [(q, f)]
                if direct(C.State(sub)):
                    trivial.append(f)
                else:
                    children[str(f)] = sub
            f += 1
            size *= q
        assert set(node['cases']) == set(children), ('incorrect split coverage', parts, q)
        splits.append(dict(path=parts[1:], valuation=h, q=q, scale_floor=floor10(scale), tail=f,
                           tail_floor=floor10(size), inadmissible=rejected, direct=trivial,
                           children=list(map(int, children))))
        for k, sub in children.items():
            walk(sub, node['cases'][k])

    walk([(7, 36)], tree)
    assert used == set(x['ecpp']) and terminals
    partial_fibers = sorted({path[0][1] for path in open_paths})
    closed_fibers = sorted(FIBERS - set(partial_fibers))
    partial = {f: dict(open_paths=[p for p in open_paths if p[0][1]==f],
                       excluded_leaves=[p for p,_,_ in terminals if p[0][1]==f])
               for f in partial_fibers}
    return dict(scope='EXACT_COMPLETE' if not open_paths else 'CONDITIONAL_ONLY',
                closed_fibers=closed_fibers, partial_fibers=partial,
                open_paths=open_paths, terminals=terminals, splits=splits, ecpp=len(used))


def verify(path):
    raw = Path(path).read_bytes()
    return dict(sha256=sha256(raw).hexdigest(), **replay(json.loads(gzip.decompress(raw))))


if __name__ == '__main__':
    if not __debug__:
        raise SystemExit('Assertions required; do not use -O.')
    for name in sys.argv[1:]:
        print(json.dumps(verify(name), separators=(',', ':')), flush=True)
