"""Canonical (3,6), Euler 1093. Exact deficits; no factor/probable-prime assumptions."""
from math import gcd,prod,isqrt
from fractions import Fraction
from pathlib import Path
import sys
R=Path(__file__).resolve().parents[2]
sys.path.insert(0,str(R/'FinalSprint'))
import JointValuation as J
q=547;B=10**2400;ban=(19,7,11,31,13);MAX=436;X0=3**6*1093

def sig(p,h):return (p**(h+1)-1)//(p-1)
def exc():
 # uniform superset for all exact exponents 1..436
 E={};maxf=B.bit_length();m=q**(MAX+1)
 for f in range(2,maxf+1,2):
  if 5**f>=q**(2*MAX):break
  s=J.val(f+1,q);d=gcd(f+1,q-1)
  def allclasses():
   if s:yield q,1,s
   for k in J.divisors(d):
    if k==1:continue
    for j,roots in enumerate(J.lifts(q,k,MAX-s),1):
     if 5**f<q**(2*(j+s)):
      for z in roots:yield q**j,z,j+s
  for mod,r,j in allclasses():
   lim=q**(2*j)
   while J.less(r,f,lim):
    if r>=5 and r%2 and r not in (1093,q,*ban) and all(r==p or r%p for p in (3,5,17,23,29,37,41,43,47)) and pow(2,r-1,r)==1 and all(((f+1)%p if r%p==1 else (pow(r,f+1,p)-1)%p) for p in ban):
     v=J.val(f+1,q) if r%q==1 else J.val((pow(r,f+1,m)-1)%m or m,q)
     if 1<=v<=MAX:E[r]=max(E.get(r,Fraction(1)),Fraction(q**(2*v),r**f))
    r+=mod
 return E

def run():
 assert __debug__ and sig(3,6)==1093 and sig(1093,1)==2*q and all(all(p%d for d in range(2,isqrt(p)+1)) for p in (q,1093))
 E=exc();U=prod(E.values(),start=Fraction(1));live=[];kill=[]
 for h in range(2,876,2):
  X=X0*q**h;S=1093*q*sig(q,h);D=S//gcd(S,X)
  if gcd(X,D)!=1 or gcd(D,prod(ban))!=1 or X*D>B or S>X:continue
  live.append(h);assert h<=MAX
  if X*q**(2*(h-1))>B*U:kill.append(h)
 assert X0*q**876>B and len(live)==160
 print('discounts',len(E),'live',len(live),'excluded',len(kill),kill,'remaining',len(live)-len(kill),flush=True)
if __name__=='__main__':run()
