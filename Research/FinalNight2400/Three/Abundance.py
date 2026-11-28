"""Explicit disjoint completion of the hard 66 exterior-Euler bound.
Run from anywhere: python -I -S -B Abundance.py
"""
from math import gcd,isqrt,prod
from fractions import Fraction
from pathlib import Path
import sys
src=Path(__file__).resolve().parents[2]/'Night2400'/'B'
sys.path.insert(0,str(src))
from EulerRoute import Q,P,F,B,cap_two,sigma
from Balance import lower

def run():
 assert __debug__
 X,S,c,V,_=cap_two(F,(Q,P)); D=S//gcd(X,S); A=sigma(P,12); T=sigma(Q,66)//5897
 assert c==[65,11] and V>B and D==A*T and gcd(A,T)==gcd(X,D)==1
 rough=20_000_001
 for b,z,k in ((A,P,13),(T,Q,67)):
  assert isqrt(b)**2!=b and gcd(b,2*k*z*(z-1))==1
  assert all(b%r for r in range(2*k+1,rough,2*k))
 n=0; w=D
 while w>=rough: w//=rough;n+=1
 # Outside square mass: if at most two distinct outside primes, 5 and 17 maximize ratio.
 # If smallest is not 5 or 17 nothing better can happen; 3 is fixed, 7,11,13 banned.
 floor=(5*17*23)**2 # 19 is banned too
 raw=old=0;new=[];left=[]
 for i in range(66):
  for j in range(12):
   m=Q**i*P**j;a=2*m-1
   if V*a>B*m*m:continue
   # Exclude e|D by its exact cofactor class. e=2m-1 mod 4m.
   for block in (A,T):
    k=block*pow(a,-1,4*m)%(4*m) or 4*m; h=block//a
    assert k>h or (h-k<17*4*m and all(block%r for r in range(k,h+1,4*m)))
   if X*D*a>B:continue
   raw+=1;l=(2*a+2)//3
   assert X*D*a*l>B # exterior emitter impossible
   # All primes on A,T have final abundancy ratio <rough/(rough-1), regardless of powers.
   assert Fraction(S,X)*Fraction(a+1,a)*Fraction(rough,rough-1)**n*Fraction(5,4)*Fraction(17,16)<2
   net=min(max(Fraction(rough),Fraction((l+b-1)//b),lower(z,k,s,a,dict(F)[z])) for b,z,k,s in ((A,P,13,j),(T,Q,67,i)))*rough
   if X*D*a*net>B:continue
   old+=1
   if X*D*a*net*floor>B:new.append((i,j))
   else:left.append((i,j))
 assert raw==184 and old==153
 print('historical survivors',old,'newly excluded',len(new),new,'remaining',len(left),flush=True)
 return left
if __name__=='__main__':run()
