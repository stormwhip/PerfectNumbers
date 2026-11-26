"""Bind and compare the historic low-root proof with each sprint incremental packet, without trusting counts."""
from pathlib import Path
import sys,gzip,json,hashlib
from math import prod
R=Path(sys.argv[1]).resolve()/'Research';paths=list(map(Path,sys.argv[2:]));assert __debug__ and len(paths) in (3,4)
hs=['4d746a1d6e913953761b0b07ec5df5a42bdbf89aaca2e345467005964c96bfa0','f9545a514eb6db321302d5090663b42d108babcf1497a9a0f780df3c4c604fc6','4e5bfdec9fc6eafdf0a80078bd1c81526a234c82c0e689f7621408e2bbf0d1f2','a12ff742b5f2c246b72cd0387ff5281beb7d540e5574ddac4bfcfb680463542e','aa9afe7863e8ba7b38006645914c683f6d8df732058c78a408af2086ec77dc59'];paths=[R/'Session20261126/LowBranches/Branches.json.gz',*paths];done={};deltas=[]
for path,sha in zip(paths,hs):
 raw=path.read_bytes();assert hashlib.sha256(raw).hexdigest()==sha;obj=json.loads(gzip.decompress(raw));this={}
 for e,q,cs in obj['roots']:
  assert (e,q) in [(6,1093),(12,797161)] and e not in this;v=set(map(int,cs));prior=done.setdefault(e,set());assert not prior&v;prior.update(v);this[e]=sorted(v)
 deltas.append(this)
sys.path.insert(0,str(R/'Session20261126'));import PivotCheck as P
for e,q in [(6,1093),(12,797161)]:
 s=P.C.State([(3,e)]);c=P.C.valuation(s.D,q);assert c;M=s.base//q**c;f=c;domain=set()
 while M*q**f<=P.B:
  if s.possible(q,f,c):
   a=P.C.State([(3,e),(q,f)]);
   if not a.conflict and a.base<=P.B and prod(P.C.sigma(z,j) for z,j in a.rows.items())<=2*a.X:domain.add(f)
  f+=1
 assert done[e]<=domain;left=sorted(domain-done[e]);print('root',e,'prime',q,'domain',len(domain),'prior',len(deltas[0][e]),'new',sorted(y for d in deltas[1:] for y in d.get(e,[])),'excluded',len(done[e]),'left',left)
 assert len(left)=={6:23 if len(paths)==5 else 26,12:4}[e]
print('New complete exponents: 0; new complete shards: 0.')
