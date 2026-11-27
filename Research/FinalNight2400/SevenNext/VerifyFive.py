"""Independent exact enumeration for anchored Euler-five support and saturated flow."""
import sys,json,gzip
from pathlib import Path
from math import gcd,prod
from fractions import Fraction as F
from functools import cache
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(R/'Session20261126'),str(R/'Night2400/A')];from PivotCheck import C,B;from MaskedForest import exact_absence_bound
Q=16148168401;r=173;q0=30103;banned=[5,11,17,23,31,37,41,47,53]
def ab(p,h):return F(C.sigma(p,h),p**h)
def main(expect=None,filename='FiveAnchor.json.gz'):
 assert __debug__;data=json.load(gzip.open(H/filename));used=set()
 @cache
 def prime(q):
  n=q
  if n>=2**64:
   used.add(str(n))
   for row in data['ecpp'][str(n)]:assert row[0]==n;n=C.pc.level(*row)
  return C.pc.prime64(n)
 rows=[(7,12),(Q,42),(r,5)];s=C.State(rows);forced=[3,13,29,43,109,q0];assert all(prime(p) for p in [7,Q,r]) and C.sigma(7,12)==Q and s.fixed_euler and all(prime(p) and s.D%p==0 for p in forced)
 K=prod(ab(p,e) for p,e in rows)*prod(ab(p,2) for p in forced);assert K*ab(3,4)/ab(3,2)>2
 assert all(prime(p) and p not in set(forced)|set(s.rows) and K*ab(p,2)>2 for p in banned)
 rows+= [(3,2)];s0=C.State(rows,absent=banned);assert not s0.conflict and C.valuation(s0.S,3)==2 and C.valuation(s0.D,q0)==1
 # 'bad' below also governs future emissions. 3 is present, but its exact inflow is exhausted by the fixed rows.
 filt=s0.bad+(3,);domain=[];h=2
 while s0.base//q0*q0**h<=B:
  if C.permitted(q0,h,filt):
   z=C.State(rows+[(q0,h)],absent=banned)
   if not z.conflict and z.base<=B and prod(C.sigma(k,v) for k,v in z.rows.items())<=2*z.X:domain.append(h)
  h+=2
 assert len(domain)==45 and set(map(int,data['nodes']))<=set(domain)
 if expect is not None:assert set(map(int,data['nodes']))==set(expect)
 minv=None
 for k,node in data['nodes'].items():
  rr=rows+[(q0,int(k))];s=C.State(rr,absent=banned);s.bad+=(3,);rt,es,head,more,ws=node;assert C.valuation(s.S,3)==2 and not s.conflict
  assert len(ws)==len(set(ws)) and all(prime(q) and s.D%q==0 and q not in s.rows for q in ws)
  a=prod(ab(p,e) for p,e in rr)
  for q in ws:
   h=C.valuation(s.D,q);h+=h%2
   while not C.permitted(q,h,s.bad):h+=2
   a*=ab(q,h)
  assert all(prime(p) and p not in s.rows and p not in ws and a*ab(p,2)>2 for p in more)
  s.bad+=tuple(more);C.validate_forest(s,rt,es,head,prime);lb=min(C.Forest(s,rt,es,head).lower()[0],exact_absence_bound(rr,rt,es,head,s.bad,B));assert lb>B;minv=lb if minv is None else min(lb,minv)
 assert used==set(data['ecpp']);print('30103 live',len(domain),'certificates',len(data['nodes']),'remaining',sorted(set(domain)-set(map(int,data['nodes']))),'weakest millionths',minv*10**6//B,flush=True)
 return domain
if __name__=='__main__':main()
