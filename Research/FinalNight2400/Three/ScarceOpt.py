"""Subset-safe mixed incoming-price with scarcity at fixed Euler 1093, target 547.

At any component supplying 3, for u=v3(sig(r^f))=v3(f+1), require r=1 mod3.
Price a labelled unit at lambda^u times q^(2v); per-base maximum shortfall.
"""
from pathlib import Path
import sys
from math import gcd,prod
from functools import cache
from fractions import Fraction
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Six import B,q,ban,J,sig
@cache
def options(p,c,f):
 s=J.val(f+1,p);out=[]
 if 0<s<=c:out.append((p,1,s))
 for o in J.divisors(gcd(f+1,p-1)):
  if c<=s or o==1:continue
  for j,rr in enumerate(J.lifts(p,o,c-s),1):
   out.extend((p**j,x,j+s) for x in rr)
 return out
@cache
def exceptions(c,lam):
 E={};mod=q**(c+1)
 def charge(r,f):
  if r<5 or not r%2 or r in (*ban,q,1093) or any(r%p==0 and r!=p for p in (5,17,23,29,37,41,43,47,53,59,61,67,71,73,79,83,89,97)):return
  if any((not (f+1)%p if r%p==1 else pow(r,f+1,p)==1) for p in ban):return
  u=J.val(f+1,3) if r%3==1 else 0
  v=J.val(f+1,q) if r%q==1 else J.val((pow(r,f+1,mod)-1)%mod or mod,q)
  if u>6 or v>c:return
  num=q**(2*v)*lam**u;den=r**f
  if num>den and pow(2,r-1,r)==1:E.setdefault(r,[]).append((f,u,v,Fraction(num,den)))
 for f in range(2,6000,2):
  if 5**f>=q**(2*c)*lam**6:break
  u=min(J.val(f+1,3),6);s=lam**u
  for m,r,v in [(1,0,0),*options(q,c,f)]:
   if m>1 and v>0 and q**(2*v)*s<=5**f:continue
   lim=q**(2*v)*s
   while J.less(r,f,lim):
    if r**f<q**(2*v) or (u and r%3==1):charge(r,f)
    r+=m
 return E

def prove(P,E,lam):
 X=prod(x**h for x,h in P);S=prod(sig(x,h)//(1+h%2) for x,h in P);D=S//gcd(X,S);fix=dict(P);a=fix[3]-J.val(S,3);c=fix[q]-J.val(S,q);assert a>=0 and c>=0 and gcd(D,X)==1
 # Knapsack exact sum of exception labels may consume at most the total 3 demand.
 best=[Fraction(1)]*(a+1)
 for r,L in E.items():
  if r in fix:continue
  costs={}
  for f,u,v,p in L:
   if u>a or v>c or X*D*r**f//gcd(r**f,D)>B:continue
   costs[u]=max(costs.get(u,1),p)
  old=best.copy()
  for u,p in costs.items():
   for k in range(u,a+1):best[k]=max(best[k],p*old[k-u])
 return X*q**(2*c)*lam**a/best[a]

if __name__=='__main__':
 import json,gzip
 h=int(sys.argv[1]);lam=int(sys.argv[2]);P=[(3,6),(1093,1),(547,h)];E=exceptions(h-1,lam);V=prove(P,E,lam);print(h,lam,len(E), 'floor',len(str(V.numerator//V.denominator))-1,flush=True)