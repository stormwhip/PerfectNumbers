"""Recompute exact deficit exceptions independently on the eight T^6 proof paths.
Alternate lifts x -> x^p, generic H=sum(weights), descending CRT moduli, direct geometric valuations.
Only the comparison at the end imports the candidate enumerators.
"""
from pathlib import Path
from fractions import Fraction
from functools import cache
from itertools import product
from math import gcd,prod,isqrt
import json,sys,time
H=Path(__file__).resolve().parent.parent/'Ten';sys.path.insert(0,str(H));import Weighted,PriceCore
B=10**2400;start=time.perf_counter()
@cache
def divisors(n):return sorted({i for k in range(1,isqrt(n)+1) if not n%k for i in (k,n//k)})
@cache
def residues(p,o,cap):
 if not cap:return []
 ds=divisors(o)[:-1];a=1
 for k in range(2,p):
  a=pow(k,(p-1)//o,p)
  if a and all(pow(a,i,p)!=1 for i in ds):break
 assert pow(a,o,p)==1
 m=p;result=[]
 for i in range(cap):
  zs=tuple(pow(a,j,m) for j in range(1,o) if gcd(j,o)==1)
  assert len(zs)==len(set(zs)) and all(pow(z,o,m)==1 for z in zs)
  result.append((m,zs));m*=p;a=pow(a,p,m)
 return result
@cache
def inv(a,m):return pow(a,-1,m)
def val(x,p):
 k=0
 while x%p==0:k+=1;x//=p
 return k
for i in range(3,11):
 weighted=i in (3,9,10); d=json.loads((H/(('Weight' if weighted else 'Tree')+str(i)+'.json')).read_bytes());P=tuple(map(tuple,d['path']));fixed=dict(P);X=prod(p**k for p,k in P);S=prod((p**(k+1)-1)//(p-1) for p,k in P)//2;C=S//gcd(X,S)
 ts=[(p,k-val(S,p),6 if weighted and p==3291622576015727423 else 2) for p,k in P if k!=1];h=sum(w for _,_,w in ts);U={};quot=B//X
 @cache
 def add(r,f):
  if r<3 or not r%2 or r in fixed:return
  D=r**f
  if D>quot or D//gcd(D,C)>quot//C:return
  if pow(2,r,r)!=2:return
  s=(D*r-1)//(r-1); m=1
  for p,c,w in ts:
   a=gcd(s,p**(c+1));
   if a==p**(c+1):return
   m*=a**w
  if m>D:U[r]=max(Fraction(m,D),U.get(r,1))
 def opts(f,p,c):
  shift=val(f+1,p)
  if 0<shift<=c:yield (1,p,p**shift)
  for o in divisors(gcd(f+1,p-1)):
   if o==1 or c<=shift:continue
   for m,zs in residues(p,o,c-shift):
    for z in zs:yield (z,m,m*p**shift)
 def prog(z,m,cost,f):
  z=z or m
  if z%2==0:z+=m
  while (z.bit_length()-1)*f<cost.bit_length() and z**f<cost:
   add(z,f);z+=2*m
 for f in range(2,h,2):
  for combo in product(*([[ (0,1,1), *opts(f,p,c)] for p,c,w in ts])):
   cost=prod(a**w for (_,_,a),(_,_,w) in zip(combo,ts));mod=prod(m for _,m,_ in combo)
   z=sum(r*(mod//m)*inv(mod//m,m) for r,m,_ in combo if m>1)%mod
   prog(z,mod,cost,f)
 for p,c,w in ts:
  for f in range(h,8002,2):
   if 3**f>=p**(h*c) or 3**f>quot:break
   for z,m,a in opts(f,p,c):prog(z,m,a**h,f)
  else:raise AssertionError('exponent tail')
 other=(Weighted if weighted else PriceCore).excludes(P,(),[j for j in range(len(P)) if j!=1])[3]
 # The reference additionally uses trial division; independently overincludable Fermat pseudoprimes can be removed when a divisor is exhibited.
 for r in list(set(U)-set(other)):
  assert any(r>d and r%d==0 for d in range(3,98,2)); del U[r]
 assert U==other,(i,set(U)^set(other)); print('PASS all per-base exact deficits',i,'#',len(U),flush=True)
print('PASS independent weighted / unweighted spectra in',round(time.perf_counter()-start,3),'s')
