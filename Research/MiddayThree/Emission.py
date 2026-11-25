"""Independent incoming-3-cyclotomic tariff, for a=1, s>0 and q=2 mod 3.
For each ordinary supplier z contributing j units, its exact sigma contains
all Phi_{3^i}(z) for 1<=i<=j. Divide each by its single factor 3.
Every remaining prime is 1 mod 3: neither q nor an emitting r=2 mod 3 can
be among them. The product with A divides N even with intersecting supports.
"""
import sys,json
from pathlib import Path
from math import prod
from functools import cache
from itertools import accumulate
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parent/'Nov25/Three'));import SourceUnit as U
B=10**2400;BN=(7,11,13,19,31)
@cache
def tariff(e,limit=100000):
 # For z>limit the first increment already costs (z^2+z+1)/3;
 # each higher increment is larger. Truncation is DOWN, including phantom slots.
 stop=(limit**2+limit+1)//3; items=[]
 for z in U.I.SUP:
  if z>limit:break
  a=z
  while True:
   n=a*a+a+1
   if any(n%l==0 for l in BN):break
   x=n//3
   if x>stop:break
   items.append(x);a=a**3
 return [1,*accumulate(sorted(items+[stop]*e)[:e],int.__mul__)]
def scan(e):
 A=(3**(e+1)-1)//2;pe=3**e;P=3*pe;one,high=U.J.audit(e,[]);assert one and not high and min(one)>0
 T=tariff(e);rows=[]
 for s in sorted(one):
  Y=3**s;t=T[e-s]
  for tag in (1,2):
   q=U.euler_least(s,tag);den=pe*A*q*t
   # If source r=2 mod 3, debit its cost over A without touching T.
   ext=5*B<=4*den*q
   ins=den*q*Y>=B*max(P,q)*(P//Y+4)
   rows.append([s,tag,den>B,ext,ins])
 return {'e':e,'windows':len(one),'total':len(rows),'incoming_only':sum(x[2] for x in rows),'external_blue':sum(x[2] or x[3] for x in rows),'internal_blue':sum(x[2] or x[4] for x in rows),'cells':rows}
if __name__=='__main__':
 out=[]
 for e in (1162,1108,990,970,856):
  row=scan(e);out.append(row);print({k:v for k,v in row.items() if k!='cells'},flush=True)
 (H/'Emission.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
