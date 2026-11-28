#!/usr/bin/env python3
"""Exact additional uniform price at the compulsory cofactor prime ℓ."""
from functools import cache
from math import gcd, isqrt

R = 44119464395283956806299428681
B = 10**2400
BASE = ((19,276),(1176672733,1),(1109,2),(13,276))
X0 = 19**276 * 1176672733 * 1109**2 * 13**276
ORDERS = (5,71,277,355,1385,2287)
IN_RANGE_277 = (13,169,2197,28561,371293)


def need(value, why):
    if not value:
        raise ValueError(why)


def prime_trial(n):
    return n==2 or n>=3 and n%2 and all(n%d for d in range(3,isqrt(n)+1,2))


def vp(n,p):
    need(n>0,'positive input valuation')
    v=0
    while n%p==0:
        n//=p;v+=1
    return v


def sigma(b,f):
    return (b**(f+1)-1)//(b-1)


def is_prime_R():
    fac=(15539196401,1578110473)
    F=fac[0]*fac[1]
    need(all(prime_trial(q) for q in fac) and (R-1)%F==0 and F*F>R,'Pocklington factors at ℓ')
    need(pow(2,R-1,R)==1 and all(gcd(pow(2,(R-1)//q,R)-1,R)==1 for q in fac),'Pocklington witnesses at ℓ')


def first_roots(o):
    ds=[d for d in range(1,o) if o%d==0]
    for a in range(2,100):
        g=pow(a,(R-1)//o,R)
        if pow(g,o,R)==1 and all(pow(g,d,R)!=1 for d in ds):
            break
    else:
        raise ValueError('no verified generator')
    # At a prime modulus all o roots are powers of this element of exact
    # order o; keep precisely the primitive ones with gcd(i,o)=1.
    return [pow(g,i,R) for i in range(1,o) if gcd(i,o)==1]


def odd_min(r,m):
    m0=r if r%2 else r+m
    return m0 if m0>=3 else m0+2*m


def liftnext(rr,m,o):
    m1=m*R
    out=[]
    for r in rr:
        n=pow(r,o,m1)-1
        need(n%m==0,'root before lifting')
        v=r+m*((-(n//m)*pow(o*pow(r,o-1,R),-1,R))%R)
        need(0<v<m1 and pow(v,o,m1)==1,'exact lift')
        out.append(v)
    return out


@cache
def uniform_rare():
    """True => r's allocated rare effective exponent pays ℓ^(77*z/20).

    Valid on any ordinary unknown prime in the EXACT prefix BASE+ℓ^h,
    h even >=2, all ordinary lengths <=5031. Only order 5 is feasible;
    capped Hensel tails are strict independently of the demand h-1.
    """
    is_prime_R()
    need(all(prime_trial(q) for q in (13,19,1109,1176672733)), 'baseline prime')
    need(1176672733%4==1 and 3**5030<=B<3**5031 and R>5031, 'Euler/length cap')
    need([o for o in range(3,5032,2) if (R-1)%o==0]==list(ORDERS), 'complete odd orders')
    need(gcd(19*13*9,R*(R-1))==1,'disjoint effective supports')
    X=X0*R**2
    for o in ORDERS:
        rr=first_roots(o)
        if o!=5:
            if o in (71,355,1385,2287):
                # Conservative min across all primitive roots and all odd shifts.
                low=min(odd_min(r,R) for r in rr)
                need(X*low**(o-1)>B, ('nonempty high order',o))
            else:
                need(o==277 and X*R**276>B, 'order277 at most least odd representative')
                got=tuple(sorted(b for r in rr if X*(b:=odd_min(r,R))**276<=B))
                need(got==IN_RANGE_277 and all(b==13 or b%13==0 for b in got),'order277 actual bases')
            continue
        m=R
        # Tail proof: min odd representatives at the final depth already
        # exceed (B/X)^(1/4), so deeper lifts cannot re-enter that range.
        for z in range(1,20):
            low=min(odd_min(r,m) for r in rr)
            if X*low**4>B:
                break
            need(low**80>=R**(77*z), ('positive order-five loss',z))
            rr=liftnext(rr,m,5);m*=R
        else:
            raise ValueError('no proven order-five tail')
        need(z<=17,'unexpectedly deep tail')
    return True


def rare_supply(b,f):
    """Exact valuation of sigma(b^f) at ℓ for positive f."""
    return vp(sigma(b,f),R)


def rare_cost20(demand):
    need(demand>=0,'negative remaining rare demand')
    return R**(77*demand)


if __name__=='__main__':
    need(uniform_rare(),'failed rare price table')
    print('PASS r=44119464395283956806299428681, only ordinary order 5, weight 77/20, zero deficit')
