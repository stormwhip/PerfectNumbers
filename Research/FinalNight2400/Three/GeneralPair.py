"""Generalization of the hard66 product to siblings with one or more blocks."""
from pathlib import Path
from math import gcd,prod
import sys,json,gzip
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Night2400/B'));from EulerRoute import F,Q,P,R,cap_two,sigma,B

def score(prefix, q0=None, q1=None):
 if any(h%2 for _,h in prefix):return None
 if q0 is None:q0=Q
 z=q1 if q1 is not None else prefix[-1][0];X,S,c,V,_=cap_two(prefix,(q0,z));D=S//gcd(S,X);assert gcd(D,X)==1
 if V<=B:return ('under',V.numerator.bit_length()-V.denominator.bit_length())
 bs0=[sigma(r,e)//gcd(sigma(r,e),X) for r,e in prefix];bs=[b for b in bs0 if b>1];assert prod(bs)==D
 # For this bound cluster blocks until coprime, keeping any one emitter inside at most one cluster.
 clusters=[]
 for b in bs:
  same=[w for w in clusters if gcd(w,b)>1];clusters=[w for w in clusters if w not in same];clusters.append(b*prod(same))
 bmax=max(clusters);good=0;left=0;internal=0;weak=None
 for i in range(c[0]+1):
  for j in range(c[1]+1):
   m=q0**i*z**j;a=2*m-1
   if V*a>B*m*m:continue
   poss=False
   for b in bs:
    u=b*pow(a,-1,4*m)%(4*m) or 4*m;hi=b//a
    if u<=hi and ((hi-u)//(4*m)>16 or any(not b%v for v in range(u,hi+1,4*m))):poss=True;break
   if poss:internal+=1;continue
   if X*D*a>B:continue
   floor=4*V*X*D*a**4/(9*m*m*bmax);weak=floor if weak is None else min(weak,floor)
   if floor>B**2:good+=1
   else:left+=1
 return ('result',good,left,internal, (weak.numerator.bit_length()-weak.denominator.bit_length()) if weak else None)


if __name__=='__main__':
 import itertools
 for f in [42,58,60]:
  h=[(3,6),(1093,126),(30228287,f)]+([(12586282900669679,10)] if f==42 else [])+[(11939,66),(485816396265547,6)]
  print(f,score(h,1093,30228287),flush=True)
