"""Independent integer model for complete Any trees and one conditioned Multi tree.
No proof/dual/tree modules imported. Assumes primality of the package's named
primes (checked separately by the frozen verifier); validates divisibility here.
Python Decimal.ln is correctly rounded; expand by one 48-digit ulp on each side.
"""
import json, math, sys
from decimal import Decimal as Z, localcontext, ROUND_FLOOR, ROUND_CEILING
from functools import cache
from collections import Counter
from pathlib import Path
R=Path(__file__).resolve().parent.parent; NF=R/'NightFive'; SCALE=10**12; B=10**2400; F=(3,7,11,13,19,31); T=100000
@cache
def logs(n):
 with localcontext() as ctx:
  ctx.prec=48; a=Z(n).ln();return int((a.next_minus()*SCALE).to_integral_value(rounding=ROUND_FLOOR)),int((a.next_plus()*SCALE).to_integral_value(rounding=ROUND_CEILING))
def lo(n):return logs(n)[0]
def hi(n):return logs(n)[1]
def iroot(n,p):
 l=0;h=n.bit_length()+1
 while h-l>1:
  m=(h+l)//2
  if p**m<=n:l=m
  else:h=m
 return l
def primes(t):
 a=bytearray(b'\1')*(t+1);a[:2]=b'\0\0'
 for j in range(2,math.isqrt(t)+1):
  if a[j]:a[j*j::j]=bytes(len(a[j*j::j]))
 return tuple(i for i in range(t+1) if a[i])
PS=primes(T);M=iroot(B,3);J=iroot(M+1,5);LIMIT=hi(B);bad=math.prod(F)
def sig(p,f):return (p**(f+1)-1)//(p-1)
@cache
def ab(p):return hi(p)-lo(p-1) if p<2000 else (SCALE+p-2)//(p-1)
@cache
def good(p,f):return all(pow(p,f+1,(p-1)*z)!=1 for z in F) if p<5000 else all(((f+1)%z!=0 if p%z==1 else pow(p,f+1,z)!=1) for z in F)
def vp(x):
 n=0
 while x%5==0:x//=5;n+=1
 return n
def units(p,f):
 if p%5==1:return vp(f+1)
 if p%5==4 and f%2:return vp(p+1)+vp(f+1)
 return 0
@cache
def opt(p,c,odd,L):
 if odd and (p%4!=1 or math.gcd(p+1,bad)>1):return None
 # Finite exhaustive prefix plus rigorous price-minus-max-discount tail.
 start=max(1,c);end=start+40;logp=lo(p);j=J+(vp(p+1) if odd and p%5==4 else 0)
 ans=(end-c)*logp-L*j
 for f in range(start,end):
  if (f%4==1 if odd else f%2==0) and good(p,f):ans=min(ans,(f-c)*logp-L*units(p,f))
 return ans
