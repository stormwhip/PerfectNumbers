"""Prime source accounting for t^10, R=67 (shared odd order 3). Q7 weight2 and R weight2 cannot duplicate same order 3; use simultaneous CRT at order3. Discovery."""
from functools import cache
from math import gcd
from fractions import Fraction
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Odd42 import C,B
@cache
def cubic(p,depth):
 z=[x for x in range(2,p) if (x*x+x+1)%p==0];r=[];m=p
 for j in range(1,depth+1):
  r.append((m,z));M=m*p;z=[x+m*(-((x*x+x+1)//m)*pow(2*x+1,-1,p)%p) for x in z];m=M
 return r
@cache
def loss(cp,cr):
 # Join all simultaneous cubic lifting pairs to depth cp,cr. Price 7^u 67^v at weight 2; sparse exceptions with exponent2. No square exception needed if Euler q is already fixed and separated.
 best={}
 for m,rs in [(1,[0])]+cubic(7,cp):
  for n,rr in [(1,[0])]+cubic(67,cr):
   M=m*n
   if M==1:continue
   for x in rs:
    for y in rr:
     a=x+m*((y-x)*pow(m,-1,n)%n) if n>1 else x
     if a<=2 or a%2==0 or a in (7,19,67) or any(a%v==0 and a!=v for v in (3,5,7,11,13,17,19,23,29,31,37)):continue
     if pow(2,a-1,a)!=1:continue
     rat=Fraction(M*M,a*a);best[a]=max(best.get(a,1),rat)
 return best
