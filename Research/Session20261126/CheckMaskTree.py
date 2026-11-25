"""Complete support-indexed exact-exponent trees. H is the full set of dividing S8 primes. No assumed factor outside H. Standard library."""
from pathlib import Path
import sys,json,gzip,argparse
from functools import cache
from math import prod,gcd
H=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('files',type=Path,nargs='+');ap.add_argument('--repo',type=Path,default=H.parents[1]);op=ap.parse_args();R=op.repo.resolve()/'Research';sys.path.insert(0,str(R/'Nov25/Compose'));import Compose as C

def verify(path):
 assert __debug__;d=json.load(gzip.open(path));p,e=d['p'],d['e'];assert p==3 and type(e)==int and 0<e<=7000 and e%2==0;used=set();stat=[0,0,0];roots=C.ORDER;cost=[]
 @cache
 def prime(q):
  assert type(q)==int and q>2;t=q
  if q>=2**64:
   used.add(str(q))
   for a in d['ecpp'][str(q)]:assert a[0]==t;t=C.pc.level(*a)
  assert C.pc.prime64(t);return True
 def impossible(s):return s.conflict or s.base>C.B or prod(C.sigma(z,f) for z,f in s.rows.items())>2*s.X
 def walk(parts,node,h):
  s=C.State(parts,present=h,absent=set(roots)-h);assert not impossible(s);typ=node['type']
  if typ=='forest':
   ks,os,head=node['roots'],node['owners'],node['head'];C.validate_forest(s,ks,os,head,prime);v=C.Forest(s,ks,os,head).lower()[0];assert v>C.B,(parts,h);stat[0]+=1;return
  assert typ=='split';z=node['q'];assert z not in s.rows and z not in s.bad and prime(z) and (z in h or s.D%z==0);c=C.valuation(s.D,z);st=s.base//z**c;seen=set();stat[1]+=1;f=max(1,c)
  while st*z**f<=C.B:
   if s.possible(z,f,max(1,c)):
    np=parts+[(z,f)];ns=C.State(np,present=h,absent=set(roots)-h)
    if not impossible(ns):seen.add(str(f));walk(np,node['cases'][str(f)],h)
    else:stat[2]+=1
   f+=1
  assert seen==set(node['cases'])
 tail=roots[roots.index(p)+1:];supports=[{p}|{z for i,z in enumerate(tail) if b>>i&1} for b in range(1<<len(tail))];keys=set()
 for h in supports:
  key=','.join(map(str,sorted(h)));keys.add(key);walk([(p,e)],d['supports'][key],h)
 assert keys==set(d['supports']) and used==set(d['ecpp']);return p,e,stat
for f in op.files:print(verify(f),flush=True)
