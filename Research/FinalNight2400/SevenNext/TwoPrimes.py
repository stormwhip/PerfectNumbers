"""A stock-Python root-only integer proof of (7,12;Q,12;T,2;L,130)."""
from pathlib import Path
from math import gcd,isqrt,prod
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Session20261126'));from PivotCheck import C,B
Q=16148168401;T=C.sigma(Q,12)//13;L=3453283
def cut(k,roots):
 rows=[(7,12),(Q,12),(T,2),(L,k)];s=C.State(rows);assert not s.conflict and s.base<=B
 assert len(set(roots))==len(roots) and all(C.pc.prime64(z) and z%4==3 and C.valuation(s.D,z)==1 for z in roots)
 v=s.base//prod(roots);minimum=[]
 for z in roots:
  h=2;best=B+1
  while z**h<best:
   out=C.sigma(z,h);g=gcd(out,s.base)
   while g>1:out//=g;g=gcd(out,s.base)
   best=min(best,z**h*out);h+=2
  v*=best;minimum.append((z,h))
 assert v>B;print(k,minimum,'floor',len(str(v))-1,flush=True)
if __name__=='__main__':
 assert __debug__;cut(130,[209676169384343,315434173696972219])
