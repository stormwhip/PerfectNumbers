"""Compulsory ordinary-credit joint price at Q^42 when 173 is Euler. Standalone, no other candidate code imported."""
from pathlib import Path
from math import gcd,isqrt,prod
from functools import cache
from fractions import Fraction
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Session20261126'));from PivotCheck import C,B
Q=16148168401;p=7;R=173
@cache
def cost(t,c,w,joint=False,squares=False):
 """Rational weights w (integer); odd length; all actual suppliers here primes, Euler fixed."""
 loss={};assert 3**5100>B and (2*t+1)**min(t-1,5100)>t**w and 3**(3*min(t-1,5100))>t**w
 for o in range(3,5101,2):
  if (t-1)%o:continue
  bgt=(40 if t==R else o-1-40) if joint and o%43==0 else o-1
  if 3**bgt>=t**(w*c):continue
  assert bgt>=w
  def update(r,b):
   if r<3 or r%2==0 or r in (7,Q,R,19):return
   sq=isqrt(r);is_sq=squares and sq*sq==r and sq%4==1 and sq not in (7,Q,R,19)
   if any(r%j==0 and r!=j and not(is_sq and sq==j) for j in [3,5,7,11,13,17,19,23,29,31,37]):return
   if pow(2,r-1,r)!=1 and not(is_sq and pow(2,sq-1,sq)==1):return
   n=t**(w*b)
   if (r.bit_length()-1)*bgt<n.bit_length() and r**bgt<n:loss[r]=max(loss.get(r,1),Fraction(n,r**bgt))
  if 5000**bgt>=t**(w*c):
   for r in range(3,5000,2):
    if r**bgt>=t**(w*c):break
    if r%t!=1 and pow(r,o,t)==1:
     n=(pow(r,o,t**(c+1))-1)%t**(c+1) or t**(c+1);u=0
     while n%t==0:u+=1;n//=t
     update(r,min(c,u))
   continue
  primes=[k for k in range(2,o+1) if o%k==0 and all(k%i for i in range(2,isqrt(k)+1))];g=2
  while True:
   a=pow(g,(t-1)//o,t)
   if a and all(pow(a,o//k,t)!=1 for k in primes):break
   g+=1
  rr=[pow(a,i,t) for i in range(1,o) if gcd(i,o)==1];m=1
  for b in range(1,c+1):
   m*=t
   for r in rr:update(r,b)
   if b<c:rr=[r+m*(-((pow(r,o,m*t)-1)//m)*pow(o*pow(r,o-1,t),-1,t)%t) for r in rr]
 return prod(loss.values(),start=Fraction(1))
def val(n,t):
 assert n>0;k=0
 while n%t==0:k+=1;n//=t
 return k
@cache
def net(r,t,w):
 e=2;z=r*r;best=None
 while z<=B:
  if r%t==1:u=val(e+1,t)
  else:u=val(pow(r,e+1,t**85)-1,t) if pow(r,e+1,t)==1 and pow(r,e+1,t**85)!=1 else (85 if pow(r,e+1,t**85)==1 else 0)
  v=Fraction(z,t**(w*u));best=v if best is None else min(best,v);z*=r*r;e+=2
 return best
if __name__=='__main__':
 from sympy import factorint,isprime
 for h in [1,5,9,13,21,25,29,33,37,41]:
  D=C.State([(7,12),(Q,42),(R,h)]);F={43}|set(factorint(C.sig_odd(R,h),limit=50000));F={p for p in F if p not in D.rows and p<2**64 and C.pc.prime64(p)}
  # Q-1 and 173-1 share order-43, cannot multiply single prices without handling this order.
  for t,w in [(R,38),(Q,2)]:
   c=D.rows[t]-val(D.S,t);U=cost(t,c,w);G=prod((net(r,t,w) for r in F),start=Fraction(1)); bound=D.X*t**(w*c)*G/U; print(h,t,'price', d0:=len(str(bound.numerator))-len(str(bound.denominator)), 'close',bound>B,flush=True)
