"""Project two already cold-verified primary-fiber manifests; no new assumptions or shard credits."""
from pathlib import Path
import hashlib,json,gzip,sys
H=Path(__file__).resolve().parent
R=Path(sys.argv[1]).resolve()/'Research' if len(sys.argv)>1 else H.parents[1]
raw=(R/'Session20261126/LowBranches/Branches.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()=='4d746a1d6e913953761b0b07ec5df5a42bdbf89aaca2e345467005964c96bfa0';old=json.loads(gzip.decompress(raw));new=(H/'Branches.json.gz').read_bytes();assert hashlib.sha256(new).hexdigest()=='f9545a514eb6db321302d5090663b42d108babcf1497a9a0f780df3c4c604fc6';new=json.loads(gzip.decompress(new));sys.path.insert(0,str(R/'Session20261126'));import PivotCheck as P
from math import prod
for e,q,cas in old['roots']:
 s=P.C.State([(3,e)]);c=P.C.valuation(s.D,q);assert c and s.D%q==0;f=c;fs=set();M=s.base//q**c
 while M*q**f<=P.B:
  if s.possible(q,f,c):
   p=P.C.State([(3,e),(q,f)]);
   if not p.conflict and p.base<=P.B and prod(P.C.sigma(z,h) for z,h in p.rows.items())<=2*p.X:fs.add(f)
  f+=1
 a=set(map(int,cas));bb=[r for i,z,r in new['roots'] if (i,z)==(e,q)];assert len(bb)==1;b=set(map(int,bb[0]));assert a|b<=fs and not a&b;left=fs-a-b;print(e,q,'domain',len(fs),'baseline excluded',len(a),'new',sorted(b),'now excluded',len(a|b),'left',len(left),sorted(left));assert len(fs)=={6:182,12:100}[e]
print('Complete root exponents newly excluded: 0; complete shards newly excluded: 0.')
