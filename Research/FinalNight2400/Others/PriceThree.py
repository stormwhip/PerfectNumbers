"""Joint weighted order-three price for (13,262) and its 46-fiber. No input files."""
from math import gcd,isqrt,prod
from functools import cache
from fractions import Fraction
P=13;T=231050784610489;E=262;F=46;B=10**2400
@cache
def prime64(n):
 if n<2:return False
 for p in (2,3,5,7,11,13,17,19,23,29,31,37):
  if n%p==0:return p==n
 # deterministic for n<2**64, cf. existing certified pivot independent deterministic test
 assert n<2**64
 d=n-1;s=0
 while d%2==0:d//=2;s+=1
 for a in (2,325,9375,28178,450775,9780504,1795265022):
  if a%n==0:continue
  x=pow(a,d,n)
  if x in (1,n-1):continue
  for _ in range(s-1):
   x=x*x%n
   if x==n-1:break
  else:return False
 return True
@cache
def roots(p,c):
 x=next(a for g in range(2,100) for a in [pow(g,(p-1)//3,p)] if a!=1);r=[x,x*x%p];m=p;ret=[(1,[0])]
 for j in range(1,c+1):
  ret.append((m,r));r=[a+m*((-((pow(a,3,m*p)-1)//m)*pow(3*a**2,-1,p))%p) for a in r];m*=p
 return ret

def loss(den=1,penalty=0):
 # Charge W=2-penalty/den on each p,t unit; exact formulas accumulate U^den. ROOT modulus equals the full product; minimal odd representatives suffice for W<=2.
 w=2*den-penalty;out={}
 def upd(r,N,D):
  if r<3 or not r%2 or (r in (P,T)) or any(r%k==0 and r not in (k,k*k) for k in (3,5,7,11,13,17,19,23,29,31,37,41,43)):return
  if any(r in (k,k*k) for k in (19,7,11,31)):return
  if N>D:out[r]=max(out.get(r,1),Fraction(N,D))
 assert T-1==8*3*263*401*877*104087 and all(prime64(v) for v in (13,T,263,401,877,104087)); assert T>8000 and 3**8000>B and 3**(12*den)>=13**w
 for b,bb in roots(T,F-1):
  inv=1;ip=pow(P,-1,b)
  for a,aa in roots(P,E):
   m=a*b
   for x in aa:
    for y in bb:
     r=x+a*((y-x)*inv%b)
     if r>=3 and r%2 and r<m:upd(r,m**w,r**(2*den))
   inv=inv*ip%b
 # For t-order o>3 reserve 2 powers for p's order3. Cost h=o-3; if simultaneously p units via length multiple 13^v, pay its incremental cost separately via product lengths. Large-order losses are bounded by brute odd bases.
 for o in (263,401,789,877,1203,2631):
  h=o-3
  if 3**(h*den)>=T**((F-1)*w):continue
  r=3
  while r**(h*den)<T**((F-1)*w):
   if pow(r,o,T)==1:
    m=gcd(pow(r,o,T**(F-1))-1,T**(F-1));upd(r,m**w,r**(h*den))
   r+=2
 # Remaining odd orders >=3*877 (or >=104087) exceed threshold; checked by enumerating all divisors, including the coprime products.
 allO=[1]
 for z in (3,263,401,877,104087):allO += [a*z for a in allO]
 assert all(o in (3,263,401,789,877,1203,2631) or o==1 or 3**(min(8000,o-3)*den)>=T**((F-1)*w) for o in allO)
 return prod(out.values(),start=Fraction(1)),len(out)
if __name__=='__main__':
 import sys,math
 den=int(sys.argv[1]) if len(sys.argv)>1 else 1;pen=int(sys.argv[2]) if len(sys.argv)>2 else 0
 u,n=loss(den,pen);print('loss digits',math.log10(u.numerator)-math.log10(u.denominator),'per-charge',den,'exceptions',n,flush=True)
