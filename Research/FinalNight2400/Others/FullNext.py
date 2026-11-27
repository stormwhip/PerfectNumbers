"""Cold disjoint union of all exact first valuations of (13,310)."""
from pathlib import Path
import sys,importlib.util
H=Path(__file__).resolve().parent;N=H.parents[1]/'Night2400';sys.path[:0]=[str(H),str(N)]
from NextPrice42 import main as price42
from VerifyFibers import verify
spec=importlib.util.spec_from_file_location('c6_historical',N/'C6/Verify.py');c6=importlib.util.module_from_spec(spec);spec.loader.exec_module(c6)
if __name__=='__main__':
 assert __debug__ and c6.KEY==(13,310) and c6.Q==5424477432443
 c6.verify();historical={6,10,12,20,22,32,38,48,50,52,56,58,60,66};new=verify(H/'Thirteen310Seven.json.gz'); assert new['key']==[13,310] and new['pivot']==str(c6.Q) and new['domain']==c6.DOMAIN
 price42(); parts=[historical,set(new['covered']),{42}];assert sum(map(len,parts))==len(set.union(*parts))==len(c6.DOMAIN) and set.union(*parts)==set(c6.DOMAIN)
 print('FULL canonical exact 13^310: disjoint 14+7+1=22, P13_I00063.',flush=True)
