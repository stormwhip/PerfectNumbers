"""Full-key verifier; insists on complete disjoint coverage and exact source key/domain."""
from pathlib import Path
import sys,importlib.util
H=Path(__file__).resolve().parent;N=H.parents[1]/'Night2400';sys.path[:0]=[str(N/'C14'),str(N)]
sp=importlib.util.spec_from_file_location('legacy_c14',N/'C14/Verify.py');c14=importlib.util.module_from_spec(sp);sp.loader.exec_module(c14)
from VerifyFibers import verify
if __name__=='__main__':
 assert __debug__;A=verify(N/'Fibers19x312.json.gz');T=verify(N/'Fiber19x312Ten.json.gz');assert A['key']==T['key']==[19,312] and A['pivot']==T['pivot']==str(c14.Q) and A['domain']==T['domain'] and A['open']==[1,2,8,10,12,16,22,36] and T['covered']==[10]
 c14.packet(8);c14.packet(36);supp=verify(H/'FiveFibers.json.gz');assert supp['key']==A['key'] and supp['pivot']==A['pivot'] and supp['domain']==A['domain']
 parts=[set(A['covered']),set(T['covered']),{8,36},set(supp['covered'])];assert len(set.union(*parts))==sum(map(len,parts))==40 and set.union(*parts)==set(A['domain']);print('FULL (19,312) 40/40, singleton P19_I00063.',flush=True)
