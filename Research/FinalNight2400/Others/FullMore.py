"""Disjoint cold replay of all 31 first exponents at canonical 31^352."""
from pathlib import Path
import sys,importlib.util
H=Path(__file__).resolve().parent;N=H.parents[1]/'Night2400';sys.path[:0]=[str(H),str(N/'C8'),str(N)]
spec=importlib.util.spec_from_file_location('c8_source',N/'C8/Verify.py');c8=importlib.util.module_from_spec(spec);spec.loader.exec_module(c8)
from FrontierTree import replay
if __name__=='__main__':
 assert __debug__ and c8.KEY==(31,352) and c8.Q==1797674429773
 c8.verify();sets=[{2}|set(c8.SPLITS)|set(c8.PRICES)]
 for name in ('ThirtyOne352One.json.gz','ThirtyOne352Thirteen.json.gz'):
  v=replay(H/name);assert not v['open_paths'] and v['key']==[31,352] and v['pivot']==str(c8.Q) and v['domain']==c8.DOMAIN;sets.append(set(v['covered']))
 assert sum(map(len,sets))==len(set.union(*sets))==len(c8.DOMAIN)==31 and set.union(*sets)==set(c8.DOMAIN)
 print('FULL canonical exact 31^352: all 31 first exponents; singleton shard P31_I00069.',flush=True)