class Bank:
 def __init__(self,a,cut,ps):
  self.mu=mu=a['mu_num'];self.lam=lam=a['lam_p_num'];assert a['mu_den']==a['lam_p_den']==1 and mu>=0 and lam>=0
  th=Counter();edge=Counter();last=Counter()
  for p,f,r,v in a['flows']:
   assert p!=r and pow(p,f+1,r*(p-1))==1 and v>0 and p not in F+(5,) and r not in F+(5,) and 2<r<10**18 and f%2==0 and good(p,f)
   edge[p,f]+=v*10**6;th[r]+=v*10**6;last[p]=max(last[p],f)
  self.th=th;self.credit={};self.C=0;self.dq=self.de=mu*ab(cut);assert 2*lo(cut)>=mu*ab(cut) and 4*lo(cut)>=lam*hi(5)+mu*ab(cut)
  for p in set(ps)|set(th)|set(last):
   if p in F+(2,5):continue
   l=lo(p);t=th[p];h=ab(p);f=2
   while not good(p,f):f+=2
   stop=max(f,last[p]+2,42 if p<=300 else 0,64 if p<=80 else 0, min(40,2*((t+mu*h)//(2*l)+2)) if t else 0)
   tail=stop*l-t-mu*h
   if p%5==1:tail=min(tail,*[max(stop,5**j-1)*l-t-mu*h-j*lam*hi(5) for j in range(1,J+1)])
   m=min(0,tail)
   for k in range(f,stop,2):
    if good(p,k):
     h0=min(h,hi(sig(p,k))-k*lo(p)) if p<=500 else h
     m=min(m,k*l+edge[p,k]-t-mu*h0-lam*hi(5)*units(p,k))
   self.C+=m
   if m:self.credit[p]=-m
   self.de=max(self.de,t+mu*h+m)
   if p%4==1:self.dq=max(self.dq,t+mu*h+m)

def parts(n,known):
 m={};u=n
 for p in set(known)|set(PS):
  if u%p==0:
   v=0
   while not u%p:u//=p;v+=1
   m[p]=v
 return m,u
class Model:
 def __init__(self,e,a,ds):self.e=e;self.a=a;self.ds=ds;self.stats=Counter();self.eg={};self.P=5**(e+1);self.A=(self.P-1)//4
 def state(self,x):
  X=math.prod(p**f for p,f in x);ws=[sig(p,f) for p,f in x];S=math.prod(ws);D=S//math.gcd(S,2*X);V=self.e-vp(S);self.stats['nodes']+=1
  if X*D>B or math.gcd(X*bad*2,D)>1 or V<0:
   self.stats['arithmetic']+=1;return None
  ks=set(map(int,self.a['roots'][str(self.e)])); assert all(self.A%r==0 for r in ks)
  for (p,f),w in zip(x,ws):
   zs=list(map(int,self.a['secondary'].get(f'{p}:{f}',[])));assert all(w%z==0 for z in zs); ks.update(zs)
  m,u=parts(D,ks);gone=set(m)|{p for p,_ in x};n=iroot(u,T);target=lo(2)-sum(map(ab,gone))-n*ab(T);rows=[]
  for d in self.ds:
   L=min(d.lam*lo(5),4*lo(T)) if u>1 else d.lam*lo(5);pr={p:opt(p,c,False,L) for p,c in m.items()};base=lo(X*D)+d.mu*target+d.C+sum(d.credit.get(p,0) for p in gone)-sum(t for p,t in d.th.items() if (X*D)%p==0)+sum(pr.values())-(n*L+3)//4+V*L
   rows.append((d,L,pr,base))
  return X,D,V,ws,m,u,rows
 def any(self,x):
  a=self.state(x)
  if a is None:return True
  X,D,V,ws,m,u,rows=a; eu=any(f%2 for p,f in x)
  if eu:close=any(b>LIMIT for d,L,pr,b in rows)
  else:
   known=all(all(opt(p,c,True,L) is None for d,L,pr,b in rows) or any((z:=opt(p,c,True,L)) is not None and b-pr[p]+z>LIMIT for d,L,pr,b in rows) for p,c in m.items());rough=(u==1 or any(b-L*min(V,iroot(u+1,5)+J)>LIMIT for d,L,pr,b in rows));outside=all(any(b-L*s+max(0,s-1)*lo(5)-d.dq>LIMIT for d,L,pr,b in rows) for s in range(V+1));close=known and rough and outside
  if close:
   k='any-assigned' if eu else 'any-3-way';self.stats[k]+=1;self.eg.setdefault(k,[(str(p),f) for p,f in x]);return True
  if not m:self.stats['open']+=1;return False
  p=max(m);c=m[p];rem=B//(X*(D//p**c));return all(self.any(x+[(p,f)]) for f in range(c,iroot(rem,p)+1) if (f%2==0 or (not eu and p%4==f%4==1)) and good(p,f))
if __name__=='__main__':
 from time import monotonic
 start=monotonic(); cert=json.loads((R/'IndicatorCapacity/Certificates/DualP5.json').read_text());ps=primes(cert['R_act']); es=list(map(int,sys.argv[1:])) or [196,178]; pack=json.loads((NF/'Batch13.json').read_text());bank=[Bank(v,cert['R_act'],ps) for v in cert['duals']+pack['duals']]; print('bank seconds',round(monotonic()-start,2),flush=True)
 for e in es:
  m=Model(e,pack,bank);ok=m.any([(5,e)]);print(json.dumps(dict(e=e,passed=ok,stats=m.stats,examples=m.eg)),flush=True);assert ok
