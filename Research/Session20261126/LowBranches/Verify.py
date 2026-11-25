"""Issue and verify a strictly scoped subset of primary pivots; exact list of unproved exponents is recomputed from integers. Not a complete exponent certificate."""
from pathlib import Path
import gzip,json,sys,hashlib,math
from functools import cache
L=Path(__file__).resolve().parent;D=L.parent;import argparse;ap=argparse.ArgumentParser();ap.add_argument('--repo',type=Path,default=L.parents[2]);op=ap.parse_args();out=L/'Branches.json.gz';R=op.repo.resolve()/'Research';sys.path.insert(0,str(R/'Session20261126'));import PivotCheck as PC
C=PC.C;B=PC.B

def impossible(s):return s.conflict or s.base>B or math.prod(C.sigma(z,h) for z,h in s.rows.items())>2*s.X

def children(P,z):
 s=C.State(P);assert not impossible(s) and z not in s.rows and z not in s.bad and s.D%z==0;h=C.valuation(s.D,z);f=h;st=s.base//z**h;out=[]
 while st*z**f<=B:
  if s.possible(z,f,h) and not impossible(C.State(P+[(z,f)])):out.append(f)
  f+=1
 return out

def verify(d):
 rr=[];u=set();covered=[];visited=set()
 @cache
 def prime(z):
  assert type(z)==int and z>2;n=z
  if z>=2**64:
   u.add(str(z))
   for a in d['ecpp'][str(z)]:assert a[0]==n;n=C.pc.level(*a)
  assert C.pc.prime64(n);return True
 def walk(P,x):
  s=C.State(P);assert not impossible(s)
  if x['type']=='forest':
   k,o,h=x['roots'],x['owners'],x['head'];C.validate_forest(s,k,o,h,prime);assert C.Forest(s,k,o,h).lower()[0]>B and PC.exact_leaf(P,k,o,h)>B,('under-budget forest',P);return
  z=x['q'];assert x['type']=='split' and prime(z);ss=children(P,z);assert set(map(str,ss))==set(x['cases']);
  for h in ss:walk(P+[(z,h)],x['cases'][str(h)])
 for e,q,cas in d['roots']:
  assert e in (6,10,12,22) and e not in visited;visited.add(e);assert prime(q);fs=children([(3,e)],q);assert all(str(int(h))==h and int(h) in fs for h in cas)
  for h,row in cas.items():walk([(3,e),(q,int(h))],row)
  left=sorted(set(fs)-set(map(int,cas)));rr.append([e,q,len(fs),len(cas),left]);print('PASS',rr[-1],flush=True)
 assert u==set(d['ecpp']);return rr
assert __debug__;verify(json.load(gzip.open(out)))
