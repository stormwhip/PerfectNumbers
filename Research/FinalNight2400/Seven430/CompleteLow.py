"""Historical plus five new mask gaps: complete exact first Q^2; also run Q^12."""
from pathlib import Path
import sys,importlib.util
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path.insert(0,str(H));from VerifyQ import certify,Q,Z
from Verify12 import check
G=R/'Night2400/G5';spec=importlib.util.spec_from_file_location('g5_masked',G/'MaskedVerify.py');old=importlib.util.module_from_spec(spec);spec.loader.exec_module(old)
if __name__=='__main__':
 assert __debug__;a=old.verify(G/'Seven430.json.gz');holes={(m,tuple(r)) for m,v in a.items() for r in v.get(2,[])};expected={(m,((7,430),(Q,2),(Z,j))) for j,mm in [(2,[50,58,178]),(6,[50,58])] for m in mm};assert holes==expected
 for j in (2,6):certify(j)
 check();print('PASS (7,430) complete firsts Q^2, Q^12; sole remaining Q^4 after historical C3/G5.')
