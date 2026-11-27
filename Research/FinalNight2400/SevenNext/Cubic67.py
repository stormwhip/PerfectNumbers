"""Relaxed complete 19/10 price for 7 and 67, both sharing order3; separate handling of orders 11,33."""
from fractions import Fraction
from pathlib import Path
from math import gcd,prod
import sys,time
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Mixed7 import cubic,C,B
p=7;r=67;t=572749682520506652634407616247
# A subset of primes known composite may be rejected with small integer gcd before expensive Fermat.
SM=prod(q for q in range(3,2001,2) if C.pc.prime64(q));BAN={7,19,r,t}
def cheap(y,limit,h):
 if y<=2 or y%2==0 or y in BAN:return False
 if (y.bit_length()-1)*h>=limit.bit_length():return False
 if y**h>=limit:return False
 return (y<=2000 or gcd(y,SM)==1) and pow(2,y-1,y)==1

def loss(cp=438,cr=300):
 U={};P=[(1,[0])]+cubic(p,cp);R=[(1,[0])]+cubic(r,cr)
 for a,rs in P:
  for b,ss in R:
   m=a*b
   if m==1:continue
   lim=m**19; inv=pow(a,-1,b) if b>1 else 0
   for x in rs:
    for z in ss:
     y=x+a*((z-x)*inv%b) if b>1 else x
     if cheap(y,lim,20):U[y]=max(U.get(y,1),Fraction(lim,y**20))
 # positive order 11 /33 at 67: reserve 2 powers of the base for a simultaneous 7 order of 3; for order 11, minimal mixed length 33 gives extra budget. For nonmixed simply relaxing to exponent 8 or 30 is safe. Take per-67 isolated losses for these orders plus *marginal* 7 losses already present above (a nonmixed zero 67 coordinate row contributes a max loss in U).
 V={}
 for o in (11,33):
  g=o-1-2;gen=next(x for x in range(2,r) if pow(x,o,r)==1 and all(pow(x,o//d,r)!=1 for d in [3,11] if o%d==0));rr=[pow(gen,j,r) for j in range(1,o) if gcd(o,j)==1];b=1
  for j in range(1,cr+1):
   b*=r;lim=b**19
   for y in rr:
    if cheap(y,lim,g*10):V[y]=max(V.get(y,1),Fraction(lim,y**(g*10)))
   rr=[y+b*((-(pow(y,o,b*r)-1)//b*pow(o*pow(y,o-1,r),-1,r))%r) for y in rr]
 return prod(U.values(),start=Fraction(1))*prod(V.values(),start=Fraction(1))
if __name__=='__main__':
 u=loss();print('loss bits',u.numerator.bit_length()-u.denominator.bit_length(),flush=True)
