"""Recompute complete (19,420), t valuation 6 only. Other fibers not claimed."""
from pathlib import Path
import sys,json,gzip
from math import prod,gcd
from fractions import Fraction
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'Session20261126')]
from Price import price,sig,T,B
from PivotCheck import C

def verify(e,f):
 t=T[e];rows=[(19,e),(t,f)];S=C.State(rows);assert not S.conflict and not S.fixed_euler and not S.bad
 V,Q,_,_=price(rows,[2,2]);assert V>B
 F=json.loads((H/f'Forest{e}x{f}.json').read_bytes());K,O=F['roots'],F['owners'];nodes=set(K)|{v for v,_ in O}
 book=json.loads(gzip.decompress((H/f'Primes{e}x{f}.json.gz').read_bytes()));used=set()
 def prime(n):
  a=n
  if n>=2**64:
   used.add(str(n));chain=book[str(n)];assert chain
   for row in chain:assert row[0]==a;a=C.pc.level(*row)
  assert C.pc.prime64(a);return True
 assert prime(t) and prime(19) and sig(19,e)%t==0
 C.validate_forest(S,K,O,128,prime);assert used==set(book)
 M=prod(p**c for p,c,w in Q)
 for q in nodes:
  if q%4==1:assert V*q>B*gcd(q+1,M)**2 # exponent one
 S.fixed_euler=True;lo,how=C.Forest(S,K,O,128).lower();assert lo>B and how is None
 print('PASS exact',e,f,'forest floor',len(str(lo))-1,'vertices',len(nodes),'ECPP',len(book))
if __name__=='__main__':verify(420,6)
