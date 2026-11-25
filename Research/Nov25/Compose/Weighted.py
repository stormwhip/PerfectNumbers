"""Outward-log abundance surcharge on an exact-prefix static private forest."""
from functools import cache
from math import gcd,prod
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Compose import euler,need,nonsupport,permitted,sig_odd,sigma,valuation
from Terminal import SCALE,log_bounds,odd_primes


def ceildiv(a,b):return -(-a//b)


def weighted(s,roots,owners,head,mu,logs=log_bounds):
    """Price logs by ln(N)-mu ln(sigma(N)/N), then add mu ln(2)."""
    need(type(mu)==int and 0<=mu<=1000000,'abundance multiplier')
    T=5001
    U=prod(s.rows)
    extra=set(s.present)-set(roots)-s.rows.keys()
    V=set(roots)|owners.keys()
    small=(set(odd_primes(T-1))|V|extra)-set(s.rows)-set(s.bad)
    kids={q:[] for q in V}
    for q,z in owners.items():kids[z].append(q)
    U*=prod(small)
    D=nonsupport(s.D,U)
    # Fixed components and exact outgoing rough prime powers outside all
    # explicit and negative-price primes have disjoint support. Extra powers
    # at a prime already in D can be charged through sigma multiplicity.
    @cache
    def hi(q):return logs(q,q-1)[1]
    @cache
    def lo(q):return logs(q)[0]
    # For r>=T, the abundance share is <=(ln(r)/ln(T))*ln(T/(T-1)).
    # Discount all rough mass by this rigorous worst price ratio.
    beta=ceildiv(mu*hi(T)*SCALE,lo(T));need(beta<=SCALE,'rough price becomes negative')
    @cache
    def rough(C):return (SCALE-beta)*lo(C)//SCALE
    @cache
    def f0(q,sp):
        step=4 if sp else 2;f=1 if sp else 2
        while not permitted(q,f,s.bad):f+=step
        return f
    @cache
    def offset(q):return max(0,mu*hi(q)-f0(q,False)*lo(q))
    # A single Euler coupon may be spent at a tracked prime or an external
    # known small base. Generic outside primes already have nonnegative cost
    # even at exponent one, so cannot need an additional coupon.
    coupons={q:max(0,mu*hi(q)-f0(q,True)*lo(q)-offset(q)) for q in small if not s.fixed_euler and euler(q,s.bad)}
    external=max(coupons.values(),default=0); all_coupon=external
    start=lo(s.X)+rough(D)+mu*(lo(2)-sum(logs(sigma(q,f),q**f)[1] for q,f in s.rows.items()))-sum(offset(q) for q in small)
    # The exact D includes untracked small explicit primes. Recover their
    # mandatory extra price separately, using translated minimum exponents.
    for q in (small-V):
        v=valuation(s.D,q)
        if v and (s.fixed_euler or not euler(q,s.bad)):
            start+=max(0,v*lo(q)-mu*hi(q)+offset(q))
    for q in V-set(roots):
        need(s.D%q,'multiply charged residual')
    @cache
    def node(q,h,m):
        if m==1:
            return min(node(q,h,3),node(q,h,2)) if euler(q,s.bad) else node(q,h,3)
        sp=m==2;step=4 if sp else 2
        f=h+((1-h)%4 if sp else h%2)
        def bare(f):return f*lo(q)-mu*hi(q)+offset(q)
        # Some special prices may be negative: avoid size-based early cutoff
        # unless the whole descendant calculation, including Euler credit, is
        # considered. All ordinary prices are nonnegative.
        b=10**30;n=0
        while n<head:
            if bare(f)-(all_coupon if m==3 else 0)>=b:
                break
            if permitted(q,f,s.bad):
                n+=1
                C=sig_odd(q,f); v=bare(f)+rough(nonsupport(C,U)); save=0
                for r in kids[q]:
                    a=valuation(C,r)
                    if a:
                        z=node(r,a,0); v+=z
                        if m==3:save=max(save,z-node(r,a,1))
                b=min(b,v-save)
            f+=step
        while not permitted(q,f,s.bad):f+=step
        return min(b,bare(f)-(all_coupon if m==3 else 0))
    c={q:max(1,valuation(s.D,q),s.lo.get(q,0)) for q in roots}
    full={q:node(q,h,0) for q,h in c.items()}
    total=start+sum(full.values())
    if s.fixed_euler:return total
    discount=max([external]+[full[q]-node(q,h,1) for q,h in c.items()])
    return total-discount
