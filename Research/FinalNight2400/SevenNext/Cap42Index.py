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
def go(h,forces):
 z=C.State([(7,12),(Q,42),(R,h)]); c=42-val(z.S,Q);j=h-val(z.S,R);U=cost(Q,41,2,True,True)*cost(R,231,38,True,True);X=z.X;D=z.D;A=C.sigma(Q,42)//R;B0=[A]+[phis(R,k) for k in divisors(h+1) if k>1];
 for i,b in enumerate(B0):
  for q in z.rows: b//=q**val(b,q)
  B0[i]=b
 assert prod(B0)==D
 ys=sorted(set(forces+[43]));assert all((y>=2**64 or C.pc.prime64(y)) and D%y==0 and y not in z.rows for y in ys)
 rr={y:net_credit(y) for y in ys}; MGQ=MGR=0
 for y in ys:
  gy=2;yy=y*y
  while yy<=B:
   ss=(yy*y-1)//(y-1);MGQ=max(MGQ,val(ss,Q));MGR=max(MGR,val(ss,R));gy+=2;yy*=y*y
 G=prod(rr.values());F=prod(y for y in ys if val(D,y)%2);bs=B0[:]
 while any(gcd(b,g)>1 for a,b in enumerate(bs) for g in bs[a+1:]):
  a,b=next((u,v) for u,x in enumerate(bs) for v,y in enumerate(bs) if v>u and gcd(x,y)>1);bs[a]*=bs.pop(b)
 M=max(bs)
 for i in range(c+1):
  for k in range(j+1):
   m=Q**i*R**k; q=2*m-1;V=Q**(2*(c-i))*R**(38*(j-k));
   Gsafe=G if q>max(ys) else prod(rr[y] for y in ys if y%(4*m)!=q)
   if X*q*V*Gsafe.numerator*U.denominator>B*U.numerator*Gsafe.denominator:continue
   if not all(outside(Z,m) for Z in B0):return False,(i,k,'inside')
   if X*D*q*F>B:continue
   for rv in range(j-k+1):
    tq=2*X*q*q*R**rv;au=min(c-i,4) if rv else c-i
    # size increases and discounted price decreases in QU
    for left,right,dis in [(0,min(au,MGQ),rv>MGR),(MGQ+1,au,True)]:
     if right<left:continue
     lo,hi=left-1,right+1;A1=(F if dis else 1)*tq*D;A2=G if dis else Fraction(1)
     while hi-lo>1:
      mid=(lo+hi)//2
      if A1*Q**mid>3*B*M:hi=mid
      else:lo=mid
     if lo>=left and A2.numerator*tq*Q**lo*Q**(2*(c-i-lo))*R**(38*(j-k-rv))*U.denominator<=3*B*U.numerator*A2.denominator:return False,(i,k,lo,rv)
 return True,()
if __name__=='__main__':
 from sympy import isprime
 from Find30Factors import get
 from SimulCap import check;assert check(5)==[]
 for h in map(int,sys.argv[1:]):
  fs=set()
  for k in divisors(h+1)[1:]:
   n=phis(R,k)
   for label in (get(R,k) or b'').split():
    if not label.isdigit():continue
    q=int(label)
    if q>1 and n%q==0 and isprime(q):
     fs.add(q)
     while n%q==0:n//=q
   if n>1 and isprime(n):fs.add(n)
  fs=sorted(fs-{7,Q,R});print('credit even',h,go(h,fs),fs,flush=True)
