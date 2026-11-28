#!/usr/bin/env python3
"""Standalone integer replay of rare-supplier joint pricing for (19,276)."""
from fractions import Fraction
from itertools import combinations
from math import gcd, isqrt, prod

B = 10**2400
P, T, S = 19, 1176672733, 1109
FROZEN = '495c59f55456a70994ce7848487e0c4e262c1984'


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def prime(n):
    return n == 2 or n >= 3 and n % 2 == 1 and all(n % d for d in range(3, isqrt(n) + 1, 2))


def sigma(p, a):
    return (p**(a + 1) - 1)//(p - 1)


def vp(n, p):
    v = 0
    while n % p == 0:
        v += 1
        n //= p
    return v


def odd(n):
    return n >> vp(n, 2)


def state(rows):
    X = prod(p**a for p, a in rows)
    H = prod(sigma(p, a) for p, a in rows)
    Y = odd(H)
    return X, H, Y, X*(Y//gcd(X, Y))


def raw_closed(rows):
    X, H, Y, base = state(rows)
    return base > B or H > 2*X or any(vp(Y, q) > a for q, a in rows)


def loss19(c, forbidden):
    # Each positive deficit at depth z forces b<19^z. With z=min(c,v),
    # this holds also at the terminal cap; no roots of higher order are dropped.
    tab = {}
    for o in (3, 9):
        m = P
        roots = [r for r in range(2, P) if pow(r, o, P) == 1 and (o == 3 or pow(r, 3, P) != 1)]
        require(len(roots) == (2 if o == 3 else 6), 'initial 19 roots')
        for z in range(1, c + 1):
            num = P**(2*z)
            for b in roots:
                if b < 3 or b % 2 == 0 or b in forbidden or b**(o - 1) >= num:
                    continue
                # Fermat witnesses exclude composites without relying on probable primes.
                if any(pow(a, b - 1, b) != 1 for a in (2, 3, 5, 7, 11, 13) if a < b):
                    continue
                ratio = Fraction(num, b**(o - 1))
                tab[b] = max(tab.get(b, 1), ratio)
            m1 = P*m
            roots = [r + m*((-(pow(r, o, m1) - 1)//m) * pow(o*pow(r, o - 1, P), -1, P) % P) for r in roots]
            require(len(set(roots)) == len(roots) and all(0 < r < m1 and pow(r, o, m1) == 1 for r in roots), '19 lift')
            m = m1
    return prod(tab.values()), tab


def main():
    require(all(prime(q) for q in (P, T, S, 277)), 'fixed prime proof')
    require(T % 4 == 1 and P - 1 == 2*9 and S - 1 == 4*277 and gcd(9*P, S*277) == 1, 'Euler or support')
    require(3**5030 <= B < 3**5031, 'length cap')
    require(3**18 >= P**2 and all(3**(o*(P**k - 1)) >= P**(2*k) for o in (3, 9) for k in (1, 2)) and 3*P**3 > 5031, '19 LTE payment')
    require((2*S + 1)**(S - 1) > B and 277*S > 5031, '1109 order one and LTE exclusion')
    parent = [(P, 276), (T, 1)]
    X0, _, Y0, D0 = state(parent)
    D0 //= X0
    require(D0 % S == 0 and Y0 % S**2 != 0, '1109 forced with lower bound 1')
    U, loss = loss19(276, {P, S, T})
    require(U <= 10**6, 'rounded loss cap')
    print('19 loss bases:', sorted(loss), 'U =', U)
    print('Baseline:', FROZEN)
    for h, K, demand19, demandS in [(2, 68465, 275, 1), (4, 63700, 276, 3)]:
        rows = parent + [(S, h)]
        X, _, Y, _ = state(rows)
        require(not raw_closed(rows) and 276 - vp(Y, P) == demand19 and h - vp(Y, S) == demandS, 'open prefix or demands')
        V = X*P**(2*demand19)
        require(V*(K - 1)**276 <= B*10**6 < V*K**276, 'strict combined product cap')
        # Every supplying b is a prime <K, exactly of order 277 mod S.
        # Check z>=2 directly on the full actual base range, including all lifts.
        pool = [q for q in range(3, K, 2) if q not in {P, T, S} and pow(q, 277, S) == 1 and prime(q)]
        require(pool[:3] == [13, 29, 53], 'supplier minima')
        require(all(pow(q, 277, S**2) != 1 for q in pool), 'higher valuation supplier survived')
        if h == 4:
            require(13**3*29*53 >= K, 'nonminimal source length possible')
            possibles = [qs for qs in combinations([q for q in pool if q*13*29 < K], 3) if prod(qs) < K]
            require(len(possibles) == 9, 'triple count')
            for qs in possibles:
                rp = rows + [(q, 276) for q in qs]
                require(state(rp)[3] > B, ('strict raw triple tail', qs))
            print('EXCLUDED h=4: all 9 exact source triples via strict raw size:', possibles)
        else:
            # h=2: enumerate the one exact supplier using the same strict budget.
            survivors = []
            total = 0
            for q in pool:
                for m in range(1, 5031//277 + 1, 2):
                    if q**m >= K:
                        break
                    total += 1
                    f = 277*m - 1
                    if not raw_closed(rows + [(q, f)]):
                        survivors.append((q, f))
            print('OPEN h=2:', len(survivors), 'of', total, 'exact source rows survived raw tests:', survivors)


if __name__ == '__main__':
    main()
