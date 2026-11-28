"""Exhaustive, non-binary-search audit of the final supplier step in Explore."""
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Dual'))
import Explore as e
from functools import cache
from math import gcd
p,t,B=e.P,e.T,e.B; A=e.sigma(p,432)//t; C=e.sigma(t,18); X=p**432*t**18;D=A*C
assert e.trial(p) and all(e.trial(z) for z in e.TF) and t-1==8*11*101*433*3077160600929
e.gen(t,[2,*e.TF]);assert gcd(D,X)==gcd(A,C)==gcd(C,19*(t-1))==1
U=p**21*e.deficit(p,432,2)*e.deficit(t,17,9); a,b=U.numerator,U.denominator
@cache
def overlap(u):
 if u<=2:return max(A,C)
 m=19**(u-2); possible=[1]
 for Z in (A,C):
  if m*m<=Z:possible.append(Z);continue
  for R in e.roots19(u-2):
   k=(Z*pow(R,-1,m))%m
   if (R%2 and Z%R==0) or (0<k<=Z//m and Z%k==0):possible.append(Z);break
 return max(possible)
@cache
def ext(Z,m):
 q=2*m-1
 if q>Z:return True
 mod=4*m; k=Z*pow(q,-1,mod)%mod
 return Z//q<mod and not(0<k<=Z//q and Z%k==0)
count=[0,0,0]; pairs=0
for j in range(18):
 for i in range(433):
  m=p**i*t**j;q=2*m-1; left=X*q*p**(2*(432-i))*b
  if left*t**(9*(17-j))>B*a:count[0]+=1;continue
  assert (i or ext(A,m)) and ext(C,m)
  if X*D*q>B or left**8*C**7>(B*a)**8:count[1]+=1;continue
  for v in range(18-j):
   h=2*X*q*q*t**v;tp=t**(9*(17-j-v));
   for u in range(433-i):
    pairs+=1
    if h*D*p**u>3*B*overlap(u):continue
    z=h*p**(2*(432-i)-u)*b
    if z*tp>3*B*a:continue
    assert u>2 and z**8*C**7>(3*B*a)**8,(i,j,u,v)
  count[2]+=1
assert count==[6447,985,362];print('exhaustive allocation counts',count,'u,v comparisons',pairs)
