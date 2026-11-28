"""Independently rebuild every high Euler window of canonical 7^808."""
from functools import cache
from math import gcd, isqrt

B = 10**2400
X = 7**808
W = 7*X
A = sum(7**i for i in range(809))
C = 10**7


def isprime(n):
    return n > 1 and all(n % d for d in range(2,isqrt(n)+1))


@cache
def floorroot(n, h):
    lo, hi = 0, 1 << (n.bit_length()//h+1)
    while hi-lo > 1:
        mid = (lo+hi)//2
        if mid**h > n:
            hi = mid
        else:
            lo = mid
    assert lo**h <= n < (lo+1)**h
    return lo


def first_q(s,h):
    # Find the lowest actual odd m via finite scan rather than modular inverse.
    y = 7**s
    o = h+1
    m0, = [m for m in range(1,2*o,2) if m*y % o == 1]
    primes = tuple(p for p in range(2,98) if isprime(p))
    for j in range(81):
        m = m0 + 2*o*j
        q = 2*m*y-1
        if j == 80 or (m%7 and m%19 and not any(q%p == 0 and q>p for p in primes)):
            return q
    raise AssertionError


def side_magnitudes(y):
    # D0 == -1-6A mod 1618. Scan the complete modulus in both signs.
    m = 1618
    residue = (-1-6*A)%m
    pos, = [j for j in range(1,m+1) if y*j % m == residue]
    neg, = [j for j in range(1,m+1) if (-y*j) % m == residue]
    return y*pos, y*neg


def windows(s):
    y = 7**s
    q0 = 2*y-1
    assert xbound(q0)
    cap = B//(X*A)
    plus, minus = side_magnitudes(y)
    survived = []
    audit = 0
    h = 2
    while X*q0*(C+1)**h <= B:
        if (h+1)%7:
            q = first_q(s,h)
            t = cap//q
            lo = max(C+1, floorroot(2*q//3,h)+1)
            for c in range(1,h+1):
                audit += 1
                excess = h-c
                hi = floorroot(A,c)
                if excess:
                    hi = min(hi,floorroot(t,excess))
                elif t == 0:
                    continue
                else:
                    mmax = (9*A-1)//q
                    if mmax*(2*mmax)**h+mmax**h < y:
                        continue
                if 3*W*t < y*q and 3*t < 2*y:
                    hi = min(hi, 2*W//y+1)
                if lo > hi:
                    continue
                power = hi**(excess+1)
                vmax = 6*(A//lo**c)
                # No magnitude floor and no shared modular inverse.
                if (W-1)*power <= q*plus and q*power+(q+1)*vmax < q*minus:
                    continue
                # Compare the lower endpoint directly against the necessary budget.
                if q**(2*h-c)*2**excess > cap**h*3**excess:
                    continue
                survived.append((h,c))
        h += 2
    return survived, audit


def xbound(q):
    return q>5031 and X*A*q**5>B and 2*X*A*q*q>3*B and 8*X*q**4>27*B


def main():
    assert __debug__ and isprime(809)
    assert 6*A == W-1 and gcd(A,42)==1
    assert 3**5030 <= B < 3**5031
    # A prime divisor must have order 809; multiplying residues by 7 repeatedly
    # computes the test without the applicant's modular exponentiation primitive.
    count = 0
    for b in range(1+1618,C+1,1618):
        power = 1
        for _ in range(809):
            power = (7*power)%b
        assert power != 1
        count += 1
    total = 0
    for s in range(708,809):
        survivors, examined = windows(s)
        assert not survivors,(s,survivors)
        total += examined
    low,_ = windows(707)
    assert sorted(low) == [(8,3),(10,5),(12,7)]
    print('PASS',count,'unfiltered roughness classes, 101 Euler windows,',total,'h,c pairs before cuts')
    print('707 remains unproved; independent survivor shapes:',low)


if __name__ == '__main__':
    main()
