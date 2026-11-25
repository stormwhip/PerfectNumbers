"""Exact simultaneous output/abundance terminal for canonical root five.
All active exact-source odd divisor sums divide N *in product*. Split each
output between explicit bases and a residual (all its primes >= L). Residuals
need not be coprime. A true N pays every residual in product; give all their
prime supports their maximal abundance free, even multiply credited. The
remaining outside primes not occurring in any emitted residual cost at least
the ordinary cost per abundance, with at most one separate Euler exception.
"""
import json,gzip,sys,math
from pathlib import Path
from functools import cache
H=Path(__file__).resolve().parent;R=H.parent
sys.path[:0]=[str(R/'Session20261122/Python'),str(R/'RootFiveNext')]
from RoadblockDual import SCALE as S, log_bounds as lg, odd_primes
from TerminalCertificate import DYADIC as W, allowed,sigma
from PrimeCheck import prime64,level
BAD=(3,7,11,13,19,31); B=10**2400
@cache
def data():return json.loads(gzip.decompress((H/'Seeds.json.gz').read_bytes()))
@cache
def prime(p):
 if type(p) is not int or p<2:raise ValueError('invalid prime label')
 n=p
 if n>=2**64:
  rows=data()['ecpp'][str(p)]
  if not isinstance(rows,list) or not rows:raise ValueError('missing ECPP chain')
  for row in rows:
   if len(row)!=5 or not all(type(v) is int for v in (*row[:4],*row[4])) or n!=row[0]:raise ValueError('chain binding')
   n=level(*row)
 if not prime64(n):raise ValueError(('nonprime',p))
 return True
