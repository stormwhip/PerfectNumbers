"""Disjoint odd order budget, shared square-Euler atom lemma from Batch."""
from pathlib import Path
import sys
from math import gcd,isqrt,prod
from fractions import Fraction
from functools import cache
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path.insert(0,str(R/'FinalNight2400/Ten'));from Weighted import lifts,less,val,B
@cache
def loss(p,c,w):
 # All odd atom exponents h+1 <= bit length bound: b^h<=B, b>=3.
 esc={}
 def put(b,o,z):
  if b<3 or not b%2:return
  if any(b%k==0 and b not in (k,k*k) for k in (3,5,7,11,13,17,19,23,29,31,37)):return
  if not less(b,o-1,p**(w*z)):return
  s=isqrt(b)
  if pow(2,b-1,b)!=1 and not (s*s==b and s%4==1 and pow(2,s-1,s)==1):return
  esc[b]=max(esc.get(b,1),Fraction(p**(w*z),b**(o-1)))
 for o in range(3,B.bit_length()+2,2):
  if (p-1)%o or not less(3,o-1,p**(w*c)):continue
  assert o-1>=w
  if not less(1000,o-1,p**(w*c)):
   for b in range(3,1000,2):
    if pow(b,o,p)!=1:continue
    z=val(gcd(pow(b,o,p**c)-1,p**c),p) if pow(b,o,p**c)!=1 else c
    put(b,o,z)
   continue
  for z,rs in enumerate(lifts(p,o,c),1):
   for b in rs:put(b,o,z)
 return prod(esc.values(),start=Fraction(1))
def dj(P,targets):
 X=prod(p**e for p,e in P);zs=[(p**(e+1)-1)//(p-1)//(1+e%2) for p,e in P];S=prod(zs);C=S//gcd(S,X);assert gcd(X,C)==1
 L=[z//gcd(z,X) for z in zs];assert prod(L)==C
 Q=[(p,dict(P)[p]-val(S,p),w) for p,w in targets];used=1;U=1
 for p,c,w in Q:
  d=(p-1)*p
  while d%2==0:d//=2
  assert gcd(d,used)==1
  # 3^(p-1) >= 2^(p-1) > p^w suffices for the LTE shift.
  assert (3**(p-1)>=p**w) if p<10000 else (p-1>=w*p.bit_length())
  used*=d;U*=loss(p,c,w)
 return Fraction(X*prod(p**(c*w) for p,c,w in Q),1)/U,Q,(X,C,L)
