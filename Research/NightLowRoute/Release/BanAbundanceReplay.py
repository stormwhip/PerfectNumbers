"""Combine a rigorously replayed support incompatibility with the improved all-source forbidden-index forest. Applies only to a declared positive small prime q branch by abundancy. Proof independently computes exact component exponents and every Euler placement with prior-root bans; excludes self-dependent reasoning."""
from pathlib import Path
from fractions import Fraction
import sys,json,gzip,math
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from ForestReplay import proof,B,check,R,sigma,valuation

def minf(p,c,sp,bans):
 if sp and (p%4!=1 or any((p+1)%t==0 for t in bans)):return None
 e=max(c,1);e+=((1-e)%4 if sp else e%2)
 while any(sigma(p,e)%t==0 for t in bans):e+=4 if sp else 2
 return e

def check_absent(p,e,prior,q,known):
 A=sigma(p,e);K=set(known);check(all(r%2 and 3<=r<1000 and all(r%j for j in range(2,math.isqrt(r)+1)) and A%r==0 for r in K) and q not in K and p not in K,'unproved trial factors');K.add(q);vals=[]
 for z in [0,*[r for r in K if minf(r,1,True,prior)]]:
  x=Fraction(A,p**e)
  for r in K:
   f=minf(r,max(1,valuation(A,r)),r==z,prior);x*=Fraction(sigma(r,f),r**f)
  check(x>2,'compatible cooccurrence');vals.append(x)
 return min(vals)
if __name__=='__main__':
 for s in sys.argv[1:]:
  f=Path(s);f=f if f.is_file() else H/s;d=json.loads(gzip.decompress(f.read_bytes()));r=d['row'];p,e=r['p'],r['e'];q=d['absent'];check(q in (3,5,7,11,13,17,19,23,29,31) and q!=p and q not in R[:R.index(p)] and r.get('den',1)==1,'scope');v=check_absent(p,e,R[:R.index(p)],q,d['factors']);m=min(proof(r,d['ecpp'],support=(q,False)).values());check(m>B,'forest open');print(p,e,'absent',q,'abundance lower ppm',v.numerator*10**6//v.denominator,'forest floorlog10',len(str(m))-1,flush=True)
