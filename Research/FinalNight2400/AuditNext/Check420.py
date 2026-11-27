"""Direct domain binding and two-mode independent forest evaluation at 19,420/f4/r2."""
from pathlib import Path
import json,gzip,time
from math import gcd,prod
from functools import cache
H=Path(__file__).resolve().parents[1]/'ShortNineteen';B=10**2400;sg=lambda p,h:(p**(h+1)-1)//(p-1);t=28174642921954703272833689609691232580811241064837460583;r=72688845161;a=200433813211;s0=time.perf_counter()
def state(L):
 X=prod(p**f for p,f in L);raw=prod(sg(p,f) for p,f in L);odd=sum(f%2 for p,f in L);S=raw//2**odd;D=S//gcd(S,X);return X,D,gcd(X,D)==1 and raw<=2*X and X*D<=B and odd<=1 and all(not f%2 or p%4==f%4==1 for p,f in L)
def dom(L,q):
 X,d,ok=state(L);assert ok and d%q==0;f=0;z=[]
 while d%q==0:d//=q;f+=1
 while X*d*q**f<=B:
  if state(L+[(q,f)])[2]:z.append(f)
  f+=1
 return z,f
P=[(19,420)];L,tail=dom(P,t);assert L==[2,4,6,8,10,12];P.append((t,4));L2,tail2=dom(P,r);assert len(L2)==32 and set(L2)-{1,2,4}==set(map(int,json.load(gzip.open(H/'Four420.json.gz'))['cases']));P.append((r,2));L3,tail3=dom(P,a);d=json.load(gzip.open(H/'SecondaryTwo.json.gz'));assert L3==list(range(2,41,2)) and set(L3)==set(map(int,d['cases']))
def val(x,p):
 n=0
 while x%p==0:x//=p;n+=1
 return n
floors=[]
for h in L3:
 X,D,_=state(P+[(a,h)]);K,O=d['cases'][str(h)];V=set(K)|set(dict(O));kids={z:[] for z in V};
 for y,x in O:kids[x].append(y)
 childprod={z:prod(v) for z,v in kids.items()};pool=X*D*prod(x for x,y in O);lock=h in (10,12,18,22)
 @cache
 def node(z,c):
  base=B+1;flex=B+1
  for odd in [0,1]:
   if odd and (lock or z%4!=1):continue
   f=c+((1-c)%4 if odd else c%2);step=4 if odd else 2;cnt=0
   while z**f<(flex if odd else base) and cnt<128:
    o=sg(z,f)//(odd+1);anon=o
    while (g:=gcd(anon,pool))>1:anon//=g
    deps=[node(y,val(o,y)) for y in kids[z] if o%y==0] if gcd(o,childprod[z])>1 else []
    n=z**f*anon*prod(q for q,_ in deps);v=n
    if not odd:
     base=min(base,n);v=min([v,*[n//q*w for q,w in deps]])
    flex=min(flex,v);cnt+=1;f+=step
   flex=min(flex,z**f)
   if not odd:base=min(base,z**f)
  return base,flex
 vals=[node(z,val(D,z)) for z in K];lb=X*D//prod(z**val(D,z) for z in K)*prod(v for v,w in vals)
 if not lock:lb=min([lb,*[lb//v*w for v,w in vals]])
 assert lb>B;floors.append(len(str(lb))-1)
G=H.parents[1]/'GeminiFrontier';sh=json.loads((G/'ShardToKeys.json').read_bytes());iv=json.loads((G/'KeyToShards.json').read_bytes());assert [(n,z) for n,z in sh.items() if [19,420] in z]==[('P19_I00080',[[19,420]])] and iv['19,420']==['P19_I00080'];print('PASS first/second/tertiary raw tails',tail,tail2,tail3,'independent 20 forests min',min(floors),'seconds',round(time.perf_counter()-s0,3))
