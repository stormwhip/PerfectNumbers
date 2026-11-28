"""Independent coverage arithmetic for one exact (19,276) conditional prefix."""
from fractions import Fraction
from bisect import bisect_right
from math import gcd, isqrt, prod

B = 10**2400
P, Q, S = 19, 1176672733, 1109
F = {P: 276, Q: 1, S: 4}


def geom(b, h):
    return (b**(h+1)-1)//(b-1)


def vp(b, p):
    a = 0
    while b % p == 0:
        a += 1
        b //= p
    return a


def plainprime(n):
    return n > 1 and (n == 2 or n % 2 == 1 and all(n % d for d in range(3, isqrt(n)+1, 2)))


def composite_witness(n):
    # Strong test used one-way only: a witness rejects a composite.
    # Non-witnesses, even beyond deterministic ranges, are kept.
    d, a = n - 1, vp(n-1, 2)
    d >>= a
    for b in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37):
        if 1 < b < n:
            r = pow(b, d, n)
            if r not in (1, n-1) and not any(pow(r, 2**i, n) == n-1 for i in range(1, a)):
                return True
    return False


def u19(c):
    loss = {}
    # Odd orders >1 exhaustively from order |18, length odd.
    assert [d for d in range(3, P, 2) if (P-1) % d == 0] == [3, 9]
    for o in (3, 9):
        assert o-1 >= 2
        roots = [r for r in range(1,P) if pow(r,o,P)==1 and pow(r,o//3,P)!=1]
        assert len(roots) == o-o//3
        m = P
        for z in range(1,c+1):
            for b in roots:
                if b >= 3 and b % 2 == 1 and b not in F and b**(o-1) < m*m and not composite_witness(b):
                    # Check every capped depth. Taking the max includes the actual
                    # capped order valuation, even when a representative repeats.
                    loss[b] = max(loss.get(b, 1), Fraction(m*m, b**(o-1)))
            if z < c:
                # Enumerate every digit instead of using a shared Hensel formula.
                new = [r+j*m for r in roots for j in range(P) if pow(r+j*m,o,m*P)==1]
                assert len(new) == len(roots)
                m *= P
                roots = new
    return loss, prod(loss.values())


def main():
    assert __debug__
    assert all(plainprime(p) for p in (*F, 277))
    assert Q % 4 == 1 and Q + 1 == 2*588336367
    X = prod(p**h for p,h in F.items())
    odd = prod(geom(p,h) for p,h in F.items()) // 2
    c19, c1109 = (F[p]-vp(odd,p) for p in (P,S))
    assert (c19,c1109) == (276,3)
    assert 3**5030 <= B < 3**5031
    assert S-1 == 4*277 and S*277 > 5031 and X*(2*S+1)**(S-1) > B
    assert gcd(P*3,S*277)==1
    # LTE extra exponent A-o >= 18o*k for A=o*19^k; order 1
    # A-1 >=18u, both enough to pay the corresponding 19-adic units.
    assert 3**18 > P**2
    losses, U19 = u19(c19)
    assert U19 < 10**6
    K = 63700
    # Combined lower bound X*19^(2*c19)/U19 * prod(b^m)^276.
    # Use the independently proved relaxation U19 < 10^6 to certify K.
    assert X*P**(2*c19)*K**276 >= B*10**6
    sieve = [p for p in range(3,K,2) if plainprime(p) and p not in F and p % S != 0 and pow(p,277,S)==1]
    assert sieve[:3] == [13,29,53]
    assert all(pow(p,277,S*S)!=1 for p in sieve)
    assert sieve[0]**3*sieve[1]*sieve[2] >= K
    triples = [(a,b,c) for i,a in enumerate(sieve) if a**3 < K
               for j,b in enumerate(sieve[i+1:], i+1) if a*b*b < K
               for c in sieve[j+1:bisect_right(sieve,(K-1)//(a*b))]]
    ratios = []
    for t in triples:
        xx = X*prod(t)**276
        ss = odd*prod(geom(p,276) for p in t)
        lower = xx*(ss//gcd(xx,ss))
        assert lower > B
        ratios.append(lower)
    assert len(triples) == 9
    print('PASS fixed Euler, target demands', (c19,c1109), '19-loss bases', sorted(losses), 'U19 < 10^6')
    print('277-order prime bases below', K, ':', len(sieve), '; all lift to depth exactly 1')
    print('9 complete triples:', triples)
    print('Minimum terminal floor(log10 N lower):', min(len(str(v))-1 for v in ratios))


if __name__ == '__main__':
    main()
