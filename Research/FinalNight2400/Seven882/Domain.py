from pathlib import Path
from functools import cache
from math import prod,gcd,isqrt
import sys,json,gzip
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path.insert(0,str(R/'Session20261126'));from PivotCheck import C,B,floor10
Q=21193;ROOT=(7,882);piv={1:10597,2:1645291,4:48717502357961,8:30201838022902600352247769,12:167572909473275194734712401197760222706024523}
def state(row,mask=0):
 yes={p for i,p in enumerate(C.ORDER) if mask>>i&1} if mask else set();no=set(C.ORDER)-yes if mask else {19};s=C.State(row,yes,no);s.bad=tuple(set(s.bad)|{p for p,h in row if s.S%p**h==0});return s

def domain(row,z,mask=0):
 s=state(row,mask);v=C.valuation(s.D,z);assert z not in s.rows and v>0;out={};h=v
 while s.base//z**v*z**h<=B:
  if s.possible(z,h,v):
   r=row+[(z,h)];u=C.State(r,s.present,tuple(x for x in s.bad if x not in s.rows));
   if not u.conflict and u.base<=B and prod(C.sigma(x,g) for x,g in r)<=2*u.X:out[str(h)]=r
  h+=1
 return out
