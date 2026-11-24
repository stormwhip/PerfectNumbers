"""Independent arithmetic for each factor-tree branch, including unit/deletion duals."""
import json,sys
from functools import lru_cache
from math import gcd,prod,isqrt
from pathlib import Path
from PrimeCheck import proved,check
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parent/'IndicatorCapacity'));import VerifyIndicatorCapacity2400 as I
F={3,7,11,13,19,31};B=10**2400; Q=I.SCALE; ln5=I.log_interval(5)[0]

@lru_cache(None)
def block(p,n):
 if n%2 and (p%4!=1 or n%4!=1):return False
 # Direct geometric sums reduced modulo the tiny banned primes, periodic in n.
 for z in F:
  if p%z==1:
   if (n+1)%z==0:return False
  elif pow(p,n+1,z)==1:return False
 return True

def sigma(p,e):return (p**(e+1)-1)//(p-1)

@lru_cache(None)
def valuation(p,e):
 if p==5:return 0
 j=0;t=e+1
 if p%5==1 or (p%5==4 and e%2):
  while t%5==0:t//=5;j+=1
  if p%5==4:
   u=p+1
   while u%5==0:j+=1;u//=5
 return j

@lru_cache(None)
def lower_opt(p,c,odd,rate):
 if odd and (p%4!=1 or gcd(p+1,math.prod(F))>1):return None
 q=p.bit_length(); shift=max(0,q-48);lg=I.log_interval(p>>shift)[0]+shift*I.LN2_LO
 # Reserve all exponents f>=400 as an interval, including the case c>400.
 j=I.ilog(I.MAX_EXPONENT+1,5)+(valuation(p,1) if odd else 0)
 best=(max(c,400)-c)*lg-rate*j
 for f in range(max(c,1),400):
  if bool(f%2)==odd and block(p,f):best=min(best,(f-c)*lg-rate*valuation(p,f))
 return best

import math
@lru_cache(None)
def lower_pow(p,c,odd):
 if odd and (p%4!=1 or gcd(p+1,math.prod(F))>1):return None
 for f in range(max(c,1),max(c,1)+3000):
  if bool(f%2)==odd and block(p,f):return f
 raise ValueError('no choice found')

def ln_low(n):
 t=max(0,n.bit_length()-48);return I.log_interval(n>>t)[0]+t*I.LN2_LO

def max_ab(p):return (Q+p-2)//(p-1) if p>1000 else I.log_interval(p,p-1)[1]

class Replay:
 def __init__(self,e,known,ps,duals,maxdepth=9):self.e=e;self.known=known;self.ps=ps;self.duals=duals;self.maxdepth=maxdepth;self.nodes=0
 def visit(self,state):
  self.nodes+=1
  if self.nodes>10000:return False
  X=prod(p**f for p,f in state.items());sig=prod(sigma(p,f) for p,f in state.items());eu=any(f%2 for f in state.values()); D=sig//gcd(sig,2*X)
  if gcd(X*prod(F),D)!=1:return True
  u=D; ds={}
  extras=set()
  for (r,f) in state.items():extras.update(getattr(self,'chains',{}).get((r,f),()))
  for p in self.known+sorted(extras)+[q for q in self.ps if q<=2000]:
   if not u%p:
    c=0
    while u%p==0:u//=p;c+=1
    ds[p]=c
  options={p:[lower_pow(p,c,False),None if eu else lower_pow(p,c,True)] for p,c in ds.items()}
  def minprod(omit=None):
   opts=[(p,v) for p,v in options.items() if p!=omit];full=prod(p**v[0] for p,v in opts);sav=max([1]+[p**max(0,v[0]-v[1]) for p,v in opts if v[1] is not None]);return full//sav
  V=X*u*minprod()
  if V>B:return True
  # Bounding all unknown abundancies with integer products. Even if Euler already assigned,
  # allowing the unknown tail one special prime instead only weakens the checks.
  k=I.ilog(u,2001);abn=sig*2001**k*prod(ds);abd=X*2000**k*prod(p-1 for p in ds);tail=1
  for r in self.ps:
   if r in state or r in ds:continue
   tail*=r
   if V*tail**2>(1 if eu else r)*B:break
   abn*=r;abd*=r-1
  else:raise ValueError('prime tail too short')
  if abn<2*abd:return True
  if self.duals:
   k=self.e-sum(valuation(p,f) for p,f in state.items()); check(k>=0,'valuation deficit should have closed'); deleted=set(state)|set(ds)
   target=I.LN2_LO-sum(max_ab(r) for r in deleted)-I.ilog(u,2001)*max_ab(2001); gift=I.ilog(u,2001**4); base=ln_low(X*D)
   regimes={'assigned'} if eu else {'known','rough','outside'}
   for d in self.duals:
    rate=d.lam_p*ln5 if u==1 else min(d.lam_p*ln5,ln_low(2001)); removed=sum(v for r,v in d.theta_map.items() if (D*X)%r==0); linear=base+d.const_no_target+d.mu*target-removed+rate*(k-gift);nom=sum(lower_opt(p,c,False,rate) for p,c in ds.items());limit=I.LN_B_HI
    if eu:
     if linear+nom>limit:regimes.clear()
    else:
     adjusted=[]
     for p,c in ds.items():
      special=lower_opt(p,c,True,rate)
      if special is not None:adjusted.append(nom-lower_opt(p,c,False,rate)+special)
     if not adjusted or linear+min(adjusted)>limit:regimes.discard('known')
     if u==1 or linear+nom-rate*min(k,I.ilog(u+1,5)+5)>limit:regimes.discard('rough')
     if linear+nom-max(0,(rate-ln5)*k)-ln5-d.delta_q>limit:regimes.discard('outside')
   if not regimes:return True
  if not ds or len(state)>self.maxdepth:return False
  p=max(ds); c=ds[p];z=X*u*minprod(p);f=c
  while z*p**f<=B:
   if (not eu or f%2==0) and block(p,f) and not self.visit(dict(state)|{p:f}):return False
   f+=1
  return True

def main():
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--input',default='DualAudit.json');ap.add_argument('--depth',type=int,default=9);ap.add_argument('--skip-dual',action='store_true');ap.add_argument('--chains',action='store_true');a=ap.parse_args();audit=json.loads((H/a.input).read_text());j=json.loads((H/'Candidates.json').read_text());ps=[p for p in I.sieve_primes(20000) if p not in F|{2,5}];ds=[]
 if not a.skip_dual:
  cert=json.loads((I.CERT_DIR/'DualP5.json').read_text());prime_table=I.sieve_primes(cert['R_act']);ds=[I.verify_dual_entry(5,tuple(cert['forbidden']),cert['R_act'],cert['W_max'],d,prime_table) for d in cert['duals']]
 chains={}
 if a.chains:
  for pair,vs in json.loads((H/'Chains.json').read_text()).items():
   p,f=map(int,pair.split(':'));cs=list(map(int,vs));check(all(proved(v) and sigma(p,f)%v==0 for v in cs),'unproved chain prime or invalid implication');chains[p,f]=cs
 count=0;nodes=0
 for r in audit:
  if not r['closed']:continue
  e=r['e'];factors=[p for p in sorted(set(map(int,j[str(e)]))) if proved(p)];check(all(sigma(5,e)%p==0 for p in factors),'factor does not divide');tr=Replay(e,factors,ps,ds,a.depth);tr.chains=chains;check(tr.visit({5:e}),'independent failure: '+str(e));count+=1;nodes+=tr.nodes
 print('independently reproduced',count,'complete exponents in',nodes,'nodes')
if __name__=='__main__':main()
