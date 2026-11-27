"""No author imports: recompute tree partitions/leaf scopes of twelve published full firsts."""
from pathlib import Path
import hashlib,json,gzip
from math import gcd,prod
from functools import cache
from collections import Counter
H=Path(__file__).resolve().parent.parent/'Three';B=10**2400;ban=19*7*11*31*13
@cache
def sig(q,h):return (q**(h+1)-1)//(q-1)
def vp(n,q):
 a=0
 while n%q==0:n//=q;a+=1
 return a
def state(rr):
 odd=sum(h%2 for q,h in rr);X=prod(q**h for q,h in rr);S=prod(sig(q,h) for q,h in rr)//(1+odd)
 if odd>1 or any(h%2 and (q%4!=1 or h%4!=1) for q,h in rr) or gcd(X*S,ban)>1 or S*(1+odd)>2*X or any(vp(S,q)>h for q,h in rr):return None
 D=S
 while (v:=gcd(X,D))>1:D//=v
 return (X,D,S) if X*D<=B else None
E=[5,102,106,130,148,180,190,192,196,226,240,250];sums=Counter()
for f in E:
 fp=H/f'Full{f}.json.gz';d=json.loads(gzip.decompress(fp.read_bytes()));assert (d['p'],d['e'],d['f'])==(3,6,f) if 'p' in d else True
 c=Counter();labels=set();oddpair=0;fixedpair=0
 def go(rr,t):
  global fixedpair,oddpair
  X,D,S=state(rr);kind=t['type'];c[kind]+=1
  if kind=='forest':
   K=t['roots'];O=dict(t['owners']);labels.update(K);labels.update(O);assert all(D%q==0 and q not in dict(rr) for q in K) and len(K)==len(set(K)) and len(O)==len(t['owners']);return
  if kind=='fastpair':
   q,p,c1,c2=t['args'];assert q!=p and q in dict(rr) and p in dict(rr);assert 0<=dict(rr)[q]-vp(S,q)<=c1 and 0<=dict(rr)[p]-vp(S,p)<=c2
   if any(h%2 for x,h in rr):fixedpair+=1
   else:oddpair+=1
   return
  assert kind=='split';q=t['q'];labels.add(q);a=vp(D,q);assert a>0 and q not in dict(rr) and gcd(q,ban)==1;take={};h=a;size=X*D
  while size<=B:
   r2=rr+((q,h),)
   if state(r2) is not None:take[str(h)]=r2
   h+=1;size*=q
  assert set(take)==set(t['cases']);
  for j,r2 in take.items():go(r2,t['cases'][j])
 go(((3,6),(1093,f)),d['tree']);assert {str(q) for q in labels if q>=2**64}==set(d['ecpp']);sums.update(c);print(f,dict(c),len(d['ecpp']),'fixed/free pairs',fixedpair,oddpair,hashlib.sha256(fp.read_bytes()).hexdigest(),flush=True)
assert sums=={'split':279,'forest':8227,'fastpair':50}
print('PASS exact disjoint set of twelve firsts',E,'counts',dict(sums),'NO FULL exact key credit')
