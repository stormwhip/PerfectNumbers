"""Independent model reconstruction and sparse-dual pricing (standard library).
No imports from Joint, generators or forest code. Decimal.ln is correctly
rounded; adjacent representables give outward enclosures. Different indices
are intentionally retained to make the sparse row witness portable.
"""
from pathlib import Path
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
from functools import cache
from math import gcd,prod
import json,gzip,sys
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R/'RootFiveNext'))
from PrimeCheck import level,prime64
S=2**80;W=2**24;BAD=[19,7,11,31,13,3];FIVE=5
@cache
def logs(n,d=1):
 if n==d:return 0,0
 with localcontext() as c:
  c.prec=65; a=Decimal(n).ln();b=Decimal(d).ln();l=(a.next_minus()-b.next_plus()).next_minus();u=(a.next_plus()-b.next_minus()).next_plus();return int((l*S).next_minus().to_integral_value(rounding=ROUND_FLOOR)),int((u*S).next_plus().to_integral_value(rounding=ROUND_CEILING))
@cache
def primes(L):return tuple(q for q in range(3,L,2) if all(q%z for z in range(3,int(q**0.5)+1,2)))
@cache
def roughbase(L,T):return tuple(p for p in primes(T) if p>=L)
@cache
def geom(p,f):return (p**(f+1)-1)//(p-1)
@cache
def chunks(v):return tuple((v[k:k+24],prod(v[k:k+24])) for k in range(0,len(v),24))
@cache
def primeproduct(v):return prod(P for _,P in chunks(v))
@cache
def split(n,v):
 u=n;out=[]
 allg=gcd(u,primeproduct(v))
 for ps,P in chunks(v):
  if allg==1:break
  g=gcd(allg,P)
  if g==1:continue
  allg//=g
  for q in ps:
   if g%q:continue
   num=0
   while not u%q:num+=1;u//=q
   out.append((q,num))
 return u,out

