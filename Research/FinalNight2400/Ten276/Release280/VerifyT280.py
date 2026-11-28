"""Exact s-square T domain. Replays all 21 newly closed T values by default."""
from pathlib import Path
import sys,json,gzip,runpy,hashlib
from math import prod
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Verify280 as v
from Paths280 import pre,t,r,z,paths,Tdomain
Hist=H.parents[2]/'Night2400/C13';old=runpy.run_path(str(Hist/'Verify.py'))
C=old['C'];B=old['B'];exact=old['exact_leaf'];split=old['split']
for f in [*H.glob('AbBook*.json.gz'),*H.glob('GrowBook*.json.gz')]:v.book.update(json.loads(gzip.decompress(f.read_bytes())))
def compact(i):
 P=paths[i];K,O,h=json.loads((H/f'Grow280Case{i}.json').read_bytes());s=C.State(P)
 assert not s.conflict and all(v.prime(q) is None for q,f in P)
 for j,(q,f) in enumerate(P):
  if j:
   k,*_=split(P[:j],q);assert k[str(f)]==P[:j+1]
 def prime(q):v.prime(q);return True
 C.validate_forest(s,K,O,h,prime);a=C.Forest(s,K,O,h).lower()[0];b=exact(P,K,O,h);assert min(a,b)>B
 print('PASS compact',i,[f for p,f in P],min(len(str(a)),len(str(b)))-1,flush=True)
def run(short=False):
 assert __debug__;d,_,_,sha,top=old['reader']('Paths2.json.gz');assert sha=='2e8230b7e7c98f4ee89ab29389fcda7db8aa4ca81ceb383082ec630ffa57dd6c' and top['2']==pre
 k,_,_,tail=split(pre,t);assert list(map(int,k))==Tdomain
 compact(18);compact(17)
 for i in (0,1,2,3):v.verify(i)
 # Consume only actually needed old paths, recomputing all included arithmetic.
 new={tuple(paths[i]) for i in [0,1,2,3,17]};hist={tuple(map(tuple,rec['parts'])):rec['tree'] for rec in d['paths'].values()};k0,_,_,rtail=split(pre+[(t,4)],r);oldneeded=0
 v.book.update(d['ecpp']);v.prime.cache_clear()
 def pr(q):v.prime(q);return True
 def close(P):
  nonlocal oldneeded
  if tuple(P) in new:return
  for b,f in P:pr(b)
  old['forest'](P,hist[tuple(P)],pr);oldneeded+=1
 for e,P in k0.items():
  if e!='2':close(P)
  else:
   sub,_,_,ztail=split(P,z)
   for L in sub.values():close(L)
 print('PASS T^4 exact union old leaves',oldneeded,'new exact leaves',len(new),'tails',rtail,ztail,flush=True)
 if short:print('Only T^1,T^4 here; other 19 direct trees not replayed',flush=True);return
 for i in [21,*range(23,41)]:v.verify(i)
 done={1,4}|{paths[i][2][1] for i in [21,*range(23,41)]};assert set(Tdomain)-done=={2,6}
 print('PASS s^2: 21 of 23 viable exact T valuations; only T^2 and T^6 remain. Not whole s^2/key/shard.',flush=True)
if __name__=='__main__':run(sys.argv[1:]==['--two-only'])
