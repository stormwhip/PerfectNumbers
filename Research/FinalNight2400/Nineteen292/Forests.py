from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Night2400'));from FrontierTree import replay
assert __debug__
r=replay(H/'Forests292.json.gz');assert r['key']==[19,292] and len(r['covered'])==38 and r['pivot']=='10018843' and r['open']==[2,4,6,8,10,12,14,16,18,20,22,24,26,28,30,32,36,40,52,58,88] and not r['open_paths']
v=replay(H/'Ten292.json.gz');assert v['key']==r['key'] and v['domain']==r['domain'] and v['pivot']==r['pivot'] and not v['open_paths'] and set(v['covered'])=={10,12,14,16,18,20,22,24,30,32} and not set(v['covered'])&set(r['covered'])
