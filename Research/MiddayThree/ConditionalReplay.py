"""Offline stdlib proof of all blue-source cells AND the incoming-only cells.
Independent implementation: no discovery/SymPy imports, recompute divisibility,
cyclotomic unit and all rho=0,1/2 price lower bounds. Explicit (s,tag) claims
only, no reliance on likely-prime facts or numerical root-window audit.
"""
from pathlib import Path
from functools import lru_cache
from itertools import accumulate
from math import isqrt,prod,gcd
import json,sys
H=Path(__file__).resolve().parent;B=10**2400;BAN=(19,7,11,31,13)
def require(t,msg):
 if not t:raise ValueError(msg)
@lru_cache(None)
def charges(t,m,weighted):
 sieve=bytearray([1])*(t+1);sieve[:2]=bytes(2)
 for n in range(2,isqrt(t)+1):
  if sieve[n]:sieve[n*n::n]=bytes((t-n*n)//n+1)
 marks={a for a in range(7,m+1,6) if sieve[a] and a not in BAN and not any((a*a+a+1)%z==0 for z in BAN)};mod=prod(marks);ceil=(t*t+t+1)//3;slots=[]
 for a in range(7,t+1,6):
  if not sieve[a] or a in BAN:continue
  h=1
  while True:
   x=a**h;n=(x*x+x+1)//3
   if n>=ceil or any(n%b==0 for b in BAN):break
   d=n
   if weighted:
    while (g:=gcd(d,mod))!=1:d//=g
    d*=n
    if a in marks:d*=x*x
   if d<ceil:slots.append(d)
   h*=3
 return mod,[1,*accumulate(sorted(slots+[ceil]*256)[:256],int.__mul__)]
def lower(s,c):
 y=3**s;v=1 if c==1 else 5
 for k in range(v,v+72,6):
  q=2*y*k-1
  if not any(k%z==0 or q%z==0 for z in BAN) and pow(2,q-1,q)==1:return q
 return 2*y*(v+72)-1
def main():
 ledger=json.loads((H.parent/'Nov25/Delta.json').read_bytes());targets={e for z in ledger['remaining_shards'] if z['root']==3 for e in z['remaining_actuals']};out=[];allseen=set()
 files=json.loads((H/'Weighted.json').read_bytes());cfg=[(100000,0,False),(2000000,239,True),(2000000,997,True),(2000000,4000,True)]
 for rec in files:
  e=rec['e'];require(e in targets and e not in allseen,'target');allseen.add(e);P=3**(e+1);A=(P-1)//2;pe=P//3;prices=[];seen=set();counts=[0]*3
  for cutoff,marker,w in cfg:
   mod,cost=charges(cutoff,marker,w);require(gcd(mod,A)==1,'marked root factor');prices.append((2 if w else 1,cost))
  for s,c,*claims in rec['cells']:
   require(0<s<=e and e-s<=256 and c in (1,2) and (s,c) not in seen and len(claims)==3 and all(type(x)==bool for x in claims),'bad cell');seen.add((s,c));y=3**s;q=lower(s,c);results=[False]*3
   for d,price in prices:
    M=(pe*A*q)**d*price[e-s];a=M>B**d;b=a or M*(4*q)**d>=(5*B)**d;f=a or M*(q*y)**d>=(B*max(P,q)*(P//y+4))**d;results=[old or new for old,new in zip(results,(a,b,f))]
   require(results==claims,'mismatch');counts=[n+b for n,b in zip(counts,results)]
  out.append([e,len(seen),*counts]);print('PASS',out[-1],flush=True)
 print('TOTAL',[sum(x[i] for x in out) for i in range(1,5)],'conditional cells only, no exact exponents');return out
if __name__=='__main__':main()
