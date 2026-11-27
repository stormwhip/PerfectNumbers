"""Alternate mandatory D in the q^6 path: odd and high even exclusions."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Verify46 import prime,sig,dom,price,q,B,prod,Interior
from Disjoint import dj
from fractions import Fraction
from itertools import product
assert __debug__
D=1252106774386973;prime(D);assert sig(q,6)%D==0 and D%4==1
L=dom(6,D);assert len(L)==41
small=[3,11,17,31,97,769,1579,3907];assert sig(D,5)%(9*prod(small))==0 and sig(q,6)%(43*71)==0
for r in small+[43,71]:prime(r)
a=[(19,46),(3,4)]+[(r,2) for r in small[1:]+[43,71]]
assert prod(sig(p,f) for p,f in a)>2*prod(p**f for p,f in a)
closed=[]
for f in L:
 if f==5:closed.append(f);continue
 if f<9 or (not f%2 and f<36):continue
 P=[(19,46),(q,6),(D,f)]
 if f==9:
  V,_,_,_=price(P,[2,4,6]);assert V>B and f%4==1;closed.append(f);continue
 V,Q,(X,C,L0)=dj(P,[(q,4),(D,6)]);assert V>B
 if f%2:closed.append(f);continue
 u=Interior({})
 for (j,k) in product(range(Q[0][1]+1),range(Q[1][1]+1)):
  m=q**j*D**k;lo=2*m-1;top=B*q**(4*j)*D**(6*k)//V
  if lo>top:continue
  assert X*C*lo>B
  for i,((r,h),b) in enumerate(zip(P,L0)):
   if b>=lo:assert u(i,r,h,b,m,lo,top,(j,k))
 closed.append(f)
assert len(closed)==23 and set(L)-set(closed)=={1,*range(2,35,2)}
print('PASS q^6 alternate pivot: D-domain',len(L),'closed',closed,'remain',[1,*range(2,35,2)])
