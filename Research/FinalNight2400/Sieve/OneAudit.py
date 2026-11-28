"""Independent exceptional 19^618 2477^1 tree; tighter directed log bounds, independent primitive roots; no import of the original price/tree routines."""
from pathlib import Path
import json
from fractions import Fraction
from math import prod,gcd,isqrt
from functools import cache
from collections import Counter
H=Path(__file__).resolve().parent;tree=json.loads((H.parent/'Nineteen/OneTree.json').read_bytes());F={int(i):v for i,v in tree['emissions'].items()};p,t=19,2477;B=10**2400;D=50;N=99;K=16384
@cache
def prime(x):return x>=2 and all(x%i for i in range(2,isqrt(x)+1)) if x<10**10 else mr(x)
def mr(x):
 assert 2<x<2**64
 h=x-1;s=0
 while h%2==0:s+=1;h//=2
 return all(a%x==0 or pow(a,h,x)==1 or any(pow(a,h<<i,x)==x-1 for i in range(s)) for a in (2,325,9375,28178,450775,9780504,1795265022))
assert prime(p) and prime(t) and all(all(q>2 and prime(q) and a%q==0 for q in zz) for a,zz in F.items())
@cache
def sigma(q,h):return (q**(h+1)-1)//(q-1)
def vp(z,q):
 k=0
 while z%q==0:k+=1;z//=q
 return k
loss={};assert 39**(18*D)>19**N and 3**(54*D)>19**N
for o in (3,9):
 m=p;root=next(j for j in range(2,p) if pow(j,o,p)==1 and pow(j,o//3,p)!=1)
 for v in range(1,619):
  for j in range(1,o):
   if gcd(j,o)>1:continue
   r=pow(root,j,m)
   if r<=2 or r%2==0 or r in (19,t) or any(r!=s and r%s==0 for s in (3,5,7,11,13,17,19,23,29,31,37)):continue
   if r**(D*(o-1))<m**N:loss[r]=max(loss.get(r,1),Fraction(m**N,r**(D*(o-1))))
  m*=p;root=pow(root,p,m)
assert len(loss)==8
R=prod(loss.values())*Fraction(B**D,(p**618*t)**D*p**(N*618));ceil=lambda x:-(-x.numerator//x.denominator);threshold=((ceil(R)**256).bit_length()*K)//256
@cache
def lo(q):return (q**K).bit_length()-1
@cache
def values(q):
 a=2;y=q*q;ans=[];v0=vp(q**9-1,p);order=next((j for j in (1,3,9) if pow(q,j,p)==1),0)
 while y<=B:
  h=a+1;u=0 if not order or h%order else vp(h,p)+(v0 if order>1 else 0);ans.append((a,D*a*lo(q)-N*u*(lo(p)+1)));a+=2;y*=q*q
 return ans
counts=Counter();initial={p:618,t:1};visited=[]
def walk(assign,oblig,paid,node):
 counts['visited']+=1;S=prod(sigma(q,h)//(2 if q==t else 1) for q,h in assign.items());
 if any(vp(S,q)>h for q,h in assign.items()):counts['conflict']+=1;return
 candidates={q:[(h,v) for h,v in values(q) if h>=vp(S,q)] for q in oblig-assign.keys()};assert all(candidates.values());floor={q:min(u for h,u in vv) for q,vv in candidates.items()};price=paid+sum(floor.values());
 if price>threshold:counts['price']+=1;return
 rr=assign|{q:vv[0][0] for q,vv in candidates.items()};
 if prod(sigma(q,h) for q,h in rr.items())>2*prod(q**h for q,h in rr.items()):counts['abundance']+=1;return
 q=node['q'];counts['split']+=1;assert q in candidates
 for h,v in candidates[q]:
  if price-floor[q]+v>threshold:continue
  assert str(h) in node['cases'];z=sigma(q,h);walk(assign|{q:h},oblig|set(F[z]),paid+v,node['cases'][str(h)])
assert (t+1)//2==3*7*59 and (t+1)%p and sigma(p,618)%p
walk(initial,{3,7,59},0,tree['tree']);print('PASS independent tighter pricing tree',counts,'uniform losses',len(loss))
