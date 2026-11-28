"""Exact-integer helpers for Euler positions, paid support and valuation deficits.

All primality hypotheses are obligations of the certificate caller. The loss
kernel optionally uses a one-sided necessary candidate filter, never a proof of
primality. Resource caps raise rather than silently dropping candidates.
"""
from functools import cache
from fractions import Fraction
from math import gcd, isqrt, prod


def sigma(p, e):
    return (p**(e+1)-1)//(p-1)


def val(x, p):
    assert x > 0 and p > 1
    n = 0
    while x % p == 0:
        x //= p
        n += 1
    return n


def part(x, n):
    """Largest divisor of x supported on prime divisors of n (no factorization)."""
    assert x > 0 and n > 0
    keep = 1
    while (g := gcd(x, n)) > 1:
        keep *= g
        x //= g
        n = g*g
    return keep


def partition(emissions, strip_support=1, isolate=()):
    """Partition the product into coprime ownership classes, with no fake primes.

    Each returned pair (base, powers) has the exact contributions of all
    emissions at the primes dividing base. An isolate is an extra support
    test (usually a certified compulsory prime), not an added emission.
    """
    blocks = [x//part(x, strip_support) for x in emissions]
    support = prod(blocks)
    classes = [support] if support > 1 else []
    for test in (*blocks, *isolate):
        new = []
        for c in classes:
            a = part(c, test)
            new.extend(x for x in (a, c//a) if x > 1)
        classes = new
    result = [(c, tuple(part(x, c) for x in blocks)) for c in classes]
    assert all(c == prod(row) for c, row in result)
    assert prod(c for c, _ in result) == support
    assert all(gcd(c, d) == 1 for i, c in enumerate(classes) for d in classes[:i])
    return result


def outside_progression(block, residue, modulus, lower, upper, quota=64):
    """Prove no divisor q in the prescribed class, or return False (unknown).

    Scan whichever of q and block/q has fewer representatives. The proof
    uses all of them, even when the interval covers multiple lifts.
    """
    assert block > 0 and 0 < residue < modulus and gcd(residue, modulus) == 1
    assert lower > 1 and quota >= 0
    upper = min(upper, block)
    if lower > upper:
        return True
    def sequence(r, lo, hi):
        first = lo + (r-lo) % modulus
        return first, max(0, (hi-first)//modulus+1)
    x, n = sequence(residue, lower, upper)
    y, m = sequence(block*pow(residue,-1,modulus) % modulus,
                    (block+upper-1)//upper, block//lower)
    start, count = (x,n) if n <= m else (y,m)
    return count <= quota and all(block % (start+i*modulus) for i in range(count))


def introot(n, k):
    """Floor of the nonnegative integer k-th root."""
    assert n >= 0 and k >= 1
    if n < 2 or k == 1:
        return n
    if k >= n.bit_length():
        return 1
    x = 1 << ((n.bit_length()+k-1)//k)
    while True:
        y = ((k-1)*x + n//x**(k-1))//k
        if y >= x:
            return x
        x = y


def divisors(x):
    return sorted({d for i in range(1,isqrt(x)+1) if x%i == 0 for d in (i,x//i)})


def prime_divisors(x):
    return [p for p in divisors(x) if p > 1 and all(p%i for i in range(2,isqrt(p)+1))]


def primitive_residues(p, order):
    """All exact order-o representatives modulo the (certified) prime p."""
    assert order>1 and (p-1)%order == 0
    factors = prime_divisors(order)
    for g in range(2,p):
        x=pow(g,(p-1)//order,p)
        if all(pow(x,order//d,p) != 1 for d in factors):
            roots = tuple(pow(x,j,p) for j in range(1,order) if gcd(j,order)==1)
            assert pow(x,order,p)==1 and len(set(roots))==len(roots)
            return roots
    raise ValueError('no primitive root; verify prime/order')


def hensel(p, o, depth):
    """Yield (p**z, residues) for all simple exact-order-o roots, z=1..depth."""
    roots = primitive_residues(p,o)
    m = p
    inv = [pow(o*pow(r,o-1,p),-1,p) for r in roots]
    for z in range(1, depth+1):
        yield m, roots
        if z < depth:
            k = m*p
            roots = tuple(r+m*(-((pow(r,o,k)-1)//m)*d % p)
                          for r,d in zip(roots,inv))
            m = k


def all_below(residues, modulus, bound):
    """Enumerate every positive integer in every residue class <= bound."""
    assert modulus > 0 and all(0 < r <= modulus for r in residues)
    for r in residues:
        yield from range(r,bound+1,modulus)


def screened_prime(x):
    return x >= 3 and x%2 == 1 and all(x==r or x%r for r in (3,5,7,11,13,17,19,23,29,31,37)) and pow(2,x-1,x)==1


def odd_price(p, demand, n, d, B, max_length, may_be_base=screened_prime, quota=200000):
    """Bound the distinct-base loss product for ordinary, odd-length atoms.

    Target p is prime. Atom base >=3 can be composite if the caller supplies
    a filter accepting that base (e.g. an Euler square); max_length is a proven
    upper bound on every length. For each loss level and exact order, check
    ALL progressions up to the strict price/size cap, not just least residues.
    """
    assert demand >= 0 and n > 0 and d > 0 and (p%2==1 and p>2)
    assert 3**(max_length-1)>B  # at least this strong suffices for length bound
    if p <= max_length:
        assert (2*p+1)**(d*(p-1)) >= p**n
        assert 3**(3*d*(p-1)) >= p**n
    losses = {}
    count = outward = 0
    for o in range(3, max_length+1, 2):
        if (p-1)%o:
            continue
        h = o-1
        size = introot(B,h)
        if size<3 or 3**(d*h)>=p**(n*demand):
            continue
        for z,(m,roots) in enumerate(hensel(p,o,demand),1):
            A = m**n
            cap = min(size, introot(A-1,d*h)) if n>d*h else size
            if cap < 3:
                continue
            # If n<=d*h, any strict loss already forces x < modulus.
            cap = min(cap,m-1) if n<=d*h else cap
            howmany = sum(max(0,(cap-r)//m+1) for r in roots)
            count += howmany
            if count > quota:
                raise ValueError('complete lift budget exceeded')
            for x in all_below(roots,m,cap):
                outward += x>=m
                if x<3 or (x.bit_length()-1)*d*h>=A.bit_length() or not may_be_base(x):
                    continue
                W = x**(d*h)
                if W<A:
                    losses[x] = max(losses.get(x,1),Fraction(A,W))
    return prod(losses.values(),start=Fraction(1)), count, outward, losses
