"""Four exact anonymous cyclotomic outputs at the remaining bottlenecks.

This is a factor-free constraint, not an exclusion theorem for any fiber.
"""
from math import gcd, isqrt

ATOMS = ((398581,103), (398581,109), (797161,97),
         (589657170962820100934139512775879733212083419, 13))
BOUND = 20_000_001


def run():
    assert __debug__
    for r,d in ATOMS:
        assert r > 1 and d > 2 and all(d%u for u in range(2,isqrt(d)+1))
        a=(r**d-1)//(r-1)
        assert a%2==1 and gcd(a,r*(r-1)*d)==1
        assert pow(2,a-1,a)!=1 and isqrt(a)**2!=a
        # Each prime factor s of a has ord_s(r)=d, and s is odd.
        # Trial-test all eligible integers (prime or not) below BOUND.
        seen=0
        for t in range(2*d+1,BOUND,2*d):
            assert a%t
            seen+=1
        print(f'ATOM {r}^{d-1}: {len(str(a))} digits, composite nonsquare, '
              f'prime divisors 1 mod {2*d}, all >= {BOUND}; {seen} trials')


if __name__ == '__main__':
    run()
