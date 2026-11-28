"""Apply the published Disjoint single-target loss tables to stated longer prefixes."""
from pathlib import Path
import sys,importlib.util
from math import gcd,prod
H=Path(__file__).resolve().parent;proof=H.parent/'Disjoint/Verify.py';sp=importlib.util.spec_from_file_location('disjoint_price',proof);v=importlib.util.module_from_spec(sp);sp.loader.exec_module(v)
def verify(f,z,h,extra=()):
 p,t=13,3543791;assert __debug__ and v.prime(t) and v.prime(p) and t-1==2*5*389*911 and all(v.prime(x) for x in (5,389,911));assert gcd(p*3,t*((t-1)//2))==1 and 3**(p-1)>p**2 and t>8000
 # The outer verifier must establish the extra row at the stated prime and exponent.
 row=[(p,388),(t,f),(z,h),*extra];X=prod(x**e for x,e in row);Z=[v.geom(x,e)//(1+e%2) for x,e in row];S=prod(Z);M=X//gcd(X,S);cp=388;ct=f
 while S%p==0:S//=p;cp-=1
 while S%t==0:S//=t;ct-=1
 for j in range(len(Z)):
  while (g:=gcd(Z[j],X))>1:Z[j]//=g
 D=prod(Z);H0=max(a*prod(gcd(a,b) for j,b in enumerate(Z) if j!=i) for i,a in enumerate(Z));B=10**2400
 U=v.price(p,cp,2,(1,3))*v.price(t,ct,4,tuple(d for d in range(1,(t-1)//2+1,2) if (t-1)//2%d==0));u=(U.numerator+U.denominator-1)//U.denominator;cnt=[0,0,0];holes=[]
 for i in range(cp+1):
  for j in range(ct+1):
   m=p**i*t**j;q=2*m-1;R=p**(2*(cp-i))*t**(4*(ct-j))
   if X*q*R>B*u:cnt[0]+=1;continue
   def outside(n):
    if q>n:return True
    if n//q>=4*m:return False
    k=n*pow(q,-1,4*m)%(4*m);return k==0 or k>n//q or n%k!=0
   ext=all(outside(n) or (jj==1 and j>0) for jj,n in enumerate(Z))
   if not ext:holes.append((i,j,'internal'));continue
   if X*D*q>B:cnt[1]+=1;continue
   for w in range(ct-j+1):
    lim=(3*B*H0)//(2*X*D*q*q*t**w)
    if lim and 2*X*q*q*R<=3*B*u*t**(3*w)*min(p**(cp-i),lim):break
   else:cnt[2]+=1;continue
   holes.append((i,j,'supplier'))
 print(f,z,h,'counts',cnt,'holes',len(holes),holes[:2],flush=True);return not holes
if __name__=='__main__':
 for f,z,h in [(42,1113708120497983331,12),(66,459911137111,10)]:print('local sufficient?',verify(f,z,h),flush=True)
