"""Cold union for the canonical exact exponent 13^262. No other shard credited."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;N=H.parents[1]/'Night2400';sys.path[:0]=[str(H),str(N/'G6'),str(N)]
from Verify46 import verify as forty_six
from VerifyFibers import verify as fibers
import importlib.util
spec=importlib.util.spec_from_file_location('g6_exact_tree',N/'G6/Verify.py');G6=importlib.util.module_from_spec(spec);spec.loader.exec_module(G6)
from FrontierTree import replay
if __name__=='__main__':
 assert __debug__
 a=fibers(N/'Fibers13x262.json.gz');b=G6.verify(N/'G6/Thirteen262.json.gz');c=replay(H/'Thirteen262.json.gz');d=fibers(H/'Thirteen262Direct16.json.gz');forty_six()
 assert a['key']==c['key']==d['key']==[13,262] and a['pivot']==c['pivot']==d['pivot']==str(G6.Q)
 assert a['domain']==b['root_domain']==c['domain']==d['domain'] and b['covered']==[1] and c['covered']==[12,28,42,60] and d['covered']==[16]
 parts=list(map(set,[a['covered'],b['covered'],c['covered'],d['covered'],[46]]));assert len(set.union(*parts))==sum(map(len,parts))==29 and set.union(*parts)==set(a['domain'])
 print('FULL canonical exact key 13^262, all 29 siblings; sole frozen pair of P13_I00055.',flush=True)
