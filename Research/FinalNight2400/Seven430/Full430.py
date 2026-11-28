"""Complete exact (7,430) union; all 64 support masks, and every compatible pivot valuation."""
from pathlib import Path
import sys,importlib.util
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from CompleteLow import old,G,certify,Q,Z,check
from Verify4 import run
R=H.parents[1];C3=R/'Night2400/C3/Verify.py';spec=importlib.util.spec_from_file_location('frozen_C3_430',C3);hist=importlib.util.module_from_spec(spec);spec.loader.exec_module(hist)
if __name__=='__main__':
 assert __debug__ and hist.ROOT==(7,430) and hist.Q==Q and old.P==7 and old.E==430 and old.Q==Q
 hist.verify();a=old.verify(G/'Seven430.json.gz');assert set(a)==set(range(2,256,4));assert {f for row in a.values() for f in row}=={2,4,12}
 expected={(m,((7,430),(Q,2),(Z,j))) for j,mm in [(2,[50,58,178]),(6,[50,58])] for m in mm};assert {(m,tuple(r)) for m,v in a.items() for r in v.get(2,[])}==expected
 for j in (2,6):certify(j)
 check();assert not run();print('FULL canonical exact 7^430, P7_I00082, every first Q valuation 2,4,6,8,10,12,14,16; no mask holes.',flush=True)
