"""Independent ordinary-only forest and t-only price for canonical (31,16), first 16."""
from pathlib import Path
from functools import cache
from fractions import Fraction
from math import gcd,isqrt,prod
import json,time
s0=time.perf_counter();H=Path(__file__).resolve().parent.parent/'ThirtyOne';f=json.loads((H/'Forest16.json').read_bytes());K=f['roots'];head=f['head'];edges=f['owners'];T=751670559138758105956097;B=10**2400;no=(19,7,11);P=[(31,16),(T,16)]
def sigma(p,e):return (p**(e+1)-1)//(p-1)
S=prod(sigma(p,e) for p,e in P);X=prod(p**e for p,e in P);D=S//gcd(S,X);assert gcd(D,X)==1
vs=set(K)|{a for a,z in edges};children={z:[] for z in vs};assert all(z%4!=1 or (z+1)%T for z in vs)
for a,z in edges:children[z].append(a)
cp={z:prod(child) for z,child in children.items()};pool=X*D*prod(a for a,z in edges)
def val(n,z):
 k=0
 while n%z==0:k+=1;n//=z
 return k
def trim(z):
 while (g:=gcd(z,pool))!=1:z//=g
 return z
@cache
def low(z,h):
 e=h+h%2;best=B+1;cnt=0
 while z**e<best and cnt<head:
  s=sigma(z,e)
  if all(s%b for b in no):
   cnt+=1;g=gcd(s,cp[z]);n=z**e*trim(s)
   if g>1:n*=prod(low(a,val(s,a)) for a in children[z] if not g%a)
   best=min(n,best)
  e+=2
 return min(best,z**e)
root=X*D
for z in K:
 h=val(D,z);assert h>0;root//=z**h;root*=low(z,h)
assert root>B and len(str(root))-1==2402 and X*T**180>B
# For independent price enumeration, use a different generator per order and Hensel Newton digits, testing every possibly losing primitive class.
orders=[1]
for a in (13,17,31,37,409,1129,25085030513):orders += [v*a for v in orders]
L=T**180;bad={31,T,19,7,11}
@cache
def viable(r):
 w=lambda z:z>=3 and z%2 and z not in bad and pow(2,z,z)==2
 return w(r) or isqrt(r)**2==r and w(isqrt(r))
for o in orders[1:]:
 if o>8000 or 3**(o-1)>=L:continue
 h=o-1;assert h>=12
 if 10000**h>=L:
  for r in range(3,10000,2):
   if r**h>=L:break
   if pow(r,o,T)==1:assert gcd(pow(r,o,T**15)-1,T**15)**12<=r**h or not viable(r)
  continue
 divisors=[v for v in range(1,o) if o%v==0]
 a=next(v for g in range(2,1000) if all(pow((v:=pow(g,(T-1)//o,T)),k,T)!=1 for k in divisors))
 roots=[pow(a,j,T) for j in range(1,o) if gcd(j,o)==1];m=T
 for level in range(15):
  for r in roots:
   if r>2 and r%2 and (r.bit_length()-1)*h<12*m.bit_length() and r**h<m**12:assert not viable(r)
  if level<14:roots=[r+m*((-((pow(r,o,m*T)-1)//m)*pow(o*pow(r,o-1,T),-1,T))%T) for r in roots];m*=T
print('PASS all Euler placements: independent ordinary recurrence floor',len(str(root))-1,'zero t-price exceptions; elapsed',round(time.perf_counter()-s0,3),'s')
