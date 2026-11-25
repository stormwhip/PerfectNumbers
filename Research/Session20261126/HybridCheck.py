"""Verifies canonical exact trees with an optional local multisource terminal dual. Leaf preconditions must equal the exact path, with no unproved support assumptions."""
from pathlib import Path
import sys,json,gzip,argparse
from math import prod
from functools import cache
H=Path(__file__).resolve().parent;ap=argparse.ArgumentParser();ap.add_argument('packet',type=Path);ap.add_argument('--repo',type=Path,default=H.parents[1]);args=ap.parse_args();R=args.repo.resolve()/'Research';sys.path.insert(0,str(R/'Session20261126'));from PivotCheck import C,B,exact_leaf;sys.path.insert(0,str(R/'MiddayTerminal'));import Audit,Common
assert Path(Audit.__file__).resolve()==(R/'MiddayTerminal/Audit.py').resolve() and __debug__
def verify(path):
 d=json.load(gzip.open(path));p,e=d['p'],d['e'];assert p==3 and type(e)==int and 0<e<7000 and e%2==0;used=set();st=[0,0,0,0]
 @cache
 def prime(q):
  assert type(q)==int and q>2;n=q
  if n>=2**64:
   used.add(str(q))
   for r in d['ecpp'][str(q)]:assert r[0]==n;n=C.pc.level(*r)
  assert C.pc.prime64(n);return True
 def dead(s):return s.conflict or s.base>B or prod(C.sigma(q,h) for q,h in s.rows.items())>2*s.X
 def walk(P,node):
  s=C.State(P);assert not dead(s);typ=node['type'];
  if typ=='terminal':
   kw,ec,fl=d['duals'][node['key']];assert kw['root']==p and kw['e']==e and [(r,h) for r,h in kw['x']]==P[1:] and kw['extra']==kw['lower']==[] and set(kw)=={'root','e','extra','x','lower','L','T','cut','cap','wide','extend','weights','parity'};Common.dataset=lambda:{'ecpp':ec,'rows':{}};Common.chain.cache_clear();u=Audit.replay(**kw)[0];den=Audit.W*Audit.logs(10)[1];assert u>2400*den and u//den==fl;st[3]+=1;return
  if typ=='forest':
   k,o,a=node['roots'],node['owners'],node['head'];C.validate_forest(s,k,o,a,prime);assert min(C.Forest(s,k,o,a).lower()[0],exact_leaf(P,k,o,a))>B;st[0]+=1;return
  assert typ=='split';z=node['q'];assert prime(z) and z not in s.bad and z not in s.rows and s.D%z==0;v=C.valuation(s.D,z);f=v;start=s.base//z**v;seen=set();st[1]+=1
  while start*z**f<=B:
   if s.possible(z,f,v):
    pp=P+[(z,f)];ss=C.State(pp)
    if dead(ss):st[2]+=1
    else:seen.add(str(f));walk(pp,node['cases'][str(f)])
   f+=1
  assert seen==set(node['cases'])
 walk([(p,e)],d['tree']);assert used==set(d['ecpp']);return p,e,st
print(verify(args.packet),flush=True)
