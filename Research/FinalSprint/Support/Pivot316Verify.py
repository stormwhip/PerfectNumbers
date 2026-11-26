"""Portable standard-library replay of 36 support cuts for (19,316). No discovery code or prior support exclusion is trusted. --repo PATH selects the frozen public library."""
from pathlib import Path
from functools import cache
from math import gcd,prod
import sys,json,gzip,argparse
assert __debug__;H=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=H.parents[2]);ns=ap.parse_args();R=ns.repo.resolve()/'Research';sys.path.insert(0,str(R/'Session20261126'));import PivotCheck as PC
O=(19,7,11,31,13,3,5,17);B=10**2400;p,e=19,316;q=1255900817071954721881883552067931;d=json.load(gzip.open(H/'Pivot316.json.gz'));A=PC.C.sigma(p,e);c=PC.C.valuation(A,q);assert c>0
@cache
def prime(z):
 assert type(z)==int and z>2;n=z
 if z>=2**64:
  for row in d['ecpp'][str(z)]:assert n==row[0];n=PC.C.pc.level(*row)
 assert PC.C.pc.prime64(n);return True
assert prime(q);fs=set()
for t in d['rows']:
 f=t['f'];assert f>0 and (f%2==0 or q%4==f%4==1) and f not in fs;P=[(p,e),(q,f)];s=PC.C.State(P);assert not s.conflict;PC.C.validate_forest(s,t['roots'],t['owners'],t['head'],prime);a=PC.independent(p,e,q,f,t['roots'],t['owners'],t['head']);assert a>B;fs.add(f);print('FOREST',f,PC.floor10(a),flush=True)
claimed=d['masks'];assert sorted(set(claimed))==claimed and len(claimed)==36;current=json.loads((R/'Session20261126/OpenSupport.json').read_bytes());assert current['order']==list(O) and set(claimed)<=set(current['rows']['19:316'])
for m in claimed:
 assert 0<m<256 and m&1;bad=prod(z for i,z in enumerate(O) if not m>>i&1);f=c
 while p**e*(A//q**c)*q**f<=B:
  if f%2==0 or q%4==f%4==1:
   X=p**e*q**f;Z=A*PC.C.sigma(q,f);T=Z//(1+f%2);D=T//gcd(T,X)
   if gcd(T,bad)==1 and gcd(q,bad)==1 and gcd(D,X)==1 and X*D<=B and Z<=2*X:assert f in fs,(m,f)
  f+=1
print('VERIFIED',p,e,len(claimed),'conditional masks',claimed)
