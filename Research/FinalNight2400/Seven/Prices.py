"""Ordinary (including square-base Euler residual) price; geometric sums of odd length."""
from math import gcd,prod,isqrt
from fractions import Fraction
from functools import cache
from itertools import count
B=10**2400
@cache
def loss(t,c,n,d):
 assert c>=0 and n>0 and d>0
 # 3^5000 < B < 3^5100: no prime power exponent >=5100.
 assert 3**5100>B
 assert 3**(d*min(t-1,5100))>=t**n
 U={}; cap=t**(n*c)
 for o in range(3,5101,2):
  if (t-1)%o or 3**(d*(o-1))>=cap:continue
  assert d*(o-1)>=n
  if 10000**(d*(o-1))>=cap:
   for r in range(3,10000,2):
    if r**(d*(o-1))>=cap:break
    if r%t==1 or pow(r,o,t)!=1:continue
    # Including nonprimitive roots here is a safe relaxation for this order.
    mod=t**(c+1);A=(pow(r,o,mod)-1)%mod or mod;u=0
    while A%t==0 and u<c:u+=1;A//=t
    rat=Fraction(t**(n*u),r**(d*(o-1)))
    if rat>U.get(r,1):U[r]=rat
   continue
  primes=[p for p in range(2,o+1) if o%p==0 and all(p%k for k in range(2,isqrt(p)+1))]
  for g in count(2):
   x=pow(g,(t-1)//o,t)
   if x and all(pow(x,o//p,t)!=1 for p in primes):break
  roots=[pow(x,j,t) for j in range(1,o) if gcd(j,o)==1];m=1
  for u in range(1,c+1):
   m*=t; limit=m**n
   for r in roots:
    if r>=3 and r%2 and (r.bit_length()-1)*d*(o-1)<limit.bit_length():
     den=r**(d*(o-1))
     if den<limit:U[r]=max(U.get(r,1),Fraction(limit,den))
   if u<c:
    M=m*t; roots=[r+m*((-(pow(r,o,M)-1)//m*pow(o*pow(r,o-1,t),-1,t))%t) for r in roots]
 return prod(U.values(),start=Fraction(1))
