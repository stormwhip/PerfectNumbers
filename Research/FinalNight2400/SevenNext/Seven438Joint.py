"""Exact 7/R ordinary-source price, Euler exponent and t supply already forced by preceding Verify438 proof."""
from pathlib import Path
from functools import cache
from fractions import Fraction
from math import gcd,isqrt,prod
import sys
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H.parent/'Seven'),str(H)];import Verify438 as V
from Odd42 import C,B
p=7;t=V.t;r=27431;T=t**11
@cache
def fracprice(l,c,w,divs):
 ds={};assert 3**(3*min(5100,l-1))>l**w and (2*l+1)**min(5100,l-1)>l**w
 for o in divs:
  assert (l-1)%o==0 and o%2==1;g=o-1
  if g>=5100 or 3**g>=l**(w*c):continue
  assert g>=w
  def save(x,u):
   if x<3 or not x%2 or x in (7,t,r,19) or any(x%a==0 and x!=a for a in (3,5,7,11,13,17,19,23,29,31,37)) or pow(2,x-1,x)!=1:return
   n=l**(w*u)
   if (x.bit_length()-1)*g<n.bit_length() and x**g<n:ds[x]=max(ds.get(x,1),Fraction(n,x**g))
  if 5000**g>=l**(w*c):
   for x in range(3,5000,2):
    if x**g>=l**(w*c):break
    if x%l!=1 and pow(x,o,l)==1:save(x,min(c,V.v(x**o-1,l)))
   continue
  fs=[q for q in range(2,o+1) if o%q==0 and C.pc.prime64(q)];h=2
  while True:
   a=pow(h,(l-1)//o,l)
   if a and all(pow(a,o//q,l)!=1 for q in fs):break
   h+=1
  roots=[pow(a,i,l) for i in range(1,o) if gcd(i,o)==1];m=1
  for u in range(1,c+1):
   m*=l
   for x in roots:save(x,u)
   if u<c:roots=[x+m*(-((pow(x,o,m*l)-1)//m)*pow(o*pow(x,o-1,l),-1,l)%l) for x in roots]
 return prod(ds.values(),start=Fraction(1))
@cache
def credit(y):
 g=2;x=y*y;best=None;mx=[0,0]
 while x<=B:
  ss=(x*y-1)//(y-1);u=V.v(ss,p);v=V.v(ss,r);mx=[max(mx[0],u),max(mx[1],v)];q=Fraction(x,p**(2*u)*r**(4*v));best=q if best is None else min(best,q);x*=y*y;g+=2
 return best,mx

def go(h,fs):
 X=p**438*t**12*r**h;S=C.sigma(p,438)*C.sigma(t,12)*C.sigma(r,h);D=V.strip(S,[p,t,r]); cp=438-V.v(S,p);cr=h-V.v(S,r);assert V.v(S,t)==1 and gcd(3*p,r*(r-1)//2)==1
 blk=[C.sigma(p,438)//t,C.sigma(t,12)//r,V.strip(C.sigma(r,h),[p,t,r])];assert prod(blk)==D;why=blk[-1]
 while any(gcd(x,y)!=1 for i,x in enumerate(blk) for y in blk[i+1:]):
  a,b=next((a,b) for a,x in enumerate(blk) for b,y in enumerate(blk) if b>a and gcd(x,y)!=1);blk[a]*=blk.pop(b)
 M=max(blk);U=fracprice(p,438,2,(3,))*fracprice(r,71,4,(5,13,65,211,1055,2743));assert (r-1)//2==5*13*211
 ys={y for y in fs if y not in (p,r,t,19) and y>2};assert all(D%y==0 for y in ys);G=prod((credit(y)[0] for y in ys),start=Fraction(1));F=prod(y for y in ys if V.v(D,y)%2);mp=max([0]+[credit(y)[1][0] for y in ys]);mr=max([0]+[credit(y)[1][1] for y in ys]);
 for i in range(cp+1):
  for j in range(cr+1):
   m=T*p**i*r**j;q=2*m-1;K=X*D*q;uk=cr-j;up=cp-i;g=G if not ys or q>max(ys) else prod((credit(y)[0] for y in ys if y%(4*m)!=q),start=Fraction(1))
   if X*q*p**(2*up)*r**(4*uk)*g.numerator*U.denominator>B*g.denominator*U.numerator:continue
   if not V.outside(why,m):return False,(i,j,'internal')
   if K*F>B:continue
   for v in range(uk+1):
    for first,last,ac in [(0,min(mp,up),v>mr),(mp+1,up,True)]:
     if first>last:continue
     hh=2*X*q*q*r**v; denom=3*M*B; Z=hh*D*(F if ac else 1);lo,hi=first-1,last+1
     while hi-lo>1:
      mid=(hi+lo)//2
      if Z*p**mid>denom:hi=mid
      else:lo=mid
     if lo>=first:
      g2=G if ac else Fraction(1)
      if hh*p**lo*p**(2*(up-lo))*r**(4*(uk-v))*U.denominator*g2.numerator<=3*B*U.numerator*g2.denominator:return False,(i,j,lo,v)
 return True,()
if __name__=='__main__':
 from Find30Factors import get
 from sympy import divisors,isprime
 for h in map(int,sys.argv[1:]):
  ys=set()
  for k in divisors(h+1)[1:]:
   for label in (get(r,k) or b'').split():
    if label.isdigit() and (y:=int(label))>1 and C.sigma(r,h)%y==0 and isprime(y):ys.add(y)
  print(h,go(h,ys),sorted(ys),flush=True)
