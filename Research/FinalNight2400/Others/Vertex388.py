"""Finish (13,388) first6/second12 by vertex enumeration and ordinary forest."""
from pathlib import Path
from math import gcd,prod,isqrt
import sys,json,gzip,importlib.util
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'Session20261126')];from PivotCheck import C,B
sp=importlib.util.spec_from_file_location('dprice',H.parent/'Disjoint/Verify.py');d=importlib.util.module_from_spec(sp);sp.loader.exec_module(d)
def verify():
 p,t,r=13,3543791,14199329591297809156875293;P=[(p,388),(t,6),(r,12)];s=C.State(P);X=s.X;factors=[2,7,11,503,9006499,10176375725767];assert prod(factors)*2==r-1 and all(d.prime(k) for k in factors) and all(gcd(x,y)==1 for x,y in [(39,5*389*911*t),(39,(r-1)//4*r),(5*389*911*t,(r-1)//4*r)]) and 3**8000>B
 ds=[1]
 for k in factors[1:]:ds +=[a*k for a in ds]
 # For r, all odd nontrivial orders are >=7: powers of order-minus-one cover weight 3 unless explicitly charged. Full certified r primality is supplied by the forest/split caller.
 U=d.price(p,388,2,(1,3))*d.price(t,5,4,tuple(x for x in range(1,(t-1)//2+1,2) if (t-1)//2%x==0));ur={};cap=11
 for o in ds:
  if o==1 or o>8000 or 3**(o-1)>=r**(3*cap):continue
  # only small active orders: generate primitive o-th roots and lift
  g=next(g for g in range(2,200) if all(pow(g,(r-1)//q,r)!=1 for q in factors));v=pow(g,(r-1)//o,r);rs=[pow(v,j,r) for j in range(1,o) if gcd(j,o)==1];m=1
  for i in range(cap):
   m*=r
   for x in rs:
    if x>=3 and x%2 and x**(o-1)<m**3:from fractions import Fraction;ur[x]=max(ur.get(x,1),Fraction(m**3,x**(o-1)))
   rs=[x+m*((-((pow(x,o,m*r)-1)//m)*pow(o*pow(x,o-1,r),-1,r))%r) for x in rs]
 U*=prod(ur.values());D=json.loads(gzip.decompress((H/'Vertex388Forest.json.gz').read_bytes()));K,O,h=D['roots'],D['owners'],D['head'];book=D['ecpp'];used=set()
 def prime(q):
  n=q
  if n>=2**64:
   used.add(str(q));c=book[str(q)];assert c
   for v in c:assert n==v[0];n=C.pc.level(*v)
  assert C.pc.prime64(n);return True
 assert all(prime(x) for x,_ in P);assert [(x,n-C.valuation(s.S,x)) for x,n in P]==[(p,388),(t,5),(r,11)];C.validate_forest(s,K,O,h,prime);assert used==set(book)
 V=set(K)|set(dict(O));charges=[(x,x**(n-C.valuation(s.S,x)),w) for (x,n),w in zip(P,[2,4,3])];eligible=[q for q in V if q%4==1];assert all(X*q*prod((a//gcd(a,q+1))**w for x,a,w in charges)>B*U for q in eligible)
 assert not s.fixed_euler;s.fixed_euler=True;v,_=C.Forest(s,K,O,h).lower();assert v>B;print('PASS first6/12 all Euler vertices',len(eligible),'ordinary floor',len(str(v))-1,'r-loss',len(ur),flush=True)
if __name__=='__main__':verify()
