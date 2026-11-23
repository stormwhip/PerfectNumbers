"""Independent multiplicative proof for the two ranges. No CSV or project imports."""
from fractions import Fraction
from math import prod, isqrt
from functools import lru_cache

B = 10**2400
# p, index offset for primes after the special representatives, m interval,
# exclusions, incoming-unit cap, multiplier for the abundancy dual, tail sum.
CASES = [
    (3, 5, 7, 1697, 2503, (19, 7, 11, 31, 13), 255, 265, Fraction(2,1000)),
    (5, 1, 3, 1069, 1709, (19, 7, 11, 31, 13, 3), 131, 2880, Fraction(3,1000)),
]


def prime(n):
    return n >= 2 and all(n%i for i in range(2, isqrt(n)+1))


def require(ok):
    if not ok:
        raise ValueError("Invalid proof inequality")


def residual(p, forbidden, mul, hbound, free_prime=None):
    # c is a rational lower bound on the residual size for this prime.
    ratio, weight = Fraction(1), Fraction(1)
    for r in range(3, 1001, 2):
        if not prime(r) or r == p or r in forbidden:
            continue
        c = Fraction(r**32, 33)
        for e in range(2, 32, 2):
            sig = (r**(e+1)-1)//(r-1)
            if any(sig%f == 0 for f in forbidden):
                continue
            power = 1
            while sig % (p*power) == 0:
                power *= p
            c = min(c, Fraction(r**e, power))
        if c < Fraction(r, r-1)**mul:
            weight *= c
            ratio *= Fraction(r-1, r)
    require(Fraction(1001, 1000)**mul < Fraction(1000**2, 3))
    # All A-primes have product of upper abundancies <= 1/(1-hbound).
    upper = Fraction(p, p-1)*Fraction(1000001, 1000000)/(1-hbound)
    if free_prime:
        upper *= Fraction(free_prime, free_prime-1)
    dual = weight*(2*ratio/upper)**mul
    return (dual.numerator//dual.denominator).bit_length()-1


@lru_cache(None)
def harmonic(t):
    return sum((Fraction(1,i) for i in range(1,t+1)), Fraction(0))


def log_floor(n, base):
    lo, hi = 0, n.bit_length()//(base.bit_length()-1)+1
    while hi-lo > 1:
        mid = (lo+hi)//2
        if pow(base, mid) <= n:
            lo = mid
        else:
            hi = mid
    return lo


def suppliers(p, forbidden, m, units, bfull, bfree, hbound):
    d, a = m-1, (p**m-1)//(p-1)
    # For any larger covered exponent x, p^(2x)/2 divides the size budget as a lower bound.
    require(p**(2*(2*m-1)) > 2*B)
    product = p**d
    for k, z in enumerate(sorted(units)):
        product *= z**(p-1)
        if product > B:
            break
    else:
        raise ValueError("Incomplete marginal list")
    s = d-k-(7 if p==3 else 5)
    require(s > 0 and (2*p**s-1)*(p**s+1) > p**m-1 and 2*p**s-1 >= 1000001)
    require(harmonic(log_floor(a, 2*m+1)) <= 2*m*hbound)
    step = 2*p*m
    candidates = [1+step*i for i in range(1,129)]
    cutoff = 1+129*step
    rep = next((r for r in candidates if a % r**(p-1) == 0), cutoff)
    share = next((r for r in candidates if a % r == 0), cutoff)
    gift = log_floor(a, rep**(p-1))
    small = next(r for r in range(3,1000,2) if prime(r) and r%p==1 and r not in forbidden)
    unit = min(share, small**(p-1))
    while True:
        y = p**s
        q = 2*y-1
        cap = B//(p**d*a*q)
        if not cap:
            return
        gain = d-gift-log_floor(cap,unit)-log_floor(2+log_floor(cap,q),p)
        if gain <= s:
            break
        s = gain
    require(3*(cap//(2**bfree)) < 2*q)
    cap //= 2**bfull
    if cap == 0:
        return
    bounds = [(1,isqrt(a))]
    if cap >= 2:
        h = 1 << ((a.bit_length()+2)//3)
        while True:
            z = (2*h+a//(h*h))//3
            if z >= h:
                break
            h = z
        require(h**3 <= a < (h+1)**3)
        bounds.extend([(cap,isqrt(cap)),(min(h,cap),min(h,cap))])
        if p != 3 and cap*cap+cap+1 >= q:
            bounds.append((cap,cap))
    for t,r in bounds:
        require((p-1)*a*t*r < y*q)
        require(3*(p-1)*a*t + 2*q*t*r < 2*y*q)


def run():
    for p, offset, first, lo, hi, forbidden, k, mul, hbound in CASES:
        possible = [n for n in range(first, hi+1, 2) if prime(n)]
        # All marginal bases <= 10000. Larger bases follow the first k+1.
        units = []
        for r in range(3, 10001, 2):
            if r % p != 1 or r in forbidden or not prime(r):
                continue
            base = r
            while base <= 10000:
                units.append(base)
                base **= p
        require(len(units) >= k+1)
        require(p**(lo-1)*prod(sorted(units)[:k+1])**(p-1) > B)
        j = 7 if p == 3 else 5
        require(3**(p**(j+1)-1) > B)
        bits = residual(p, forbidden, mul, hbound)
        proved = []
        for index, m in enumerate(possible, offset):
            if m < lo:
                continue
            d = m-1
            a = (p**m-1)//(p-1)
            s = d-k-j
            y = p**s
            require(2*y-1 >= 1000001)
            require((2*y-1)*(y+1) > p**m-1)
            t, power = 0, 1
            while power*(2*m+1) <= a:
                t += 1
                power *= 2*m+1
            require(harmonic(t) <= 2*m*hbound)
            # Find the first progression member not ruled out as a repeated divisor.
            base = 1 + 2*m*p
            while base < 1+129*2*m*p and a % (base**(p-1)) != 0:
                base += 2*m*p
            power, gift = 1, 0
            step = base**(p-1)
            while power*step <= a:
                power *= step
                gift += 1
            require((p**(2*d)*a << bits) > B*p**gift)
            proved.append(index)
        print(f"p={p}: {len(proved)} verified, indices {proved[0]}..{proved[-1]}, residual >= 2^{bits}")
        require(proved == list(range(266,370) if p == 3 else range(179,267)))
        start, cutoff = (1481, Fraction(22,10000)) if p==3 else (953, Fraction(33,10000))
        bfull = residual(p, forbidden, mul, cutoff)
        bfree = residual(p, forbidden, 40 if p==3 else 1919, cutoff, 5 if p==3 else 17)
        indices = []
        for idx, m in enumerate(possible, offset):
            if start <= m < lo:
                suppliers(p, forbidden, m, units, bfull, bfree, cutoff)
                indices.append(idx)
        require(indices == list(range(235,266) if p==3 else range(161,179)))
        print(f"p={p}: {len(indices)} supplier proofs, indices {indices[0]}..{indices[-1]}, bits={bfull}/{bfree}")


if __name__ == "__main__":
    run()
