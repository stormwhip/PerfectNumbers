"""Exact high 173 anchor extension; incoming-cap joint tests recomputed after pinning a. Do not use without certificating all prime rows."""
from pathlib import Path
import sys,math
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Cap42Index import *
def go(h,forces,a,f):
 z=C.State([(7,12),(Q,42),(R,h),(a,f)]); c=42-val(z.S,Q);j=h-val(z.S,R);U=cost(Q,41,2,True,True)*cost(R,231,38,True,True);X=z.X;D=z.D;A=C.sigma(Q,42)//R;B0=[A]+[phis(R,k) for k in divisors(h+1) if k>1]+[C.sig_odd(a,f)];
 for i,b in enumerate(B0):
  for q in z.rows: b//=q**val(b,q)
  B0[i]=b
 assert prod(B0)==D
 ys=sorted(set(forces+[43])-{a});assert all((y>=2**64 or C.pc.prime64(y)) and D%y==0 and y not in z.rows for y in ys)
 rr={y:net_credit(y) for y in ys}; MGQ=MGR=0
 for y in ys:
  gy=2;yy=y*y
  while yy<=B:
   ss=(yy*y-1)//(y-1);MGQ=max(MGQ,val(ss,Q));MGR=max(MGR,val(ss,R));gy+=2;yy*=y*y
 G=prod(rr.values());F=prod(y for y in ys if val(D,y)%2);bs=B0[:]
 while any(gcd(b,g)>1 for a,b in enumerate(bs) for g in bs[a+1:]):
  a,b=next((u,v) for u,x in enumerate(bs) for v,y in enumerate(bs) if v>u and gcd(x,y)>1);bs[a]*=bs.pop(b)
 M=max(bs)
 if f%2:
  assert z.fixed_euler;return X*G*Q**(2*c)*R**(38*j)>B*U,()
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
 from AllCut import fs
 from sympy import factorint,isprime,primerange
 from SimulCap import check
 assert check(5)==[]
 for h in map(int,sys.argv[1:]):
  zz=fs(h);a=max(zz);s=C.State([(7,12),(Q,42),(R,h)]);c=val(s.D,a);i=c;kept=[]
  while s.base//a**c*a**i<=B:
   if s.possible(a,i,c):
    z=C.State([(7,12),(Q,42),(R,h),(a,i)])
    if not z.conflict and z.base<=B:
     pp=sorted(set(zz)|{r for r in primerange(3,10000) if C.sig_odd(a,i)%r==0 and r not in z.rows});ok,fail=go(h,pp,a,i);print('anchor',h,i,ok,fail,flush=True)
     if not ok:kept.append(i)
   i+=1
  print('domain remaining',h,kept,flush=True)
