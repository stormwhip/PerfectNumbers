"""Complete root-5 exact exponent replay, independently checking both branches."""
import gzip
import hashlib
import json
from math import gcd, prod
from pathlib import Path
import sys

HERE = Path(__file__).resolve().parent
RESEARCH = HERE.parents[1]
for path in (HERE, RESEARCH / 'NightFive', RESEARCH / 'NightFiveReview'):
    sys.path.insert(0, str(path))
from FiveForestReplay import proof
from OrdinaryForest import lower as second
from HybridReplay import dual, bind, load_duals, I
from LocalModel import Bank, Model, primes, LIMIT

E = 148
B = 10**2400
BAD = (3, 7, 11, 13, 19, 31)
PACK = '59342e4bf2a1b4193e45af911feae42f298eac7781f4c8e0220b55bb5e7cdf20'


def verify(verbose=False):
    if not __debug__:
        raise ValueError('replay requires assertions; do not use -O')
    raw = (HERE / 'Forest148.json.gz').read_bytes()
    assert hashlib.sha256(raw).hexdigest() == PACK
    cert = json.loads(gzip.decompress(raw))
    row, = cert['rows']
    pe = 5**E
    q = (5*pe-1)//4
    assert set(row) == {'p', 'e', 'roots', 'owners', 'head'}
    assert row['p'] == 5 and row['e'] == E and row['roots'] == [q]
    vertices = {q} | {p for p, _ in row['owners']}
    assert {str(p) for p in vertices if p >= 2**64} == set(cert['ecpp'])
    values = proof(row, cert['ecpp'])
    assert set(values) == {0, q} and values[0] > B
    # The separate exact ratio-coupon implementation has the same branch:
    # keep q ordinary, allow at most one Euler coupon among children/outside.
    v = second(row)
    assert v > B

    bank = json.loads((I.CERT_DIR / 'DualP5.json').read_text())
    ds = [bind(d, a) for d, a in zip(load_duals(), bank['duals'], strict=True)]
    ps = primes(bank['R_act'])
    model = Model(E, {'roots': {str(E): []}, 'secondary': {}},
                  [Bank(d, bank['R_act'], ps) for d in bank['duals']])
    assert q%4 == 1 and pe*q**22 <= B < pe*q**23
    used = []
    for a in range(1, 23, 4):
        t = q**a
        w = (q*t-1)//(q-1)
        # These are exact sigma values, not inferred from a lower exponent.
        if any(w % b == 0 for b in BAD):
            used.append((a, 'forbidden'))
            continue
        X, S = pe*t, q*w
        D = S//gcd(2*X, S)
        if X*D > B:
            used.append((a, 'size'))
            continue
        assert gcd(X*prod(BAD), D) == 1
        xs = [(5, E), (q, a)]
        assert dual(xs, X, S, D, [], ds)
        # Independent fixed-Euler dual: direct recomputation with Decimal
        # rather than NightFive fixed-point tables; no recursive search.
        state = model.state(xs)
        assert state is not None and state[:2] == (X, D)
        assert max(b for d, rate, prices, b in state[-1]) > LIMIT
        used.append((a, 'two duals'))
    assert used == [(1, 'two duals'), (5, 'forbidden'), (9, 'forbidden'),
                    (13, 'size'), (17, 'forbidden'), (21, 'size')]
    if verbose:
        print(f'5 {E} ordinary floors: {len(str(values[0]))-1}, {len(str(v))-1}; Euler: {used}')
    return {(5, E)}


if __name__ == '__main__':
    verify(verbose=True)
