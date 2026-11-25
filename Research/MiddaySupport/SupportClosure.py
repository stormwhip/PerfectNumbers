"""Exact monotone abundance propagation on a positive support cell, no solver or cache."""
import json,math,sys,argparse
from fractions import Fraction as F
from pathlib import Path
from functools import cache
from collections import Counter
H=Path(__file__).resolve().parent
ORDER=(19,7,11,31,13,3,5,17)
@cache
def sig(q,f):return (q**(f+1)-1)//(q-1)
@cache
def I(q,f):return F(sig(q,f),q**f)
@cache
def primes(n):return tuple(q for q in range(3,n+1,2) if all(q%i for i in range(3,math.isqrt(q)+1,2)))
@cache
def hints(p,e):
 n=sig(p,e); ds=[q for q in primes(6001) if n%q==0]; z=n
 for q in (2,*ds):
  while z%q==0:z//=q
 if 1<z<=10**9 and all(z%i for i in range(2,math.isqrt(z)+1)):ds.append(z)
 return tuple(ds)
def legal(q,f,bad):return all((f+1)%r if q%r==1 else pow(q,f+1,r)!=1 for r in bad)
def ev(q,a,bad,sp):
 if sp and (q%4!=1 or not legal(q,1,bad)):return None
 step,m=(4,1) if sp else (2,0); f=a+(m-a)%step
 while not legal(q,f,bad):f+=step
 return f

def close(p,e,yes,absent=(),fixed=(),low=(),steps=20):
 X=dict([(p,e),*fixed]); L={q:1 for q in yes};L.update(low); bad=set(ORDER[:ORDER.index(p)])|set(absent); trace=[]
 for loop in range(steps):
  if (why:=set(X)&bad or set(L)&bad):return 'forbidden',trace
  C=math.prod(sig(q,f)//(2 if f%2 else 1) for q,f in X.items()); base=math.prod(q**f for q,f in X.items()); K=set(L)|{r for q,f in X.items() for r in hints(q,f)}|set(X)
  if any(C%r==0 for r in bad):return 'emission',trace
  if any(f<L.get(q,1) or C%q**(f+1)==0 for q,f in X.items()) or sum(f%2 for f in X.values())>1:return 'capacity',trace
  if base*(C//math.gcd(C,base))>10**2400:return 'size',trace
  lo={q:max(1,L.get(q,1)) for q in K-set(X)}
  for q in lo:
   v=0;n=C
   while n%q==0:n//=q;v+=1
   lo[q]=max(lo[q],v)
  tot=math.prod(I(q,f) for q,f in X.items()); sp0=any(f%2 for f in X.values()); A={q:ev(q,h,bad,False) for q,h in lo.items()}; E={q:f for q,h in lo.items() if not sp0 and (f:=ev(q,h,bad,True))}; tot*=math.prod(I(q,f) for q,f in A.items()); cuts={q:I(q,f)/I(q,A[q]) for q,f in E.items()}; discount=min([F(1),*cuts.values()]); lb=tot*discount
  if lb>2:return 'abundance',trace
  # Monotonicity: even a first power at an as-yet-unrepresented r would be too abundant.
  add={r for r in primes(251) if r not in K and r not in bad and lb*(r+1)>2*r};
  if add:bad.update(add);trace.append(['ban',sorted(add)]);continue
  fix=False
  for q in sorted(lo):
   other=min([F(1)]+[v for r,v in cuts.items() if r!=q]); t=tot/I(q,A[q]); opts=[]
   for f,d,z in [(A[q],2,other)]+([(E[q],4,1)] if q in E else []):
    if t*I(q,f)*z<=2:
     opts.append(f);g=f+d
     while not legal(q,g,bad):g+=d
     if t*I(q,g)*z<=2:opts.append(g)
   if not opts:return 'all-options',trace
   if len(opts)==1:X[q]=opts[0];trace.append(['fix',q,opts[0]]);fix=True;break
  if not fix:return 'open',trace
 return 'open',trace

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--check',action='store_true');a=ap.parse_args(); d=json.loads((H.parent/'Nov25/Delta.json').read_text());actual=sorted({(s['root'],e) for s in d['remaining_shards'] for e in s['remaining_actuals']});out=[]
 for p,e in actual:
  if p in (3,5) or any(r in ORDER[:ORDER.index(p)] for r in (3,5)):continue
  why,t=close(p,e,(3,5));out.append([p,e,why,t]);
 f=H/'Positive35.json';text=json.dumps(out,separators=(',',':'))+'\n'
 if a.check:
  if text!=f.read_text():raise ValueError('record mismatch')
 else:f.write_text(text)
 print(Counter((p,w) for p,e,w,t in out));print('rows',len(out),'open',sum(w=='open' for p,e,w,t in out))
if __name__=='__main__':main()
