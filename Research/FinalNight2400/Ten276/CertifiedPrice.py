"""Uniform nonlinear price for rare-order s=1109, and a cheap interior-Euler cap."""
from pathlib import Path
import sys,math,bisect
from fractions import Fraction
from functools import cache
from itertools import count
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path.insert(0,str(H.parent/'Ten'));from Weighted import lifts,val,B
from PriceLoss import loss
p,s,t,e=19,1109,1176672733,276;Ws=96
@cache
def sig(q,h):return (q**(h+1)-1)//(q-1)
A=sig(p,e);assert A%(s*t)==0 and A%(s*s) and A%(t*t)
@cache
def universal():
 # p,s disjoint odd effective lengths: p's {3,19}; s's {277,1109}.
 assert s-1==4*277 and p-1==2*9 and math.gcd(19*9,s*277)==1 and 3**18>=19**2 and 3**(s-1)>=s**Ws
 maxb=50000000;assert p**e*maxb**276>B
 for z,roots in enumerate(lifts(s,277,4),1):
  if z==4:assert min(roots)>maxb
  for b in roots:
   # If beyond the smallest representative it is bigger still, so this lower bound suffices.
   if b%2==0:b+=s**z
   assert b>maxb or b**276>=s**(Ws*z)
 return loss(p,276,2)
def proof(P):
 # Returns true only on sound coarse cap/whole-row dual; no reliance on failure.
 U=universal();fixed=dict(P);X=math.prod(q**h for q,h in P);blocks=[sig(q,h)//(1+h%2) for q,h in P];S=math.prod(blocks);Y=S//math.gcd(S,X);assert math.gcd(X,Y)==1 and s in fixed
 cp=fixed[p]-val(S,p);cs=fixed[s]-val(S,s);assert min(cp,cs)>=0;M=p**cp*s**cs;V=Fraction(X*p**(2*cp)*s**(Ws*cs),U)
 assert any(h%2 for q,h in P)
 return V>B
