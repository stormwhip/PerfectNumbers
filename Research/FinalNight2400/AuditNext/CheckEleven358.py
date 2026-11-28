"""Independent (11,358) t^28/30 disjoint order spectra and complete Euler allocation windows."""
from math import prod,gcd,lcm,isqrt
from fractions import Fraction
from functools import cache
from pathlib import Path
import json,time
s0=time.perf_counter();p,t=11,2471107084783904470093;B=10**2400;facs=(3,7,109,359,34147,22016018359);assert 4*prod(facs)==t-1 and gcd(5*11,t*(t-1)//4)==1
assert all(n%d for n in facs for d in range(2,isqrt(n)+1));assert any(pow(g,t-1,t)==1 and all(gcd(pow(g,(t-1)//z,t)-1,t)==1 for z in (2,*facs)) for g in range(2,1000));assert 3**8000>B and 3**10>=11**2
@cache
def viable(r):
 ok=lambda n:n>=3 and n%2 and n not in (p,t,19,7) and pow(2,n,n)==2
 return ok(r) or isqrt(r)**2==r and ok(isqrt(r))
for F in [28,30]:
 X=p**358*t**F;A=(p**359-1)//10//t;C=(t**(F+1)-1)//(t-1);D=A*C;M=X//t;H=max(A,C);assert t*A==(p**359-1)//10 and gcd(A,C)==gcd(X,D)==1
 all_losses=[]
 for s,w,c,ds in [(p,2,358,(5,)),(t,2,F-1,facs)]:
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

 U=prod(u for z in all_losses for u in z.values());assert [len(z) for z in all_losses]==[2,0] and -(-U.numerator//U.denominator)==404
 stat=[0,0,0]
 for i in range(359):
  for j in range(F):
   m=p**i*t**j;q=2*m-1;R=(M//m)**2
   if X*q*R>B*404:stat[0]+=1;continue
   for Z in (A,C):
    if Z>=q:
     step=4*m;z=(Z*pow(q,-1,step))%step or step;assert Z//q<step and (z>Z//q or Z%z)
   if X*D*q>B:stat[1]+=1;continue
   assert 4*X*X*D*q**4*R>9*B*B*404*H;stat[2]+=1
 assert stat==([4941,4987,124] if F==28 else [7095,3675,0]);print('PASS alternative lifts, 2+0 labels U404, windows',F,stat)
G=Path(__file__).resolve().parents[2]/'GeminiFrontier';d=json.loads((G/'ShardToKeys.json').read_bytes());k=json.loads((G/'KeyToShards.json').read_bytes());assert [(n,vs) for n,vs in d.items() if [11,358] in vs]==[('P11_I00070',[[11,358]])] and k['11,358']==['P11_I00070'];print('PASS singleton, elapsed',round(time.perf_counter()-s0,3))
