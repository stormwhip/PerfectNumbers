"""Exact disjoint auxiliary abundance price without a cutoff or high-weight shortcut."""
from Prices import *
from CleanPrice import price2
from Emitters import certificate
from Explore import CASES
from TwoSided import lower_euler
from Strengthen150 import verify
from fractions import Fraction as F

# For r≥T, a weighted abundance price may be impossible to reconcile with
# a scalar valuation loss approaching 1. Cope by integer margin test
# on *only* near-loss candidates r^h <= (T/(T−1))^lam * p^(2u).
@cache
def positive_tail(p,c,T,lam,X,D):
    lim=F(T,T-1)**lam;out={};hmax=0
    while 5**(hmax+1)<=B//X:hmax+=1
    assert p>hmax+1 and lim<2
    for o in divisors(p-1):
        if o==1 or o%2==0:continue
        h=o-1
        # The target supply disappears on r=1 mod p since length<p.
        if T**h>=lim*p**(2*c):continue
        depth=min(c,2+(B//X).bit_length()//(h*(p.bit_length()-1)))
        while depth<c and any(less(r,h,B//X+1) for r in root_levels(p,o,depth)[-1][-1]):depth=min(c,depth+2)
        for j,m,RR in root_levels(p,o,depth):
            # Weight 2 and factor <2 imply for r in a progression exactly
            # the least representative or its first translate: r<sqrt(2)*m<2m.
            Q=lim*p**(2*j);P=p**(2*j)
            for a in RR:
                for r in (a,a+m):
                    if r<T or r%2==0 or r in (3,1093,p) or any(r!=t and r%t==0 for t in SMALL):continue
                    if not less(r,h,(Q.numerator+Q.denominator-1)//Q.denominator):continue
                    if any(exact_supply(r,h,d,0)>0 for d in BAN):continue
                    if X*D*r**h//gcd(D,r**h)>B:continue
                    if pow(2,r-1,r)!=1:continue
                    v=F(r,r-1)**lam*P/r**h
                    if v>1:out[r]=max(out.get(r,F(1)),v)
    return out

def run():
    assert __debug__;rows=CASES['6-2-150'];R,f0,odd,X,S,D,_=certificate(rows);p=398581
    V,E=price2(rows,p);assert not E
    L=200;T=1000; c=f0[p]-vp(S,p);disc=F(1)
    for r in range(5,T,2):
        if r in f0 or r in BAN or not prime(r):continue
        v=F(1);b=F(r,r-1)**L;h=2;a=r*r
        while a<=B//(X*D) and a<b*p**(2*c):
            t=exact_supply(r,h,p,c)
            if t<=c and all(not exact_supply(r,h,d,0) for d in BAN):v=max(v,b*p**(2*t)/a)
            h+=2;a*=r*r
        disc*=v
    E=positive_tail(p,c,T,L,X,D);disc*=prod(E.values(),start=F(1))
    assert T*T>F(T,T-1)**L
    # Auxiliary abundance excludes only Euler and prefix (not A), to avoid
    # omitting A-support cost where it overlaps the valuation price. Fixed
    # abundancy is exactly S/X; for q≥lower threshold the residue ratio bounds.
    # All ordinary powers, including A-support, pay net price exactly once.
    C=[]
    for i,j,a,t in verify():
      if t not in ('internal Euler possible','exterior Euler open'):continue
      e=lower_euler(1093**i*p**j,a)
      ab=F(2*X,S)*F(e,e+1)
      if V*e*ab**L>B*p**(2*j)*disc:C.append((i,j,a))
    expected=[*((0,22,j) for j in range(6)),(0,23,5),*((1,22,j) for j in range(4)),*((1,23,j) for j in (0,2,3,4,5))]
    assert C==expected and not E,(C,len(E))
    print('additional priced abundance windows',len(C),C,'tail discounts',len(E),flush=True)
    return C
if __name__=='__main__':run()
