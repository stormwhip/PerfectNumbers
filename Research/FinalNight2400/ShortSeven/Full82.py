"""Recheck the archival C4 arithmetic and test the complete complement, not a mask projection."""
from pathlib import Path
import sys,importlib.util
H=Path(__file__).resolve().parent;N=H.parents[1]/'Night2400';sys.path.insert(0,str(N));from VerifyFibers import verify
sp=importlib.util.spec_from_file_location('canon_c4',N/'C4/Verify.py');c4=importlib.util.module_from_spec(sp);sp.loader.exec_module(c4)
if __name__=='__main__':
 assert __debug__ and (c4.P,c4.E)==(19,82);c4.verify();v=verify(H/'Nineteen82Six.json.gz');assert v['key']==[19,82] and v['pivot']==str(c4.Q) and v['covered']==[6] and v['domain']==[2,4,6,8,10] and v['open']==[2,4,8,10]
 print('FULL canonical exact (19,82), 4 full historical firsts + 1 unconditional new first; singleton P19_I00021.',flush=True)
