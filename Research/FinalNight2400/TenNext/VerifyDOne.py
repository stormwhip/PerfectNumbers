"""D-one: exhaustive compulsory-prime tree, with safe dynamic support bans."""
from pathlib import Path
from math import prod,gcd
from fractions import Fraction
from functools import cache
from itertools import count
from collections import Counter
import json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Verify46 import sig,price,q,A6,B,pc,prime as oldprime
assert __debug__
D=1252106774386973;oldprime(D);assert sig(q,6)%D==0
book=json.loads((H/'D1Primes.json').read_bytes());seen=set()
@cache
def prime(p):
 assert type(p)==int and p>2;n=p
 if p>=2**64:
  chain=book[str(p)];assert chain;seen.add(str(p))
  for row in chain:assert row[0]==n;n=pc.level(*row)
 assert pc.prime64(n)
@cache
def val(n,p):
 v=0
 while n%p==0:v+=1;n//=p
 return v
@cache
def ab(p,e):return Fraction(sig(p,e),p**e)
P=[(19,46),(q,6),(D,1)];V,Q,exc,(X,C,blocks)=price(P,[2,4,0]);M=prod(p**(c*w) for p,c,w in Q);assert Q==[(19,46,2),(q,5,4)]
S=prod(sig(p,e) for p,e in P)//2;I=prod(ab(p,e) for p,e in P)
@cache
def gain(p,h,bad):
 best=None
 for f in count(h+h%2,2):
  a=p**f
  if best is not None and a>=best*M:return best*exc.get(p,1)
  if any((f+1)%u==0 if p%u==1 else pow(p,f+1,u)==1 for u in bad):continue
  n=1
  for t,c,w in Q:
   if p%t==1:k=val(f+1,t)
   elif pow(p,f+1,t)!=1:k=0
   else:
    lim=t**(c+1);rem=(pow(p,f+1,lim)-1)%lim;k=val(rem,t) if rem else c+1
   if k>c:break
   n*=t**(w*k)
  else:
   b=Fraction(a,n);best=b if best is None else min(best,b)
small=[u for u in range(3,53,2) if pc.prime64(u)];stats=Counter();rootf={43,71,1609126413025321,A6,3,11,17,371986563989}
for r in rootf:prime(r);assert C%r==0

def walk(T,z,K,S,I,rows,known):
 Y=S//gcd(K,S)
 if gcd(Y,K)>1 or K*Y>B:assert T=='raw';stats['raw']+=1;return
 F={r:val(Y,r) for r in known if r not in rows and Y%r==0};bad=set()
 while True:
  hs={}
  for r,h in F.items():
   for f in count(h+h%2,2):
    if all((f+1)%u if r%u==1 else pow(r,f+1,u)!=1 for u in bad):break
   hs[r]=f
  lowI=I*prod(ab(r,f) for r,f in hs.items())
  if lowI>2:assert T=='abund';stats['abund']+=1;return
  new={u for u in small if u not in rows and u not in hs and lowI*ab(u,2)>2}
  if new<=bad:break
  bad|=new
 bad=tuple(sorted(bad));nets={r:gain(r,h,bad) for r,h in hs.items()};U=z*prod(nets.values())
 if U>B:assert T=='gain';stats['gain']+=1;return
 assert isinstance(T,list) and len(T)==2; r,cases=T;assert r in hs;stats['split']+=1;other=U/nets[r];done=set()
 for f in count(hs[r],2):
  if other*gain(r,f,bad)>B or K*r**f>B:break
  a=sig(r,f)
  if any(a%u==0 for u in bad):continue
  xs,child=cases[str(f)];done.add(str(f));assert sorted(set(xs))==xs and r not in xs and not set(xs)&rows.keys()
  for p in xs:prime(p);assert a%p==0
  exact=Fraction(r**f,prod(t**(w*val(a,t)) for t,c,w in Q))*exc.get(r,1)
  walk(child,z*exact,K*r**f,S*a,I*ab(r,f),rows|{r:f},set(F)|set(xs))
 assert set(cases)==done
packet=json.loads((H/'D1Scout.json').read_bytes());walk(packet['tree'],V,X,S,I,dict(P),rootf);assert seen==set(book) and stats=={'split':140,'abund':11,'gain':201}
print('PASS q^6,D^1: zero open; 140 splits, 201 net-price leaves, 11 abundance leaves;',len(seen),'ECPP certificates.')
