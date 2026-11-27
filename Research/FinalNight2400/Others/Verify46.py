"""All Euler allocations for the last exact 13^262, t^46 fiber. Stdlib only."""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Critical import *
def outside(n,m,q):
 if q>n:return True
 modulus=4*m;maximum=n//q
 if maximum>=modulus:return False
 k=n*pow(q,-1,modulus)%modulus
 return k==0 or k>maximum or n%k!=0

def verify():
 assert __debug__ and prime64(P) and prime64(T) and X==P**E*T**F and M==P**E*T**(F-1)
 assert (P**(E+1)-1)//(P-1)==A*T and gcd(D,X)==gcd(A,C)==1
 assert T-1==8*3*263*401*877*104087 and all(prime64(z) for z in (263,401,877,104087));assert 3**8000>B and T>8000 and 3**(P-1)>=P**2
 div=[1]
 for z in (3,263,401,877,104087):div += [a*z for a in div]
 assert all(o in (1,3,263,401,789,877,1203,2631) or 3**min(8000,o-3)>=T**(2*(F-1)) for o in div)
 loss=get();U=prod(loss.values(),start=Fraction(1));u=(U.numerator+U.denominator-1)//U.denominator;assert len(loss)==23 and u<10**19
 count=[0,0,0];H=max(A,C)
 for i in range(E+1):
  for j in range(F):
   m=P**i*T**j;q=2*m-1;rem=(M//m)**2
   if X*q*rem>B*u:count[0]+=1;continue
   assert outside(A,m,q) and outside(C,m,q),(i,j,'Euler could be internal')
   if X*D*q>B:count[1]+=1;continue
   assert (2*X*q**2*rem)*(2*X*D*q**2)>9*B**2*u*H,(i,j,'supplier')
   count[2]+=1
 assert sum(count)==(E+1)*F
 print('PASS canonical (13,262) exact first 46: all',sum(count),'Euler windows; price,mandatory,supplier',count,'U',u,'loss bases',len(loss),flush=True)
if __name__=='__main__':verify()
