"""Independent linear enumeration of all price/supplier endpoints; reuses deficit table only."""
from pathlib import Path
import runpy
v=runpy.run_path(str(Path(__file__).resolve().parents[1]/'Dual/Verify.py'))
p,t,B=19,v['T'],10**2400
from math import gcd
def sig(x,e):return sum(x**a for a in range(e+1))
def lift(z):
 R=[i for i in range(2,p) if pow(i,9,p)==1]; m=p
 for _ in range(1,z):
  R=[r+i*m for r in R for i in range(p) if pow(r+i*m,9,m*p)==1];m*=p
 return R
def overlap(Z):
 # Find just the first permanent root exclusion; later values never need new test.
 for u in range(3,433):
  m=p**(u-2)
  if m*m<=Z:continue
  for r in lift(u-2):
   k=Z*pow(r,-1,m)%m
   if (r%2 and Z%r==0) or (0<k<=Z//m and Z%k==0):break
  else:return u
 return 433
def outside(Z,m):
 q=2*m-1
 if q>Z:return True
 h=Z//q; k=Z*pow(q,-1,4*m)%(4*m)
 return h<4*m and (not k or k>h or Z%k!=0)
for f in [20,22]:
 X=p**432*t**f; A=sig(p,432)//t; C=sig(t,f); D=A*C;assert gcd(A,C)==1
 cutA,cutC=overlap(A),overlap(C);U=p**21*v['deficit'](p,432,2)*v['deficit'](t,f-1,5);a,b=U.as_integer_ratio();counts=[0]*3; tuples=0
 for j in range(f):
  for i in range(433):
   m=p**i*t**j;q=2*m-1;rp=432-i;rt=f-1-j
   if X*q*p**(2*rp)*t**(5*rt)*b>B*a:counts[0]+=1;continue
   assert (i or outside(A,m)) and outside(C,m)
   if X*D*q>B:counts[1]+=1;continue
   counts[2]+=1
   for k in range(rt+1):
    lhs=2*X*D*q*q*t**k;lhs2=2*X*q*q*t**k*p**(2*rp)*t**(5*(rt-k))*b
    for u in range(rp+1):
     ov=max(1,A if u<cutA else 1,C if u<cutC else 1);assert lhs>3*B*ov or lhs2>3*B*a,(f,i,j,k,u)
     lhs*=p;lhs2//=p;tuples+=1
 print(f,cutA,cutC,counts,tuples,flush=True)
