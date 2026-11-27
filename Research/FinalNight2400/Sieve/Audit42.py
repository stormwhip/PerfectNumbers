"""Independent conditional-42 audit. Teichmuller lifts and exact power caps for emitter windows."""
from math import gcd,prod,isqrt
from fractions import Fraction
from itertools import combinations
p,t=13,5424477432443; B=10**2400;X=p**310*t**42;M=p**310*t**41;A=(p**311-1)//12//t;C=(t**43-1)//(t-1);D=A*C
assert gcd(X,D)==gcd(A,C)==1 and t*A==(p**311-1)//12
assert t-1==2*31*179*311*787*1997 and gcd((t-1)*t//2,39)==1
ban={7,11,13,19,31,t}
def possible(x):
 def ok(q):return q>=3 and q%2 and q not in ban and pow(2,q-1,q)==1
 return ok(x) or (isqrt(x)**2==x and ok(isqrt(x)))
def audit(s,fac,c,w):
 assert all(all(z%j for j in range(2,isqrt(z)+1)) for z in (s,*fac))
 orders={prod(x) for k in range(len(fac)+1) for x in combinations(fac,k)}-{1}
 g=next(i for i in range(2,500) if all(pow(i,(s-1)//z,s)!=1 for z in set(fac)|{2}));loss={};lim=s**(c*w)
 def price(x,m,n):
  if n>=m**w or not possible(x) or X*D*(n//gcd(D,n))>B:return
  loss[x]=max(loss.get(x,1),Fraction(m**w,n))
 for o in sorted(orders):
  if o>8000 or 3**(o-1)>=lim:continue
  h=o-1
  if o>=1997:
   r=3
   while r**h<lim:
    if pow(r,o,s)==1:price(r,gcd(pow(r,o,s**c)-1,s**c),r**h)
    r+=2
   continue
  root=pow(g,(s-1)//o,s);m=s
  for j in range(1,c+1):
   z=1;limbits=(m**w).bit_length()
   for i in range(1,o):
    z=z*root%m
    if gcd(i,o)==1 and z>=3 and z%2 and (z.bit_length()-1)*h<limbits:price(z,m,z**h)
   m*=s;root=pow(root,s,m) # s=1 mod o; canonical roots lift preserving their reduction.
 return loss
u=audit(p,[3],310,2);v=audit(t,[31,179,311,787,1997],41,10);L=prod(u.values())*prod(v.values());U=-(-L.numerator//L.denominator);assert (len(u),len(v),U)==(6,0,4016)
cts=[0]*3;H=max(A,C)
from bisect import bisect_right
powers=[p**i for i in range(311)]
for i in range(311):
 for j in range(42):
  m=p**i*t**j;Q=2*m-1;R=p**(2*(310-i))*t**(10*(41-j))
  if X*Q*R>B*U:cts[0]+=1;continue
  for Z in (A,C):
   if Z<Q:continue
   k=Z*pow(Q,-1,4*m)%(4*m);assert Z//Q<4*m and not (0<k<=Z//Q and Z%k==0)
  if X*D*Q>B:cts[1]+=1;continue
  for v in range(42-j):
   hi=3*B*H//(2*X*D*Q**2*t**v)
   e=min(310-i,bisect_right(powers,hi)-1)
   if e>=0:assert 2*X*Q**2*R>3*B*U*t**(9*v)*p**e
  cts[2]+=1
assert cts==[11596,930,536];print('PASS independent first42 U and windows:',U,cts)
