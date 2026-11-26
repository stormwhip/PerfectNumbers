"""Alternate arithmetic for support forests. Independent of Compose, ForestReplay and CheckMaskTree; shares only PrimeCheck's pure ECPP kernel."""
from pathlib import Path
from functools import cache
import argparse,sys,json,gzip
from math import gcd,prod
assert __debug__;H=Path(__file__).resolve().parent;cli=argparse.ArgumentParser();cli.add_argument('file',type=Path);cli.add_argument('--repo',type=Path,default=H.parents[1]);a=cli.parse_args();sys.path.insert(0,str(a.repo.resolve()/'Research/RootFiveNext'));import PrimeCheck as pc
B=10**2400;O=(19,7,11,31,13,3,5,17);v=json.load(gzip.open(a.file));p,e=v['p'],v['e'];assert p==3 and type(e)==int and 0<e<=7000 and e%2==0
@cache
def sigma(q,h):return (q**(h+1)-1)//(q-1)
def val(n,p):
 k=0
 while n%p==0:k+=1;n//=p
 return k
seen=set();stats=[0,0,0]
@cache
def prime(q):
 assert type(q)==int and q>2;n=q
 if n>=2**64:
  seen.add(str(q))
  for r in v['ecpp'][str(q)]:assert r[0]==n;n=pc.level(*r)
 assert pc.prime64(n)
def state(P,bad):
 X=prod(q**h for q,h in P);Z=prod(sigma(q,h) for q,h in P);odd=sum(h%2 for q,h in P);t=Z//(2**odd);D=t//gcd(X,t);dead=odd>1 or gcd(prod(q for q,h in P)*t,bad)!=1 or gcd(X,D)>1 or Z>2*X or X*D>B;return X,D,dead,odd

def walk(P,H,n):
 bad=prod(set(O)-H);X,D,dead,odd=state(P,bad);assert not dead;S=set(dict(P))
 if n['type']=='split':
  q=n['q'];prime(q);assert q not in S and (q in H or D%q==0) and bad%q!=0;c=val(D,q);f=max(c,1);used=set();st=X*(D//q**c);stats[1]+=1
  while st*q**f<=B:
   if (not f%2 or q%4==f%4==1 and not odd) and gcd(sigma(q,f),bad)==1:
    ch=P+[(q,f)]
    if state(ch,bad)[2]:stats[2]+=1
    else:used.add(str(f));walk(ch,H,n['cases'][str(f)])
   f+=1
  assert set(n['cases'])==used;return
 assert n['type']=='forest';stats[0]+=1;roots=set(n['roots']);edges=dict(n['owners']);V=roots|set(edges);assert len(roots)==len(n['roots']) and len(edges)==len(n['owners']) and not roots&set(edges);assert not V&(S|(set(O)-H));assert all(q in H or D%q==0 for q in roots);assert all(D%q!=0 and q not in H and z in V for q,z in edges.items());kids={q:[] for q in V};
 for q in V:prime(q)
 for q,z in edges.items():kids[z].append(q)
 st=list(roots);visited=set()
 while st:
  z=st.pop();assert z not in visited;visited.add(z);st.extend(kids[z])
 assert visited==V;U=X*D*prod(edges)*prod(H-S);head=n['head'];assert type(head)==int and 1<=head<=1024
 @cache
 def block(q,c):
  zero=flex=B+1
  for sp in (0,1):
   if sp and (odd or q%4!=1 or gcd(q+1,bad)>1):continue
   f=c+((1-c)%4 if sp else c%2);step=4 if sp else 2;cnt=0
   while cnt<head and q**f<(flex if sp else zero):
    sig=sigma(q,f)
    if gcd(sig,bad)==1:
     cnt+=1;z=t=sig//(1+sp)
     while (g:=gcd(t,U))>1:t//=g
     sub=[block(y,val(z,y)) for y in kids[q] if z%y==0];raw=q**f*t*prod(x for x,y in sub)
     if not sp:
      zero=min(zero,raw);raw=min([raw]+[raw//x*y for x,y in sub])
     flex=min(flex,raw)
    f+=step
   flex=min(flex,q**f)
   if not sp:zero=min(zero,q**f)
  return zero,flex
 sub=[block(q,max(1,val(D,q))) for q in roots];base=X*(D//prod(q**val(D,q) for q in roots))*prod(x for x,y in sub);assert min([base]+[base//x*y for x,y in sub])>B;block.cache_clear()
keys=set()
for h in [{3},{3,5},{3,17},{3,5,17}]:
 k=','.join(map(str,sorted(h)));keys.add(k);walk([(3,e)],h,v['supports'][k]);print('support',k,'PASS',stats,flush=True)
assert keys==set(v['supports']) and seen==set(v['ecpp']);print('verified',p,e,stats,flush=True)
