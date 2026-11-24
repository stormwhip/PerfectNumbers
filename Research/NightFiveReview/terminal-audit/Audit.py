"""Independent FourAvoid model/reduced cost, no project imports. Narrow to requested target.
Rebuild rows by weight indexing and accumulate their effect on each column, while
independently certifying the needed prime factors (Pocklington, archive data only).
Independent conservatively rounded integer log interval, standard lib Decimal.ln.
"""
from pathlib import Path
import json, math, hashlib, gzip
from collections import Counter, defaultdict
from decimal import Decimal as D, localcontext, ROUND_FLOOR, ROUND_CEILING
from functools import cache
R=Path(__file__).resolve().parents[2]; P=R/'NightUniform/FourAvoid.json'; S=2**80; W=2**24
expected='e141e86e04c662397c93b0f4cac7f0f3ef3b92daf12255619712339889081d2f'
def check(x,msg):
 if not x:raise ValueError(msg)
@cache
def logs(n):
 with localcontext() as ctx:
  ctx.prec=90;z=D(n).ln();return int((z.next_minus()*S).to_integral_value(rounding=ROUND_FLOOR)),int((z.next_plus()*S).to_integral_value(rounding=ROUND_CEILING))
def lower(n):return logs(n)[0]
def upper(n,d):return logs(n)[1]-logs(d)[0]
def sieve(n):
 a=bytearray(b'\1')*(n+1);a[:2]=b'\0\0'
 for p in range(2,math.isqrt(n)+1):
  if a[p]:a[p*p::p]=bytes(len(a[p*p::p]))
 return {i for i in range(3,n+1,2) if a[i]}
@cache
def pp(L):return math.prod(sieve(L-1))
@cache
def sigma(p,e):return (p**(e+1)-1)//(p-1)
def mr(n):
 if n<2 or n>=2**64:return False
 if n%2==0:return n==2
 d=n-1;s=0
 while d%2==0:d//=2;s+=1
 for a in (2,325,9375,28178,450775,9780504,1795265022):
  if a%n==0:continue
  t=pow(a,d,n)
  if t==1 or any(pow(t,2**j,n)==n-1 for j in range(s)):continue
  return False
 return True
if __name__=='__main__':
 check(hashlib.sha256(P.read_bytes()).hexdigest()==expected,'unexpected publication');packet=json.loads(P.read_bytes());d,=packet['cases'];bad=tuple(d['forbidden']);check(bad==(3,5,7,11),'wrong class');prod_bad=math.prod(bad);proof=dict(packet['proof']);arch=[]
 for v in ('Original','Replacement'):
  g=(R/f'Session20261122/Certificates/Terminal{v}.json.gz').read_bytes();check(hashlib.sha256(g).hexdigest()==packet['archive_sha256'][v],'archive');ar=json.loads(gzip.decompress(g));arch.extend(ar['edges']);proof.update(ar['proofs'])
 @cache
 def prime(n):
  if n<2**64:return mr(n)
  if str(n) not in proof:return False
  F=1;seen=set()
  for q,k,a in proof[str(n)]:
   if not (1<q<n and prime(q) and q not in seen and 1<=k<=n.bit_length() and 1<a<n and (n-1)%q**k==0 and pow(a,n-1,n)==1 and math.gcd(n,pow(a,(n-1)//q,n)-1)==1):return False
   seen.add(q);F*=q**k
  return F**2>n
 small=sieve(5000)-set(bad);cuts={p:d['cut'] for p in small};extra=dict(d['promoted']);check(len(extra)==len(d['promoted']) and all(p>5000 and 0<v<=100 and prime(p) for p,v in extra.items()),'promotion');cuts.update(extra);edges={}
 def legal(p,e):return math.gcd(sigma(p,e),prod_bad)==1
 for p,e,q,k in arch:
  if p in small and e<=cuts[p] and q not in bad and legal(p,e):edges[p,e,q]=max(k,edges.get((p,e,q),0))
 for p,e,q,k in d['new']:
  check(p in cuts and 1<=e<=cuts[p] and legal(p,e),'edge source');edges[p,e,q]=max(k,edges.get((p,e,q),0))
 bsets=sorted(set(cuts)|{q for p,e,q in edges});gam={};hs={};slots={};j=-1;covered=math.prod(set(bsets)|set(bad));bl={}
 for p,e,n,L in d['blocks']:
  check(n>1 and n%2 and L>=5001 and L%2 and sigma(p,e)%n==0 and math.gcd(covered,n)==1 and math.gcd(pp(L),n)==1 and (p,e) not in bl,'unverified block');covered*=n
  k=0
  while L**(k+1)<=n:k+=1
  bl[p,e]=lower(n),sum(upper(L+2*i,L+2*i-1) for i in range(k))
 cols={}; target=defaultdict(list)
 for p in bsets:
  opts=[]
  for sp in (False,True):
   if sp and (p%4!=1 or math.gcd(p+1,prod_bad)>1):continue
   f=1 if sp else 2;step=4 if sp else 2
   while True:
    if legal(p,f):
     j+=1;ex=f<=cuts.get(p,0);b0,b1=bl.get((p,f),(0,0)) if ex else (0,0)
     gam[j]=f*lower(p)+b0;hs[j]=(upper(sigma(p,f),p**f) if ex else upper(p,p-1))+b1;opts.append((j,f,sp,ex))
     if ex:slots[p,f]=j
     else:break
    f+=step
  cols[p]=opts
 check(set(bl)<=slots.keys(),'inactive block attached to nonexact option');t=j+1;l=lower(5001);h=upper(5001,5000);gam[t]=2*l*S//h;gam[t+1]=l;hs[t]=S;hs[t+1]=h
 weights=dict(d['weights']);check(len(weights)==len(d['weights']) and all(type(k)==type(w)==int and w>=0 for k,w in weights.items()),'weight');mul=lambda i:weights.get(i,0);rd={k:g*W-hs[k]*mul(0) for k,g in gam.items()};rd[t+1]+=S*mul(1);con=lower(2)*mul(0)-S*mul(1)
 for idx,p in enumerate(bsets,2):
  con-=S*mul(idx)
  for j,f,sp,ex in cols[p]:rd[j]+=S*(mul(idx)+sp*mul(1))
 for idx,((p,e,q),k) in enumerate(sorted(edges.items()),2+len(bsets)):
  check(prime(q) and q not in bad and q!=p and k>0 and sigma(p,e)%q**k==0,'unverified factor');w=mul(idx)*S
  if w:
   rd[slots[p,e]]+=w
   for j,f,sp,ex in cols[q]:
    if not (e%2 and sp) and (not ex or f>=k):rd[j]-=w
 check(min(weights)>=0 and max(weights)<2+len(bsets)+len(edges) and rd[t]>=0,'unbounded objective or nonexistent row')
 value=con+min(0,rd[t+1])+sum(min([0]+[rd[j] for j,f,sp,ex in g]) for g in cols.values());den=W*logs(10)[1];check(value>2411*den,'below target');print(json.dumps(dict(packet=expected,forbidden=bad,variables=t+2,groups=len(bsets),expanded=len(extra),blocks=len(bl),rows=len(bsets)+2+len(edges),edges=len(edges),nonzero=len(weights),recomputed_numerator=value,recomputed_denominator=den,micro_floor=value*1000000//den,reported_numerator=d['lb'],independent_logs=True)))
