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



def trial(P,q,r,w,v,aa=None,bb=None):
 S=prod(sig(z,h) for z,h in P);X=prod(z**h for z,h in P);D=S//gcd(X,S);assert gcd(X,D)==1 and all(h%2==0 for z,h in P)
 A=dict(P)[q]-val(S,q);C=dict(P)[r]-val(S,r);assert A>=0 and C>=0;aa=A if aa is None else aa;bb=C if bb is None else bb;assert aa>=A and bb>=C
 E={};fixed=dict(P)
 for z,j,a,b in enum(q,r,aa,bb,w,v):
  base=isqrt(z) if isqrt(z)**2==z else z
  if base in fixed or a>A or b>C:continue
  mass=z**j
  if X*D*(mass//gcd(mass,D))>B:continue
  E[z]=max(E.get(z,Fraction(1)),Fraction(q**(w*a)*r**(v*b),mass))
 V=X*q**(w*A)*r**(v*C)/prod(E.values(),start=Fraction(1));blocks=[sig(z,h)//gcd(X,sig(z,h)) for z,h in P];assert prod(blocks)==D
 clusters=[]
 for t in blocks:
  c=[b for b in clusters if gcd(b,t)>1];clusters=[b for b in clusters if b not in c]+[prod(c)*t]
 big=max(clusters);count=0
 for a in range(A+1):
  for b in range(C+1):
   m=q**a*r**b;lo=2*m-1;t=q**(w*a)*r**(v*b)
   if V*lo>B*t:continue
   for z in blocks:
    co=z*pow(lo,-1,4*m)%(4*m) or 4*m;hi=z//lo
    if co<=hi and ((hi-co)//(4*m)>16 or any(not z%y for y in range(co,hi+1,4*m))):return False
   if X*D*lo>B:continue
   for u in range(A-a+1):
    bound=3*B*big//(2*X*D*lo**2*q**u);vv=0
    if bound<1:continue
    while vv<C-b and r**(vv+1)<=bound:vv+=1
    if 2*V*lo**2*q**u*r**vv<=3*B*t*q**(w*u)*r**(v*vv):return False
 return True
if __name__=='__main__':
 import gzip,json
 H=Path(__file__).resolve().parent;T=json.loads(gzip.decompress((H/'DeepPrimary2.json.gz').read_bytes()))['branch'];ans=[]
 def rec(n,P):
  if n is None:
   if any(h%2 for p,h in P):return
   for r,j in reversed(P):
    if r<=3 or r==398581:continue
    if not(r-1)%3:w=2
    elif not(r-1)%5:w=4
    elif not(r-1)%7:w=6
    else:w=8
    if w==2:continue
    print('try',P[-1],r,w,flush=True);ok=trial(P,398581,r,2,w);ans.append([P,398581,r,2,w,ok]);print('squareatom',ok,flush=True);(H/'SqrFirst2.json').write_text(json.dumps(ans));
    if ok:break
   return
  if n.get('type')=='split':
   for k,v in n['cases'].items():rec(v,P+[(n['q'],int(k))])
 rec(T,[(3,6),(1093,2)])
