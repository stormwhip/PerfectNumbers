"""Standalone constrained valuation forest dual for 3^6,1093^1,547^h."""
from fractions import Fraction
from functools import cache
from math import gcd,prod
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Scarcity import q,B,ban,sig,J
@cache
def row(r,f,c,a,lam):
 if r%3==1:u=J.val(f+1,3)
 else:u=0
 if u>a or (f+1)%1093==0 and r%1093==1 or r%1093!=1 and pow(r,f+1,1093)==1:return None
 if any((not (f+1)%p if r%p==1 else pow(r,f+1,p)==1) for p in ban):return None
 if r%q==1:v=J.val(f+1,q)
 else:
  mod=q**(c+1);v=J.val((pow(r,f+1,mod)-1)%mod or mod,q)
 if v>c:return None
 return Fraction(r**f,q**(2*v)*lam**u)

def more(P,targets,lam,E):
 fixed=dict(P);X=prod(z**h for z,h in P);S=prod(sig(z,h)//(1+h%2) for z,h in P);D=S//gcd(S,X);c=fixed[q]-J.val(S,q);a=fixed[3]-J.val(S,3);assert 0<=c and 0<=a<=6 and gcd(X,D)==1
 W=q**(2*c)*lam**a;assert all(D%r==0 and r not in fixed for r in targets)
 best=[Fraction(1)]*(a+1)
 for r,L in E.items():
  if r in targets or r in fixed:continue
  old=best.copy();costs={}
  for f,u,v,k in L:
   if u>a or v>c or X*D*r**f//gcd(r**f,D)>B:continue
   costs[u]=max(costs.get(u,1),k)
  for u,k in costs.items():
   for j in range(u,a+1):best[j]=max(best[j],k*old[j-u])
 base=X*W/best[a];gains=[]
 for r in targets:
  o=J.val(D,r);lo=None
  for f in range(o+o%2,B.bit_length(),2):
   mass=r**f
   if mass>B//X:break
   if lo is not None and mass>=lo*W:break
   k=row(r,f,c,a,lam)
   if k is not None:lo=k if lo is None else min(k,lo)
  if lo is None:return B+1
  gains.append(lo)
 return base*prod(gains)
