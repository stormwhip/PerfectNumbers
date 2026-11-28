"""Independent exact prefix recomputation and discrete Euler-window coverage; shared price only."""
from pathlib import Path
import sys
from math import gcd,prod
from functools import cache
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'Eleven'))
import FortySix as F
p,t,E,f,B=11,879701,462,46,10**2400
R,S=F.R,F.S;W=193882521011;Z=2150985008682894323231;V=13584009104671777218460029405269012416436766343
U=int(F.check(f)); powp=[p**a for a in range(E+1)];powt=[t**a for a in range(f)]; windows=0;union=[]
@cache
def sig(q,h):return sum(q**i for i in range(h+1))
for node,pr in [(R,()),(S,((R,2),)),(W,((R,4),)),(Z,((R,4),(W,4))),(V,((R,2),(S,2)))]:
 rows=((p,E),(t,f))+pr;assert node%4==3 and any(sig(z,h)%node==0 for z,h in rows);s0=prod(z**h for z,h in rows);h=2;pending=[]
 while s0*node**h<=B:
  row=rows+((node,h),);x=s0*node**h; h+=2;sv=[sig(z,e) for z,e in row];s=prod(sv)
  if gcd(s,7*19)>1:continue
  cap=[]
  for z,e in row:
   i=0
   while s%z==0:s//=z;i+=1
   cap.append(e-i)
  if min(cap)<0 or x*s>B:continue
  tail=[]
  for v in sv:
   while (g:=gcd(v,x))>1:v//=g
   tail.append(v)
  assert prod(tail)==s
  H=max(v*prod(gcd(v,w) for j,w in enumerate(tail) if j!=i) for i,v in enumerate(tail));M=powp[cap[0]]*powt[cap[1]];left=x**5*M**19;right=B**5*U
  # For each exponent of t in m find the smallest discrete p-power not already price-excluded; larger m in that column increase both size and supplier bounds.
  ok=True
  for td in powt[:cap[1]+1]:
   lo=0;hi=cap[0]+1
   while lo<hi:
    mid=(lo+hi)//2;m=td*powp[mid]
    if left>right*m**14:lo=mid+1
    else:hi=mid
   if lo>cap[0]:continue
   m=td*powp[lo];windows+=1
   if lo==0 or 2*m-1<=max(tail[1:]):ok=False;break
   if x*s*(2*m-1)>B:continue
   if (2*x)**5*M**19*(2*x*s)**14*m**19>(3*B)**5*U*(3*B*H)**14:continue
   ok=False;break
  if not ok:pending.append(h-2)
 assert set(pending)<=set({R:[2,4],S:[2],W:[4],Z:[],V:[]}[node]);union.append((node,h,pending))
print('PASS richer discrete Euler allocation; columns',windows,'nodes',union)
