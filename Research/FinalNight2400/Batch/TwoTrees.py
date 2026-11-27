"""Rebuild the complete domains for firsts 112 and 136."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Night2400'));from FrontierTree import replay
assert __debug__
r=replay(H/'Trees112And136.json.gz');assert r['key']==[11,396] and r['pivot']=='2383' and set(r['covered'])=={112,136} and not r['open_paths']
