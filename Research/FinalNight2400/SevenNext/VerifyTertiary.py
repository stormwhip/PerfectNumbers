"""Sealed exact third-pivot valuation exclusions, no discovery dependencies."""
import gzip,json,sys
from pathlib import Path
from functools import cache
from math import prod
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path.insert(0,str(R/'Session20261126'));from PivotCheck import C,B,exact_leaf
Q=16148168401;T=C.sigma(Q,12)//13;S2=3453283;S6=62936242392988051361
EXPECTED={2:[94,98,104,114,116,118,120,122,124,128,132,134,136],6:[13,14,16,18,20]}
def main():
 assert __debug__;z=json.load(gzip.open(H/'Tertiary.json.gz'));seen=set()
 @cache
 def prime(q):
  k=q
  if k>=2**64:
   seen.add(str(k))
   for row in z['ecpp'][str(q)]:assert row[0]==k;k=C.pc.level(*row)
  assert C.pc.prime64(k);return True
 assert C.sigma(7,12)==Q and C.sigma(Q,12)==13*T and prime(T) and prime(Q)
 for h,r in [(2,S2),(6,S6)]:
  assert prime(r);rows=[(7,12),(Q,12),(T,h)];s=C.State(rows); assert not s.conflict and C.valuation(s.D,r)==1
  fs=[];j=1
  while s.base//r*r**j<=B:
   if s.possible(r,j,1):
    u=C.State(rows+[(r,j)])
    if not u.conflict and u.base<=B and prod(C.sigma(x,k) for x,k in u.rows.items())<=2*u.X:fs.append(j)
   j+=1
  nodes=z['nodes'][str(h)]; assert sorted(map(int,nodes))==EXPECTED[h] and set(EXPECTED[h])<=set(fs)
  for i,node in nodes.items():
   urows=rows+[(r,int(i))];u=C.State(urows);rt,es,head=node;C.validate_forest(u,rt,es,head,prime)
   assert min(C.Forest(u,rt,es,head).lower()[0],exact_leaf(urows,rt,es,head))>B
  print('T',h,'third pivot',r,'raw live',len(fs),'tail',j,'excluded',EXPECTED[h],flush=True)
 assert seen==set(z['ecpp'])
if __name__=='__main__':main()
