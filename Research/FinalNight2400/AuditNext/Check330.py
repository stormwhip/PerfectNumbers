"""Direct canonical domain, final Euler-minimum abundance bans and two-state recurrence for (19,330)."""
from pathlib import Path
import json,gzip,time
from math import gcd,prod
from fractions import Fraction
from functools import cache
H=Path(__file__).resolve().parents[1]/'ShortNineteen';B=10**2400;sg=lambda p,h:(p**(h+1)-1)//(p-1);t=1214428680506010004551311201724184433986966434253654794712076383;r=2649006202622389754026474949684537136117722932291062868195158132223440533168779423867212541;a=541060314202200985634836209806257;s0=time.perf_counter()
def state(L):
 X=prod(p**f for p,f in L);raw=prod(sg(p,f) for p,f in L);odd=sum(f%2 for p,f in L);S=raw//2**odd;D=S//gcd(S,X);return X,D,gcd(X,D)==1 and raw<=2*X and X*D<=B and odd<=1 and all(not f%2 or p%4==f%4==1 for p,f in L)
def dom(L,q):
 X,d,ok=state(L);assert ok and d%q==0;f=0;z=[]
 while d%q==0:d//=q;f+=1
 while X*d*q**f<=B:
  if state(L+[(q,f)])[2]:z.append(f)
  f+=1
 return z,f
def val(x,p):
 n=0
 while x%p==0:x//=p;n+=1
 return n
P=[(19,330)];L,t0=dom(P,t);assert L==[2,4,6,8,10,12];P.append((t,2));R,t1=dom(P,r);assert R==[1,2,4,5,6,8];P.append((r,2));L,t2=dom(P,a);assert L==[1,2,4,5,6,8,9,10,12,13,14,16,17];P.append((a,6));X,D,_=state(P);S=prod(sg(z,e) for z,e in P);packet=json.load(gzip.open(H/'LastSix330.json.gz'));K,O,ban=packet['cases']['6'];assert len(K)==5 and len(O)==45 and set(ban)=={5,11} and all(D%z==0 for z in K);v=sg(a,6);assert v%(K[-1]*K[-2])==0
# Independently reconstruct necessary forbidden labels by strict minimum over all allowable Euler choices.
bans=set()
while set(ban)!=bans:
 def first(z,h,odd):
  f=h+((1-h)%4 if odd else h%2);step=4 if odd else 2
  while any(sg(z,f)%b==0 for b in bans):f+=step
  return f
 def I(z,h):return Fraction(sg(z,h),z**h)
 out=Fraction(S,X);rates=[Fraction(1)]
 for z in K:
  h=val(D,z);ordinary=I(z,first(z,h,False));out*=ordinary
  if z%4==1 and all((z+1)%b for b in bans):rates.append(I(z,first(z,h,True))/ordinary)
 nxt={b for b in ban if b not in bans and out*min(rates)*I(b,1 if b%4==1 else 2)>2};assert nxt;bans|=nxt
V=set(K)|set(dict(O));kids={z:[] for z in V};
for y,x in O:kids[x].append(y)
childprod={z:prod(k) for z,k in kids.items()};pool=X*D*prod(y for y,x in O)
@cache
def node(z,c):
 base=B+1;flex=B+1
 for odd in [0,1]:
  if odd and (z%4!=1 or any((z+1)%b==0 for b in bans)):continue
  f=c+((1-c)%4 if odd else c%2);step=4 if odd else 2;cnt=0
  while z**f<(flex if odd else base) and cnt<128:
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
vals=[node(z,val(D,z)) for z in K];n=X*D//prod(z**val(D,z) for z in K)*prod(m for m,w in vals);lb=min([n,*[n//m*w for m,w in vals]]);assert lb>B and len(str(lb))-1==2401
G=H.parents[1]/'GeminiFrontier';sh=json.loads((G/'ShardToKeys.json').read_bytes());iv=json.loads((G/'KeyToShards.json').read_bytes());assert [(n,z) for n,z in sh.items() if [19,330] in z]==[('P19_I00065',[[19,330]])] and iv['19,330']==['P19_I00065'];print('PASS complete 3-level domains, tails',t0,t1,t2,'new dynamic bans',bans,'free-Euler floor',len(str(lb))-1,'seconds',round(time.perf_counter()-s0,3))