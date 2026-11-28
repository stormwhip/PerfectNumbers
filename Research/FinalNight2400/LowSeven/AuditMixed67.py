"""No project imports. Independent Teichmuller lifting and reversed CRT for the common cubic loss."""
from math import gcd,prod,isqrt
from fractions import Fraction
from pathlib import Path
import json,gzip,hashlib
p,r,t=7,67,572749682520506652634407616247;D={7:[2,3],67:[2,3,11]};small=prod(x for x in range(3,2000,2) if all(x%v for v in range(2,isqrt(x)+1)))
def roots(q,o,cap):
 g=next(z for z in range(2,q) if all(pow(z,(q-1)//x,q)!=1 for x in D[q]));a=pow(g,(q-1)//o,q);m=q;out=[(1,[0])]
 for i in range(cap):
  out.append((m,[pow(a,j,m) for j in range(1,o) if gcd(j,o)==1]));m*=q;a=pow(a,q,m)
 return out
E={};H={}
def add(z,n,h,tab):
 if z<3 or z%2==0 or z in (7,19,r,t) or (z.bit_length()-1)*h>=n.bit_length():return
 d=z**h
 if d>=n or (z>2000 and gcd(z,small)>1) or pow(2,z-1,z)!=1:return
 tab[z]=max(tab.get(z,1),Fraction(n,d))
A=roots(p,3,438);C=roots(r,3,300)
for m,ls in A:
 inv=1;step=pow(r,-1,m)
 for n,rs in C:
  goal=(m*n)**19
  for y in rs:
   for x in ls:add(y+n*((x-y)*inv%m),goal,20,E)
  inv=inv*step%m
for o in [11,33]:
 for m,ls in roots(r,o,300)[1:]:
  for x in ls:add(x,m**19,10*(o-3),H)
U=prod(E.values(),start=Fraction(1))*prod(H.values(),start=Fraction(1));hh=Path(__file__).resolve().parents[1]/'SevenNext';fp=hh/'Mixed67Primes.json.gz';raw=fp.read_bytes();z=json.loads(gzip.decompress(raw));cases=sorted(map(int,z['nodes']['67']));assert cases==[192,194,196,198,202,204,206,208,210,224];old={148,172,190,200,212,214,216,218,220,222,226,294,296,298,300}|set(range(228,293,2));assert not old&set(cases)
seen=set()
for v in cases:
 sig=(67**(v+1)-1)//66;ls=z['nodes']['67'][str(v)];assert len(set(ls))==len(ls) and all(sig%a==0 and a not in (7,19,r,t) for a in ls);seen.update(a for a in ls if a>=2**64)
assert {str(a) for a in seen}==set(z['ecpp']);print('PASS independent mixed U',len(E),len(H),'ceil',-(-U.numerator//U.denominator),'U fraction digest',hashlib.sha256((str(U.numerator)+'/'+str(U.denominator)).encode()).hexdigest(),'large',len(seen),'blob',hashlib.sha256(raw).hexdigest())
