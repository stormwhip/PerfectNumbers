"""Pair supplier price with option/discount tables cached per target tuple; per-leaf filtered floors."""
from pathlib import Path
from math import gcd,prod,isqrt
from functools import cache
from fractions import Fraction
from itertools import product
import sys
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path.insert(0,str(R/'FinalSprint'));import JointValuation as J
B=10**2400;BAN=(19,7,11,31,13)
def val(z,p):return J.val(z,p)
def sig(z,f):return (z**(f+1)-1)//(z-1)
@cache
def lifts(p,k,c):return J.lifts(p,k,c)
@cache
def enum(q,r,c1,c2,w1,w2):
 qs=(q,r);cap=(c1,c2);cand=set();powers=[p**(c+1) for p,c in zip(qs,cap)]
 @cache
 def options(p,c,f):
  t=f+1;s=val(t,p);out=[]
  if 0<s<=c:out.append((p,1,p**s))
  for o in J.divisors(gcd(p-1,t)):
   if o==1 or c<=s:continue
   for j,rr in enumerate(lifts(p,o,c-s),1):
    m=p**j;out.extend((m,x,m*p**s) for x in rr)
  return out
 def add(z,h):
  if z<5 or z%2==0 or z in BAN or z in qs or (h%2 and z%4!=1):return
  if any(z!=p and z%p==0 for p in (3,5,17,23,29,37,41,43,47,53,59,61,67,71,73,79,83,89,97)):return
  if any((not (h+1)%p if z%p==1 else pow(z,h+1,p)==1) for p in BAN):return
  vs=[]
  for p,c,m in zip(qs,cap,powers):
   if z%p==1:v=val(h+1,p)
   elif pow(z,h+1,p)!=1:v=0
   else:v=val((pow(z,h+1,m)-1)%m or m,p)
   if v>c:return
   vs.append(v)
  if z**h<q**(w1*vs[0])*r**(w2*vs[1]) and pow(2,z-1,z)==1:cand.add((z,h,*vs))
 for h in range(2,w1+w2):
  if h%2:continue
  for (m,x,b),(m2,x2,b2) in product([(1,0,1),*options(q,c1,h)],[(1,0,1),*options(r,c2,h)]):
   z=x+m*((x2-x)*pow(m,-1,m2)%m2);M=m*m2;lim=b**w1*b2**w2
   while J.less(z,h,lim):add(z,h);z+=M
 # High exponents: work order-first rather than repeatedly materializing the same
 # lifted roots for thousands of h values. For an actual positive supply u=j+s,
 # r>=R (least class representative). Once R^h >= p^(H*(j+smax)), no later
 # h can lose, where smax is the greatest p-adic valuation of h+1 up to hmax.
 H=w1+w2;hmax=0
 while 5**(hmax+1)<=B:hmax+=1
 for p,c in zip(qs,cap):
  smax=0
  while p**(smax+1)<=hmax+1:smax+=1
  # order-one class, LTE; its f must satisfy v_p(f+1)>0.
  for h in range(H+(H%2),hmax+1,2):
   sh=val(h+1,p)
   if 0<sh<=c:
    r0=p+1;lim=p**(H*sh)
    while J.less(r0,h,lim):add(r0,h);r0+=p
  # Only divisors o<=hmax+1 are relevant. Avoid divisors(p-1) at giant p.
  for o in range(3,hmax+2,2):
   if (p-1)%o or 5**(o-1)>=p**(H*c):continue
   for j,rr in enumerate(lifts(p,o,c),1):
    mod=p**j;high=p**(H*min(c,j+smax));first=o-1
    while first<H:first+=2*o
    for x in rr:
     for h in range(first,hmax+1,2*o):
      if not J.less(max(5,x),h,high):break
      sh=val(h+1,p)
      if j+sh>c:continue
      lim=p**(H*(j+sh));z=x
      while J.less(z,h,lim):add(z,h);z+=mod
 return tuple(sorted(cand))

def prove(rows,q,r,c1,c2,w1=2,w2=4):
 assert sum(h%2 for z,h in rows)==1
 X=prod(z**h for z,h in rows);S=prod(sig(z,h)//(1+h%2) for z,h in rows);D=S//gcd(X,S);assert gcd(D,X)==1
 fixed=dict(rows);odd=any(h%2 for z,h in rows);actual=[fixed[p]-val(S,p) for p in (q,r)];caps=(c1,c2);assert all(0<=a<=c for a,c in zip(actual,caps));M=q**actual[0]*r**actual[1];E={}
 for z,h,a,b in enum(q,r,c1,c2,w1,w2):
  if z in fixed or h%2 and odd or a>actual[0] or b>actual[1]:continue
  mass=z**h
  if X*D*(mass//gcd(mass,D))>B:continue
  E[z]=max(E.get(z,Fraction(1)),Fraction(q**(w1*a)*r**(w2*b),mass))
 V=X*q**(w1*actual[0])*r**(w2*actual[1])/prod(E.values(),start=Fraction(1));
 if V<=B:return False
 if odd:return True
 blocks=[sig(z,h)//gcd(sig(z,h),X) for z,h in rows];cl=[];assert prod(blocks)==D
 for b in blocks:
  same=[w for w in cl if gcd(w,b)>1];cl=[w for w in cl if w not in same];cl.append(b*prod(same))
 bmax=max(cl)
 for a in range(actual[0]+1):
  for b in range(actual[1]+1):
   m=q**a*r**b;t=2*m-1
   if V*t>B*q**(w1*a)*r**(w2*b):continue
   for z in blocks:
    u=z*pow(t,-1,4*m)%(4*m) or 4*m;hi=z//t
    if hi>=u and ((hi-u)//(4*m)>16 or any(not z%j for j in range(u,hi+1,4*m))):return False
   if X*D*t>B:continue
   # If n(r) denotes unweighted supply, the emitter's discount loss is at most n(r)^max(w).
   # Stronger: exact finite valuations u,v in residual cap rectangle.
   for u in range(actual[0]-a+1):
    for v in range(actual[1]-b+1):
     y=q**u*r**v
     if 2*X*D*t*t*y>3*bmax*B:continue
     if 2*V*t*t*y>3*B*q**(w1*(a+u))*r**(w2*(b+v)):continue
     return False
 return True
if __name__=='__main__':
 z=9616400017587385400438896773389435561
 for h in [4,6,10]:print('weighted at top',h,prove([(3,6),(1093,240),(z,h)],1093,z,240,10),flush=True)