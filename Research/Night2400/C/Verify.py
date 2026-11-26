"""Cold replay of three exact conditional fibers, not a root/shard cover."""
import gzip
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
COVERED = (8, 10, 12)
FORCED8 = 18716166489844799458885230781362655242022878296316554735036307387001821111739679109236269675618028263


def certify(q, chain):
    for row in chain:
        assert row[0] == q and q >= 2**64
        q = C.pc.level(*row)
    assert C.pc.prime64(q)


def split():
    assert __debug__
    assert PIVOT.bit_length() == 185
    assert C.pc.prime64(ROOT)
    certify(PIVOT, json.loads((HERE / 'PivotECPP.json').read_bytes()))
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


def forced_square(parts, r):
    """Infer r^2 || N from an exact path and prime r; no search/factoring."""
    state = C.State(parts)
    assert not state.conflict and r not in state.rows and r % 4 == 3
    assert C.valuation(state.D, r) in (1, 2)
    next_parts = parts + [(r, 2)]
    # Test any higher even exponents below the monotone prefix-only tail.
    # The strengthened full-state bound is checked separately at each one.
    scale = state.base // r**C.valuation(state.D, r)
    f = 4
    while scale * r**f <= B:
        assert C.State(parts + [(r, f)]).base > B
        f += 2
    assert not C.State(next_parts).conflict and C.State(next_parts).base <= B
    return next_parts


def check_price(parts, forced=None):
    if forced is not None:
        parts = forced_square(parts, forced)
    return excludes(parts, C.State(parts).bad, [0, 1])


def verify():
    domain, direct = split()
    print('DOMAIN', SHARD, (ROOT, EXPONENT), PIVOT, domain, flush=True)
    print('DIRECT', direct, 'TAIL even >= 26', flush=True)
    certify(FORCED8, json.loads((HERE / 'Forced8ECPP.json').read_bytes()))
    for f in COVERED:
        parts = [(ROOT, EXPONENT), (PIVOT, f)]
        state = C.State(parts)
        assert not state.conflict and state.base <= B
        result = check_price(parts, FORCED8 if f == 8 else None)
        print('PASS conditional fiber', f, result, flush=True)
    print('OPEN in this packet', sorted(set(domain) - set(COVERED)), flush=True)


def regression():
    case = json.loads(gzip.decompress((RESEARCH / 'FinalSprint/Tree7x168.json.gz').read_bytes()))
    assert (case['p'], case['e']) == (7, 168)
    split_node = case['tree']
    q = split_node['q']
    r = 1452979915402500135854417362573926368874134931212567
    assert r in split_node['cases']['12']['roots']
    assert C.pc.prime64(7)
    certify(q, case['ecpp'][str(q)])
    certify(r, case['ecpp'][str(r)])
    result = check_price([(7, 168), (q, 12)], r)
    assert result == (4, [1763, 73, 192])
    print('PASS known Tree7x168 fiber 12, regression only', result)


if __name__ == '__main__':
    if sys.argv[1:] == ['--regression']:
        regression()
    else:
        assert not sys.argv[1:]
        verify()
