"""Independent 31,240 final high-order prime leaf, full split domains and root ledger."""
import json,gzip,sys,time
from pathlib import Path
from fractions import Fraction
from math import gcd,prod,isqrt
from collections import Counter
H=Path(__file__).resolve().parents[1]/'ThirtyOne268/Root240';B=10**2400;sg=lambda p,h:(p**(h+1)-1)//(p-1);t=4339;z=366204586019;P=[(31,240),(t,82),(z,36)];s0=time.perf_counter();banned=19*7*11
def state(L):
 X=prod(p**f for p,f in L);raw=prod(sg(p,f) for p,f in L);odd=sum(f%2 for p,f in L);S=raw//2**odd;D=S//gcd(S,X);return X,D,gcd(raw*X,banned)==1 and gcd(X,D)==1 and raw<=2*X and X*D<=B and odd<=1 and all(not f%2 or p%4==f%4==1 for p,f in L)
def dom(L,q):
 X,D,ok=state(L);assert ok and not D%q and q not in dict(L);c=0
 while not D%q:c+=1;D//=q
 res=[]
 while X*D*q**c<=B:
  if state(L+[(q,c)])[2]:res.append(c)
  c+=1
 return res,c
a=json.load(gzip.open(H/'Forest.json.gz'));first,tail=dom(P[:1],t);assert len(first)==62 and tail==465 and set(map(int,a['cases']))==set(first);counts=Counter();todo=[(P[:1]+[(t,int(k))],v) for k,v in a['cases'].items()];special=[]
while todo:
 path,node=todo.pop();k=node['type'];counts[k]+=1
 if k=='split':
  q=node['q'];es,_=dom(path,q);assert set(es)==set(map(int,node['cases']));todo.extend((path+[(q,e)],node['cases'][str(e)]) for e in es)
 elif k=='high':special.append(path)
 else:assert k in ('price','forest','square')
assert special==[P]
fs=(83,11743,187861);assert 2*prod(fs)==z-1 and all(all(n%d for d in range(2,isqrt(n)+1)) for n in (z,*fs)) and z>8000;X,D,ok=state(P);S=prod(sg(p,n) for p,n in P);assert ok and S%z==0 and S%z**2
m=z;g=next(g for g in range(2,z) if (v:=pow(g,(z-1)//83,z))!=1);u=pow(g,(z-1)//83,z);rs=[pow(u,i,z) for i in range(1,83)];exc={}
for i in range(1,36):
 for r in rs:
  if r<3 or not r%2 or (r.bit_length()-1)*82>=m.bit_length()*70:continue
  if r**82<m**70:exc[r]=max(exc.get(r,1),Fraction(m**70,r**82))
 rs=[r+m*((-((pow(r,83,m*z)-1)//m)*pow(83*pow(r,82,z),-1,z))%z) for r in rs];m*=z
U=prod(exc.values(),start=Fraction(1));U=-(-U.numerator//U.denominator);blocks=[]
for r,h in P:
 v=sg(r,h)
 while (gg:=gcd(v,X))>1:v//=gg
 blocks.append(v)
# Instead of connected components use one largest-valuation block: its contribution times other pairwise gcds bounds any prime-power overlap.
Hmax=max(v*prod(gcd(v,b) for j,b in enumerate(blocks) if j!=k) for k,v in enumerate(blocks));stats=[0,0,0]
for j in range(36):
 m=z**j;Q=2*m-1;R=z**(70*(35-j))
 if X*Q*R>B*U:stats[0]+=1;continue
 for r,h in P:
  b=sg(r,h);k=b*pow(Q,-1,4*m)%(4*m) or 4*m;assert all(b%c for c in range(k,b//Q+1,4*m))
 if X*D*Q>B:stats[1]+=1;continue
 for u in range(36-j):
  v=z**u;assert 2*X*D*Q**2*v>3*B*Hmax or X*D*Q*v**70>B*Hmax*U or 2*X*Q**2*R>3*B*U*v**69
 stats[2]+=1
G=H.parents[2]/'GeminiFrontier';sh=json.loads((G/'ShardToKeys.json').read_bytes());iv=json.loads((G/'KeyToShards.json').read_bytes());assert [(n,zz) for n,zz in sh.items() if [31,240] in zz]==[('P31_I00051',[[31,240]])] and iv['31,240']==['P31_I00051'];print('PASS complete domain',len(first),'tail',tail,counts,'high-order deficit labels',len(exc),'Euler windows',stats,'seconds',round(time.perf_counter()-s0,3))
