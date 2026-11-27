"""Exact joint-price/forced-component proofs on residual T^6 paths."""
import sys,json,gzip,hashlib
from math import prod,gcd
from fractions import Fraction
from itertools import count
from pathlib import Path
from functools import cache
assert __debug__
H=Path(__file__).resolve().parent; R=H.parents[1]
sys.path[:0]=[str(H),str(R/'RootFiveNext')]
import PrimeCheck
from PriceCore import excludes,val,B
b=(R/'Night2400/C10/EulerF1.json.gz').read_bytes();assert hashlib.sha256(b).hexdigest()=='f52b0f8b3fd0f8e869e0e38f7d6ac34cf0254a1082dce5c2ad8df3f2ca7f5c90'
d=json.loads(gzip.decompress(b)); book=d['ecpp']
@cache
def prime(q):
 assert type(q)==int and q>2
 n=q
 if n>=2**64:
  for a in book[str(n)]:assert a[0]==n;n=PrimeCheck.level(*a)
 assert PrimeCheck.prime64(n)
def sig(q,f):return (q**(f+1)-1)//(q-1)
@cache
def low(q,h,Q,cs):
 # Lower bound on r^f / (product target supply)^2, for every even f >= h.
 # To skip an exponent we must prove it overfills an exact target.
 M2=prod(p**(2*c) for p,c in zip(Q,cs));best=None
 for f in count(h+h%2,2):
  a=q**f
  if best is not None and a*best.denominator>=best.numerator*M2:return best
  vs=[]
  for p,c in zip(Q,cs):
   if q%p==1:v=val(f+1,p)
   elif pow(q,f+1,p)!=1:v=0
   else:
    m=p**(c+1);r=(pow(q,f+1,m)-1)%m;v=val(r,p) if r else c+1
   vs.append(v)
  if all(v<=c for v,c in zip(vs,cs)):
   x=Fraction(a,prod(p**(2*v) for p,v in zip(Q,vs)));best=x if best is None else min(best,x)
def check(index):
 z=json.loads((H/f'Tree{index}.json').read_bytes());P=[tuple(row) for row in z['path']];fixed=dict(P)
 assert P[0]==(19,58) and P[1]==(d['pivot'],1) and P[2]==(d['tree']['q'],6) and len(P)==len(fixed)
 t=d['tree'];
 for p,e in P[2:]:assert t['type']=='split' and t['q']==p;t=t['cases'][str(e)]
 assert t is None and sum(e%2 for p,e in P)==1
 for p in fixed:prime(p)
 X=prod(p**e for p,e in P);S=prod(sig(p,e) for p,e in P)//2;C=S//gcd(X,S)
 V,Q,cs,exc=excludes(P,(),[i for i in range(len(P)) if i!=1]);assert Q==tuple(p for i,(p,e) in enumerate(P) if i!=1)
 def gain(q,h):return low(q,h,Q,cs)*exc.get(q,1)
 roots=z['roots'];assert len(roots)==len(set(roots)) and not set(roots)&fixed.keys()
 for q in roots:prime(q);assert C%q==0
 stats=[0,0,0];worst=None
 def close(U):
  nonlocal worst
  assert U>B
  worst=U if worst is None else min(worst,U)
 def walk(t,Z,F,spent):
  U=Z*prod(gain(r,h) for r,h in F.items());assert not F.keys()&spent
  if t is True:close(U);stats[0]+=1;return
  assert type(t)==dict and set(t)=={'q','cases'};q=t['q'];assert q in F
  h=F[q];others={r:b for r,b in F.items() if r!=q};other=U/gain(q,h);ch=t['cases'];done=set();stats[1]+=1
  for f in count(h+h%2,2):
   if other*gain(q,f)>B:close(other*gain(q,f));stats[2]+=1;break
   row=ch[str(f)];done.add(str(f));s=sig(q,f);vs=[val(s,p) for p in Q]
   if any(v>c for v,c in zip(vs,cs)):assert row=='conflict';continue
   new,child=row;assert len(set(new))==len(new) and not set(new)&(set(others)|set(spent)|set(fixed)|{q})
   for r in new:prime(r);assert s%r==0
   exact=Fraction(q**f,prod(p**(2*v) for p,v in zip(Q,vs)))*exc.get(q,1)
   walk(child,Z*exact,{**others,**dict.fromkeys(new,1)},spent|{q})
  assert done==set(ch)
 walk(z['tree'],V,{q:val(C,q) for q in roots},set());assert worst is not None
 floor=len(str(worst.numerator//worst.denominator))-1
 print('PASS',index,[e for p,e in P], 'terminal/split/tail',stats,'minimum floor',floor,flush=True)
if __name__=='__main__':
 if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
 for i in (4,5,6,7,8):check(i)
