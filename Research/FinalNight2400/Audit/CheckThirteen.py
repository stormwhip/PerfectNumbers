"""Independent primitive-root CRT enumeration and all (13,262) f=46 Euler windows."""
from fractions import Fraction as R
from math import gcd,isqrt,prod,lcm
from pathlib import Path
import json,time
s0=time.perf_counter();p,t=13,231050784610489;B=10**2400;X=p**262*t**46;M=X//t;A=(p**263-1)//12//t;C=(t**47-1)//(t-1);D=A*C
assert gcd(X,D)==gcd(A,C)==1 and A*t==(p**263-1)//12
# Independent prime tests for < 50-bit factorization endpoints (trial division).
assert all(n%d for n in (13,t,263,401,877,104087) for d in range(2,isqrt(n)+1)); assert t-1==8*3*263*401*877*104087
@__import__('functools').cache
def labels(n):
 primepossible=lambda a:a>=3 and a%2 and a not in (7,11,13,19,31,t) and all(a%d or a==d for d in range(3,98,2) if all(d%j for j in range(2,isqrt(d)+1))) and pow(2,a,a)==2
 return primepossible(n) or isqrt(n)**2==n and primepossible(isqrt(n))
def cubic(p,c):
 yield 1,[0]; a=pow(next(i for i in range(2,p) if pow(i,(p-1)//3,p)!=1),(p-1)//3,p);m=p
 for _ in range(c):
  z=[a,(-1-a)%m];assert all((i*i+i+1)%m==0 for i in z) and z[0]!=z[1];yield m,z;m*=p;a=pow(a,p,m)
U={};L=list(cubic(t,45));high={}
def put(box,r,m,h):
 if r<3 or not r%2 or r**h>=m*m or X*lcm(D,r**h)>B or not labels(r): return
 box[r]=max(box.get(r,1),R(m*m,r**h))
for a,aa in cubic(p,262):
 for b,bb in L:
  inv=pow(b,-1,a) if a!=1 else 0
  for z in aa:
   for v in bb:put(U,v+b*(((z-v)*inv)%a),a*b,2)
orders=[1]
for z in (3,263,401,877,104087):orders+= [o*z for o in orders]
for o in sorted(orders):
 if o<=3 or 3**min(8000,o-3)>=t**90:continue
 for r in range(3,10**6,2):
  if r**(o-3)>=t**90:break
  if pow(r,o,t)==1:put(high,r,gcd(pow(r,o,t**45)-1,t**45),o-3)
 else:raise AssertionError('high order tail')
assert not high;u=prod(U.values());assert len(U)==23 and -(-u.numerator//u.denominator)==2247129787084402954
# Keep the exact rational U rather than its integer ceiling throughout.
e=[0,0,0];H=max(A,C)
for i in range(263):
 for j in range(46):
  m=p**i*t**j;q=2*m-1;F=(M//m)**2
  if X*q*F>u*B:e[0]+=1;continue
  for Z in (A,C):
   if q>Z:continue
   step=4*m;upper=Z//q;z=Z*pow(q,-1,step)%step or step
   assert upper<step and (z>upper or Z%z!=0)
  if X*D*q>B:e[1]+=1;continue
  # Nested price, emitter-sigma incidence. Compare using exact denominators.
  assert 4*X**2*D*q**4*F > 9*B**2*H*u;e[2]+=1
assert e==[4984,5320,1794];print('PASS CRT 23, high 0, exact Euler windows',e,'elapsed',round(time.perf_counter()-s0,3))
H=Path(__file__).resolve().parents[2]/'GeminiFrontier';sh=json.loads((H/'ShardToKeys.json').read_bytes());ks=json.loads((H/'KeyToShards.json').read_bytes());assert [(n,z) for n,z in sh.items() if [13,262] in z]==[('P13_I00055',[[13,262]])] and ks['13,262']==['P13_I00055']
