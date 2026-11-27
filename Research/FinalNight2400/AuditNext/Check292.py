"""Data-only raw domain reconstruction; arithmetic forest endpoints are separately replayed."""
from math import gcd,prod
from pathlib import Path
import json,gzip,hashlib
B=10**2400;H=Path(__file__).resolve().parents[1]/'Nineteen292';sig=lambda p,k:(p**(k+1)-1)//(p-1);tails=[]
def state(P):
 X=prod(p**k for p,k in P);Z=prod(sig(p,k) for p,k in P);s=Z//2**sum(k%2 for p,k in P);c=s//gcd(X,s);good=(gcd(X,c)==1 and X*c<=B and Z<=2*X and sum(k%2 for p,k in P)<=1 and all(not k%2 or p%4==k%4==1 for p,k in P));return X,c,good
def dom(P,r):
 X,c,ok=state(P);assert ok and c%r==0 and r not in dict(P);h=0
 while c%r==0:c//=r;h+=1
 li=[]
 while X*c*r**h<=B:
  if state(P+[(r,h)])[2]:li.append(h)
  h+=1
 tails.append(h);return li
base=[(19,292)];r=10018843;domain=dom(base,r);assert tails[-1]==238 and domain==list(range(2,119,2));from collections import Counter
groups=[]
for file in ['Forests292','Ten292','TwoMore','CloseFour','First26','First28','LastThree']:
 d=json.load(gzip.open(H/(file+'.json.gz')));assert d['p']==19 and d['e']==292 and d['pivot']==r;groups.append(set(map(int,d['cases'])))
 if file!='LastThree':continue
 stats=Counter();used=set()
 def go(P,node):
  kind=node['type'];stats[kind]+=1
  if kind in ('forest','masked'):used.update(node['roots']);used.update(q for q,z in node['owners']);
  if kind=='forest':return
  if kind=='split':
   q=node['q'];used.add(q);ks=dom(P,q);assert set(ks)==set(map(int,node['cases']))
   for n in ks:go(P+[(q,n)],node['cases'][str(n)])
  else:
   assert kind in ('ab','masked');used.update(node['roots']);used.update(node.get('bad',[]));X,D,ok=state(P);S=prod(sig(p,h) for p,h in P);A=X;F=node['roots'];assert len(F)==len(set(F)) and not(set(F)&dict(P).keys())
   for q in F:
    y=D;h=0
    while y%q==0:y//=q;h+=1
    assert h>0
    if any(k%2 for _,k in P) or q%4==3:h+=h%2
    S*=sig(q,h);A*=q**h
   if kind=='ab':assert S>2*A
   else:
    bad=node['bad'];assert bad and len(set(bad))==len(bad) and not set(bad)&(set(F)|dict(P).keys())
    for q in bad:
     k=2 if any(e%2 for p,e in P) or q%4==3 else 1;assert S*sig(q,k)>2*A*q**k
 for h,n in d['cases'].items():assert int(h) in domain;go(base+[(r,int(h))],n)
 print(file,'exact exponent keys',sorted(map(int,d['cases'])),stats)
 assert set(d['ecpp'])=={str(q) for q in used if q>=2**64};print('final all used large labels',len(d['ecpp']))
assert sum(map(len,groups))==len(set.union(*groups))==59 and set.union(*groups)==set(domain);G=H.parents[1]/'GeminiFrontier';sh=json.loads((G/'ShardToKeys.json').read_bytes());iv=json.loads((G/'KeyToShards.json').read_bytes());assert [(n,z) for n,z in sh.items() if [19,292] in z]==[('P19_I00060',[[19,292]])] and iv['19,292']==['P19_I00060'];print('PASS all 59 disjoint scoped firsts, raw tail238; singleton P19_I00060')
