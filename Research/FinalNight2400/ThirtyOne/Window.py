"""Exact t-only window test, conservative external-emitter credits. Ordinary-only prefix."""
from AtomPrice import *
from math import prod
from functools import cache
import json
O=H.parent/'Others';sys.path.insert(0,str(H.parents[1]/'Session20261126'));from PivotCheck import C,floor10
F=22; fp=H/'Windows22.json';sig=C.sigma;val=C.valuation
@cache
def capcredit(z,c):
 # Returns min size/price; size>=B fixed B-only tail irrelevant. s is odd order in admissible h+1.
 assert prime64(z) if z<2**64 else True
 o=1;v0=0
 if z%T!=1:
  possible=sorted([prod(tf[i] for i in range(len(tf)) if mask>>i&1) for mask in range(1,2**len(tf))]);o=next((o for o in possible if o<=8000 and pow(z,o,T)==1),0)
  if o:v0=val(z**o-1,T)
 best=None;h=c+c%2;y=z**h;mx=0
 while y<=B:
  u=v0 if o and (h+1)%o==0 else 0;mx=max(mx,u);n=Fraction(y,T**(12*u));best=n if best is None else min(best,n)
  h+=2;y*=z*z
 return best,mx

def ext(Z,m):
 q=2*m-1
 if q>Z:return True
 mx=Z//q
 if mx>=4*m:return False
 k=Z*pow(q,-1,4*m)%(4*m);return k==0 or k>mx or Z%k!=0

def status(row,labels):
 s=C.State(row);assert not s.fixed_euler and not s.conflict
 fixed=s.rows;em=[sig(z,h) for z,h in row];c=fixed[T]-sum(val(a,T) for a in em);U,n=bound(c,12);assert U==1
 X=s.X;D=s.D;fs0={z for z in labels if z not in fixed and D%z==0};gs=[];r=D
 for z in fs0:
  v=val(r,z);r//=z**v;gs.append(z**v)
 # split anonymous parts by input rows; pairwise blocks may share primes, use coprime basis refinement.
 blocks=[C.nonsupport(a,prod(fixed)*prod(fs0)) for a in em]; blocks=[z for z in blocks if z>1];ex={}
 while blocks:
  a=blocks.pop();hit=next(((b,gcd(a,b)) for b in blocks if gcd(a,b)>1 and a!=b),None)
  if hit:
   b,g=hit;blocks.remove(b);blocks.extend(z for z in [g,a//g,g,b//g] if z>1);continue
  # Must split earlier extracted blocks as well if input shared only partially.
  ex[a]=ex.get(a,0)+1
 gs+= [a**k for a,k in ex.items()];assert prod(gs)==D and all(gcd(a,b)==1 for i,a in enumerate(gs) for b in gs[i+1:]);unknown=max((a**k for a,k in ex.items()),default=1)
 miss=[]
 for j in range(c+1):
  m=T**j;q=2*m-1;R=T**(12*(c-j));
  if X*q*R>B:continue
  # If the true Euler base is any forced certified z, its j is known. Otherwise all fs are ordinary; q itself can be internal to unnamed parts.
  if any(z%4==1 and val(z+1,T)==j for z in fs0):miss.append((j,'knownEuler'));continue
  G=Fraction(1);F=1;maxu=0
  for z in fs0:
   v=val(D,z);a,k=capcredit(z,v);G*=a;F*=z**(v%2);maxu=max(maxu,k)
  if X*q*R*G>B:continue
  if not all(ext(a,m) for a in em):miss.append((j,'interior'));continue
  if X*D*F*q>B:continue
  for u in range(c-j+1):
   y=T**u;outsideKnown=u>maxu
   # if source known check its own row h is possibly large enough to supply q; relax by discarding its particular credits
   if not outsideKnown:
    bad=False
    for z in fs0:
     a,k=capcredit(z,val(D,z));
     if k<u:continue
     if 2*X*q*q*R*(G/a)>3*B*T**(11*u):continue
     # New size without double charging emitter z, retaining all other forced multiplicities.
     if 2*X*D*F*q*q*y>3*B*z**(val(D,z)+val(D,z)%2):continue
     bad=True;break
    if bad:miss.append((j,'knownSupplier',u));break
   if X*D*F*q*T**(12*u)>B*unknown or 2*X*q*q*R*G>3*B*T**(11*u) or 2*X*D*F*q*q*y>3*B*unknown:continue
   miss.append((j,'emitter',u));break
 return miss
