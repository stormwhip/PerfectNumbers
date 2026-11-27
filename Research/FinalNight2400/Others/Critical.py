"""Joint order three exact-size losses with global prefix net-budget amortization."""
from PriceThree import *
from math import isqrt,log10
X=P**E*T**F;M=X//T;A=(P**(E+1)-1)//(P-1)//T; C=(T**(F+1)-1)//(T-1);D=A*C;budget=B//(X*D)
@cache
def primal(r):
 if r<3 or not r%2 or r in (P,T,7,19,31,11):return False
 # If a prime divisible by one small label, it equals that label. Composite Fermat failures are never primes.
 if any(r%d==0 and r!=d for d in (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)):return False
 return pow(2,r-1,r)==1

def get():
 loss={};high={}
 def charge(store,r,m,h):
  if r<3 or not r%2 or r**h>=m*m:return
  # This r^(h) divides the true component, even for the square Euler atom. gcd(r^h,D) can only reduce the forced net expenditure. If square Euler base, its underlying prime must remain admissible.
  power=r**h;net=power//gcd(power,D)
  if net>budget:return
  if not primal(r):
   y=isqrt(r)
   if y*y!=r or not primal(y):return
  v=Fraction(m*m,power);store[r]=max(store.get(r,1),v)
 for b,bb in roots(T,F-1):
  inv=1;ip=pow(P,-1,b)
  for a,aa in roots(P,E):
   m=a*b
   for x in aa:
    for y in bb:
     r=x+a*((y-x)*inv%b);charge(loss,r,m,2)
   inv=inv*ip%b
 for o in (263,401,789,877,1203,2631):
  h=o-3
  if 3**min(h,8000)>=T**(2*(F-1)):continue
  r=3
  while r**h<T**(2*(F-1)):
   if pow(r,o,T)==1:charge(high,r,gcd(pow(r,o,T**(F-1))-1,T**(F-1)),h)
   r+=2
 assert not high,high
 return loss
if __name__=='__main__':
 u=get();print('exceptions',len(u),'logprod',sum(log10(v.numerator)-log10(v.denominator) for v in u.values()),'logmax',max(log10(v.numerator)-log10(v.denominator) for v in u.values()));import json;from pathlib import Path;(Path(__file__).resolve().parent/'CriticalLoss.json').write_text(json.dumps([[r,v.numerator,v.denominator] for r,v in u.items()]));print(sorted([(round(log10(v.numerator)-log10(v.denominator),2),round(log10(r),2)) for r,v in u.items()],reverse=True)[:20]);
