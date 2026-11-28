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
  if any(z!=p and z!=p*p and z%p==0 for p in (3,5,17,23,29,37,41,43,47,53,59,61,67,71,73,79,83,89,97)):return
  if any((not (h+1)%p if z%p==1 else pow(z,h+1,p)==1) for p in BAN):return
  vs=[]
  for p,c,m in zip(qs,cap,powers):
   if z%p==1:v=val(h+1,p)
   elif pow(z,h+1,p)!=1:v=0
   else:v=val((pow(z,h+1,m)-1)%m or m,p)
   if v>c:return
   vs.append(v)
  if z**h<q**(w1*vs[0])*r**(w2*vs[1]) and (pow(2,z-1,z)==1 or (isqrt(z)**2==z and isqrt(z)%4==1)):cand.add((z,h,*vs))
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


def test(h):
 q=1093;r=2035349;P=[(3,6),(q,156),(r,h)];X=prod(z**k for z,k in P);S=prod(sig(z,k) for z,k in P);D=S//gcd(X,S);assert gcd(X,D)==1
 A=156-val(S,q);C=h-val(S,r);w=2;v=6;E={}
 for z,j,a,b in enum(q,r,156,66,w,v):
  base=isqrt(z) if isqrt(z)**2==z else z
  if base in (3,q,r) or a>A or b>C:continue
  mass=z**j
  if X*D*(mass//gcd(mass,D))>B:continue
  E[z]=max(E.get(z,Fraction(1)),Fraction(q**(w*a)*r**(v*b),mass))
 V=X*q**(w*A)*r**(v*C)/prod(E.values(),start=Fraction(1));blocks=[sig(z,k)//gcd(X,sig(z,k)) for z,k in P];assert prod(blocks)==D and gcd(blocks[1],blocks[2])==1;big=max(blocks)
 from fractions import Fraction as F
 # Both anonymous blocks have exact known cyclotomic orders and are nonsquares.
 rough=10000001;A0=blocks[1];C0=blocks[2]
 for blk,k,center in ((A0,157,q),(C0,h+1,r)):
  assert gcd(blk,2*k*center*(center-1))==1 and isqrt(blk)**2!=blk and all(blk%s for s in range(2*k+1,rough,2*k))
 R=D;mcount=0
 while R>=rough:R//=rough;mcount+=1
 cut=0;cutone=0
 for power in [1,2]:
  for level in range(25,100):
   m=q**level
   if (m*314)**(power+1)<max(A0,C0):continue
   good=True
   for blk,k in [(A0,157),(C0,h+1)]:
    K=2*k*m
    for order in [v for v in J.divisors(q-1) if v%2 and v>1]:
     for zz in J.lifts(q,order,level)[-1]:
      rr=zz+m*((1-zz)*pow(m,-1,2*k)%(2*k));j0=blk*pow(rr,-power,K)%K or K
      if rr**power*j0<=blk:good=False;break
     if not good:break
    if not good:break
   if good:break
  assert good and rough**(3*q-1)>B
  if power==2:cut=level
  else:cutone=level
 print('inverse cuts at h',h,cut,cutone,flush=True)
 sup=F(S,X)*F(rough,rough-1)**mcount
 from itertools import count
 # Outside X,D,e: 0,1,2 primes incompatible by multiplicative abundancy for large e.
 external=(5*17*23)**2
 if sup*F(1000,999)*F(5,4)*F(17,16)>=2:external=1
 assert rough>=external # for exterior emitter charge both block parities instead of overlapping its outside reserve
 def internal(m):
  lo=2*m-1
  return any((lambda a,k,b: a<=k and ((k-a)//(4*m)>16 or any(not b%t for t in range(a,k+1,4*m))))(z*pow(lo,-1,4*m)%(4*m) or 4*m,z//lo,z) for z in blocks)
 fail=[];intc=0;testc=0
 for a in range(A+1):
  for b in range(C+1):
   m=q**a*r**b;lo=2*m-1;t=q**(w*a)*r**(v*b)
   if V*lo>B*t:continue
   if internal(m):intc+=1;fail.append(('int',a,b));continue
   if X*D*lo>B:continue
   ex=external if lo>=1000 else 1
   if X*D*lo*rough**2*ex>B:continue
   testc+=1
   for u in range(A-a+1):
    best=-1
    # monotone size bounds with r^2 or higher excluded by inverse residues.
    for vv in range(C-b+1):
     H2=2*lo*q**u*r**vv;K=ex*rough*X*D*lo
     if K*H2>3*B*big:break
     if u>=cut and K*K*H2>3*B**2:break
     if u>=cutone and K*H2>3*B:break
     best=vv
    if best>=0 and 2*V*lo**2*q**u*r**best<=3*B*t*q**(w*u)*r**(v*best):fail.append(('ext',a,b,u,best));break
 print('failwindows',h,fail,flush=True); print(h,'Vfloor',len(str(V.numerator//V.denominator))-1,'exc',len(E),'interior',intc,'exterior',testc,'fail',len(fail),fail[:5],flush=True);return not fail
if __name__=='__main__':
 assert test(66)