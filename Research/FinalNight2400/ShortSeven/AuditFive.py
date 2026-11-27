"""Independent exact 30103^h enumeration and saturation/absences. No project imports."""
from pathlib import Path
import json,gzip,hashlib
from fractions import Fraction
from math import gcd,prod,isqrt
from functools import cache
H=Path(__file__).resolve().parents[1]/'SevenNext';B=10**2400;Q=16148168401;R=173;Z=30103;nos={19,5,11,17,23,31,37,41,47,53};force={3,13,29,43,109,Z}
@cache
def sig(p,h):return (p**(h+1)-1)//(p-1)
def val(n,p):
 a=0
 while n%p==0:a+=1;n//=p
 return a
def state(rows):
 X=prod(p**h for p,h in rows);S=prod(sig(p,h) for p,h in rows)//2;D=S
 while (g:=gcd(D,X))>1:D//=g
 return X,S,D
def ab(q,n):return Fraction(sig(q,n),q**n)
rows=[(7,12),(Q,42),(R,5)];X,S,D=state(rows);assert sig(7,12)==Q and all(D%p==0 for p in force);base=prod(ab(k,v) for k,v in rows)*prod(ab(p,2) for p in force);assert base*ab(3,4)/ab(3,2)>2 and all(base*ab(p,2)>2 for p in nos-{19});rows.append((3,2));X,S,D=state(rows);assert val(S,3)==2 and val(D,Z)==1 and gcd(S,prod(nos))==1;domain=set();h=2
while X*D//Z*Z**h<=B:
 P=rows+[(Z,h)];x,s,d=state(P)
 if gcd(sig(Z,h),3*prod(nos))==1 and all(val(s,q)<=a for q,a in P) and s<=x and x*d<=B:domain.add(h)
 h+=2
allh=set();dig=[]
for n in ('FiveAnchor','FiveAdd','FiveLast'):
 p=H/(n+'.json.gz');raw=p.read_bytes();d=json.loads(gzip.decompress(raw));ks=set(map(int,d['nodes']));assert not allh&ks;allh.update(ks);dig.append((n,len(ks),len(d['ecpp']),hashlib.sha256(raw).hexdigest()))
 for h0,node in d['nodes'].items():
  P=rows+[(Z,int(h0))];x,s,delta=state(P);rt,es,head,more,ws=node;assert val(s,3)==2
  a=prod(ab(q,h) for q,h in P);filt=prod(nos|{3});
  for q in ws:
   assert delta%q==0;v=val(delta,q);v+=v%2
   while gcd(sig(q,v),filt)>1:v+=2
   a*=ab(q,v)
  assert len(ws)==len(set(ws)) and all(q not in dict(P) and q not in ws and a*ab(q,2)>2 for q in more)
  if n=='FiveLast':assert int(h0)==30 and not es and len(rt)==3 and prod(rt)==sig(Z,30)
assert domain==allh and len(allh)==45;print('PASS 45/45; raw even tail',h,'partition',dig,'3 is fixed and saturated, not absent')
