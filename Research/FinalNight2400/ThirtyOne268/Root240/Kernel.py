"""Simultaneous cubic square price for 31 and 3229; optional order5/15 or 269/807, disjoint or reserved budgets."""
from pathlib import Path
import sys,json,gzip
from math import prod,gcd,isqrt
from fractions import Fraction
from functools import cache
H=Path(__file__).resolve().parent;R=H.parents[2];sys.path.insert(0,str(R/'Session20261126'));from PivotCheck import C,B,floor10
p,e,t=31,240,4339;P=[(p,e)];sigma=C.sigma;val=C.valuation
@cache
def roots(z,o,c):
 g=next(pow(v,(z-1)//o,z) for v in range(2,z) if all(pow(pow(v,(z-1)//o,z),o//s,z)!=1 for s in (3,5,241) if o%s==0));x=g;m=z;out=[(1,(0,))]
 for j in range(1,c+1):out.append((m,tuple(pow(x,i,m)for i in range(1,o) if gcd(i,o)==1)));m*=z;x=pow(x,z,m)
 return out
@cache
def value(row):
 s=C.State(row);a=e-val(s.S,p);b=s.rows[t]-val(s.S,t);cap=B//s.base;assert p-1==2*3*5 and t-1==2*9*241 and 3**8000>B;U=Fraction(1);ex={};
 def add(x,h,goal):
  if x<3 or not x%2 or (x.bit_length()-1)*h>=goal.bit_length():return
  v=x**h
  if v>=goal or v//gcd(v,s.D)>cap:return
  ok=lambda z:z>=3 and z%2 and z not in (*s.rows,*s.bad) and all(z==k or z%k for k in (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)) and pow(2,z-1,z)==1;y=isqrt(x)
  if ok(x)or(not s.fixed_euler and y*y==x and ok(y)):ex[x]=max(ex.get(x,1),Fraction(goal,v))
 for n,bb in roots(t,3,b):
  inv=1;step=pow(p,-1,n)
  for m,aa in roots(p,3,a):
   goal=(m*n)**2
   for x in aa:
    for y in bb:add(x+m*((y-x)*inv%n),2,goal)
   inv=inv*step%n
 U*=prod(ex.values(),start=Fraction(1));
 for z,c,orders in [(p,a,(5,15)),(t,b,(9,241,723,2169))]:
  ex={}
  for o in orders:
   # Reserve o−3 (even when o prime); two separate powers remain for a potential cubic charge at the other target. If both orders >3 overlap only at 3, sum budgets fits by direct lcm comparison.
   h=o-3
   if 3**h>=z**(2*c):continue
   for m,vs in roots(z,o,c)[1:]:
    for x in vs:add(x,h,m*m)
  U*=prod(ex.values(),start=Fraction(1))
 # length units at t possible when L>=3229, not zero. 3^(t−1) and 3^(p−1) pay all length increments. Orders coprime to both targets.
 return -(-U.numerator//U.denominator),a,b

def outside(Z,m):
 q=2*m-1
 if q>Z:return True
 k=Z*pow(q,-1,4*m)%(4*m);return Z//q<4*m and (not k or k>Z//q or Z%k)

@cache
def marginal(row):
 s=C.State(row);a=e-val(s.S,p);b=s.rows[t]-val(s.S,t);# For h+1 divisible by 3229, odd length <=8000 implies h+1=3229, so y=1 mod t requires y≥2t+1 and (2t+1)^3228 exceeds B.
 assert 3**8000>B and (2*t+1)**(t-1)>B
 # also any t length multiplier at other orders implies length≥3t>8000, so t valuations from length impossible here.

def windows(row,roots):
 row=tuple(row);s=C.State(row);X=s.X;D=s.D;U,a,b=value(row);M=p**a*t**b
 if s.fixed_euler:return [] if X*M*M>B*U else [(-1,-1)]
 fs=[z for z in roots if z not in s.rows and D%z==0];F=prod(z**(val(D,z)%2) for z in fs);em=[C.sig_odd(z,h) for z,h in row];G=[C.nonsupport(v,X*prod(fs)) for v in em];hs=[z**(val(D,z)+val(D,z)%2) for z in fs]
 while G:
  v=G.pop();o=[z for z in G if gcd(v,z)>1]
  if o:
   for z in o:G.remove(z);v*=z
   G.append(v)
  else:hs.append(v)
 Hm=max(hs,default=1);bad=[]
 for j in range(b+1):
  n=t**j;R=p**(2*a)*t**(2*(b-j));m=n
  for i in range(a+1):
   q=2*m-1
   if X*q*R<=B*U and (not all(k==0 and i or outside(z,m)for k,z in enumerate(em))or (X*D*F*q<=B and 4*X**2*D*F*q**4*R<=9*B**2*U*Hm)):bad.append((i,j))
   m*=p;R//=p*p
 return bad