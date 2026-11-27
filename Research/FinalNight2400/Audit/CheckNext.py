"""Separate (13,310) f=42 loss enumeration and direct, monotone p^a crossing search."""
from math import prod,gcd,lcm,isqrt
from fractions import Fraction
from functools import cache
from pathlib import Path
import json,time
s0=time.perf_counter();p,t=13,5424477432443;B=10**2400;X=p**310*t**42;A=(p**311-1)//12//t;C=(t**43-1)//(t-1);D=A*C;H=max(A,C)
assert A*t*12+1==p**311 and gcd(X,D)==gcd(A,C)==1
facs=(31,179,311,787,1997);assert prod(facs)*2==t-1 and gcd(3*13,t*(t-1)//2)==1
assert all(n%d for n in (*facs,t,13) for d in range(2,isqrt(n)+1));assert 3**12>=13**2 and 3**8000>B
@cache
def viable(r):
 ok=lambda n:n>=3 and n%2 and n not in (p,t,19,31,11,7) and pow(2,n,n)==2
 return ok(r) or isqrt(r)**2==r and ok(isqrt(r))
all_losses=[]
for s,w,c,ds in [(p,2,310,(3,)),(t,10,41,facs)]:
 out={};div=[1]
 for z in ds:div += [o*z for o in div]
 for o in sorted(div)[1:]:
  h=o-1
  if o>8000 or 3**h>=s**(w*c):continue
  def put(r,n):
   if r<3 or not r%2 or (r.bit_length()-1)*h>=w*n.bit_length():return
   rr=r**h;nn=n**w
   if rr<nn and X*lcm(D,rr)<=B and viable(r):out[r]=max(out.get(r,1),Fraction(nn,rr))
  # At a small search radius directly test all odd bases; otherwise lift primitive roots by s-th powering.
  if 10000**h>=s**(w*c):
   for r in range(3,10001,2):
    if r**h>=s**(w*c):break
    if pow(r,o,s)==1:put(r,gcd(pow(r,o,s**c)-1,s**c))
   continue
  ordps=[a for a in ds if o%a==0];a=1
  for k in range(2,s):
   a=pow(k,(s-1)//o,s)
   if all(pow(a,o//g,s)!=1 for g in ordps):break
  m=s
  for _ in range(c):
   roots=[pow(a,j,m) for j in range(1,o) if gcd(j,o)==1];assert len(set(roots))==len(roots)
   for r in roots:put(r,m)
   m*=s;a=pow(a,s,m)
 all_losses.append(out)
U=prod(u for d in all_losses for u in d.values());assert [len(d) for d in all_losses]==[6,0] and -(-U.numerator//U.denominator)==4016
stat=[0,0,0]
for i in range(311):
 for j in range(42):
  m=p**i*t**j;q=2*m-1;R=p**(2*(310-i))*t**(10*(41-j))
  if X*q*R>B*4016:stat[0]+=1;continue
  for Z in (A,C):
   if Z>=q:
    step=4*m;k=Z*pow(q,-1,step)%step or step;assert Z//q<step and (k>Z//q or Z%k)
  if X*D*q>B:stat[1]+=1;continue
  for v in range(42-j):
   # Binary search the actual powers p^a (not the real-valued endpoint). All smaller a obey the second bound if this maximum a does.
   lo,hi=-1,311-i
   while hi-lo>1:
    mid=(hi+lo)//2
    if 2*X*D*q*q*t**v*p**mid <= 3*B*H:lo=mid
    else:hi=mid
   if lo>=0:assert 2*X*q*q*R > 3*B*4016*t**(9*v)*p**lo
  stat[2]+=1
assert stat==[11596,930,536];P=Path(__file__).resolve().parents[2]/'GeminiFrontier';d=json.loads((P/'ShardToKeys.json').read_bytes());k=json.loads((P/'KeyToShards.json').read_bytes());assert [(name,z) for name,z in d.items() if [13,310] in z]==[('P13_I00063',[[13,310]])] and k['13,310']==['P13_I00063'];print('PASS independent 13x310 f42: 6+0 deficits, ceilU 4016, windows',stat,'time',round(time.perf_counter()-s0,3))
