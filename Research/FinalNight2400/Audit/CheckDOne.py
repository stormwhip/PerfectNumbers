"""Independent D^1 finite-tree arithmetic; imports the static two-target price only."""
from pathlib import Path
from fractions import Fraction as F
from itertools import count
from functools import cache
from math import gcd,prod
from collections import Counter
import sys,json,time
start=time.perf_counter();H=Path(__file__).resolve().parent.parent/'TenNext';sys.path.insert(0,str(H));from Price46 import price
B=10**2400;Sg=lambda p,e:(p**(e+1)-1)//(p-1);A=lambda p,e:F(Sg(p,e),p**e);q=Sg(19,46);D=1252106774386973;P=((19,46),(q,6),(D,1));V,T,E,_=price(P,[2,4,0]);M=prod(p**(c*w) for p,c,w in T);small={3,5,7,11,13,17,19,23,29,31,37,41,43,47};K0={43,71,1609126413025321,2247860239402417332211,3,11,17,371986563989};counts=Counter()
@cache
def net(r,f):
 sig=Sg(r,f);u=1
 for p,c,w in T:
  a=gcd(p**(c+1),sig)
  if a==p**(c+1):return None
  u*=a**w
 return F(r**f,u)*E.get(r,1)
@cache
def gain(r,h,bans):
 v=None;mult=E.get(r,1)
 for f in count(h+h%2,2):
  if v is not None and F(r**f,M)*mult>=v:return v
  if gcd(Sg(r,f),bans)==1 and (n:=net(r,f)) is not None:v=n if v is None else min(v,n)
def vpow(y,r):
 h=0
 while y%r==0:y//=r;h+=1
 return h
book=json.loads((H/'D1Scout.json').read_bytes());
def go(node,extra,known):
 full=P+extra;X=prod(p**e for p,e in full);S=prod(Sg(p,e) for p,e in full)//2;Y=S//gcd(X,S);rows=dict(full);I=F(2*S,X);assert gcd(X,Y)==1 and X*Y<=B
 hs={r:vpow(Y,r) for r in known if r not in rows and Y%r==0};ban=set()
 while True:
  bans=prod(ban);mn={r:next(f for f in count(h+h%2,2) if gcd(Sg(r,f),bans)==1) for r,h in hs.items()};a=I*prod(A(r,f) for r,f in mn.items());
  if a>2:assert node=='abund';counts['abundance']+=1;return
  nb={p for p in small if p not in rows and p not in mn and a*A(p,2)>2}-ban
  if not nb:break
  ban|=nb
 z=V*prod(net(r,f) for r,f in extra);g=z*prod(gain(r,h,bans) for r,h in mn.items())
 if node=='gain':assert g>B;counts['gain']+=1;return
 assert g<=B;counts['split']+=1;r,cases=node;base=g/gain(r,mn[r],bans);done=set()
 for f in count(mn[r],2):
  if X*r**f>B or base*gain(r,f,bans)>B:break
  sig=Sg(r,f)
  if gcd(sig,bans)>1:continue
  done.add(str(f));ns,child=cases[str(f)];assert all(sig%s==0 for s in ns) and not(set(ns)&(set(rows)|{r}));go(child,extra+((r,f),),set(hs)|set(ns))
 assert done==set(cases)
go(book['tree'],(),K0);assert counts=={'gain':201,'split':140,'abundance':11};print('PASS independently reconstituted all D^1 nodes and exact tail tests',counts,'elapsed',round(time.perf_counter()-start,3))
