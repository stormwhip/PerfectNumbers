"""Independent optional-Euler recurrence on hardest (7,36) first12/2887^2 forest."""
from pathlib import Path
from functools import cache
from math import prod,gcd
import gzip,json,time
H=Path(__file__).resolve().parents[1]/'ShortSeven';B=10**2400;sg=lambda p,h:(p**(h+1)-1)//(p-1);s0=time.perf_counter();t=4805345109492315767981401
def val(x,p):
 n=0
 while x%p==0:x//=p;n+=1
 return n
pack=json.load(gzip.open(H/'Seven36Twelve.json.gz'));t0=pack['cases']['12'];assert len(t0['cases'])==128 and t0['q']==2887;v=t0['cases']['2'];K,O,head=v['roots'],v['owners'],v['head'];P=[(7,36),(t,12),(2887,2)];X=prod(p**h for p,h in P);S=prod(sg(p,h) for p,h in P);D=S//gcd(S,X);bans={19};assert gcd(X,D)==1
V=set(K)|set(dict(O));kids={z:[] for z in V};
for y,x in O:kids[x].append(y)
childprod={z:prod(k) for z,k in kids.items()};pool=X*D*prod(y for y,x in O)
@cache
def node(z,c):
 base=B+1;flex=B+1
 for odd in [0,1]:
  if odd and (z%4!=1 or any((z+1)%b==0 for b in bans)):continue
  f=c+((1-c)%4 if odd else c%2);step=4 if odd else 2;cnt=0
  while z**f<(flex if odd else base) and cnt<head:
   full=sg(z,f)
   if any(full%b==0 for b in bans):f+=step;continue
   o=full//(odd+1);anon=o
   while (g:=gcd(anon,pool))>1:anon//=g
   deps=[node(y,val(o,y)) for y in kids[z] if o%y==0] if gcd(o,childprod[z])>1 else []
   n=z**f*anon*prod(q for q,_ in deps);v=n
   if not odd:
    base=min(base,n);v=min([v,*[n//q*w for q,w in deps]])
   flex=min(flex,v);cnt+=1;f+=step
  flex=min(flex,z**f)
  if not odd:base=min(base,z**f)
 return base,flex
vals=[node(z,val(D,z)) for z in K];n=X*D//prod(z**val(D,z) for z in K)*prod(m for m,w in vals);lb=min([n,*[n//m*w for m,w in vals]]);assert lb>B and len(str(lb))-1==2403
print('PASS independent recurrence',len(K),len(O),head,'last branch floor',len(str(lb))-1,'seconds',round(time.perf_counter()-s0,3))
