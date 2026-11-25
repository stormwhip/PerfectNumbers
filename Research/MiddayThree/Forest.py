"""Root-three private-source forest. Euler is optional anywhere; root exponent exact.
Each external odd sigma prime-power is charged with full multiplicity. The
registered parent of a forest child may activate it only by actual divisibility.
Discovery hints are never needed by the replay.
"""
from pathlib import Path
from functools import cache
from math import gcd,prod
import json,sys,gzip
HERE=Path(__file__).resolve().parent
sys.path.insert(0,str(HERE.parent/'RootFiveNext'))
import PrimeCheck as pc
B=10**2400; BAN=(19,7,11,31,13)
def check(x,msg):
 if not x:raise ValueError(msg)
def v(n,p):
 t=0
 while n%p==0:n//=p;t+=1
 return t
def sg(r,f):return (r**(f+1)-1)//(r-1)
@cache
def prime_cached(q,chain):
 t=q
 for z in chain:check(z[0]==t,'ECPP mismatch');t=pc.level(*z)
 return pc.prime64(t)
def prime(q,cs):
 return prime_cached(q,tuple((n,t,f,a,tuple(pt)) for n,t,f,a,pt in cs[str(q)]) if q>=2**64 else ())
def legal(r,f):return all((f+1)%b if r%b==1 else pow(r,f+1,b)!=1 for b in BAN)
def rough(x,u):
 while (g:=gcd(x,u))!=1:x//=g
 return x
def measure(row,cs,verified=True,case=None):
 e=row['e'];A=sg(3,e);K=set(row['roots']);par={q:z for q,z in row['edges']};V=set(par)|K;hs=row['head'];check(e>=2 and e%2==0 and 0<hs<100,'cell');check(len(K)==len(row['roots']) and len(par)==len(row['edges']) and not(K&par.keys()),'duplicates');check(all(q>3 and q not in BAN and (not verified or prime(q,cs)) for q in V),'prime');check(all(A%q==0 for q in K),'root');check(all(3*A%q and z in V for q,z in par.items()),'edge');U=3*A*prod(par);kids={q:[] for q in V}
 for q,z in par.items():kids[z].append(q)
 seen=set();stack=list(K)
 while stack:
  z=stack.pop();check(z not in seen,'cycle');seen.add(z);stack.extend(kids[z])
 check(seen==V,'unreachable')
 @cache
 def node(r,c):
  best=[B+1,B+1];why=[None,None]
  for mode in (0,1):
   if mode and (r%4!=1 or any((r+1)%b==0 for b in BAN)):continue
   f=c+((1-c)%4 if mode else c%2);step=4 if mode else 2
   for ix in range(hs+1):
    while not legal(r,f):f+=step
    raw=r**f
    if raw>=max(best):break
    sel=(case.get(r) if isinstance(case,dict) else case[1:] if case and r==case[0] else None)
    if sel and ix<hs and ((sel[0]=='eq' and f!=sel[1]) or (sel[0]=='ge' and f<sel[1])):
     f+=step;continue
    if ix==hs:
     vals=[B+1,raw] if mode else [raw,raw]
    else:
     S=sg(r,f)//(2 if mode else 1);cost=raw*rough(S,U);terms=[node(q,h)[0] for q in kids[r] if (h:=v(S,q))];cost*=prod(x[0] for x in terms);vals=[B+1,cost] if mode else [cost,min([cost]+[cost//x[0]*x[1] for x in terms])]
    for k in (0,1):
     if vals[k]<best[k]:best[k]=vals[k];why[k]=[f,mode,ix==hs]
    f+=step
  return tuple(best),why
 base=3**e*A//prod(q**v(A,q) for q in K);ns={q:node(q,v(A,q)) for q in K};std=base*prod(x[0][0] for x in ns.values());ans=min([std]+[std//x[0][0]*x[0][1] for x in ns.values()]);return ans,{str(q):x[1] for q,x in ns.items()},(node,std)

def replay(path):
 pk=json.loads(gzip.decompress(Path(path).read_bytes()));row=pk['row'];cs=pk['ecpp'];m,_,_=measure(row,cs);print(row['e'],len(str(m))-1,'CLOSED' if m>B else 'OPEN');return m
if __name__=='__main__':
 for f in sys.argv[1:]:replay(f)
