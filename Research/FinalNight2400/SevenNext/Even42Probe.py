"""Joint 173/Q 38/2 + containment and mixed source reimbursement, Q42 even second pivots."""
from pathlib import Path
import sys,math,json
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Odd42 import *
from VerifyOdd42 import net_credit
from VerifyTertiary import C
def divisors(n):return sorted({v for d in range(1,isqrt(n)+1) if n%d==0 for v in (d,n//d)})
@cache
def outside(Z,m):
 q=2*m-1
 if Z<q:return True
 k=Z*pow(q,-1,4*m)%(4*m);return Z//q<4*m and not(0<k<=Z//q and Z%k==0)
@cache
def phis(r,k):
 return (r**k-1)//prod(phis(r,d) for d in divisors(k) if d<k)
def go(h):
 z=C.State([(7,12),(Q,42),(R,h)]); c=42-val(z.S,Q);j=h-val(z.S,R);U=cost(Q,41,2,True,True)*cost(R,231,38,True,True);X=z.X;D=z.D;A=C.sigma(Q,42)//R;B0=[A]+[phis(R,k) for k in divisors(h+1) if k>1];
 for i,b in enumerate(B0):
  for q in z.rows: b//=q**val(b,q)
  B0[i]=b
 assert prod(B0)==D
 # No forced boosting until Euler relation for these secondary blocks is secured.
 for i in range(c+1):
  for k in range(j+1):
   m=Q**i*R**k; q=2*m-1;V=Q**(2*(c-i))*R**(38*(j-k));
   if X*q*V*U.denominator>B*U.numerator:continue
   if not all(outside(Z,m) for Z in B0):return False,(i,k,'inside')
   if X*D*q>B:continue
   bs=B0[:]
   while any(gcd(b,g)>1 for i0,b in enumerate(bs) for g in bs[i0+1:]):
    a,b=next((a,b) for a,x in enumerate(bs) for b,y in enumerate(bs) if b>a and gcd(x,y)>1);bs[a]*=bs.pop(b)
   M=max(bs)
   for rv in range(j-k+1):
    tq=2*X*q*q*R**rv;au=c-i
    # size increases and discounted price decreases in QU
    lo,hi=-1,au+1
    while hi-lo>1:
     mid=(lo+hi)//2
     if tq*D*Q**mid>3*B*M:hi=mid
     else:lo=mid
    if lo>=0 and tq*Q**lo*Q**(2*(au-lo))*R**(38*(j-k-rv))*U.denominator<=3*B*U.numerator:return False,(i,k,lo,rv)
 return True,()
if __name__=='__main__':
 for h in map(int,sys.argv[1:]):print('even',h,go(h),flush=True)
