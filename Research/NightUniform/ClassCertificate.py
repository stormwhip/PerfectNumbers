"""Standalone verifier for h-divisible prime support incompatibility in ANY odd perfect N; no size bound or canonical ordering. If h|e+1, sub-sigma S0|(2N), p^e contributes ≥I(p,h-1). Supposing another prime q|N, enumerate its ordinary and legal Euler exponents by finite head and a monotone tail. Use multiplication of S0 with sigma(q^f) only for an EXACT second component. All small factors listed checked trial prime/division. Multiple rows with no witnesses invalid; no large data or primality guesses. Emits triples (p,h,q): p^e||N and h|e+1 force q absent. Do not count a class as global shard closure unless all branches covered.
"""
import json,math,sys,argparse
from fractions import Fraction
from functools import cache
@cache
def prime(n):return 2<=n<10**8 and all(n%j for j in range(2,math.isqrt(n)+1))
@cache
def sig(p,f):return (p**(f+1)-1)//(p-1)
@cache
def ratio(p,f):return Fraction(sig(p,f),p**f)
def val(z,r):
 c=0
 while not z%r:z//=r;c+=1
 return c

def lower(p,h,q,f,tail,special,rs):
 A=sig(p,h-1)*(1 if tail else sig(q,f));v=ratio(p,h-1)*ratio(q,f);discount=Fraction(1)
 for r in rs:
  if type(r)!=int or not prime(r) or r in (p,q) or A%r:raise ValueError('bad factor');
  c=val(A,r);t=c+c%2;v0=ratio(r,t);v*=v0
  if not special and r%4==1:discount=min(discount,ratio(r,c+(1-c)%4)/v0)
 return v*discount

def check(d):
 p,h,q,K=[d[k] for k in ['p','h','q','cut']];assert all(type(a)==int for a in (p,h,q,K)) and prime(p) and prime(q) and p>2 and q>2 and p!=q and 2<=h<=10000 and h%2 and 2<=K<=1000;A=sig(p,h-1);c=val(A,q);exp=[]
 for sp in (False,True):
  if sp and q%4!=1:continue
  f=max(c,1);k=4 if sp else 2;f+=((1 if sp else 0)-f)%k
  while True:
   exp.append((f,f>K,sp))
   if f>K:break
   f+=k
 rows=d['rows'];assert [(f,tail,sp) for f,tail,sp,rs in rows]==exp;worst=100
 for f,tail,sp,rs in rows:
  assert len(set(rs))==len(rs);z=lower(p,h,q,f,tail,sp,rs);assert z>2;worst=min(worst,z)
 return [p,h,q,len(rows),(worst-2)*10**9//1]
if __name__=='__main__':
 if not __debug__:raise SystemExit('never use -O')
 a=argparse.ArgumentParser();a.add_argument('packet');o=a.parse_args();D=json.load(open(o.packet));assert set((r['p'],r['h'],r['q']) for r in D).__len__()==len(D);print(json.dumps([check(r) for r in D],separators=(',',':')))
