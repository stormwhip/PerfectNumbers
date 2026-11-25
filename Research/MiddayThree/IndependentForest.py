"""Separate offline root-3 forest verifier. Uses an independent ECPP arithmetic
implementation and bottom-up finite exact Euler-location enumeration.
No discovery imports, no external prime cache, no fixed process-local cutoff.
"""
import json,gzip,sys,math
from pathlib import Path
from functools import lru_cache
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parent/'ThreeChainNext'));from Replay import elliptic,mr
B=10**2400;BAN=7*11*13*19*31
def must(x,t):
 if not x:raise ValueError(t)
def geom(z,f):return (z**(f+1)-1)//(z-1)
def ordp(n,r):
 h=0
 while n%r==0:n//=r;h+=1
 return h
@lru_cache(None)
def checkprime(z,chain):
 k=z
 for n,t,f,a,point in chain:
  must(k==n,'wrong prime');k=elliptic(n,t,f,a,point)
 must(mr(k),'wrong terminal')
def checkfile(path,strict=True):
 return checkdata(json.loads(gzip.decompress(Path(path).read_bytes())),strict=strict)
def checkdata(data,strict=True,select=None):
 must(set(data)=={'row','ecpp'},'fields');r=data['row'];cs=data['ecpp'];must(set(r)=={'e','head','roots','edges'},'row fields');e=r['e'];a=geom(3,e);K=r['roots'];ed=r['edges'];p=dict(ed);must(e>=2 and e%2==0,'nonordinary root');V=set(p)|set(K);must(len(V)==len(K)+len(ed) and all(q not in p for q in K),'duplicate vertex');must(all(a%z==0 for z in K),'bad forced root');must(all(a%q!=0 and w in V for q,w in ed),'bad owner');must(set(cs)=={str(q) for q in V if q>=2**64},'prime bank');must(1<=r['head']<=64,'head')
 for z in V:
  must(z>3 and BAN%z!=0,'forbidden');checkprime(z,tuple((n,t,f,a,tuple(point)) for n,t,f,a,point in cs.get(str(z),[])))
 kids={q:[] for q in V}
 for q,w in ed:kids[w].append(q)
 levels={q:0 for q in K};order=list(K)
 for q in order:
  for k in kids[q]:must(k not in levels,'cyclic');levels[k]=levels[q]+1;order.append(k)
 must(set(levels)==V,'disconnected');universe=3*a*math.prod(p);bases=3**e*a//math.prod(q**ordp(a,q) for q in K);TH=B+1
 @lru_cache(None)
 def outcomes(q,h):
  # Return normal-only, and min with zero or one Euler inside; enumerate
  # the unique exceptional child's slot explicitly, never use two coupons.
  regular=flex=TH
  for euler in (False,True):
   if euler and (q%4!=1 or math.gcd(q+1,BAN)>1):continue
   step=4 if euler else 2;f=h+(1-h)%4 if euler else h+h%2;done=0
   while True:
    power=q**f
    if power>=flex and (euler or power>=regular):break
    S=geom(q,f)
    if math.gcd(S,BAN)>1:f+=step;continue
    if done==r['head']:
     if not euler:regular=min(regular,power)
     flex=min(flex,power);break
    entry=(select.get(q) if isinstance(select,dict) else select[1:] if select and q==select[0] else None)
    if entry and ((entry[0]=='eq' and f!=entry[1]) or (entry[0]=='ge' and f<entry[1])):
     done+=1;f+=step;continue
    odd=S//2 if euler else S;w=odd
    while (g:=math.gcd(universe,w))!=1:w//=g
    forced=[outcomes(k,ordp(odd,k)) for k in kids[q] if odd%k==0];val=power*w*math.prod(x for x,y in forced)
    if euler:flex=min(flex,val)
    else:
     regular=min(regular,val);flex=min([flex,val]+[val//x*y for x,y in forced])
    done+=1;f+=step
  return regular,flex
 forest=[outcomes(z,ordp(a,z)) for z in K];normal=bases*math.prod(x for x,y in forest);low=min([normal]+[normal//x*y for x,y in forest]);must(not strict or low>B,'failed threshold');print('PASS' if low>B else 'OPEN',e,len(K),len(ed),len(cs),'floor',len(str(low))-1,flush=True);return low
if __name__=='__main__':
 for f in sys.argv[1:]:checkfile(f)
