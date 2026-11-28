"""Replay all supplied exact descendant branches, binding two price leaves."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;N=H.parents[1]/'Night2400';sys.path[:0]=[str(H),str(N)]
from FrontierTree import replay
from Price388Leaf import verify
if __name__=='__main__':
 assert __debug__
 v=replay(H/'Thirteen388Six.json.gz');assert v['key']==[13,388] and v['pivot']=='3543791' and set(v['covered'])=={2,36,40,52}
 expected=[[(13,388),(3543791,42),(1113708120497983331,12),(217387,52)],[(13,388),(3543791,66),(459911137111,10)]]
 assert sorted(v['open_paths'])==expected;assert verify(42,1113708120497983331,12,[(217387,52)]) and verify(66,459911137111,10)
 print('PASS six complete first exponents at (13,388): 2,36,40,42,52,66. No first-6 closure inferred.',flush=True)
