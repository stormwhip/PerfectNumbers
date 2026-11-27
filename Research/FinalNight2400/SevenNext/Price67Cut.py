"""Both-target 19/10 ordinary pricing at 7^438,t^10,67^h. Derived q^1,q external as before."""
from pathlib import Path
import sys,math
from fractions import Fraction
from functools import cache
from math import gcd,prod
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Seven438One import C,B,p,r,t,T,V,phi,ds
from Cubic67 import loss
SCALE=2048
@cache
def loglo(a):return (a**SCALE).bit_length()-1
@cache
def deficit():return loss(438,300)
@cache
def price(y):
 pw=y*y;h=2;v=None;maxu=maxr=0
 while pw<=B:
  z=(pw*y-1)//(y-1);u=V.v(z,p);a=V.v(z,r);g=Fraction(pw*pw,(p**u*r**a)**4); # price square, conservative 2 vs 1.9; use tenth power below
  cost=Fraction(pw**10,(p**u*r**a)**19);v=cost if v is None else min(v,cost);maxu=max(maxu,u);maxr=max(maxr,a);pw*=y*y;h+=2
 return v,maxu,maxr

def go(h,fs,U=None):
 if U is None:U=deficit()
 X=p**438*t**10*r**h;S=C.sigma(p,438)*C.sigma(t,10)*C.sigma(r,h);cp=438-V.v(S,p);cr=h-V.v(S,r);D=V.strip(S,[p,t,r]);A=C.sigma(p,438)//t;C0=C.sigma(t,10)//r;blk=[A,C0]+[V.strip(phi(r,k),(p,t,r)) for k in ds(h+1) if k>1];assert prod(blk)==D and V.v(S,t)==1 and 0<=cp<=438 and 0<=cr<=300
 why=blk[2:];blocks=blk[:]
 while any(gcd(x,y)>1 for i,x in enumerate(blocks) for y in blocks[i+1:]):
  i,j=next((i,j) for i,x in enumerate(blocks) for j,y in enumerate(blocks) if j>i and gcd(x,y)>1);blocks[i]*=blocks.pop(j)
 M=max(blocks);ys=sorted(set(fs));assert all(D%y==0 and y not in (7,t,r,19) for y in ys);F=prod(y for y in ys if V.v(D,y)%2);G=prod((price(y)[0] for y in ys),start=Fraction(1));mu=max([0]+[price(y)[1] for y in ys]);mv=max([0]+[price(y)[2] for y in ys]);one=Fraction(1);big=B**10*U.numerator;big3=(3*B)**10*U.numerator
 LP=loglo(p);LR=loglo(r);lx=loglo(X);lu=loglo(U.numerator)-loglo(U.denominator)+1;LB=loglo(B)+1;LB3=loglo(3*B)+1
 # All bases 7 and 67 are odd. An initial comparison that passes at an (i,j) covers just that point; no monotonic shortcut except increasing size and u crossover.
 for i in range(cp+1):
  pp=p**i
  for j in range(cr+1):
   m=T*pp*r**j;q=2*m-1;K=X*D*q;up=cp-i;vr=cr-j
   if X//r**h*A*C0*r*q>B:break # old two-fixed base, always q-external; q increases in j
   gs=G if not ys or q>max(ys) else prod((price(y)[0] for y in ys if y%(4*m)!=q),start=Fraction(1));V0=None
   lq=(q.bit_length()-1)*SCALE;lg=loglo(gs.numerator)-loglo(gs.denominator)-1
   if 10*(lx+lq)+19*(up*LP+vr*LR)+lg>10*LB+lu:continue
   if not all(V.outside(z,m) for z in why):
    if (X*q)**10*(p**up*r**vr)**19*gs.numerator*U.denominator>big*gs.denominator:continue
    return False,(i,j,'internal')
   if False:return False,(i,j,'internal')
   if K*F>B:continue
   # Strong lower bound on log2 of mandatory size, fixed within one (i,j) window.
   zbase=SCALE+lx+loglo(D)+2*lq; rhsSize=loglo(3*M*B)+1
   for a in range(vr+1):
    z=2*X*q*q*r**a
    for l0,h0,ac in [(0,min(mu,up),a>mv),(mu+1,up,True)]:
     if h0<l0:continue
     lo,hi=l0-1,h0+1;bb=z*D*(F if ac else 1)
     cap=(rhsSize-zbase-a*LR-(loglo(F) if ac else 0))//LP
     if cap<l0:continue
     hi=min(hi,cap+1)
     while hi-lo>1:
      mid=(lo+hi)//2
      if bb*p**mid>3*B*M:hi=mid
      else:lo=mid
     if lo>=l0:
      gg=G if ac else one
      lhs=10*(SCALE+lx+2*lq+a*LR+lo*LP)+19*((up-lo)*LP+(vr-a)*LR)+loglo(gg.numerator)-loglo(gg.denominator)-1
      if lhs<=10*LB3+lu and (z*p**lo)**10*(p**(up-lo)*r**(vr-a))**19*gg.numerator*U.denominator<=big3*gg.denominator:return False,(i,j,lo,a)
 return True,()
if __name__=='__main__':
 from Find30Factors import get
 from sympy import isprime
 for h in map(int,sys.argv[1:]):
  ys=set()
  for k in ds(h+1)[1:]:
   n=phi(r,k)
   for w in (get(r,k) or b'').split():
    if w.isdigit() and (q:=int(w))>1 and n%q==0 and isprime(q):
     ys.add(q)
     while n%q==0:n//=q
   if n>1 and isprime(n):ys.add(n)
  print(h,go(h,sorted(ys-{7,r,t,19})),flush=True)
