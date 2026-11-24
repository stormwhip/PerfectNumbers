"""Pure-integer ECPP replay. Every projective nonzero denominator is a unit."""
from functools import cache
from hashlib import sha256
from math import gcd,isqrt
from pathlib import Path
import json
H=Path(__file__).resolve().parent

def check(x,msg):
 if not x:raise ValueError(msg)

def prime64(n):
 if not 2<=n<2**64:return False
 for r in (2,3,5,7,11,13,17,19,23,29,31,37):
  if n%r==0:return n==r
 d=n-1;s=0
 while d%2==0:d//=2;s+=1
 for a in (2,325,9375,28178,450775,9780504,1795265022):
  if not a%n:continue
  x=pow(a,d,n)
  if x in (1,n-1):continue
  for _ in range(s-1):
   x=x*x%n
   if x==n-1:break
  else:return False
 return True

def level(n,t,s,a,P):
 m=n+1-t;check(n>3 and gcd(n,6)==1 and t*t<4*n and s>0 and m%s==0,'invalid trace/factor');q=m//s
 check(q>(isqrt(isqrt(n))+2)**2 and q<n,'Hasse bound') # stronger than PARI criterion
 x,y=P; b=(y*y-x**3-a*x)%n; check(gcd(4*a**3+27*b*b,n)==1,'bad discriminant'); prod=1
 def double(X):
  nonlocal prod
  if X is None:return None
  x,y,z=X
  if y==0:return None
  prod=prod*y%n; yy=y*y%n;d=4*x*yy%n;h=(3*x*x+a*pow(z,4,n))%n;xx=(h*h-2*d)%n;return xx,(h*(d-xx)-8*yy*yy)%n,2*y*z%n
 def plus(X,Y):
  nonlocal prod
  if X is None:return Y
  if Y is None:return X
  x,y,z=X;xx,yy,zz=Y; u=x*zz**2%n;v=xx*z**2%n;l=y*pow(zz,3,n)%n;h=yy*pow(z,3,n)%n; D=(v-u)%n;R=(h-l)%n
  if D==0:
   if R==0:return double(X)
   check((h+l)%n==0 and gcd(R,n)==1,'mixed infinity');return None
  prod=prod*D%n; dd=D*D%n;nx=(R*R-(v+u)*dd)%n;return nx,(R*(u*dd-nx)-l*dd*D)%n,z*zz*D%n
 def mul(k,X):
  Y=None
  for bit in bin(k)[2:]:
   Y=double(Y)
   if bit=='1':Y=plus(Y,X)
  return Y
 U=mul(s,(x%n,y%n,1));check(U and gcd(U[2],n)==1,'not affine');check(mul(q,U) is None and gcd(prod,n)==1,'invalid elliptic multiplication');return q

@cache
def proved(n):
 if n<2**64:return prime64(n)
 p=H/'ECPP'/(sha256(str(n).encode()).hexdigest()[:24]+'.json')
 if not p.exists():return False
 rows=json.loads(p.read_text());cur=n
 for row in rows:
  check(row[0]==cur,'incorrect next prime');cur=level(*row)
 check(prime64(cur),'invalid 64-bit terminus');return True
