"""Integer-weight joint supplier price; exponent-one Euler handled separately."""
from pathlib import Path
import sys
from functools import cache
from math import prod,gcd
from fractions import Fraction
from itertools import product
R=Path(__file__).resolve().parents[2];sys.path.insert(0,str(R/'FinalNight2400/Ten'))
from Weighted import lifts, divisors,val,inverse,less,B

def sig(p,e):return (p**(e+1)-1)//(p-1)
def price(P,weights):
 assert __debug__ and len(P)==len(weights) and all(type(w)==int and w>=0 for w in weights) and sum(weights)>0
 fixed=dict(P);assert len(P)==len(fixed);X=prod(p**e for p,e in P);Z=[sig(p,e)//(1+e%2) for p,e in P];S=prod(Z);C=S//gcd(X,S);assert gcd(C,X)==1
 L=[z//gcd(z,X) for z in Z];assert prod(L)==C
 Q=[(p,e-val(S,p),w) for (p,e),w in zip(P,weights) if w];assert all(c>=0 for p,c,w in Q)
 H=sum(weights);M=prod(p**(c*w) for p,c,w in Q);limit=B//X;budget=B//(X*C);E={};fixedEuler=any(e%2 for p,e in P)
 def permitted(f):return f%2==0 or (not fixedEuler and f%4==1)
 @cache
 def check(r,f):
  if r<3 or r%2==0 or r in fixed or (f%2 and r%4!=1) or not less(r,f,limit+1):return
  for d in (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97):
   if r!=d and r%d==0:return
  a=1
  for p,c,w in Q:
   if r%p==1:v=val(f+1,p)
   elif pow(r,f+1,p)!=1:v=0
   else:
    m=p**(c+1);u=(pow(r,f+1,m)-1)%m;v=val(u,p) if u else c+1
   if v>c:return
   a*=p**(w*v)
  b=r**f
  if a<=b or b//gcd(b,C)>budget or pow(2,r-1,r)!=1:return
  E[r]=max(E.get(r,1),Fraction(a,b))
 def opts(p,c,f):
  s=val(f+1,p)
  if 0<s<=c:yield p,1,p**s
  for o in divisors(gcd(f+1,p-1)):
   if o==1 or c<=s:continue
   for j,rs in enumerate(lifts(p,o,c-s),1):
    m=p**j
    for r in rs:yield m,r,m*p**s
 for f in range(2,H):
  if not permitted(f):continue
  choices=[[(1,0,1)]+[(m,z,a**w) for m,z,a in opts(p,c,f)] for p,c,w in Q]
  for cells in product(*choices):
   m,x,a=1,0,1
   for d,z,b in cells:
    if d!=1:x+=m*((z-x)*inverse(m%d,d)%d);m*=d
    a*=b
   while less(x,f,a):check(x,f);x+=m
 for p,c,w in Q:
  f=H; maxcap=p**(H*c);lo=3**f
  while lo<=limit and lo<maxcap:
   if permitted(f):
    shift=val(f+1,p)
    if 0<shift<=c:
     z=p+1;lim=p**(H*shift)
     while less(z,f,lim):check(z,f);z+=p
    for o in divisors(gcd(f+1,p-1)):
     if o==1 or c<=shift:continue
     for j,rs in enumerate(lifts(p,o,c-shift),1):
      m=p**j;lim=p**(H*(j+shift))
      if lo>=lim:continue
      for z in rs:
       while less(z,f,lim):check(z,f);z+=m
   f+=1;lo*=3
 check.cache_clear()
 return Fraction(X*M,1)/prod(E.values()),Q,E,(X,C,L)
