"""Replay only new first-pivot exclusions using two existing exact forest checks. Standard library only."""
from pathlib import Path
import json,sys,gzip,math,hashlib
from functools import cache
H=Path(__file__).resolve().parent

def main(repo,packets):
 if not __debug__:raise ValueError('assertions required')
 R=repo/'Research';sys.path.insert(0,str(R/'Session20261126'));import PivotCheck as PC
 C=PC.C;B=PC.B;done=set()
 def possible(s):return not s.conflict and s.base<=B and math.prod(C.sigma(z,f) for z,f in s.rows.items())<=2*s.X
 def child(P,z):
  s=C.State(P);assert possible(s) and z not in s.rows and z not in s.bad and s.D%z==0;c=C.valuation(s.D,z);st=s.base//z**c;f=c;ks={}
  while st*z**f<=B:
   if s.possible(z,f,c):
    T=P+[(z,f)]
    if possible(C.State(T)):ks[str(f)]=T
   f+=1
  return ks
 for file in packets:
  d=json.loads(gzip.decompress(file.read_bytes()));assert 1<=len(d['roots'])<=2;seen=set();stats=[0,0,10**9];
  @cache
  def prime(z):
   assert type(z)==int and z>2;u=z
   if u>=2**64:
    seen.add(str(z));
    for row in d['ecpp'][str(z)]:assert row[0]==u;u=C.pc.level(*row)
   assert C.pc.prime64(u);return True
  def walk(P,v):
   if v['type']=='paired':
    assert P==[(3,12),(797161,112),(6781,1),(3391,102)] and v==dict(type='paired');sys.path.insert(0,str(H));import TwoSupply;assert TwoSupply.run(P,[19,5,10]);return
   if v['type']=='split':
    z=v['q'];assert prime(z);xs=child(P,z);assert set(xs)==set(v['cases']);stats[1]+=1
    for h,T in xs.items():walk(T,v['cases'][h])
   else:
    assert v['type']=='forest';s=C.State(P);k,o,h=v['roots'],v['owners'],v['head'];C.validate_forest(s,k,o,h,prime);lb=min(C.Forest(s,k,o,h).lower()[0],PC.exact_leaf(P,k,o,h));assert lb>B,('underpriced',P,PC.floor10(lb));stats[0]+=1;stats[2]=min(stats[2],PC.floor10(lb))
  for e,q,t in d['roots']:
   assert (e,q) in [(6,1093),(12,797161)] and prime(q) and len(t)>0;sb=child([(3,e)],q)
   for f,row in t.items():
    assert f in sb and (e,q,f) not in done;done.add((e,q,f));stats[:]=[0,0,10**9];walk(sb[f],row);print('PASS',e,q,f,stats,flush=True)
  assert seen==set(d['ecpp']);print('ECPP',len(seen),'sha256',hashlib.sha256(file.read_bytes()).hexdigest(),flush=True)
if __name__=='__main__':main(Path(sys.argv[1]).resolve(),list(map(Path,sys.argv[2:])))