def replay(root,e,extra,x,lower,L,cut,cap,weights,wide=False,T=0,conds=(),extend=(),skeleton=False,parity=False):
 from Common import init,chain
 BAD,V,promoted=init(root,e,extra,wide);fixed=dict(([(root,e)] if root else [])+x);minimum=dict(lower)
 for p,c in extend:
  assert p not in BAD and (p in promoted or chain(p)) and type(c)==int and c>=0
  promoted[p]=max(promoted.get(p,0),c)
 assert not(set(fixed)&set(minimum)) and len(fixed)==len(x)+bool(root) and sum(f%2 for f in fixed.values())<=1
 assert all(p not in BAD and chain(p) and type(f)==int and f>=1 for p,f in [*fixed.items(),*minimum.items()]);ps=tuple(sorted((set(primes(L))|V|set(fixed)|set(minimum)|set(promoted))-set(BAD)));G={};C=[];A=[];sp=[];flows={};src={}
 def good(p,f):return all((pow(p,f+1,t*(p-1))-1)%(t*(p-1)) for t in BAD)
 for p in ps:
  if p in fixed:
   f=fixed[p];assert good(p,f) and (f%2==0 or p%4==f%4==1);group=[(f,True)]
  else:
   group=[]
   for h,s in [(2,2),(1,4)]:
    if s==4 and (p%4!=1 or not good(p,1) or any(f%2 for f in fixed.values())):continue
    j=h
    while j<minimum.get(p,0):j+=s
    while True:
     if good(p,j):
      bound=max(cap,cut,promoted.get(p,0)) if p in V else max(cut,promoted.get(p,0)) if p<L else promoted.get(p,cut);ex=j<=bound;group.append((j,ex))
      if not ex:break
     j+=s
  g=G[p]=[]
  for f,ex in group:
   i=len(C);src[i]=p;g.append((i,f,ex));v=logs(p)[0]*f;a=logs(p,p-1)[1];
   if f%2:sp.append(i)
   if ex:
    si=geom(p,f);a=logs(si,p**f)[1];u,div=split(si//(1+f%2),ps)
    for q,k in div:flows.setdefault(q,[]).append((i,k))
    h=0
    while L**(h+1)<=u:h+=1
    if T>L:
      z,fac=split(u,roughbase(L,T));k=0
      while z>=T:z//=T;k+=1
      a+=sum(logs(q,q-1)[1] for q,_ in fac)+k*logs(T,T-1)[1]
    else:a+=h*logs(L,L-1)[1]
    v+=logs(u)[0]
   C.append(v);A.append(a)
 ids={}
 for p in sorted(set(flows)-set(fixed)):ids[p]=len(C);C.append(logs(p)[0]);A.append(0)
 tail=len(C);C.append(2*logs(L)[0]*S//logs(L,L-1)[1]);A.append(S)
 if not any(f%2 for f in fixed.values()):sp.append(len(C));C.append(logs(L)[0]);A.append(logs(L,L-1)[1])
 entries_out=[]
 ww=dict(weights);assert len(ww)==len(weights) and all(type(i)==type(k)==int and i>=0 and k>0 for i,k in weights);reduced=[c*W for c in C];fac=0;k=0
 def row(a,b):
  nonlocal fac,k
  if skeleton:entries_out.append((list(a),b))
  w=ww.get(k);k+=1
  if w:
   fac-=w*b
   for i,v in a:reduced[i]+=w*v
 row(enumerate(-a for a in A),-logs(2)[0]);row([(i,S) for i in sp],S)
 for p,g in G.items():
  row([(i,S) for i,f,ex in g],S)
  if p in fixed or p in minimum:row([(i,-S) for i,f,ex in g],-S)
 for q,entries in sorted(flows.items()):
  mandatory=sum(v for i,v in entries if src[i] in fixed);groups=G[q]
  if mandatory and q not in fixed:row([(i,-S) for i,f,ex in groups if not ex or f>=mandatory],-S)
  row([(j,t*S) for j,t in entries]+[(i,-f*S) for i,f,ex in groups]+([] if q not in ids else [(ids[q],-S)]),0)
  owners={}
  for i,v in entries:owners.setdefault(src[i],[]).append((i,v))
  for p,es in sorted(owners.items()):
   for h in sorted({v for i,v in es}):row([(j,S) for j,v in es if v>=h]+[(i,-S) for i,f,ex in groups if not ex or f>=h+(mandatory if p not in fixed else 0)],0)
 row([(i,logs(geom(p,f),p**f)[0]) for p,g in G.items() for i,f,ex in g],logs(2)[1]);
 if parity:
  for q,es in sorted(flows.items()):
   single=sorted({src[j] for j,k in es if k%2})
   if len(es)>96 or len(single)>12:continue
   for owner in single:
    row([(i,2*((k+int(src[i]==owner))//2)*S) for i,k in es]+[(i,-2*((f+1)//2)*S) for i,f,x in G[q]]+([] if q not in ids else [(ids[q],-S)]),0)
 for p,lo,hi in conds:
  assert p in G and lo>=1 and (hi is None or hi>=lo) and geom(root,e)%p==0
  row([(i,-S) for i,f,ex in G[p] if (not ex or f>=lo) and (hi is None or f<=hi)],-S)
 if skeleton:return C,entries_out,G,{tail,*ids.values()}
 assert max(ww,default=-1)<k and all(reduced[i]>=0 for i in [tail,*ids.values()]);u=fac+sum(min([0]+[reduced[i] for i,f,ex in g]) for g in G.values());
 if sp and sp[-1]>tail:u+=min(0,reduced[sp[-1]])
 return u,reduced,G,ids

def check(path):
 d=json.loads(gzip.decompress(path.read_bytes()));u,*_=replay(**d);assert u>2400*W*logs(10)[1];print(path.name,u//(W*logs(10)[1]),flush=True)
if __name__=='__main__':
 if not __debug__:raise SystemExit('no -O')
 sys.path.insert(0,str(H))
 for f in sys.argv[1:]:check(H/f)
