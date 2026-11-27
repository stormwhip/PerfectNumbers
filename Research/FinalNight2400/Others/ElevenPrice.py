"""Square-price exclusion for the canonical 11^358 residual f=28 or f=30.
The verifier certifies the large pivot by complete Lucas factorization of t−1.
"""
from math import gcd,prod,isqrt
from fractions import Fraction
from functools import cache
import sys
B=10**2400;p=11;t=2471107084783904470093;E=358
@cache
def prime_small(z):return z>=2 and all(z%d for d in range(2,isqrt(z)+1))
@cache
def generator(s):
 fs=[2,5] if s==p else [2,3,7,109,359,34147,22016018359];assert s==p or s==t;assert all(prime_small(z) for z in fs);assert prod(fs)*(1 if s==p else 2)==s-1
 return next(g for g in range(2,200) if pow(g,s-1,s)==1 and all(gcd(pow(g,(s-1)//z,s)-1,s)==1 for z in fs))
def ok(r):
 def viable(z):return z>=3 and z%2 and z not in (p,t,7,19) and pow(2,z-1,z)==1
 return viable(r) or (isqrt(r)**2==r and viable(isqrt(r)))
def losses(s,orders,cap,D,X):
 ans={};g=generator(s)
 def charge(r,m,h):
  if r<3 or not r%2 or (r.bit_length()-1)*h>=(m*m).bit_length():return
  n=r**h
  if n<m*m and n//gcd(D,n)<=B//(D*X) and ok(r):ans[r]=max(ans.get(r,1),Fraction(m*m,n))
 for o in orders:
  if o==1 or o>8000 or 3**(o-1)>=s**(2*cap):continue
  h=o-1
  if h>500:
   r=3
   while r**h<s**(2*cap):
    if pow(r,o,s)==1:charge(r,gcd(pow(r,o,s**cap)-1,s**cap),h)
    r+=2
   continue
  assert h>=2;G=pow(g,(s-1)//o,s);roots=[pow(G,j,s) for j in range(1,o) if gcd(j,o)==1];m=1
  for j in range(cap):
   m*=s
   for r in roots:charge(r,m,h)
   roots=[r+m*((-((pow(r,o,m*s)-1)//m)*pow(o*pow(r,o-1,s),-1,s))%s) for r in roots]
 return prod(ans.values(),start=Fraction(1)),len(ans)
def verify(f):
 assert __debug__ and f in (28,30);generator(p);generator(t);assert gcd(5*p,((t-1)//4)*t)==1 and 3**8000>B and t>8000 and 3**(p-1)>=p*p
 X=p**E*t**f;A=(p**(E+1)-1)//(p-1)//t;C=(t**(f+1)-1)//(t-1);D=A*C;M=X//t;assert (p**(E+1)-1)//(p-1)==t*A and gcd(D,X)==gcd(A,C)==1
 divs=[1]
 for z in (3,7,109,359,34147,22016018359):divs +=[a*z for a in divs]
 a,n=losses(p,[5],E,D,X);b,k=losses(t,divs,f-1,D,X);u=a*b;u=(u.numerator+u.denominator-1)//u.denominator;H=max(A,C);stat=[0,0,0]
 def ext(Z,m,q):
  if Z<q:return True
  if Z//q>=4*m:return False
  a=Z*pow(q,-1,4*m)%(4*m);return not 0<a<=Z//q or Z%a!=0
 for i in range(E+1):
  for j in range(f):
   m=p**i*t**j;q=2*m-1;r=(M//m)**2
   if X*q*r>B*u:stat[0]+=1;continue
   assert ext(A,m,q) and ext(C,m,q),(i,j,'external')
   if X*D*q>B:stat[1]+=1;continue
   assert (2*X*q*q*r)*(2*X*D*q*q)>9*B**2*u*H,(i,j,'supplier')
   stat[2]+=1
 print('PASS (11,358), first',f,'loss',u,'labels',n,k,'Euler counts',stat,flush=True)
if __name__=='__main__':
 for f in map(int,sys.argv[1:] or [28,30]):verify(f)
