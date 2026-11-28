"""Independent inverse-CRT enumeration and Euler-window counts, excluding no PRP except provably composite ones."""
from fractions import Fraction
from math import gcd,prod,isqrt
from functools import cache
p=13;t=231050784610489;B=10**2400;X=p**262*t**46;M=X//t;A=(p**263-1)//12//t;C=(t**47-1)//(t-1);D=A*C
assert gcd(A,C)==gcd(X,D)==1
# Lift roots of x^2+x+1=0, not roots of x^3-1.
def lift(s,n):
 yield 1,(0,)
 x=next(y for g in range(2,100) for y in [pow(g,(s-1)//3,s)] if y!=1);h=s
 for j in range(n):
  assert (x*x+x+1)%h==0;yield h,(x,h-1-x)
  x+=h*(-((x*x+x+1)//h)*pow(2*x+1,-1,s)%s);h*=s
@cache
def ok(x):
 if x<=2 or x%2==0 or x in (7,11,13,19,31,t):return False
 return all(x==s or x%s for s in range(3,100,2) if all(s%k for k in range(2,isqrt(s)+1))) and pow(2,x-1,x)==1
loss={}
def debit(x,h,m):
 if x<3 or x%2==0 or x**h>=m*m:return
 if X*D*(x**h//gcd(x**h,D))>B:return
 y=isqrt(x)
 if not ok(x) and not(y*y==x and ok(y)):return
 ratio=Fraction(m*m,x**h);loss[x]=max(loss.get(x,1),ratio)
for a,aa in lift(p,262):
 for b,bb in lift(t,45):
  inv=pow(b,-1,a);m=a*b
  for x in aa:
   for y in bb:debit(y+b*((x-y)*inv%a),2,m)
assert len(loss)==23
# Orders exceeding 3: potential losses computed exactly, including all odd order divisors of t-1.
Q=[1];
for s in (3,263,401,877,104087):Q += [z*s for z in Q]
assert 8*max(Q)==t-1
for o in Q:
 if o<=3 or 3**min(8000,o-3)>=t**90:continue
 r=3
 while r**(o-3)<t**90:
  if pow(r,o,t)==1:
   m=gcd(pow(r,o,t**45)-1,t**45);assert r**(o-3)>=m*m or X*D*(r**(o-3)//gcd(r**(o-3),D))>B or (not ok(r) and (isqrt(r)**2!=r or not ok(isqrt(r))))
  r+=2
L=prod(loss.values());U=-(-L.numerator//L.denominator);assert U==2247129787084402954
cts=[0]*3
for i in range(263):
 for j in range(46):
  m=p**i*t**j;q=2*m-1;S=M//m
  if X*q*S*S>B*U:cts[0]+=1;continue
  for z in (A,C):
   k=z*pow(q,-1,4*m)%(4*m); assert z//q<4*m and not (1<=k<=z//q and z%k==0) or q>z
  if X*D*q>B:cts[1]+=1;continue
  assert 4*X**2*D*q**4*S**2>9*B**2*U*max(A,C);cts[2]+=1
assert cts==[4984,5320,1794];print('PASS independent first46 window and exact joint U:',cts,U)
