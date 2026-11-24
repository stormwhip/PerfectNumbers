"""Exact truncated factor tree; a depth or node limit is OPEN, never a proof."""
import argparse,json,math,sys
from bisect import bisect_right
from collections import Counter
from functools import cache
from PrimeCheck import H,proved,check
F=(3,7,11,13,19,31); B=10**2400; T=2000

def sieve(n):
 a=bytearray(b'\1')*(1+n);a[:2]=b'\0\0'
 for p in range(2,math.isqrt(n)+1):
  if a[p]:a[p*p::p]=bytes(1+(n-p*p)//p)
 return [i for i,x in enumerate(a) if x]
PR=[p for p in sieve(16000) if p>2 and p not in F and p!=5]; SMALL=[r for r in PR if r<=T]
@cache
def ok(r,f):return all((f+1)%z if r%z==1 else pow(r,f+1,z)!=1 for z in F)
@cache
def minf(r,c,odd):
 if odd and (r%4!=1 or math.gcd(r+1,math.prod(F))!=1):return None
 f=max(c,1);f+=((1-f)%4 if odd else -f%2)
 for a in range(f,f+3000,4 if odd else 2):
  if ok(r,a):return a
 raise RuntimeError('unresolved exponent minimum')

def cost(cand,eused):
 M=1;save=1; mins={}
 for r,c in cand.items():
  f=minf(r,c,False); fo=None if eused else minf(r,c,True);M*=r**f;mins[r]=(f,fo)
  if fo is not None and fo<f:save=max(save,r**(f-fo))
 return M//save,mins

@cache
def tail_table(exclude,eused):
 # smallest distinct primes dominate the maximum abundancy, and minimize cost
 # for a fixed cardinality, even if the one Euler exception is on the largest.
 bad=set(exclude);t=1; num=den=1;cs=[1]; vals=[(1,1)]
 for r in PR:
  if r in bad:continue
  t*=r;w=t*t if eused else t*t//r
  if w>B:break
  num*=r;den*=r-1;cs.append(w);vals.append((num,den))
 else:raise ValueError('insufficient tail primes')
 return cs,vals

class Tree:
 def __init__(self,e,known,depth,nodes):
  self.e=e;self.A=(5**(e+1)-1)//4;self.known=known;self.depth=depth;self.maxnodes=nodes;self.st=Counter();self.examples=[]
 def visit(self,exact,prod,ss,eu,lev):
  if hasattr(self,'observed'):self.observed.update(exact.items())
  self.st['nodes']+=1
  if self.st['nodes']>self.maxnodes:self.st['budget']+=1;return False
  # Every assigned sigma is jointly multiplicative, not a product of overlapping claims.
  div=ss//math.gcd(ss,2*prod)
  if math.gcd(div,prod)>1 or math.gcd(div,math.prod(F))>1:self.st['div']+=1;return True
  rough=div; ds={}
  extra=set()
  if hasattr(self,'chains'):
   for p,f in exact.items():extra.update(self.chains.get((p,f),()))
  for r in self.known+SMALL+sorted(extra):
   if rough%r:continue
   c=0
   while rough%r==0:c+=1;rough//=r
   ds[r]=c
  M,mins=cost(ds,eu);paid=prod*M*rough
  if paid>B:self.st['size']+=1;return True
  # Forced primes' full limiting abundance, plus a rough unknown block.
  an=ss;ad=prod
  for r in ds:an*=r;ad*=r-1
  k=0;w=rough
  while w>T:w//=T+1;k+=1
  an*=(T+1)**k;ad*=T**k
  # Excluding costly large/forced nodes is optional. Use first 15 smalls in table cache.
  excl=tuple(r for r in PR[:15] if r in ds or r in exact);cs,vs=tail_table(excl,eu);u,v=vs[bisect_right(cs,B//paid)-1]
  if an*u<2*ad*v:self.st['abundance']+=1;return True
  if hasattr(self,'extra') and self.extra(exact,prod,ss,eu,div,rough,ds):self.st['dual']+=1;return True
  def choices(r):
   f,fo=mins[r];local=cost({k:v for k,v in ds.items() if k!=r},eu)[0]; budget=B//(prod*rough*local);fs=[]
   x=r**min(f,fo if fo is not None else f);n=min(f,fo if fo is not None else f)
   while x<=budget:
    if ((n%2==0 and n>=f) or (fo is not None and n%4==1 and n>=fo)) and ok(r,n):fs.append(n)
    n+=1;x*=r
   return fs
  # Fail-fast: any one mandatory split with every admissible child proved suffices.
  if not ds or lev>=self.depth:
   self.st['open']+=1
   if len(self.examples)<2:self.examples.append([(str(r)[:10],f) for r,f in exact.items()]);
   return False
  r=max(ds) # largest has the fewest exponent choices, generally.
  for f in choices(r):
   x=r**f;sig=(x*r-1)//(r-1)
   if not self.visit({**exact,r:f},prod*x,ss*sig,eu or bool(f%2),lev+1):return False
  self.st['exhaust']+=1;return True
 def run(self):return self.visit({5:self.e},5**self.e,self.A,False,0)

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--depth',default=3,type=int);ap.add_argument('--nodes',default=500,type=int);ap.add_argument('--output');ap.add_argument('es',nargs='*',type=int);args=ap.parse_args();xs=json.loads((H/'Candidates.json').read_text());rows=[]
 for e in args.es or list(map(int,xs)):
  A=(5**(e+1)-1)//4;known=[]
  for r in set(map(int,xs[str(e)])):
   if proved(r):check(A%r==0,'spurious candidate factor');known.append(r)
  tr=Tree(e,sorted(known),args.depth,args.nodes);closed=tr.run(); row=dict(e=e,closed=closed,stats=dict(tr.st),example=tr.examples);rows.append(row)
  if closed:print('CLOSED',e,dict(tr.st),flush=True)
 if args.output:(H/args.output).write_text(json.dumps(rows,indent=1)+'\n')
 print('checked',len(rows),'closed',sum(r['closed'] for r in rows))
if __name__=='__main__':main()
