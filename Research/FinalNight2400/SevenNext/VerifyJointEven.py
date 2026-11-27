"""Ten additional exact 173 powers under Q^42. Stdlib-only authoritative entry."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Even42Probe import go,Q,R,C
from Even42Credit import go as credit
if __name__=='__main__':
 assert __debug__ and C.pc.prime64(Q) and C.pc.prime64(R) and C.sigma(7,12)==Q and (Q-1)%R!=0 and R-1==4*43
 # 230 was eliminated in the earlier 122-case certificate; do not count again.
 for h in [212,214,216,218,220,222,224,226,228,232]:
  s=C.State([(7,12),(Q,42),(R,h)]);assert not s.conflict and s.base<=10**2400
  ok,hit=credit(h,[43,431,9431,95531,95891]) if h==214 else go(h)
  assert ok,(h,hit);print('PASS exact upper-even 173',h,flush=True)
