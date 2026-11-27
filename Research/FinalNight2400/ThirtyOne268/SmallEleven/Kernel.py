"""Exact universal 11-only fourth-power price for every subset of ordinary/Euler-square sources."""
from pathlib import Path
import sys,json,gzip
from math import prod,gcd,isqrt
from fractions import Fraction
from functools import cache
H=Path(__file__).resolve().parent;R=H.parents[2];sys.path.insert(0,str(R/'Session20261126'));from PivotCheck import C,B,floor10
p,e,t=11,12,3158528101;P=[(p,e)];sigma=C.sigma;val=C.valuation
@cache
def loss():
 assert 3**10>=p**4;g=next(z for z in range(2,p) if pow(z,5,p)==1);x=g;m=p;ex={}
 for a in range(1,e+1):
  for i in range(1,5):
   r=pow(x,i,m)
   if r<3 or not r%2:continue
   y=isqrt(r);ok=lambda z:z>=3 and z%2 and z not in (7,19,p,t) and pow(2,z-1,z)==1
   if ok(r) or (y*y==r and ok(y)):ex[r]=max(ex.get(r,1),Fraction(m**4,r**4))
  m*=p;x=pow(x,p,m)
 return prod(ex.values(),start=Fraction(1))

def windows(row,roots=()):
 s=C.State(row);a=e-val(s.S,p);L=loss();U=-(-L.numerator//L.denominator);X=s.X;D=s.D
 if s.fixed_euler:return [] if X*p**(4*a)>B*U else [-1]
 fs=[z for z in roots if z not in s.rows and s.D%z==0];F=prod(z**(val(D,z)%2) for z in fs);em=[C.sig_odd(z,h) for z,h in row];blocks=[C.nonsupport(v,X*prod(fs)) for v in em];hh=[z**(val(D,z)+val(D,z)%2) for z in fs]
 while blocks:
  v=blocks.pop();same=[z for z in blocks if gcd(v,z)>1]
  if same:
   for z in same:blocks.remove(z);v*=z
   blocks.append(v)
  else:hh.append(v)
 Hmax=max(hh,default=1);miss=[]
 for i in range(a+1):
  m=p**i;q=2*m-1;R=p**(4*(a-i))
  if X*q*R>B*U:continue
  def ext(Z):
   if q>Z:return True
   k=Z*pow(q,-1,4*m)%(4*m);return Z//q<4*m and (not k or k>Z//q or Z%k)
  if not all((n==0 and i>0) or ext(v)for n,v in enumerate(em)):miss.append(i);continue
  if X*D*F*q>B:continue
  # y^h supplies q and p^u. Three independent bounds: cost from sigma, own p-price, rest p-price. Global U applies to y alone or to its complement.
  failed=False
  for u in range(a-i+1):
   y=p**u
   if 2*X*D*F*q*q*y>3*B*Hmax or X*D*F*q*y**4>B*U*Hmax or 2*X*q*q*R>3*B*U*y**3:continue
   failed=True;break
  if failed:miss.append(i)
 return miss
if __name__=='__main__':
 for file in H.glob('Base*.json'):
  for f,n in json.loads(file.read_bytes()).items():
   if n['floor']>=2400:continue
   m=windows(P+[(t,int(f))],n['roots']);print(f,len(m),(min(m),max(m)) if m else '',flush=True)