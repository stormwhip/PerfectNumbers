"""Optional stronger price-only leaf for five non-Fermat root classes; no rounding of size comparisons."""
from functools import cache
from fractions import Fraction
from math import gcd,prod
import sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parent/'EveningTree'));import IndependentTree as I
B=I.B
@cache
def bounded_price(p,k,z,m,bad):
    o=1
    while pow(z,o,p)!=1:o+=1
    if o%2==0:return z**m
    t=I.vp(z**o-1,p) if o>1 else 0;best=None;f=m
    while True:
        num=z**f
        if I.permissible(f,bad):
            v=t+I.vp(f+1,p) if not (f+1)%o else 0
            cost=Fraction(num,p**(k*v));best=cost if best is None else min(best,cost)
        if best is not None and f>=k and num>=best*p**(k*t)*(f+1)**k:return max(1,best)
        f+=2
class PriceTree(I.Proof):
    def visit(self,parts,X,S,ban):self.current=parts;return super().visit(parts,X,S,ban)
    def valuation_close(self,X,S,U,base,parts,used):
        if super().valuation_close(X,S,U,base,parts,used):return True
        p,e=self.p,self.e;k,loss,dh=I.global_discounts(p,e);need=e-I.vp(S,p)
        if need<0:return True
        price={z:bounded_price(p,k,z,m,bad) for z,(c,m,o,bad) in parts.items()};V=Fraction(X*p**(k*need)*prod(price.values()),loss)
        if used:return V>B
        if V<=B*dh:return False # Euler outside known supports at high exponent
        for z,(c,m,o,bad) in parts.items():
            if o is None:continue
            f=o;w=z**f
            while base*w<=B*z**m:
                if I.permissible(f,bad):
                    b=I.vp(I.sigma(z,f),p)
                    if b<=need and V*w<=B*p**(k*b)*price[z]:return False
                f+=4;w*=z**4
        for s in range(need+1):
            y=p**s;lo=max(5,2*y-1);hi=B*y**k//V
            if lo>hi:continue
            if base*lo<=B:return False # exterior q remains
            if base>B:continue
            # q|U and U|sigma(X). At least one assigned sigma must contain q. Distinguish previous-root reciprocity.
            for z,f in self.current:
                if z==p and p%4==3 and f%2==0 and s:continue
                c=gcd(U,I.sigma(z,f));top=min(c,hi)
                if top<lo:continue
                minimum=(c+top-1)//top;res=minimum+(-c-minimum)%y
                if res>c//lo:continue
                first=lo+(2*y-1-lo)%(4*y) if s else lo+(1-lo)%4;step=4*y if s else 4
                if top-first>=20*step:return False
                if any(c%q==0 for q in range(first,top+1,step)):return False
        return True
