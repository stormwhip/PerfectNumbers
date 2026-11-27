"""Data-only raw domain reconstruction; arithmetic forest endpoints are separately replayed."""
from math import gcd,prod
from pathlib import Path
import json,gzip,hashlib
B=10**2400;H=Path(__file__).resolve().parents[1]/'Nineteen';sig=lambda p,k:(p**(k+1)-1)//(p-1);tails=[]
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
base=[(19,282),(1735317810514627,10)];r=8383027;domain=dom(base,r);assert tails[-1]==202 and domain==list(range(2,101,2));from collections import Counter
for file in ['Masked58']:
 d=json.load(gzip.open(H/(file+'.json.gz')));stats=Counter()
 def go(P,node):
  kind=node['type'];stats[kind]+=1
  if kind=='forest':return
  if kind=='split':
   q=node['q'];ks=dom(P,q);assert set(ks)==set(map(int,node['cases']))
   for n in ks:go(P+[(q,n)],node['cases'][str(n)])
  else:
   assert kind in ('ab','masked');X,D,ok=state(P);S=prod(sig(p,h) for p,h in P);A=X;F=node['roots'];assert len(F)==len(set(F)) and not(set(F)&dict(P).keys())
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
 for h,n in d['nodes'].items():assert int(h) in domain;go(base+[(r,int(h))],n)
 print(file,'exact exponent keys',sorted(map(int,d['nodes'])),stats)