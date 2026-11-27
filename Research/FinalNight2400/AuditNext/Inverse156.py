"""Independent inverse-CRT supplier and weighted-price audit at 3^6 1093^156 2035349^66."""
from pathlib import Path
from fractions import Fraction
from functools import cache
from itertools import product
from math import gcd,prod,isqrt
import json,sys,time
from math import lcm
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
for iteration in [1]:
 q,r=1093,2035349;P=((3,6),(q,156),(r,66));X=prod(p**e for p,e in P);S=prod((p**(e+1)-1)//(p-1) for p,e in P);C=S//gcd(X,S);ts=[(q,156-val(S,q),2),(r,66-val(S,r),6)];h=8;U={};quot=B//X;fixed=dict(P);banned=(19,7,11,31,13)
 @cache
 def add(r,f):
  if r<5 or not r%2:return
  b=isqrt(r);z=b if b*b==r else r
  if z in fixed or z in banned:return
  if pow(2,r,r)!=2 and not (b*b==r and b%4==1):return
  if any(r%d==0 and r not in (d,d*d) for d in (3,5,17,23,29,37,41,43,47,53,59,61,67,71,73,79,83,89,97)):return
  D=r**f
  if D>quot or D//gcd(D,C)>quot//C:return

  s=(D*r-1)//(r-1); m=1
  if gcd(s,prod(banned))>1:return
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
   if 5**f>=p**(h*c) or 5**f>quot:break
   for z,m,a in opts(f,p,c):prog(z,m,a**h,f)
  else:raise AssertionError('exponent tail')
 U=prod(U.values(),start=Fraction(1));V=Fraction(X*prod(p**(w*c) for p,c,w in ts),U);print('independent price floor',len(str(V.numerator//V.denominator))-1,flush=True);assert len(str(V.numerator//V.denominator))-1==4290
 A=[(p**(e+1)-1)//(p-1)//gcd((p**(e+1)-1)//(p-1),X) for p,e in P];A=A[1:];assert gcd(*A)==1 and C==prod(A);rough=10000001
 for n,o in zip(A,(157,67)):assert isqrt(n)**2!=n and gcd(n,2*o)==1 and all(n%x for x in range(2*o+1,rough+1,2*o))
 # Rebuild all class/cofactor comparisons by Teichmueller powers through fixed cutoffs directly.
 for e,L in [(1,77),(2,52)]:
  m=q**L;rs=[pow(x,q**(L-1),m) for x in range(2,q) if pow(x,273,q)==1];assert len(set(rs))==272
  for n,k in zip(A,[157,67]):
   mod=2*k*m;ii=pow(2*k,-1,m)
   for z in rs:
    a=1+2*k*((z-1)*ii%m);j=n*pow(a,-e,mod)%mod or mod;assert a**e*j>n
 # Recompute last bound at every feasible u via monotone binary search over v, no assumed stored window list.
 cnt=0;mx=0;n=C
 while n>=rough:mx+=1;n//=rough
 ext=(5*17*23)**2 if Fraction(S,X)*Fraction(rough,rough-1)**mx*Fraction(1000,999)*Fraction(5,4)*Fraction(17,16)<2 else 1;assert ext<=rough
 for i in range(ts[0][1]+1):
  for j in range(ts[1][1]+1):
   m=q**i*r**j;lo=2*m-1;k=q**(2*i)*r**(6*j)
   if V*lo>B*k:continue
   for n in A:
    step=4*m;z=n*pow(lo,-1,step)%step or step;assert all(n%c for c in range(z,n//lo+1,step))
   if X*C*lo>B:continue
   ff=ext if lo>=1000 else 1
   if X*C*lo*rough**2*ff>B:continue
   cnt+=1
   for u in range(ts[0][1]-i+1):
    K=ff*rough*X*C*lo;left=-1;right=ts[1][1]-j+1
    while right-left>1:
     mid=(left+right)//2;mass=2*lo*q**u*r**mid
     if K*mass>3*B*max(A) or u>=52 and K*K*mass>3*B**2 or u>=77 and K*mass>3*B:right=mid
     else:left=mid
    if left>=0:assert 2*V*lo**2*q**u*r**left>3*B*k*q**(2*u)*r**(6*left)
 assert cnt==707;print('PASS independent inverse cuts 52/77, external source windows',cnt,'seconds',round(time.perf_counter()-start,3))
