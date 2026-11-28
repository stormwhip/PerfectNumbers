"""Independent integer cover. Does not import either target verifier."""
from math import gcd,prod,isqrt
from fractions import Fraction
from functools import cache
from pathlib import Path
import json,sys
p,t,B=19,2477,10**2400
def geom(r,e):return (r**(e+1)-1)//(r-1)
def strip(n,p):
 j=0
 while n%p==0:j+=1;n//=p
 return n,j
def root(x,k): # floor of real k-th root
 if x==0:return 0
 r=1<<((x.bit_length()+k-1)//k)
 while True:
  s=((k-1)*r+x//r**(k-1))//k
  if s>=r:assert r**k<=x<(r+1)**k;return r
  r=s
def prime(n):return n>=2 and all(n%i for i in range(2,isqrt(n)+1))
def main():
 assert __debug__ and prime(t) and prime(619) and t-1==4*619
 A,j=strip(geom(p,618),t);assert j==1 and A%619
 assert (2*t+1)**(t-1)>B and 5**(2*t-1)>B
 for r in range(3,1+root(B//p**618,618)):
  if not prime(r) or r in (2,19):continue
  if pow(r,619,t)==1:assert p**618*strip(t*A,r)[0]*r**618>B
 for q in range(5,1+root(B//p**618,1237),4):
  if prime(q):assert pow(q,1238,t)!=1 or pow(q,2,t)==1
 # Enumerate ninth roots by just two primitive generator lifts at the top modulus.
 # Lifting all the way by Euler powering (no per-digit Hensel implementation).
 top=p**618; e9=18*p**617//9
 x=next(y for g in range(2,99) if (y:=pow(g,e9,top))%p!=1 and pow(y,3,p)!=1);assert pow(x,9,top)==1
 roots=[pow(x,i,top) for i in range(1,9)];exc={};m=1
 for j in range(1,619):
  m*=p
  for i,y in enumerate(roots,1):
   o=9//gcd(i,9);r=y%m
   if isqrt(r)**2==r and isqrt(r)%4==1:assert r**(50*(o-1))>=m**99
   if r<3 or not r%2 or r in (p,t) or any(r%k==0 and r!=k for k in (3,5,7,11,13,17,19,23,29,31,37)):continue
   # Take 50th powers only when bit-bound does not already certify.
   if (r.bit_length()-1)*50*(o-1)>=(m**99).bit_length():continue
   n=m**99;d=r**(50*(o-1))
   if n>d:exc[r]=max(exc.get(r,1),Fraction(n,d))
 U=prod(exc.values(),start=Fraction(1));assert len(exc)==8
 # Square reimbursement: derive residue mod M by direct reduction of top lift.
 M=p**205;K=1238*M;assert gcd(M,1238)==1 and 3**(p**3-1)>B and 1000**9<p**204-1 and 1000**(3*p*p-1)>B
 for y in roots:
  # use CRT in opposite order from submitted verifier
  R=1+1238*((y-1)*pow(1238,-1,M)%M);z=A*pow(R,-2,K)%K;assert 0<z and R*R*z>A
 # Precompute integer maxima for K such that K^50 * 19^(99w) <= B^50 * U.
 # This converts each source-price contradiction into simple integer comparison.
 a,b=U.as_integer_ratio(); thresholds={}
 for scale in [1,3]:
  # Since 99*(w+50)=99*w+99*50, each full period is rationally scaled by 19^99.
  init=[root(((scale*B)**50*a)//(b*p**(99*w)),50) for w in range(50)];thresholds[scale]=[init[w%50]//p**(99*(w//50)) for w in range(619)]
 Qlim,Slim=thresholds[1],thresholds[3];tot=0
 if '--anchor' in sys.argv:
  sys.path.insert(0,str(Path(__file__).resolve().parent));from AnchorIndependent import run_anchor
  run_anchor(Qlim,Slim,A);return
 if '--credit' in sys.argv:
  run_credit(Qlim,Slim,A);return
 for f in range(36,69,2):
  C,j=strip(geom(t,f),p);D=A*C;X=p**618*t**f;c=618-j;T=t**(f-1);q0=2*T-1;assert gcd(A,C)==gcd(D,X)==1
  maxk=C//q0;assert maxk<4*T; k=(C*pow(q0,-1,4*T))%(4*T);assert not(0<k<=maxk and C%k==0)
  assert X*D*q0**5>B and X*q0**3>Qlim[c] and X*q0>Qlim[c];tests=0;strong=0
  for s in range(1,c+1):
   q=2*T*p**s-1;M0=X*D*q
   if M0>B or X*q>Qlim[c-s]:continue
   z=2*q;v=2*X*q*q
   # Linear exhaustive u, no binary search or price/size monotonicity assumed.
   for u in range(c-s+1):
    if v<=Slim[c-s-u] and M0*z<=3*B*max(A,C):
     assert f<=46 and u>=206 and M0*M0*z>3*B*B and M0*z>3*B*C,(f,s,u)
     strong+=1
    z*=p;v*=p;tests+=1
  print(f,tests,strong,flush=True);tot+=tests
 print('supplier allocation count:',tot,flush=True)
def run_credit(Qlim,Slim,A):
 H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'RootFiveNext'));import PrimeCheck as pc
 zmap=json.loads((H.parent/'Nineteen/Extra618.json').read_bytes());assert set(zmap)=={'22','24','28'}
 for sf,rec in zmap.items():
  f=int(sf);C=geom(t,f);D=A*C;X=p**618*t**f;c=618;T=t**(f-1);q0=2*T-1
  assert gcd(A,C)==gcd(D,X)==1 and C==prod(map(int,rec));F=C
  k=C*pow(q0,-1,4*T)%(4*T);assert C//q0<4*T and not(0<k<=C//q0 and C%k==0)
  credit=Fraction(1);mg=0
  for label,chain in rec.items():
   r=y=int(label)
   for row in chain:assert row[0]==y;y=pc.level(*row)
   assert pc.prime64(y);h=2;single=[]
   while X*r**h<=B:
    # Price supplied 19 units via modular valuation, no unbounded sigma construction.
    if r%p==1:u=strip(h+1,p)[1]
    else:u=strip(pow(r,h+1,p**619)-1,p)[1] if pow(r,h+1,p)==1 else 0
    single.append(Fraction(r**h,p**(2*u)));mg=max(mg,u);h+=2
   credit*=min(single)
  # Denominator is a power of 19 dividing X, so X*credit is integral.
  E,ed=credit.as_integer_ratio();assert X%ed==0 and (X//ed)*q0*E>Qlim[c]
  tests=squares=0
  for s in range(1,c+1):
   q=2*T*p**s-1;M0=X*D*q
   if M0*F>B or (X//ed)*q*E>Qlim[c-s]:continue
   z=2*q;v=2*X*q*q
   for u in range(c-s+1):
    K=M0*(F if u>mg else 1);mul=E if u>mg else 1
    if v*mul<=Slim[c-s-u]*(ed if u>mg else 1) and K*z<=3*B*max(A,C):
     assert u>=206 and K*K*z>3*B*B and K*z>3*B*C,(f,s,u);squares+=1
    z*=p;v*=p;tests+=1
  print('credit',f,'rows',len(rec),'max-19',mg,'coordinates',tests,'square-required',squares,flush=True)
if __name__=='__main__':main()
