"""Direct auditable free-Euler lower-bound trees. Explicit path scope only."""
from pathlib import Path
from math import gcd,prod
from fractions import Fraction
from functools import cache
from itertools import count
from collections import Counter
import sys,gzip,json
assert __debug__
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'RootFiveNext')];import PrimeCheck as pc
t=1214428680506010004551311201724184433986966434253654794712076383;r=2649006202622389754026474949684537136117722932291062868195158132223440533168779423867212541;a=541060314202200985634836209806257
base=[(19,330),(t,2)];paths=[base+[(r,g)] for g in [2,4,6]]+[base+[(r,g),(a,j)] for g in [2,4,6] for j in (1,2,4,5,6,8,9,10,12,13,14,16,17)]
B=10**2400
@cache
def sig(p,e):return (p**(e+1)-1)//(p-1)
@cache
def ab(p,e):return Fraction(sig(p,e),p**e)
def val(n,p):
 h=0
 while n%p==0:h+=1;n//=p
 return h
@cache
def nextf(p,h,bad,odd):
 f=h+((1-h)%4 if odd else h%2);step=4 if odd else 2
 while p**f<=B:
  if all((f+1)%k if p%k==1 else pow(p,f+1,k)!=1 for k in bad):return f
  f+=step
 return None
small=[q for q in range(3,128,2) if pc.prime64(q)]
book={};used=set();stats=Counter()
@cache
def prime(p):
 assert type(p)==int and p>2;n=p
 if n>=2**64:
  used.add(str(p));chain=book[str(p)];assert chain
  for row in chain:
   assert n==row[0];n=pc.level(*row)
 assert pc.prime64(n)
def readfile(p):
 if p.exists():return json.loads(p.read_bytes())
 return json.loads(gzip.decompress(p.with_suffix('.json.gz').read_bytes()))
def verify(i):
 P=paths[i];fs,tr=readfile(H/f'Ab330Case{i}.json');rows={};S=X=1;I=Fraction(1);eufix=False
 for p,e in P:
  prime(p);assert p not in rows and (not rows and (p,e)==(19,330) or S%p==0)
  assert not e%2 or not eufix and p%4==e%4==1
  rows[p]=e;X*=p**e;S*=sig(p,e)//(1+e%2);I*=ab(p,e);eufix=eufix or bool(e%2)
 C=S//gcd(S,X);assert len(set(fs))==len(fs) and not set(fs)&rows.keys()
 for p in fs:prime(p);assert C%p==0
 def rec(tr,X,S,I,seen,forced,banned,usedEuler):
  Y=S//gcd(S,X);D=X*Y
  if gcd(Y,X)>1 or D>B:assert tr=='base';stats['base']+=1;return
  F={p:val(Y,p) for p in forced if p not in seen and Y%p==0};bad=set(banned)
  while True:
   bd=tuple(sorted(bad));even={p:nextf(p,h,bd,False) for p,h in F.items()};odds={p:nextf(p,h,bd,True) for p,h in F.items() if p%4==1 and not usedEuler};none=[p for p,e in even.items() if e is None]
   def minimum(row,base,unreachable):
    v0=base*prod(row(p,e) for p,e in even.items() if e is not None);lo=v0 if not none else unreachable
    for p,f in odds.items():
     if f is None or any(q!=p for q in none):continue
     lo=min(lo,v0*row(p,f)/(row(p,even[p]) if p not in none else 1))
    return lo
   lowI=minimum(ab,I,Fraction(3))
   if lowI>2:assert tr=='abundance';stats['abundance']+=1;return
   new={u for u in small if u not in seen and u not in F and u not in bad and lowI*ab(u,1 if not usedEuler and u%4==1 else 2)>2}
   if not new:break
   bad|=new
  # Fraction division, never float, in common minimum() routine.
  sz=minimum(lambda p,e:Fraction(p**(e-F[p])),Fraction(D),Fraction(B+1))
  if sz>B:assert tr=='parity';stats['parity']+=1;return
  assert isinstance(tr,list) and len(tr)==2;p,ch=tr;assert p in F;stats['split']+=1;done=set()
  for f in count(F[p]):
   if X*(Y//p**F[p])*p**f>B:break
   if f%2 and (usedEuler or p%4!=1 or f%4!=1):continue
   a=sig(p,f)
   if any(a%u==0 for u in bad):continue
   more,sub=ch[str(f)];done.add(str(f));assert len(set(more))==len(more)
   for u in more:prime(u);assert a%u==0
   rec(sub,X*p**f,S*(a//(1+f%2)),I*ab(p,f),seen|{p:f},set(F)|set(more),bad,usedEuler or bool(f%2))
  assert done==set(ch)
 rec(tr,X,S,I,rows,set(fs),set(),eufix)
if __name__=='__main__':
 ids=[1,2] if not sys.argv[1:] else list(map(int,sys.argv[1:]))
 for f in H.glob('Ab330Book*.json.gz'):book.update(json.loads(gzip.decompress(f.read_bytes())))
 for i in ids:
  prev=stats.copy();verify(i);print('PASS',i,[e for p,e in paths[i]],stats-prev,flush=True)
 print('PASS exact path trees:',len(ids),'ECPP used',len(used),'counts',stats)