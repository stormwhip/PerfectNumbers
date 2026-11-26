"""Exact simultaneous incoming-valuation price. All odd prime bases in P must
have been certified by the caller. See JointValuation.md for completeness.
No factoring, floating point, data files or third-party packages are needed.
"""
from functools import cache
from fractions import Fraction
from itertools import product
from math import gcd, isqrt, prod

B = 10**2400
ONE = Fraction(1)


def val(x, p):
    assert x > 0
    k = 0
    while x % p == 0:
        x //= p; k += 1
    return k


@cache
def divisors(n):
    return sorted({d for k in range(1, isqrt(n)+1) if n % k == 0 for d in (k, n//k)})


@cache
def lifts(p, order, depth):
    # Find a cyclic subgroup of exactly this order, without factoring p-1.
    assert order > 1 and (p-1) % order == 0
    factors = [q for q in divisors(order) if q > 1 and len(divisors(q)) == 2]
    h = 2
    while True:
        x = pow(h, (p-1)//order, p)
        if x and all(pow(x, order//q, p) != 1 for q in factors): break
        h += 1
    roots = [pow(x, j, p) for j in range(1, order) if gcd(j, order) == 1]
    table = []; m = p
    for level in range(1, depth+1):
        table.append(tuple(roots))
        roots = [z + m * ((-(pow(z, order, m*p)-1)//m * pow(order*pow(z,order-1,p),-1,p)) % p) for z in roots]
        m *= p
    return tuple(table)


@cache
def inverse(a, m): return pow(a, -1, m)


def less(x, f, limit):
    return (x.bit_length()-1)*f < limit.bit_length() and x**f < limit


def excludes(P, banned, targets=None):
    assert __debug__ and len(P) in (2,3,4) and all(f > 0 for _,f in P)
    fixed = dict(P); assert len(fixed) == len(P) and not (set(fixed) & set(banned))
    assert all(not f%2 or p%4 == f%4 == 1 for p,f in P) and sum(f%2 for _,f in P) <= 1
    X = prod(p**f for p,f in P)
    Z = [((p**(f+1)-1)//(p-1))//(1+f%2) for p,f in P]; S = prod(Z)
    C = S//gcd(S,X); assert gcd(C,X) == 1
    blocks = [z//gcd(z,X) for z in Z]; assert prod(blocks) == C
    if targets is None: targets = list(range(len(P)))
    assert 1 <= len(targets) <= len(P) and sorted(set(targets)) == targets and all(type(i)==int and 0<=i<len(P) for i in targets)
    Q = [P[i][0] for i in targets]; caps = [fixed[p]-val(S,p) for p in Q]; assert min(caps) >= 0
    powers = [p**(c+1) for p,c in zip(Q,caps)]
    M = prod(p**c for p,c in zip(Q,caps)); maxsize = B//X; n = len(Q)
    fixed_euler = any(f%2 for _,f in P); exceptions = {}

    @cache
    def charge(r,f):
        if r < 3 or not r%2 or r in fixed or r in banned: return
        if f%2 and (fixed_euler or r%4 != 1 or f%4 != 1): return
        if not less(r,f,maxsize+1): return
        if any((f+1)%z == 0 if r%z == 1 else pow(r,f+1,z) == 1 for z in banned): return
        for z in (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97):
            if r != z and r%z == 0: return
        levels = []
        for p,m,c in zip(Q,powers,caps):
            if r%p == 1: v = val(f+1,p)
            elif pow(r,f+1,p) != 1: v = 0
            else: v = val((pow(r,f+1,m)-1)%m or m,p)
            if v > c: return
            levels.append(v)
        num = prod(p**(2*v) for p,v in zip(Q,levels)); den = r**f
        if num <= den or pow(2,r-1,r) != 1: return  # only a compositeness exclusion
        exceptions[r] = max(exceptions.get(r, ONE), Fraction(num,den))

    for f in range(2,2*n):
        if f%2 and (fixed_euler or f%4 != 1): continue
        opts = []
        for p,c in zip(Q,caps):
            shift = val(f+1,p); options = [(1,0,1)]
            if 0 < shift <= c: options.append((p,1,p**shift))
            for o in divisors(gcd(p-1,f+1)):
                if o == 1 or c <= shift: continue
                for j,zs in enumerate(lifts(p,o,c-shift),1):
                    m = p**j; options.extend((m,z,m*p**shift) for z in zs)
            opts.append(options)
        for combo in product(*opts):
            m,x,b = 1,0,1
            for v,y,power in combo:
                if v > 1: x += m*((y-x)*inverse(m%v,v)%v); m *= v
                b *= power
            limit = b*b
            while less(x,f,limit): charge(x,f); x += m

    fmax = 0
    while 3**(fmax+1) <= maxsize: fmax += 1
    h = 2*n
    for p,c in zip(Q,caps):
        for f in range(h,fmax+1):
            if f%2 and (fixed_euler or f%4 != 1): continue
            if 3**f >= p**(h*c): break
            shift = val(f+1,p)
            if 0 < shift <= c:
                x,limit = p+1,p**(h*shift)
                while less(x,f,limit): charge(x,f); x += p
            for o in divisors(gcd(f+1,p-1)):
                if o == 1 or c <= shift: continue
                for j,zs in enumerate(lifts(p,o,c-shift),1):
                    m = p**j; limit = p**(h*(j+shift))
                    if 3**f >= limit: continue
                    for x in zs:
                        while less(x,f,limit): charge(x,f); x += m
    charge.cache_clear()
    U = prod(exceptions.values(),start=ONE); V = X*M*M/U
    assert V > B, ('high Euler not excluded',P)
    if fixed_euler: return len(exceptions),[0,0,0]
    counts = [0,0,0]
    for levels in product(*(range(c+1) for c in caps)):
        m = prod(p**s for p,s in zip(Q,levels)); lo = 2*m-1
        if V*lo > B*m*m: counts[0] += 1; continue
        assert X*C*lo > B, ('exterior Euler window',P,levels)
        if lo > max(blocks): counts[1] += 1; continue
        for (p,_),block in zip(P,blocks):
            if block < lo or (p%4 == 3 and m%p == 0): continue
            mod = 4*m; u = (block*pow(lo,-1,mod))%mod or mod; hi = block//lo
            assert u > hi or ((hi-u)//mod <= 128 and all(block%k for k in range(u,hi+1,mod))), ('interior Euler window',P,levels)
        counts[2] += 1
    return len(exceptions),counts
