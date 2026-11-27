"""Replay exact secondary reductions; no archive/discovery imports or shared caches."""
from functools import cache
from pathlib import Path
from math import gcd,prod
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Session20261126'));from PivotCheck import C,B,exact_leaf
Q=16148168401;T=(Q**13-1)//(Q-1)//13
def run():
 assert __debug__;z=json.load(gzip.open(H/'SevenForest.json.gz'));seen=set()
 @cache
 def prime(q):
  y=q
  if q>=2**64:
   seen.add(str(q))
   for row in z['ecpp'][str(q)]:assert row[0]==y;y=C.pc.level(*row)
  assert C.pc.prime64(y);return True
 rows=[(7,12),(Q,12)];s=C.State(rows); assert prime(Q) and prime(T) and C.sigma(7,12)==Q and C.sigma(Q,12)==13*T
 def domain(rows,r):
  s=C.State(rows);assert not s.conflict and s.D%r==0 and r not in s.rows and prime(r); out=[];h=C.valuation(s.D,r);scale=s.base//r**h
  while scale*r**h<=B:
   if s.possible(r,h,C.valuation(s.D,r)):
    u=C.State(rows+[(r,h)])
    if not u.conflict and u.base<=B and prod(C.sigma(q,e) for q,e in u.rows.items())<=2*u.X:out.append(h)
   h+=1
  return out,h
 assert domain(rows,T)==([1,2,4,5,6,8,9],19)
 def walk(rows,node):
  if isinstance(node,dict):
   r=node['pivot'];dom,tail=domain(rows,r); assert set(map(int,node['children']))==set(dom)
   for e in dom:walk(rows+[(r,e)],node['children'][str(e)])
   return
  roots,es,head=node;s=C.State(rows);C.validate_forest(s,roots,es,head,prime)
  v=min(exact_leaf(rows,roots,es,head),C.Forest(s,roots,es,head).lower()[0]);assert v>B;print('12:12 exact exponents',[e for q,e in rows[2:]],'floor',len(str(v))-1,flush=True)
 for e,node in z['nodes'].items():walk(rows+[(T,int(e))],node)
 assert seen==set(z['ecpp'])
 sys.path.insert(0,str(H));from Prices import loss
 from Verify438 import outside
 X=7**12*Q**12*T**8;u=C.State(rows+[(T,8)]);U=loss(T,7,2,1)
 blocks=(13,T**2+T+1,T**6+T**3+1);assert prod(blocks)==u.D and C.valuation(u.S,T)==1
 for j in range(8):
  m=T**j;q=2*m-1
  if X*q*T**(2*(7-j))*U.denominator>B*U.numerator:continue
  assert all(outside(b,m) for b in blocks) and X*u.D*q>B
 print('covered T powers',sorted(set(map(int,z['nodes']))|{8}),flush=True)
if __name__=='__main__':run()
