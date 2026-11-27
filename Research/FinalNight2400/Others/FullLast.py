"""Disjoint cold union of all forty canonical exact firsts at (13,388)."""
from pathlib import Path
import sys,runpy,importlib.util
H=Path(__file__).resolve().parent;N=H.parents[1]/'Night2400';sys.path[:0]=[str(H),str(N)];from FrontierTree import replay
from Vertex388 import verify as vertex
sp=importlib.util.spec_from_file_location('disjoint',H.parent/'Disjoint/Verify.py');d=importlib.util.module_from_spec(sp);sp.loader.exec_module(d)
if __name__=='__main__':
 assert __debug__
 a=replay(N/'Fibers13x388.json.gz');assert a['key']==[13,388] and a['pivot']=='3543791' and len(a['domain'])==40 and len(a['covered'])==31
 assert d.check(72) and d.check(78);runpy.run_path(str(H/'CheckSix.py'),run_name='__main__');v=replay(H/'Thirteen388One.json.gz');assert v['key']==a['key'] and v['pivot']==a['pivot'] and v['domain']==a['domain'] and v['open_paths']==[[(13,388),(3543791,6),(14199329591297809156875293,12)]];vertex()
 S=[set(a['covered']),{72,78},{2,36,40,42,52,66},{6}];assert len(set.union(*S))==sum(map(len,S))==40 and set.union(*S)==set(a['domain']);print('FULL canonical (13,388) all 40 firsts, singleton P13_I00076.',flush=True)
