#!/usr/bin/env python3
"""Independent fast exact common-price loss table at 31 and 3229."""
from fractions import Fraction
from math import gcd, isqrt, prod
from itertools import product


def priced_atoms(V, rows, a, d):
    B=V['B']; roots=V['roots']; X,Y,D,_,ok=V['state'](rows)
    assert ok and 0<a<=2*d and 3**5030<=B<3**5031
    s,t=[p for p,h in rows]
    assert (s,t)==(31,3229) and (s-1,t-1)==(30,4*3*269)
    assert V['prime_small'](269) and all(3**(d*(p-1))>=p**a for p in (s,t))
    o1,o2=(3,5,15),(3,269,807)
    assert all(gcd(x*y,s*t)==1 for x,y in product(o1,o2))
    assert all((2 if 3 in (x,y) else 0)+(x-3 if x>3 else 0)+(y-3 if y>3 else 0)<=x*y//gcd(x,y)-1 for x,y in product(o1,o2))
    caps=[f-V['valuation'](Y,p) for p,f in rows]; assert min(caps)>=0
    # Remaining size given compulsory outputs, applied only to actual
    # atoms. Ordinary bases and the special square are treated separately.
    size=B//(X*D); maxb=B//X
    fixed={p for p,h in rows}|set(V['BANNED'])
    small=(3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)
    tables=[{}, {}, {}]

    def add(tab,b,m,k):
        if b<3 or b%2==0 or b in fixed or k*(b.bit_length()-1)>=a*m.bit_length() or b*b>maxb:return
        r=isqrt(b)
        if r*r==b:
            if r%4!=1 or r in fixed:return
        else:r=b
        if any(r!=q and r%q==0 for q in small):return
        # A base atom exponent k/d is a proved allocation; the actual
        # power is divisible by this prefix. Checking the divided size
        # is sound even when the Euler square's underlying prime is in D.
        bb=b**(k//d)
        if bb//gcd(bb,D)>size:return
        nn=m**a; dd=b**k
        if dd>=nn:return
        # Do NOT reject anything probabilistically. The Fermat step is a
        # one-way compositeness test and is unnecessary above 512 bits.
        if r.bit_length()<=512 and any(pow(q,r-1,r)!=1 for q in (2,3,5,7,11) if q<r):return
        tab[b]=max(tab.get(b,1),Fraction(nn,dd))

    for n,bb in roots(t,3,caps[1]):
        step=pow(s,-1,n); inv=1
        for m,aa in roots(s,3,caps[0]):
            v=m*n
            for r,u in product(aa,bb):
                z=r+m*((u-r)*inv%n)
                add(tables[0],z,v,2*d)
            inv=inv*step%n
    for j,(p,os) in enumerate(((s,o1),(t,o2)),1):
        for k in os[1:]:
            h=k-3
            if 3**(h*d)>=p**(a*caps[j-1]):continue
            for m,rr in roots(p,k,caps[j-1])[1:]:
                for r in rr:add(tables[j],r,m,h*d)
    # Upward rounding, with no denominator cancellation overhead.
    scale=10**8
    cover=scale
    for tab in tables:
        for val in tab.values():cover=-(-(cover*val.numerator)//val.denominator)
    return -(-cover//scale),caps,[len(tab) for tab in tables]
