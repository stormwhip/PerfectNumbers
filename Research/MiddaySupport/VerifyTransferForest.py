"""Cold replay with fixed preconditions; index-11 transfers and support-only full trees."""
import gzip,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Transfer import check
sys.path.insert(0,str(H.parent/'Nov25/Compose'));from Replay import proof

def verify():
 q=150332843
 t=check(31,[19,7,11],(23,397,617,q),[('absent',[13]),('absent',[17,29,37]),('exact1',[5])]); print('transfer',t)
 for packet,assigned,yes,no in [('Full31',[[31,10]],[5],[3,13,17]),('Both31',[[31,10],[5,1]],[3,5],[13,17,29,37])]:
  u=json.loads(gzip.decompress((H/(packet+'.json.gz')).read_bytes()));
  if (u['assigned'],u['present'],u['absent'])!=(assigned,yes,no):raise ValueError('unexpected precondition')
  print(packet,proof(u,conditional=True),flush=True)
if __name__=='__main__':verify()
