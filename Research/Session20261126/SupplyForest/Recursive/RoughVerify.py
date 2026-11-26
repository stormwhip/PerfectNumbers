"""Independent cyclotomic rough-block certificate reconstruction. All values are divisibility-checked, blocks pairwise disjoint and coprime to residual complement."""
from math import gcd,prod,isqrt
from functools import cache
@cache
def cyclotomic(q,h):
 if h==1:return q-1
 n=q**h-1
 for j in range(1,h):
  if h%j==0:
   b=cyclotomic(q,j);assert n%b==0;n//=b
 return n

def free(n,s):
 while (g:=gcd(n,s))>1:n//=g
 return n

def ledger(p,e,fix,C,radius):
 assert type(radius)==int and 0<=radius<=100000
 if not radius:return 1,1,1,1
 bins=[]
 for q,f in [(p,e),*fix]:
  for h in range(2,f+2):
   if (f+1)%h==0 and (z:=gcd(C,cyclotomic(q,h)))>1:bins.append((q,h,z))
 vals=[];divisor=1
 for i,(q,h,z) in enumerate(bins):
  b=free(z,prod(v for k,(_,_,v) in enumerate(bins) if i!=k));b=free(b,C//b);b=free(b,h)
  if b==1:continue
  assert C%b==0 and gcd(b,C//b)==gcd(divisor,b)==1;divisor*=b;step=h*(1 if h%2==0 else 2);low=1+step
  for _ in range(radius):
   if b%low==0:break
   low+=step
  order=(p-1)//((p-1)&(1-p));vals.append((low if isqrt(b)**2!=b else 1,low**2 if pow(b,order,p)!=1 else 1))
 m=prod(x for x,y in vals);v=prod(y for x,y in vals);return m,v,m//max([1,*[x for x,y in vals]]),v//max([1,*[y for x,y in vals]])
