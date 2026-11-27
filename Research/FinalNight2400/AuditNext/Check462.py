"""Independent ordinary-only forest and mixed two-target price for (11,462), first 22."""
from pathlib import Path
from functools import cache
from fractions import Fraction
from math import gcd,isqrt,prod
import json,time
s0=time.perf_counter();H=Path(__file__).resolve().parent.parent/'Eleven';f=json.loads((H/'OrdinaryForest22.json').read_bytes());K=f['roots'];head=128;edges=f['owners'];T=879701;B=10**2400;no=(19,7);P=[(11,462),(T,22)]
def sigma(p,e):return (p**(e+1)-1)//(p-1)
S=prod(sigma(p,e) for p,e in P);X=prod(p**e for p,e in P);D=S//gcd(S,X);assert gcd(D,X)==1
vs=set(K)|{a for a,z in edges};children={z:[] for z in vs}
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
assert root>B and len(str(root))-1==2403 and len(vs)==1990
# Different lifts, CRT order, cap and high-order enumeration from issuer.
from functools import cache
@cache
def levels(p,o,c):
 a=next(w for g in range(2,p) if all(pow((w:=pow(g,(p-1)//o,p)),d,p)!=1 for d in range(1,o) if not o%d));m=p;ret=[]
 for _ in range(c):ret.append((m,[pow(a,i,m) for i in range(1,o) if gcd(i,o)==1]));m*=p;a=pow(a,p,m)
 return ret
u={};v={};p=11;X=p**462*T**22;M=X//gcd(X,S);assert M==p**462*T**21
def charge(out,z,m,h):
 if z<=2 or not z%2 or 5*h*(z.bit_length()-1)>=19*m.bit_length():return
 if any(z%d==0 and z not in (d,d*d) for d in (3,5,7,11,13,17,19,23,29,31,37,41,43)):return
 a=z**(5*h);b=m**19
 if b>a:out[z]=max(out.get(z,1),Fraction(b,a))
for m,aa in [(1,[0]),*levels(p,5,462)]:
 for n,bb in [(1,[0]),*levels(T,5,21)]:
  inv=pow(n,-1,m) if m>1 else 0
  for a in aa:
   for b in bb:charge(u,b+n*((a-b)*inv%m),m*n,4)
for o in range(7,8001,2):
 if (T-1)%o or 3**(5*(o-5))>=T**(21*19):continue
 h=o-5
 if 10000**(5*h)>=T**(21*19):
  for r in range(3,10000,2):
   if r**(5*h)>=T**(21*19):break
   if pow(r,o,T)==1:charge(v,r,gcd(pow(r,o,T**21)-1,T**21),h)
 else:
  for n,rs in levels(T,o,21):
   for r in rs:charge(v,r,n,h)
U=prod(u.values(),start=Fraction(1))*prod(v.values(),start=Fraction(1));badverts={z for z in vs if z%4==1};assert len(badverts)==1019 and all((X*z)**5*(M//gcd(M,z+1))**19>B**5*U for z in badverts)
G=H.parents[1]/'GeminiFrontier';sh=json.loads((G/'ShardToKeys.json').read_bytes());inv=json.loads((G/'KeyToShards.json').read_bytes());assert [(n,z) for n,z in sh.items() if [11,462] in z]==[('P11_I00088',[[11,462]])] and inv['11,462']==['P11_I00088'];print('PASS independent fixed-even forest floor 2403, 1019/1990 vertex-Euler contradictions, 2-target exception counts',len(u),len(v),'elapsed',round(time.perf_counter()-s0,3))
