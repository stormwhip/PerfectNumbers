"""Nested first-22 splits, all Euler-cofactor rebate test against constructed small divisibilities, and ledger footprint."""
import json,sys
from math import gcd,prod
from pathlib import Path
H=Path(__file__).resolve().parents[1]/'ThirtyOne';sys.path.insert(0,str(H));from EulerForest import block
B=10**2400;sig=lambda p,h:(p**(h+1)-1)//(p-1);T=sig(31,16);G=H.parents[1]/'GeminiFrontier'
def state(row):
 X=prod(p**e for p,e in row);raw=prod(sig(p,e) for p,e in row);S=raw//2**sum(e%2 for p,e in row);D=S//gcd(S,X);return X,D,gcd(X,D)==1 and gcd(19*7*11,X*S)==1 and X*D<=B and raw<=2*X and sum(e%2 for p,e in row)<=1 and all(not e%2 or p%4==e%4==1 for p,e in row)
def dom(row,z):
 X,d,ok=state(row);assert ok and d%z==0;f=0;L=[]
 while d%z==0:d//=z;f+=1
 while X*d*z**f<=B:
  if state(row+[(z,f)])[2]:L.append(f)
  f+=1
 return L,f
P=[(31,16),(T,22)];A,ta=dom(P,47);C,tc=dom(P+[(47,2)],37);d=json.loads((H/'Packet22.json').read_bytes());deep=json.loads((H/'DeepPacket.json').read_bytes());assert A==sorted(map(int,d['cases'])) and len(A)==140 and C==sorted(map(int,deep['cases'])) and len(C)==112;assert all(j%2==0 for j in [*A,*C]);assert sig(47,2)==37*61
# Every possible q^(maximal valuation) tested independently here is within its lower limit.
for m,q in [(3,5),(7,13),(7,41),(13,101),(17,101)]:
 if q%(4*m)!=2*m-1:continue
 for k in range(1,30):
  if k%q==0:continue
  for a in range(0,7):assert block(k*q**a,m)<=k
s=json.loads((G/'ShardToKeys.json').read_bytes());inv=json.loads((G/'KeyToShards.json').read_bytes());print('PASS both exact partitions; outer',len(A),'tail',ta,'inner',len(C),'tail',tc,'ledger',[(k,vs) for k,vs in s.items() if [31,16] in vs],inv['31,16']);assert [(k,vs) for k,vs in s.items() if [31,16] in vs]==[('P31_I00005',[[31,16]])] and inv['31,16']==['P31_I00005']
