"""Price the remaining exact first exponent 42 of (13,310), without factoring any sigma block."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from PriceThree import prime64
from math import gcd,isqrt,prod
from fractions import Fraction
from functools import cache
p,t,E,f=13,5424477432443,310,42; B=10**2400;X=p**E*t**f; A=(p**(E+1)-1)//(p-1)//t; C=(t**(f+1)-1)//(t-1);D=A*C;H=max(A,C);cap=f-1;W=10
@cache
def viable(r):
 def prime_candidate(z):return z>=3 and z%2 and z not in (p,t,7,11,19,31) and pow(2,z-1,z)==1
 return prime_candidate(r) or (isqrt(r)**2==r and prime_candidate(isqrt(r)))
def loss(s,orders,cap,w):
 fac=[a for a in (2,3,31,179,311,787,1997) if (s-1)%a==0];g=next(a for a in range(2,200) if all(pow(a,(s-1)//q,s)!=1 for q in fac));out={}
 assert all(prime64(q) for q in [s,*fac]);assert 3**(min(s-1,8000))>=s**w
 for o in orders:
  if o>8000 or 3**(o-1)>=s**(w*cap):continue
  h=o-1
  if o>=1997:
   limit=s**(w*cap);r=3
   while r**h<limit:
    if pow(r,o,s)==1:
     M=gcd(pow(r,o,s**cap)-1,s**cap);n=r**h
     if n<M**w and n//gcd(n,D)<=B//(X*D) and viable(r):out[r]=max(out.get(r,1),Fraction(M**w,n))
    r+=2
   continue
  gen=pow(g,(s-1)//o,s); roots=[pow(gen,j,s) for j in range(1,o) if gcd(o,j)==1];m=1
  for _ in range(cap):
   m*=s
   for r in roots:
    if r<3 or not r%2 or (r.bit_length()-1)*h>=(m**w).bit_length():continue
    n=r**h
    if n<m**w and n//gcd(n,D)<=B//(X*D) and viable(r):out[r]=max(out.get(r,1),Fraction(m**w,n))
   roots=[r+m*((-((pow(r,o,m*s)-1)//m)*pow(o*pow(r,o-1,s),-1,s))%s) for r in roots]
 return prod(out.values(),start=Fraction(1)),len(out)
def main():
 assert __debug__ and t-1==2*31*179*311*787*1997 and (p-1)==12 and gcd(p*(p-1)//4,t*(t-1)//2)==1 and 3**8000>B and t>8000
 assert (p**(E+1)-1)//(p-1)==t*A and gcd(D,X)==gcd(A,C)==1
 ot=[1]
 for z in (31,179,311,787,1997):ot +=[a*z for a in ot]
 U,n=loss(p,[3],E,2);V,k=loss(t,ot[1:],cap,W);U*=V;u=(U.numerator+U.denominator-1)//U.denominator
 def outside(Z,m,q):
  if Z<q:return True
  if Z//q>=4*m:return False
  a=Z*pow(q,-1,4*m)%(4*m);return not 0<a<=Z//q or Z%a!=0
 stat=[0,0,0];missing=[]
 for i in range(E+1):
  for j in range(f):
   m=p**i*t**j;q=2*m-1;R=p**(2*(E-i))*t**(W*(cap-j));
   if X*q*R>B*u:stat[0]+=1;continue
   if not (outside(A,m,q) and outside(C,m,q)):missing.append((i,j,'external'));continue
   if X*D*q>B:stat[1]+=1;continue
   for v in range(cap-j+1):
    a=p**(E-i);lim=(3*B*H)//(2*X*D*q*q*t**v)
    if not lim:continue
    # If size bound did not already close the emitter, p^u<=lim. The remaining atom bound decreases with p^u; test its largest allowed upper bound.
    if 2*X*q*q*R<=3*B*u*t**((W-1)*v)*min(a,lim):missing.append((i,j,'supplier'));break
   else:stat[2]+=1
 print('W',W,'U',u,'loss labels',n,k,'price/mandatory/supplier',stat,'unresolved',len(missing),missing[:10],flush=True);assert not missing
if __name__=='__main__':main()
