"""Integer two-sided supplier prices. Marking only verified non-A red primes
lets each marked base pay half its own ordinary exponent AND every unmarked
incoming sigma valuation its full cost. The other half of marked incoming
valuations is retained; no assumption that large incoming factors are prime.
"""
from pathlib import Path
import json,sys,math
from functools import cache
from itertools import accumulate
from bisect import bisect_right
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Emission as E
from Emission import U,BN,B
@cache
def sieve(n):
 b=bytearray(b'\1')*(n+1);b[:2]=b'\0\0'
 for i in range(2,math.isqrt(n)+1):
  if b[i]:b[i*i::i]=bytes((n-i*i)//i+1)
 return b
@cache
def prices(cutoff,mark,maxk):
 mask=sieve(cutoff);marked=[z for z in range(7,mark+1,6) if mask[z] and z not in BN and all((z*z+z+1)%b for b in BN)];M=math.prod(marked);sel=set(marked);cap=(cutoff**2+cutoff+1)//3;xs=[]
 for z in range(7,cutoff+1,6):
  if not mask[z] or z in BN:continue
  h=z;f=2
  while True:
   phi=h*h+h+1;n=phi//3
   if n>=cap or any(phi%b==0 for b in BN):break
   m=n
   while (g:=math.gcd(m,M))>1:m//=g
   cost=m*n*(z**f if z in sel else 1)
   if cost<cap:xs.append(cost)
   # Unlike a monotone tariff, lack of a cheap first unit does not stop
   # future levels unless the universal n>=cap lower bound applies.
   h=h**3;f*=3
 xs=sorted(xs+[cap]*maxk)[:maxk];return M,[1,*accumulate(xs,int.__mul__)]
def score(e,cfg,maxk,rows,three=True):
 A=(3**(e+1)-1)//2;pe=3**e;P=pe*3;tables=[]
 for z,mark in cfg:
  M,X=prices(z,mark,maxk);assert math.gcd(A,M)==1;tables.append(X)
 results=[]
 for s,tag,old,ext,ins in rows:
  y=3**s;q=U.euler_least(s,tag);base=pe*A*q;T=max(x[e-s] for x in tables);den=base**2*T
  allout=den>B**2;er=den*(4*q)**2>=(5*B)**2;ir=den*(q*y)**2>=(B*max(P,q)*(P//y+4))**2
  results.append([s,tag,old or allout,ext or er,ins or ir])
 return results
if __name__=='__main__':
 orig=json.loads((H/'Emission.json').read_bytes());out=[];cfg=[(2_000_000,239),(2_000_000,997),(2_000_000,4000)]
 for row in orig:
  e=row['e'];cs=score(e,cfg,256,row['cells']);out.append(dict(e=e,cfg=cfg,cells=cs));print(e,[sum(t[i] for t in cs) for i in (2,3,4)],flush=True)
 (H/'Weighted.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
