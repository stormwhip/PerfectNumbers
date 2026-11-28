"""Complete L^60 via mandatory high Euler and exact simultaneous Q,T,L pricing."""
from pathlib import Path
from math import gcd,prod
from fractions import Fraction
import json,gzip,sys
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H.parents[1]/'Session20261126'),str(H.parent/'Ten'),str(H)];from PivotCheck import C,B
def ab(p,e):return Fraction(C.sigma(p,e),p**e)
import runpy
excludes=runpy.run_path(str(H.parent/'Ten/Weighted.py'))['excludes']
Q=16148168401;T=C.sigma(Q,12)//13;L=3453283;A=C.sigma(L,60)
def main():
 assert __debug__ and all(C.pc.prime64(x) for x in [Q,L,3,5,7,11,13,73,431]) and C.sigma(7,12)==Q and C.sigma(Q,12)==13*T and C.sigma(T,2)%(3*L)==0
 for n,chain in [(T,json.load(gzip.open(H/'Tertiary.json.gz'))['ecpp'][str(T)]),(A,json.loads((H/'Cert60.json').read_bytes()))]:
  z=n
  for row in chain:assert row[0]==z;z=C.pc.level(*row)
  assert C.pc.prime64(z)
 assert ab(7,12)*ab(3,2)*ab(5,1)>2 and ab(7,12)*ab(11,2)*ab(3,4)*ab(13,1)>2 and ab(7,12)*ab(11,2)*ab(3,2)*ab(13,2)>2 and C.sigma(3,2)==13
 rs=[(7,12),(Q,12),(T,2),(L,60)];s=C.State(rs,absent=(5,11));assert not s.conflict and C.valuation(s.D,A)==1;v=1;ds=[]
 while s.base//A*A**v<=B:
  if s.possible(A,v,1):
   z=C.State(rs+[(A,v)],absent=(5,11));
   if not z.conflict and z.base<=B:ds.append(v)
  v+=1
 assert ds==[1] and v==4;rs+=[(A,1)];s=C.State(rs,absent=(5,11));assert s.fixed_euler
 lower,ps,cs,exc=excludes(rs,[5,11,19],[1,2,3]);assert tuple(ps)==(Q,T,L) and tuple(cs)==(11,1,59)
 G=Fraction(1)
 for y in [3,13,73,431]:
  assert s.D%y==0 and y not in s.rows;g=2;y2=y*y;best=None
  while y2<=B:
   S=(y2*y-1)//(y-1);cost=Fraction(y2,prod(p**(2*C.valuation(S,p)) for p in ps));best=cost if best is None else min(best,cost);y2*=y*y;g+=2
  assert best==y*y;G*=best
 assert lower*G>B;print('PASS L^60 full; 1304-bit Euler A^1; 3 demands',cs,'forced credit',G,'exceptions',len(exc),'scaled bound',lower.numerator*G.numerator*10**6//(lower.denominator*G.denominator*B),flush=True)
if __name__=='__main__':main()
