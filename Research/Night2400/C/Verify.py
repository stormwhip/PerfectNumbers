"""Cold replay of two exact conditional fibers, not a root/shard cover."""
import json
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
sys.path[:0] = [str(RESEARCH / 'FinalSprint'), str(RESEARCH / 'Session20261126')]
from JointValuation import excludes
from PivotCheck import B, C

ROOT, EXPONENT = 19, 420
PIVOT = 28174642921954703272833689609691232580811241064837460583
SHARD = 'P19_I00080'
COVERED = (10, 12)


def split():
    assert __debug__
    chain = json.loads((HERE / 'PivotECPP.json').read_bytes())
    q = PIVOT
    assert q.bit_length() == 185
    assert C.pc.prime64(ROOT)
    for row in chain:
        assert row[0] == q and q >= 2**64
        q = C.pc.level(*row)
    assert C.pc.prime64(q)
    A = C.sigma(ROOT, EXPONENT)
    assert A % PIVOT == 0 and PIVOT % 4 == 3
    c = C.valuation(A, PIVOT)
    assert c == 1
    scale = ROOT**EXPONENT * (A // PIVOT**c)
    f = c
    domain, direct = [], []
    while scale * PIVOT**f <= B:
        if f % 2 == 0:
            state = C.State([(ROOT, EXPONENT), (PIVOT, f)])
            (direct if state.base > B else domain).append(f)
        f += 1
    assert domain == [2, 4, 6, 8, 10, 12]
    assert direct == [14, 16, 18, 20, 22, 24]
    assert f == 25
    return domain, direct


def verify():
    domain, direct = split()
    print('DOMAIN', SHARD, (ROOT, EXPONENT), PIVOT, domain, flush=True)
    print('DIRECT', direct, 'TAIL even >= 26', flush=True)
    for f in COVERED:
        parts = [(ROOT, EXPONENT), (PIVOT, f)]
        state = C.State(parts)
        assert not state.conflict and state.base <= B
        result = excludes(parts, (), [0, 1])
        print('PASS conditional fiber', f, result, flush=True)
    print('OPEN in this packet', sorted(set(domain) - set(COVERED)), flush=True)


if __name__ == '__main__':
    verify()
