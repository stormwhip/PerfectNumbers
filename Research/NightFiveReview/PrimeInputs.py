"""Separate affine (no projective formulas) proof of primality for the input packs.
Hasse with a prime divisor of n up to sqrt(n); invert every attempted denominator.
Small primes use proven deterministic MR bases below 2^64, not probable-prime tests above it.
"""
from LocalModel import R,NF,primes
from functools import cache
import json,math,hashlib
BASES=(2,325,9375,28178,450775,9780504,1795265022)
@cache
def small(n):
 if n in (2,3):return True
 if n<3 or n%2==0 or n>=2**64:return False
 d=n-1;s=0
 while not d%2:d//=2;s+=1
 for a in BASES:
  if a%n==0:continue
  t=pow(a,d,n)
  if t in (1,n-1):continue
  for _ in range(s-1):
   t=t*t%n
   if t==n-1:break
  else:return False
 return True
@cache
def curve(n,t,k,a,x,y):
 b=(y*y-x**3-a*x)%n;assert n%2 and math.gcd(n,6*(4*a**3+27*b*b))==1;order=n+1-t;q,rem=divmod(order,k);assert k>0 and not rem and t*t<4*n and (math.isqrt(math.isqrt(n))+2)**2<q<n
 def add(P,Q):
  if P is None:return Q
  if Q is None:return P
  x,y=P;u,v=Q
  if x==u:
   if (y+v)%n==0:return None
   assert y==v
   slope=(3*x*x+a)*pow(2*y,-1,n)%n
  else:slope=(v-y)*pow(u-x,-1,n)%n
  w=(slope*slope-x-u)%n;return w,(slope*(x-w)-y)%n
 def times(k,P):
  A=None
  while k:
   if k%2:A=add(A,P)
   k//=2
   if k:P=add(P,P)
  return A
 P=times(k,(x%n,y%n));assert P is not None and times(q,P) is None;return q
if __name__=='__main__':
 cert=json.loads((R/'IndicatorCapacity/Certificates/DualP5.json').read_text());static=json.loads((R/'RootFiveNext/RootFiveCertificate.json').read_text())['ecpp'];replayed=set()
 for packnum,es in [(8,[460,568,592]),(13,[178,196])]:
  a=json.loads((NF/f'Batch{packnum}.json').read_text());qs=set(map(int,(v for e in es for v in a['roots'][str(e)])));qs.update(int(r) for values in a['secondary'].values() for r in values);qs.update(r for row in cert['duals']+a['duals'] for p,f,w,v in row['flows'] for r in (p,w));used=0
  for r in qs:
   n=r
   if n not in replayed and n>=2**64:
    key=hashlib.sha256(str(n).encode()).hexdigest()[:24];rows=static.get(key) or a['ecpp'][key];used+=1
    for m,t,k,z,P in rows:assert m==n;n=curve(m,t,k,z,*P)
   elif n in replayed:continue
   assert small(n);replayed.add(r)
  print('pack',packnum,'prime inputs',len(qs),'new chains',used,'cumulative levels',curve.cache_info().currsize,flush=True)
