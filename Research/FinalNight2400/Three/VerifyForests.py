"""Exact subtree accounting from packet roots; 2 independent forest lower bounds."""
from pathlib import Path
from math import prod
from functools import cache
import gzip,json,sys
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path.insert(0,str(R/'Session20261126'));import PivotCheck as PC
C=PC.C;B=PC.B

def run():
 assert __debug__
 for f in (1,16,18,22,102,192):
  packet=json.loads(gzip.decompress((H/f'Tree{f}.json.gz').read_bytes()));q=packet['p'];assert packet['f']==f
  book=packet['ecpp'];seen=set()
  @cache
  def prime(z):
   assert type(z)==int and z>=3;t=z
   if z>=2**64:
    seen.add(str(z))
    for a in book[str(z)]:assert a[0]==t;t=C.pc.level(*a)
   assert C.pc.prime64(t);return True
  assert prime(3) and prime(1093) and C.sigma(3,6)==1093 and prime(q)
  P=[(3,6),(1093,f)];s=C.State(P);assert not s.conflict and s.base<=B and s.D%q==0 and q not in s.bad and q not in s.rows
  c=C.valuation(s.D,q);h=c;live=set();covered=set();floors=[]
  while s.base//q**c*q**h<=B:
   if s.possible(q,h,c):
    T=P+[(q,h)];u=C.State(T)
    if not u.conflict and u.base<=B and prod(C.sigma(z,j) for z,j in T)<=2*u.X:
     live.add(h)
     if str(h) in packet['b']:
      roots,edges=packet['b'][str(h)];C.validate_forest(u,roots,edges,96,prime);a=C.Forest(u,roots,edges,96).lower()[0];b=PC.exact_leaf(T,roots,edges,96);assert min(a,b)>B;covered.add(h);floors.append(PC.floor10(min(a,b)))
   h+=1
  assert set(map(str,covered))==set(packet['b']) and set(book)==seen
  if f==1:assert not any(j>=294 for j in covered)
  print('PASS',f,q,'raw tail',h,'domain',len(live),'forests',len(covered),'minfloor',min(floors),'ecpp',len(seen),'covered',sorted(covered),flush=True)
if __name__=='__main__':run()
