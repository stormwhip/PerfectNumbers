"""Exact uniform t-only prices, including the composite Euler-square atom."""
from fractions import Fraction
from math import gcd,prod,isqrt
from functools import cache
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'NightSevenForest/Release'));from PrimeCheck import level,prime64
T=751670559138758105956097;P=31;B=10**2400;tf=(13,17,31,37,409,1129,25085030513)
def primeT(c):
 q=T
 for row in c:assert row[0]==q;q=level(*row)
 assert prime64(q)
@cache
def bound(cap,w):
 assert T-1==256*prod(tf) and all(prime64(z) for z in tf) and T>8000 and 3**8000>B
 g=next(z for z in range(2,201) if all(pow(z,(T-1)//j,T)!=1 for j in (2,*tf)));orders=[1];out={}
 for x in tf:orders +=[k*x for k in orders]
 def add(r,o,m):
  if r<=2 or r%2==0:return
  h=o-1
  if r**h>=m**w:return
  # Conservative: keep extra composites, except when neither prime nor square could occur.
  def can(x):return x>=3 and x%2==1 and x not in (19,7,11,P,T) and pow(2,x-1,x)==1
  if can(r) or isqrt(r)**2==r and can(isqrt(r)):out[r]=max(out.get(r,1),Fraction(m**w,r**h))
 for o in sorted(orders)[1:]:
  if o>8000 or 3**(o-1)>=T**(cap*w):continue
  assert o-1>=w
  if o>=409:
   # For moderate o=409 and large cap this may be slower than root lifting; use direct enumeration ONLY for tiny thresholds.
   if 4096**(o-1)>=T**(cap*w):
    r=3
    while r**(o-1)<T**(cap*w):
     if pow(r,o,T)==1:add(r,o,gcd(pow(r,o,T**cap)-1,T**cap))
     r+=2
    continue
  root=pow(g,(T-1)//o,T);m=T
  for i in range(1,cap+1):
   r=1;bits=(m**w).bit_length()
   for j in range(1,o):
    r=(r*root)%m
    if gcd(j,o)==1 and r>=3 and r%2 and (r.bit_length()-1)*(o-1)<bits:add(r,o,m)
   m*=T;root=pow(root,T,m)
 L=prod(out.values(),start=Fraction(1));return -(-L.numerator//L.denominator),len(out)
if __name__=='__main__':
 for cap in (15,21):
  for w in (8,12):print(cap,w,bound(cap,w),flush=True)
