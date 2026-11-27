"""Cold replay for exact key (19,330), strictly conditional on pivot fibers."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
R = HERE.parents[1]
sys.path[:0] = [str(R / 'FinalSprint'), str(R / 'Session20261126')]
from JointValuation import excludes
from PivotCheck import B, C

ROOT = (19, 330)
SHARD = 'P19_I00065'
Q = 1214428680506010004551311201724184433986966434253654794712076383
A8 = 2649006202622389754026474949684537136117722932291062868195158132223440533168779423867212541


def certify(q, filename):
    for row in json.loads((HERE / filename).read_bytes()):
        assert row[0] == q and q >= 2**64
        q = C.pc.level(*row)
    assert C.pc.prime64(q)


def split(parts, q):
    """Return remaining exact exponent domain, and record the finite direct cases."""
    state = C.State(parts)
    assert not state.conflict and state.base <= B
    assert q not in state.rows and q not in state.bad and state.D % q == 0
    h = C.valuation(state.D, q)
    scale = state.base // q**h
    f = h
    pending, direct, incompatible = [], [], []
    while scale * q**f <= B:
        if not state.possible(q, f, h):
            incompatible.append(f)
        else:
            leaf = C.State(parts + [(q, f)])
            (direct if leaf.conflict or leaf.base > B else pending).append(f)
        f += 1
    return pending, direct, incompatible, f


def check(parts, expected):
    result = excludes(parts, C.State(parts).bad, [0, 1])
    assert result == expected
    print('PASS', tuple(f for _, f in parts), result, flush=True)


def verify():
    assert __debug__ and C.pc.prime64(ROOT[0])
    assert Q.bit_length() == 210 and Q % 4 == 3
    certify(Q, 'PivotECPP.json')
    certify(A8, 'Split8ECPP.json')
    domain = split([ROOT], Q)
    assert domain == ([2, 4, 6, 8, 10, 12], list(range(14, 25, 2)), list(range(1, 26, 2)), 26)
    print('DOMAIN', SHARD, ROOT, domain, flush=True)
    P8 = [ROOT, (Q, 8)]
    subdomain = split(P8, A8)
    assert subdomain == ([1, 2], [4, 5, 6], [3, 7], 8)
    print('SPLIT 8', subdomain, flush=True)
    for f, expected in [(1, (16, [0, 0, 0])), (2, (16, [1260, 1388, 0]))]:
        check(P8 + [(A8, f)], expected)
    check([ROOT, (Q, 10)], (16, [2294, 948, 68]))
    check([ROOT, (Q, 12)], (16, [3831, 141, 0]))
    print('OPEN: 2, 4, 6', flush=True)


if __name__ == '__main__':
    verify()
