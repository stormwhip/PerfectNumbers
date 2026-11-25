"""Independent model reconstruction and sparse-dual pricing (standard library).
No imports from Joint, generators or forest code. Decimal.ln is correctly
rounded; adjacent representables give outward enclosures. Different indices
are intentionally retained to make the sparse row witness portable.
"""
from pathlib import Path
from decimal import Decimal,localcontext,ROUND_FLOOR,ROUND_CEILING
from functools import cache
from math import gcd,prod,isqrt
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
def nominated():return json.loads(gzip.decompress((H/'Seeds.json.gz').read_bytes()))
@cache
def widebank():
 arc=json.loads((R/'NightUniform/ThreeAvoid.json').read_bytes());z=arc['cases'][0];edges=list(z['new']);pf=dict(arc['proof']);caps=dict(z['promoted'])
 for a in ('Replacement','Original'):
  pack=json.loads(gzip.decompress((R/f'Session20261122/Certificates/Terminal{a}.json.gz').read_bytes()));edges+=pack['edges'];pf.update(pack['proofs'])
 @cache
 def pk(n):
  if type(n) is not int or n<2:return False
  if n<2**64:return prime64(n)
  t=1;used=set();links=pf.get(str(n),[])
  if not isinstance(links,list) or not links:return False
  for q,k,a in links:
   if q in used or not (type(q)==type(k)==type(a)==int and 1<q<n and 0<k<=n.bit_length() and pk(q) and 1<a<n):return False
   used.add(q);t*=q**k
   if pow(a,n-1,n)!=1 or gcd(pow(a,(n-1)//q,n)-1,n)>1:return False
  return (n-1)%t==0 and t*t>n
 return {p:(max(32,min(128,caps.get(p,0))) if p<5001 else min(82,caps.get(p,0))) for p in set(caps)|{q for p,f,q,a in edges} if p not in {5,*BAD} and pk(p)}
@cache
def trusted(p):
 if type(p) is not int or p<2:raise ValueError('bad ECPP input')
 n=p
 if n>=2**64:
  links=nominated()['ecpp'][str(n)]
  if not isinstance(links,list) or not links:raise ValueError('missing ECPP chain')
  for row in links:
   if len(row)!=5 or not all(type(t) is int for t in (*row[:4],*row[4])) or row[0]!=n:raise ValueError('ECPP link')
   n=level(*row)
 if not (p>2 and prime64(n)):raise ValueError('primality')
 return True
@cache
def primes(L):return tuple(q for q in range(3,L,2) if all(q%z for z in range(3,isqrt(q)+1,2)))
@cache
def good(p,f):return all((pow(p,f+1,t*(p-1))-1)%(t*(p-1)) for t in BAD)
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

def replay(e,x,lower,L,cut,cap,weights,wide=False):
 promoted=widebank() if wide else {}
 if wide and (fp:=H/f'Extra{e}.json.gz').is_file():
  extra=json.loads(gzip.decompress(fp.read_bytes()));nominated()['ecpp'].update(extra)
 else:extra={}
 forest=nominated()['rows'][str(e)];V=set(forest['roots'])|set(dict(forest['owners']))|set(map(int,extra));fixed=dict([(5,e)]+x);minimum=dict(lower);ps=tuple(sorted((set(primes(L))|V|set(fixed)|set(minimum)|set(promoted))-set(BAD)));assert len(fixed)==len(x)+1 and sum(f%2 for f in fixed.values())<=1 and all(p in promoted or trusted(p) for p in ps);G={};C=[];A=[];sp=[];flows={};src={}
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
    a+=h*logs(L,L-1)[1];v+=logs(u)[0]
   C.append(v);A.append(a)
 ids={}
 for p in sorted(set(flows)-set(fixed)):ids[p]=len(C);C.append(logs(p)[0]);A.append(0)
 tail=len(C);C.append(2*logs(L)[0]*S//logs(L,L-1)[1]);A.append(S)
 if not any(f%2 for f in fixed.values()):sp.append(len(C));C.append(logs(L)[0]);A.append(logs(L,L-1)[1])
 ww=dict(weights);assert len(ww)==len(weights) and all(type(i)==type(k)==int and i>=0 and k>0 for i,k in weights);reduced=[c*W for c in C];fac=0;k=0
 def row(a,b):
  nonlocal fac,k
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
 assert max(ww,default=-1)<k and all(reduced[i]>=0 for i in [tail,*ids.values()]);u=fac+sum(min([0]+[reduced[i] for i,f,ex in g]) for g in G.values());
 if sp and sp[-1]>tail:u+=min(0,reduced[sp[-1]])
 return u,reduced,G,ids

def check(path):
 d=json.loads(gzip.decompress(path.read_bytes()));e=d['e'];q=d['anchor'];assert trusted(q) and geom(5,e)%q==0;claimed=[]
 for leaf in d['leaves']:
  x=leaf['x'];lo=leaf['lower'];assert (len(x),len(lo)) in ((1,0),(0,1)) and (x or lo)[0][0]==q;f=(x or lo)[0][1];assert (lo and f==d['limit']) or (x and 0<f<d['limit']);b,*_=replay(e,x,lo,d['L'],d['cut'],d['cap'],leaf['w']);assert b>2400*W*logs(10)[1],(e,f,b//(W*logs(10)[1]));claimed.append((f,'tail' if lo else 'exact',b//(W*logs(10)[1])))
 print('independent conditional',e,claimed,flush=True)
if __name__=='__main__':
 if not __debug__:raise SystemExit('run without -O')
 for p in sys.argv[1:]:check(H/p)
