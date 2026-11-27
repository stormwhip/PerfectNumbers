"""Independent complete split inventory for (3,6), first 1093^156, without repo imports."""
import json,gzip,hashlib
from math import gcd,prod
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parents[1]/'Three';path=H/'Almost156.json.gz';d=json.load(gzip.open(path));B=10**2400;bad=7*11*13*19*31
sg=lambda q,e:(q**(e+1)-1)//(q-1)
def state(P):
 X=prod(q**e for q,e in P);raw=prod(sg(q,e) for q,e in P);odd=sum(e%2 for q,e in P);S=raw//2**odd;D=S//gcd(X,S);return X,D,gcd(bad,X*raw)==1 and gcd(D,X)==1 and X*D<=B and raw<=2*X and odd<=1 and all(not e%2 or q%4==e%4==1 for q,e in P)
def domain(P,r):
 X,d,ok=state(P);assert ok and d%r==0 and r not in dict(P);h=0;L=[]
 while d%r==0:d//=r;h+=1
 while X*d*r**h<=B:
  if state(P+[(r,h)])[2]:L.append(h)
  h+=1
 return L,h
P=[(3,6),(1093,156)];q=2035349;L,tail=domain(P,q);assert len(L)==62 and 46 in L and 66 in L;count=Counter();gaps=[];inv=[]
def go(P,n):
 if n is None:gaps.append(P);return
 k=n['type'];count[k]+=1
 if k=='split':
  q=n['q'];LL,_=domain(P,q);assert set(LL)==set(map(int,n['cases']))
  for h in LL:go(P+[(q,h)],n['cases'][str(h)])
 elif k=='inverse':inv.append(P)
 else:assert k in ('fastpair','forest')
go(P,d['tree']);assert d['tree']['q']==q and gaps==[P+[(q,46)]] and inv==[P+[(q,66)]];assert count=={'split':118,'forest':3408,'fastpair':28,'inverse':1};print('PASS primary 156: complete split domains,',len(L),'first secondary; tail',tail,'unique unresolved exponent 46, h=66 correctly bound; stats',count,'prime book',len(d['ecpp']))
