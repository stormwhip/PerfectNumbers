"""Eleven new upper-even exact cases using the universal conditional Q-supply cap."""
from pathlib import Path
from functools import cache
import gzip,sys,json
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Cap42Index import go,Q,R,C;from SimulCap import check
if __name__=='__main__':
 assert __debug__ and C.pc.prime64(Q) and C.pc.prime64(R) and C.sigma(7,12)==Q and R-1==4*43 and Q>5100 and (Q-1)%R!=0 and check(5)==[]
 z=json.load(gzip.open(H/'CapEvidence.json.gz'));seen=set()
 @cache
 def prime(r):
  y=r
  if r>=2**64:
   seen.add(str(r))
   for row in z['ecpp'][str(r)]:assert row[0]==y;y=C.pc.level(*row)
  return C.pc.prime64(y)
 assert sorted(map(int,z['nodes']))==[172,180,192,196,198,200,202,204,206,208,210]
 for h,fs in z['nodes'].items():
  assert all(prime(r) for r in fs);a=int(h);s=C.State([(7,12),(Q,42),(R,a)]);assert not s.conflict and s.base<=10**2400 and all(s.D%r==0 and r not in s.rows for r in fs);ok,fail=go(a,fs);assert ok,(a,fail);print('PASS capped simultaneous ordinary source',a,flush=True)
 assert seen==set(z['ecpp'])
