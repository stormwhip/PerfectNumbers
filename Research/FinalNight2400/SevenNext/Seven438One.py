"""External Euler in 7^438 t^10 with compulsory prime credits including exact-even sigma output. Reuse accepted incoming-order proof."""
from pathlib import Path
from math import gcd,isqrt,prod
from fractions import Fraction
from functools import cache
import sys
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parent/'Seven')];import Verify438 as V
from Seven438Joint import fracprice,C,B
p=7;r=67;t=V.t;E=438;T=t**9
@cache
def credit(y):
 g=2;pw=y*y;best=None;mx=0
 while pw<=B:
  ss=(y*pw-1)//(y-1);u=V.v(ss,p);v=Fraction(pw,p**(2*u));best=v if best is None else min(best,v);mx=max(mx,u);g+=2;pw*=y*y
 return best,mx
@cache
def ds(n):return sorted({v for k in range(1,isqrt(n)+1) if n%k==0 for v in (k,n//k)})
@cache
def phi(r,k):return (r**k-1)//prod(phi(r,i) for i in ds(k) if i<k)
def go(h,fs):
 X0=p**438*t**10;X=X0*r**h;S0=C.sigma(p,438)*C.sigma(t,10);S=S0*C.sigma(r,h);D=V.strip(S,(p,t,r));A=C.sigma(p,438)//t;C1=C.sigma(t,10)//r;cp=438-V.v(S,p)
 assert V.v(S,t)==1 and V.v(S0,r)==1 and V.prove_prime(t) is None
 blocks=[A,C1]+[V.strip(phi(r,i),(p,t,r)) for i in ds(h+1) if i>1];assert prod(blocks)==D;new=blocks[2:];comb=blocks[:]
 while any(gcd(x,y)>1 for i,x in enumerate(comb) for y in comb[i+1:]):
  i,j=next((i,j) for i,x in enumerate(comb) for j,y in enumerate(comb) if j>i and gcd(x,y)>1);comb[i]*=comb.pop(j)
 M=max(comb);U=fracprice(p,438,2,(3,));ys=sorted(set(fs));assert all(D%y==0 and y not in (7,t,r,19) for y in ys);F=prod(y for y in ys if V.v(D,y)%2);G=prod((credit(y)[0] for y in ys),start=Fraction(1));mg=max([0]+[credit(y)[1] for y in ys])
 for i in range(cp+1):
  m=T*p**i; q=2*m-1;g=G if not ys or q>max(ys) else prod((credit(y)[0] for y in ys if y%(4*m)!=q),start=Fraction(1));
  if X*q*p**(2*(cp-i))*g.numerator*U.denominator>B*g.denominator*U.numerator:continue
  # q external to old A,C1. Exclude from each new block rather than guessing q's identity.
  if not all(V.outside(z,m) for z in new):return False,(i,'internal')
  if X*D*q*F>B:continue
  for beg,end,ac in [(0,min(cp-i,mg),False),(mg+1,cp-i,True)]:
   if beg>end:continue
   lo,hi=beg-1,end+1;v=2*X*D*q*q*(F if ac else 1);gg=G if ac else Fraction(1)
   while hi-lo>1:
    mid=(lo+hi)//2
    if v*p**mid>3*B*M:hi=mid
    else:lo=mid
   if lo>=beg and 2*X*q*q*p**lo*p**(2*(cp-i-lo))*gg.numerator*U.denominator<=3*B*gg.denominator*U.numerator:return False,(i,lo)
 return True,()
if __name__=='__main__':
 from Find30Factors import get
 from sympy import isprime
 for h in map(int,sys.argv[1:]):
  fs=set()
  for k in ds(h+1)[1:]:
   n=phi(r,k)
   for w in (get(r,k) or b'').split():
    if w.isdigit() and (q:=int(w))>1 and n%q==0 and isprime(q):
     fs.add(q)
     while n%q==0:n//=q
   if n>1 and isprime(n):fs.add(n)
  fs=sorted(fs-{7,19,r,t});print(h,go(h,fs),len(fs),flush=True)