@cache
def tree(arr):
 if len(arr)==1:return arr[0],None,None
 a=tree(arr[:len(arr)//2]);b=tree(arr[len(arr)//2:]);return a[0]*b[0],a,b

def divisors(n,t):
 g=math.gcd(n,t[0]);
 if g==1:return
 if t[1] is None:yield t[0];return
 yield from divisors(g,t[1]);yield from divisors(g,t[2])

def model(e,x=(),L=1001,cut=14,cap=12,tailmin=(),promote=False,root_free=False):
 row=data()['rows'][str(e)];base=set(odd_primes(L-1))-set(BAD);forest=set(row['roots'])|set(dict(row['owners']));base|=forest;fixed=dict(((5,e),*x));lower=dict(tailmin);base.update(fixed);base.update(lower)
 if root_free:
  if x or tailmin:raise ValueError('this pilot only supports unrestricted root')
  fixed={};lower={5:1}
 if (not root_free and len(fixed)!=1+len(x)) or sum(f%2 for f in fixed.values())>1:raise ValueError('bad fixed state')
 prom={}
 if promote:
  from TerminalBank import specs
  prom=specs();base.update(prom)
 for p in base:
  if p in BAD or p==2 or (p not in prom and not prime(p)):raise ValueError('base')
 tree0=tree(tuple(sorted(base)));options={};cost=[];ab=[];eu=[];incoming={};surplus={};order=[];fixedEuler=any(f%2 for f in fixed.values())
 def add(p,f,exact):
  i=len(cost);options.setdefault(p,[]).append((i,f,exact));c=f*lg(p)[0];v=lg(p,p-1)[1];od=f%2
  if od:eu.append(i)
  if exact:
   z=sigma(p,f);v=lg(z,p**f)[1];u=z//(2 if od else 1)
   for q in divisors(u,tree0):
    t=0
    while u%q==0:t+=1;u//=q
    incoming.setdefault(q,[]).append((i,t))
   c+=lg(u)[0]
   # Count possible distinct primes via integer power, not floating log.
   h=0;t=u
   while t>=L:h+=1;t//=L
   v+=h*lg(L,L-1)[1]
  cost.append(c);ab.append(v)
 for p in sorted(base):
  if p in fixed:
   f=fixed[p]
   if not allowed(p,f,BAD) or (f%2 and (f%4!=1 or p%4!=1)):raise ValueError('inadmissible fixed input')
   add(p,f,True);continue
  for a,d in ((2,2),(1,4)):
   if a==1 and (fixedEuler or p%4!=1 or not allowed(p,1,BAD)):continue
   h=max(a,lower.get(p,0)); f=h+(a-h)%d
   stop=(max(cap,cut,prom.get(p,0)) if p in forest else max(cut,prom.get(p,0)) if p<L else prom.get(p,cut))
   while f<=stop:
    if allowed(p,f,BAD):add(p,f,True)
    f+=d
   while not allowed(p,f,BAD):f+=d
   add(p,f,False)
 for q in sorted(incoming):
  if q not in fixed:
   surplus[q]=len(cost);cost.append(lg(q)[0]);ab.append(0)
 tail=len(cost);cost.append(2*lg(L)[0]*S//lg(L,L-1)[1]);ab.append(S)
 if not fixedEuler:eu.append(len(cost));cost.append(lg(L)[0]);ab.append(lg(L,L-1)[1])
 rows=[(list(enumerate(-v for v in ab)),-lg(2)[0]), ([(i,S) for i in eu],S)]
 for p,G in options.items():
  terms=[(i,S) for i,_,_ in G];rows.append((terms,S));
  if p in fixed or p in lower:rows.append(([(i,-v) for i,v in terms],-S))
 source={i:p for p,g in options.items() for i,_,_ in g}
 for q,ls in sorted(incoming.items()):
  group=options[q];fixed_quota=sum(v for i,v in ls if source[i] in fixed)
  if fixed_quota and q not in fixed:
   rows.append(([(j,-S) for j,f,ex in group if not ex or f>=fixed_quota],-S))
  a=[(i,v*S) for i,v in ls]+[(i,-f*S) for i,f,_ in group]
  if q in surplus:a.append((surplus[q],-S))
  rows.append((a,0))
  by={}
  for i,v in ls:by.setdefault(source[i],[]).append((i,v))
  for _,cells in sorted(by.items()):
   for threshold in sorted(set(v for _,v in cells)):
    rows.append(([(i,S) for i,v in cells if v>=threshold]+[(j,-S) for j,f,ex in group if not ex or f>=threshold+(fixed_quota if source[cells[0][0]] not in fixed else 0)],0))
 return cost,rows,options,[tail,*surplus.values()]

def weighted(m,w):
 C,rows,groups,free=m;r=[v*W for v in C];tot=0;prev=-1
 for i,k in w:
  if not (type(k)==int and k>0 and prev<i<len(rows)):raise ValueError('invalid weights')
  prev=i;a,b=rows[i];tot-=b*k
  for j,v in a:r[j]+=k*v
 if any(r[j]<0 for j in free):raise ValueError('negative free price')
 used={j for g in groups.values() for j,_,_ in g}|set(free)
 return tot+sum(min(0,*(r[j] for j,_,_ in g)) for g in groups.values())+sum(min(0,v) for j,v in enumerate(r) if j not in used)

def solve(m):
 from scipy.sparse import coo_matrix
 from scipy.optimize import linprog
 C,rows,groups,free=m;rr=[];cc=[];vv=[];rhs=[]
 for i,(a,b) in enumerate(rows):
  rhs.append(b/S)
  for j,v in a:rr.append(i);cc.append(j);vv.append(v/S)
 fr=set(free);z=linprog([c/S for c in C],A_ub=coo_matrix((vv,(rr,cc)),shape=(len(rows),len(C))).tocsr(),b_ub=rhs,bounds=[(0,None if j in fr else 1) for j in range(len(C))],method='highs');
 if not z.success:raise RuntimeError(z.message)
 solve.primal=z.x
 # Floor all positive dual weights; unbounded columns have just one negative incidence.
 w=[[i,math.floor(-u*W)] for i,u in enumerate(z.ineqlin.marginals) if -u*W>=1]
 # Correct numerical noise on an unbounded column's one negative row.
 price=dict(w)
 rc={j:C[j]*W for j in free};negative={}
 for i,v in w:
  for j,k in rows[i][0]:
   if j in rc:
    rc[j]+=v*k
    if k<0:negative[j]=(i,-k)
 for j,d in rc.items():
  if d<0:
   i,k=negative[j];price[i]-=(-d+k-1)//k
 w=[[i,v] for i,v in sorted(price.items()) if v>0];b=weighted(m,w);return b//(W*lg(10)[1]),w
if __name__=='__main__':
 import argparse,time
 parser=argparse.ArgumentParser();parser.add_argument('es',type=int,nargs='+');parser.add_argument('--limit',type=int,default=1001);parser.add_argument('--cut',type=int,default=14);parser.add_argument('--cap',type=int,default=12);parser.add_argument('--exact',type=int,nargs=2,action='append',default=[]);parser.add_argument('--lower',type=int,nargs=2,action='append',default=[]);parser.add_argument('--out');args=parser.parse_args();
 for e in args.es:
  t=time.monotonic();m=model(e,args.exact,args.limit,args.cut,args.cap,args.lower);b,w=solve(m);print(e,args.exact,args.lower,b,len(m[0]),len(m[1]),round(time.monotonic()-t,1),flush=True)
  if args.out and b>=2400:(H/args.out).write_bytes(gzip.compress(json.dumps(dict(e=e,x=args.exact,lower=args.lower,L=args.limit,cut=args.cut,cap=args.cap,w=w),separators=(',',':')).encode(),mtime=0))
