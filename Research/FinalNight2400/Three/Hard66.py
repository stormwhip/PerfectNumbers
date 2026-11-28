"""Exact joint size-price closure of historical last hard (66,6,2,12) path."""
from pathlib import Path
import sys
from math import gcd
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Night2400/B'))
from EulerRoute import F,Q,P,R,B,cap_two,sigma

def run():
 assert __debug__
 X,S,c,V,_=cap_two(F,(Q,P));D=S//gcd(S,X);A=sigma(P,12);T=sigma(Q,66)//5897
 assert V>B and c==[65,11] and D==A*T and gcd(X,D)==gcd(A,T)==1
 left=0;n=0;weakest=None
 for i in range(c[0]+1):
  for j in range(c[1]+1):
   m=Q**i*P**j;a=2*m-1
   if V*a>B*m*m:continue
   for b in (A,T):
    u=b*pow(a,-1,4*m)%(4*m) or 4*m;hi=b//a
    assert u>hi or ((hi-u)//(4*m)<=16 and all(b%v for v in range(u,hi+1,4*m)))
   if X*D*a>B:continue
   left+=1
   # N>2V*a^2/(3m^2 t), independently N>2XD*a^2*t/(3max(A,T)).
   # Multiplying and cancelling gives contradiction without even enumerating t.
   floor=4*V*X*D*a**4/(9*m*m*max(A,T));weakest=min(weakest,floor) if weakest else floor
   if floor>B**2:n+=1
 assert 10**4844<=weakest<10**4845
 print('direct product exclusions',n,'of',left,'min joint lower N^2 floor',4844,flush=True)
 assert left==n==184
if __name__=='__main__':run()
