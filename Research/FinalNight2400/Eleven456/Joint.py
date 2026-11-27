"""Joint target price: 11 with weight 4 or 2 and t=82261 with weight 2. Cubic t-supply is disjoint from 11, common fifth order priced jointly."""
from Kernel import *
from math import log10
@cache
def roots(s,o,c):
 if o==1:return [(1,(0,))]
 g=next(pow(k,(s-1)//o,s) for k in range(2,s) if all(pow(pow(k,(s-1)//o,s),o//u,s)!=1 for u in (3,5,457) if o%u==0));m=s;ret=[(1,(0,))];
 for a in range(c):ret.append((m,tuple(pow(g,i,m) for i in range(1,o) if gcd(i,o)==1)));m*=s;g=pow(g,s,m)
 return ret
@cache
def calc(row,w=4):
 s=C.State(row);a=e-val(s.S,p);b=s.rows[t]-val(s.S,t);cap=B//s.base;L={};assert t-1==4*9*5*457 and t>8000 and 3**8000>B
 def add(x,h,mass):
  if x<3 or not x%2:return
  power=x**h
  if power>=mass or power//gcd(power,s.D)>cap:return
  ok=lambda z:z>=3 and z%2 and z not in (19,7) and z not in s.rows and pow(2,z-1,z)==1
  y=isqrt(x)
  if ok(x) or (not s.fixed_euler and y*y==x and ok(y)):L[x]=max(L.get(x,1),Fraction(mass,power))
 # Same-order fifth roots. Combined exponent budget=4; desired 11^w*t^2, so loss only x<m (w,2<=4). Optional combos supply either target or both.
 for n,bb in roots(t,5,b):
  inv=1;step=pow(p,-1,n)
  for m,aa in roots(p,5,a):
   goal=m**w*n*n;bits=goal.bit_length()
   for x0 in aa:
    for y in bb:
     x=x0+m*((y-x0)*inv%n)
     if x>2 and x%2 and (x.bit_length()-1)*4<bits:add(x,4,goal)
   inv=inv*step%n
 # Other t-orders use disjoint budgets if o coprime to 5, or charge o−5 if o divisible by 5; preserve 4 for possible p-fifth units. This independent price multiplies with the marginal p loss, even when the same r occurs.
 other={};joint=L;L=other
 for o in (3,9,15,45,457,1371,2285,4113,6855):
  h=o-5 if o%5==0 else o-1
  if 3**h>=t**(2*b):continue
  for m,rr in roots(t,o,b)[1:]:
   bits=(m*m).bit_length()
   for x in rr:
    if x>2 and x%2 and (x.bit_length()-1)*h<bits:add(x,h,m*m)
 U=prod(joint.values(),start=Fraction(1))*prod(other.values(),start=Fraction(1));return (-(-U.numerator//U.denominator),a,b)

def external(Z,m):
 q=2*m-1
 if q>Z:return True
 k=(Z*pow(q,-1,4*m))%(4*m);return Z//q<4*m and (not k or k>Z//q or Z%k)

def test(row,fs,w=4):
 row=tuple(row);s=C.State(row);X=s.X;D=s.D;U,a,b=calc(row,w);M=p**a*t**b;em=[C.sig_odd(z,h) for z,h in row];R0=p**(w*a)*t**(2*b)
 if s.fixed_euler:return 0 if X*R0>B*U else 1
 roots=[z for z in fs if z not in s.rows and s.D%z==0];F=prod(z**(val(D,z)%2) for z in roots);groups=[C.nonsupport(v,X*prod(roots)) for v in em];hs=[z**(val(D,z)+val(D,z)%2) for z in roots];
 while groups:
  v=groups.pop();others=[z for z in groups if gcd(v,z)>1]
  if others:
   for z in others:groups.remove(z);v*=z
   groups.append(v)
  else:hs.append(v)
 hh=max(hs,default=1);miss=0
 for j in range(b+1):
  n=t**j;S=p**(w*a)*t**(2*(b-j));m=n
  for i in range(a+1):
   q=2*m-1
   if X*q*S<=B*U:
    if not all((k==0 and i>0)or external(z,m) for k,z in enumerate(em)):miss+=1
    elif X*D*F*q<=B:
     # For w>2 residual uncancelled p^(w−2)u; use emitter size cap to bound its 11 contribution. Own joint price <=B U H/(X D F q). Then 11^(w u) <= this bound independent of v.
     E=B*U*hh//(X*D*F*q);T0=4*X*X*D*F*q**4*S;T1=9*B*B*U*hh
     if T0<=T1*min(p**((w-2)*(a-i)),isqrt(E) if w==4 else 1):miss+=1
   m*=p;S//=p**w
 return miss
if __name__=='__main__':
 from Survey import rows
 M={k:v for fn in H.glob('Mend?.json') for k,v in json.loads(fn.read_bytes()).items()};
 for row,u in rows():
  k=':'.join(str(h) for z,h in row);o=M.get(k,u)
  if o['type']!='open':continue
  n=test(row,o['roots']);print(k,n,flush=True)
