"""Cold exact-key union; fails on any missing sibling, duplicate, or OPEN node."""
from pathlib import Path
import sys,gzip,json
H=Path(__file__).resolve().parent; N=H.parents[1]/'Night2400'
sys.path[:0]=[str(N/'C12'),str(N)];import Verify as C12
from VerifyFibers import verify
from FrontierTree import replay
if __name__=='__main__':
 assert __debug__
 base=verify(N/'Fibers31x310.json.gz');assert base['key']==[31,310] and int(base['pivot'])==C12.Q and base['domain']==C12.DOMAIN
 C12.packet('Minimum31x310.json.gz',(6,58));C12.packet('Fiber16.json.gz',(16,));parts=[set(base['covered']),{6,58,16}]
 for f in [4,18]:
  v=replay(H/f'Root31x310F{f}.json.gz');assert v['key']==base['key'] and v['pivot']==base['pivot'] and v['domain']==base['domain'] and v['covered']==[f] and not v['open_paths'];parts.append({f})
 assert sum(map(len,parts))==len(set.union(*parts))==len(C12.DOMAIN) and set.union(*parts)==set(C12.DOMAIN)
 print('FULL canonical exact key 31^310, no other root or exponent lift. All 26 siblings.',flush=True)
