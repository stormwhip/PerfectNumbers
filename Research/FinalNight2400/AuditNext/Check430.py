"""Independent raw forest-domain walk, proof-gap binding and parity argument for 7,430."""
from pathlib import Path
from math import prod,gcd,isqrt
import json,gzip,collections,time
s0=time.perf_counter();H=Path(__file__).resolve().parents[1]/'Seven430';G=H.parents[1]/'GeminiFrontier';B=10**2400;Q=3602407438103418087310110702859943140744217508967;W=62619225867394162638521;P=((7,430),(Q,4));sg=lambda p,h:(p**(h+1)-1)//(p-1);stats=collections.Counter();tails=[]
def state(L):
 X=prod(p**f for p,f in L);raw=prod(sg(p,f) for p,f in L);odd=sum(f%2 for p,f in L);S=raw//2**odd;D=S//gcd(S,X);return X,D,gcd(19,X*raw)==1 and raw<=2*X and gcd(X,D)==1 and X*D<=B and odd<=1 and all(not f%2 or p%4==f%4==1 for p,f in L)
def dom(L,q):
 X,D,ok=state(L);assert ok and not D%q and q not in dict(L);f=0;live=[]
 while D%q==0:f+=1;D//=q
 while X*D*q**f<=B:
  if state(L+((q,f),))[2]:live.append(f)
  f+=1
 tails.append(f);return live
assert dom(P[:1],Q)==[2,4,6,8,10,12,14,16];K=json.loads((H/'Pack4.json').read_bytes());assert K['q']==W

def walk(P,node):
 assert node['type']!='open';kind=node['type'];stats[kind]+=1
 if kind=='split':
  q=node['q'];L=dom(P,q);assert set(L)==set(map(int,node['cases']))
  for f in L:walk(P+((q,f),),node['cases'][str(f)])
 elif kind=='square':
  assert P==((7,430),(Q,4),(W,6),(1112651,52),(14969459,16),(17155781,16));X,D,ok=state(P);assert ok;blocks=[]
  for p,e in P:
   s=sg(p,e)
   while (g:=gcd(s,X))!=1:s//=g
   blocks.append(s)
  assert prod(blocks)==D and len(blocks)==6 and all(isqrt(y)**2<y and all(gcd(y,z)==1 for z in range(2,1001)) for y in blocks)
  assert all(gcd(y,w)==1 for i,y in enumerate(blocks) for w in blocks[i+1:]);assert 10**15 > B//(X*D)==10368506209179
 elif kind=='price':assert P==((7,430),(Q,4),(W,9))
 else:assert kind=='forest'
walk(P,dict(type='split',q=W,cases=K['cases']));assert stats['price']==stats['square']==1
sh=json.loads((G/'ShardToKeys.json').read_bytes());iv=json.loads((G/'KeyToShards.json').read_bytes());assert [(n,z) for n,z in sh.items() if [7,430] in z]==[('P7_I00082',[[7,430]])] and iv['7,430']==['P7_I00082'];print('PASS root',tails[0],'Q4/W tail',tails[1],'Q4',stats,'square R budget',10368506209179,'seconds',round(time.perf_counter()-s0,3))
