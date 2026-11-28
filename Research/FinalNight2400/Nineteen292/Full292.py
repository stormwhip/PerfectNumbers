"""Isolated target-level cold replay, not the historical global proof."""
import sys,json,gzip
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'Night2400')];from FrontierTree import replay
import Masked,CloseFour
if __name__=='__main__':
 assert __debug__
 groups=[];expected=list(range(2,119,2))
 for name in ['Forests292','Ten292','TwoMore']:
    r=replay(H/(name+'.json.gz'));assert r['key']==[19,292] and r['domain']==expected and r['pivot']=='10018843' and not r['open_paths'];groups.append(set(r['covered']))
 for name,exps,check in [('CloseFour',[4,6,52,88],CloseFour.verify),('First26',[26],Masked.verify),('First28',[28],Masked.verify),('LastThree',[2,8,36],Masked.verify)]:
    check(name+'.json.gz',exps);groups.append(set(exps))
 assert sum(map(len,groups))==len(set.union(*groups))==59 and set.union(*groups)==set(expected)
 G=H.parents[1]/'GeminiFrontier';sh=json.loads((G/'ShardToKeys.json').read_bytes());ks=json.loads((G/'KeyToShards.json').read_bytes());name=ks['19,292'];assert len(name)==1 and sh[name[0]]==[[19,292]]
 print('FULL exact 19^292; disjoint firsts',list(map(len,groups)),name[0],flush=True)
