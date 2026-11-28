"""Derive global absence of 5 and 11 in T^2, then check exact leaves."""
from pathlib import Path
import gzip,json,sys
from fractions import Fraction as F
from functools import cache
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(R/'Session20261126'),str(R/'Night2400/A')];from PivotCheck import C,B;from MaskedForest import exact_absence_bound
Q=16148168401;T=C.sigma(Q,12)//13;L=3453283
def ab(p,e):return F(C.sigma(p,e),p**e)
def run():
 assert __debug__;pack=json.load(gzip.open(H/'TwoNest40.json.gz'));seen=set()
 @cache
 def prime(q):
  k=q
  if q>=2**64:
   seen.add(str(q))
   for row in pack['ecpp'][str(q)]:assert row[0]==k;k=C.pc.level(*row)
  return C.pc.prime64(k)
 assert all(prime(x) for x in [Q,T,L,3,5,7,11,13]);assert C.sigma(7,12)==Q and C.sigma(Q,12)==13*T and C.sigma(T,2)%(3*L)==0
 assert ab(7,12)*ab(3,2)*ab(5,1)>2
 assert ab(7,12)*ab(11,2)*ab(3,4)*ab(13,1)>2 and ab(7,12)*ab(11,2)*ab(3,2)*ab(13,2)>2
 assert C.sigma(3,2)==13 and C.sigma(Q,12)%13==0
 assert sorted(map(int,pack['nodes']))==[40]
 for k,n in pack['nodes'].items():
  rows=[(7,12),(Q,12),(T,2),(L,int(k))];s0=C.State(rows,absent=(5,11));a,rt,es,head=n;assert prime(a) and C.valuation(s0.D,a)==1;h=1;live=[]
  while s0.base//a*a**h<=B:
   if s0.possible(a,h,1):
    x=C.State(rows+[(a,h)],absent=(5,11))
    if not x.conflict and x.base<=B:live.append(h)
   h+=1
  assert live==[2];rows=rows+[(a,2)];s=C.State(rows,absent=(5,11));assert set(s.bad)=={5,11,19} and not s.conflict;C.validate_forest(s,rt,es,head,prime)
  lb=min(C.Forest(s,rt,es,head).lower()[0],exact_absence_bound(rows,rt,es,head,s.bad,B));assert lb>B;print('T^2',k,'lower/B in millionths',lb*1000000//B,flush=True)
 assert seen==set(pack['ecpp'])
if __name__=='__main__':run()
