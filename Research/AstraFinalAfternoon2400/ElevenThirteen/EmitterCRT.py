"""Standalone certified order-root restriction for q|sigma(r^h)."""
from math import gcd


def possible_q_prime(q,o,lo,hi,stride=1,rest=0):
    """One-sided. If q is prime and admissible interval has a base of order o,
    then return True. It may return True unnecessarily if no generator found.
    """
    if q<=hi or (q-1)%o or gcd(q,stride)!=1:
        return True
    # Find an exact generator of the needed cyclic subgroup if q is prime.
    g=None
    prime_divisors=[p for p in range(2,o+1) if o%p==0 and all(p%d for d in range(2,p))]
    for b in range(2,65):
        z=pow(b,(q-1)//o,q)
        if pow(z,o,q)==1 and all(pow(z,o//p,q)!=1 for p in prime_divisors):
            g=z;break
    if g is None:return True
    roots=[pow(g,j,q) for j in range(1,o) if gcd(j,o)==1]
    # Since 0<r<=hi<q, any possible r must be exactly one of these residues.
    return any(lo<=r<=hi and (r-rest)%stride==0 for r in roots)
