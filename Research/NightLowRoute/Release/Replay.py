"""Direct independent replayer: arbitrary-depth-free designated sigma mass lower bound. Python standard library. No caches, network, SymPy or proof tree."""
from pathlib import Path
from math import gcd,prod
from functools import cache
from fractions import Fraction
import sys,json
here=Path(__file__).resolve().parent
sys.path.insert(0,str(here.parents[1]/'RootFiveNext'));import PrimeCheck
B=10**2400;ORDER=(19,7,11,31,13,3,5,17)
def insist(flag,msg):
 if not flag:raise ValueError(msg)
@cache
def sig(q,f):return (q**(f+1)-1)//(q-1)
def val(x,q):
 n=0
 while x%q==0:x//=q;n+=1
 return n
def free(x,k):
 while (g:=gcd(k,x))>1:x//=g
 return x
def verify(data):
 p,e=data['p'],data['e'];insist(p in (13,19,31) and e>0 and e%2==0,'root');A=sig(p,e);ban=ORDER[:ORDER.index(p)];K=set(data['roots']);own=dict(data['owners']);Q=set(own);insist(K and len(own)==len(data['owners']),'input');C=p*A*prod(Q);K0=p**e*A
 for q in K|Q:
  cur=q
  if q>=2**64:
   for row in data['ecpp'][str(q)]:insist(row[0]==cur,'ECPP subject');cur=PrimeCheck.level(*row)
  insist(q>=3 and PrimeCheck.prime64(cur),'primality')
 for q in K:insist(A%q==0,'root factor')
 for q,z in own.items():insist(z in K and q not in K and (A*p)%q!=0,'overlap')
 @cache
 def indices(q):
  out=set()
  for r in ban:
   if q%r==0:continue
   if q%r==1:out.add(r);continue
   t=1
   while pow(q,t,r)!=1:t+=1
   out.add(t)
  return tuple(out)
 def options(q,c,spec):
  ds=indices(q)
  if spec and (q%4!=1 or 2 in ds):return
  a=c+((1-c)%4 if spec else c%2);step=4 if spec else 2
  while True:
   if all((a+1)%d for d in ds):yield a
   a+=step
 @cache
 def child(q,c,spec):
  it=options(q,c,spec);m=next(it,None)
  if m is None:return None
  best=B+1
  # Exact prefix + monotone conservative lower bound for all remaining exponents.
  for _ in range(10):
   X=q**m
   if X>=best:return best
   best=min(best,X*free(sig(q,m)//(2 if spec else 1),C));m=next(it)
  return min(best,q**m)
 @cache
 def parent(z,spec):
  c=val(A,z);it=options(z,c,spec);f=next(it,None)
  if f is None:return None
  norm=maybe=B+1
  for _ in range(6):
   base=z**(f-c);S=sig(z,f)//(2 if spec else 1);v=base*free(S,C);discount=Fraction(1)
   for q in Q:
    if own[q]!=z:continue
    h=val(S,q)
    if not h:continue
    cost=child(q,h,False);euler=child(q,h,True);v*=cost
    if euler:discount=max(discount,Fraction(cost,euler))
   norm=min(norm,v);maybe=min(maybe,v//discount);f=next(it)
  return min(norm,z**(f-c)),min(maybe,z**(f-c))
 vals={}
 for E in [0,*sorted(q for q in K if parent(q,True))]:
  # E=0 permits one outside Euler in owned Q, charged by dropping at most one parent group's markup; Euler elsewhere cannot weaken any group.
  factors=[parent(z,z==E) for z in K];M=K0*prod(m for m,_ in factors);d=max([Fraction(1)]+[Fraction(m,s) for m,s in factors]) if not E else 1;vals[E]=M//d
 return vals
if __name__=='__main__':
 for name in (sys.argv[1:] or sorted(here.glob('Case*.json'))):
  path=Path(name);path=path if path.is_file() else here/path;d=json.loads(path.read_text());v=verify(d);m=min(v.values());print(d['p'],d['e'],'modes',len(v),'closed',sum(z>B for z in v.values()),'floorlog10',len(str(m))-1,'min mode',min(v,key=v.get),flush=True);insist(m>B,'unclosed mode')
