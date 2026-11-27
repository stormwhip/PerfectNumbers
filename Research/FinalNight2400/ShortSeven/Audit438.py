"""Independent finite sets and ordinary-source price-loss table for 37 conditional 7^438 cuts."""
from pathlib import Path
from math import gcd,prod,isqrt
from fractions import Fraction
import json,gzip,hashlib
H=Path(__file__).resolve().parents[1]/'SevenNext';F=H/'New438Credits.json.gz';d=json.loads(gzip.decompress(F.read_bytes()));t=572749682520506652634407616247;B=10**2400
expect={67:[148,172,190,200,212,214,216,218,220,222,226,294,296,298,300],27431:list(range(30,73,2))}
# One scalar kernel is reused for the 67 family while forbidding 27431 as a possible 7-loss label. It cannot supply 7 from any even length: order_7(27431)=6.
assert pow(27431,3,7)!=1 and 27431%7!=1
seen=set()
for rr,hs in expect.items():
 f={67:10,27431:12}[rr];old=set(range(228,293,2)) if rr==67 else set(range(74,111,2));assert not old&set(hs) and set(map(int,d['nodes'][str(rr)]))==set(hs)
 for h in hs:
  fs=d['nodes'][str(rr)][str(h)];S0=((7**439-1)//6)*((t**(f+1)-1)//(t-1));ss=(rr**(h+1)-1)//(rr-1);assert len(fs)==len(set(fs)) and all(ss%z==0 and z not in [7,t,rr,19] for z in fs);seen.update(z for z in fs if z>=2**64);assert S0%t==0 and S0%(t*t)!=0 and ss%t!=0 and S0%rr==0 and S0%(rr*rr)!=0
assert set(map(str,seen))==set(d['ecpp']) and len(seen)==42
# Independent Teichmuller lifting; all primitive roots generated at each level, enumerating odd orders by divisors up to the 5100 length bound.
def loss(s,cap,w):
 orders=[o for o in range(3,5100,2) if (s-1)%o==0];E={};
 for o in orders:
  if 3**(o-1)>=s**(w*cap):continue
  fac=[j for j in range(2,o+1) if o%j==0 and all(j%z for z in range(2,isqrt(j)+1))];g=next(pow(y,(s-1)//o,s) for y in range(2,500) if all(pow(pow(y,(s-1)//o,s),o//j,s)!=1 for j in fac));m=s
  for a in range(1,cap+1):
   for j in range(1,o):
    if gcd(j,o)>1:continue
    r=pow(g,j,m)
    if r>=3 and r%2 and r not in (7,19,t,27431) and (r.bit_length()-1)*(o-1)<(m**w).bit_length() and r**(o-1)<m**w and pow(2,r-1,r)==1:E[r]=max(E.get(r,1),Fraction(m**w,r**(o-1)))
   m*=s;g=pow(g,s,m)
 return prod(E.values(),start=Fraction(1)),len(E)
print('PASS exact 15+22 new h and emitted credit labels; large labels',len(seen),'SHA',hashlib.sha256(F.read_bytes()).hexdigest());
for s,c,w in [(7,438,2),(27431,71,4)]:
 u,n=loss(s,c,w);print('price',s,n,'ceil',-(-u.numerator//u.denominator))
