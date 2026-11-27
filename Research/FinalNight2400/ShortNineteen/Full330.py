"""Scope: integrated (19,330) exact-key proof, including historical baseline."""
import subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;repo=H.parents[2];history=H.parents[1]/'Night2400'/'C2'/'Verify.py'
def replay(p):
 print('REPLAY',p.name,flush=True);subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(p)],cwd=repo,check=True)
if __name__=='__main__':
 assert __debug__;replay(history)
 sys.path.insert(0,str(H));from ExactTwo import verify;from CheckDeep import verify_row
 verify(330);verify_row(330,1);verify_row(330,5);verify_row(330,0)
 for p in ['Four330.py','Ab330.py','Remaining330.py','EulerOne330.py','LastSix330.py']:replay(H/p)
 print('PASS COMPLETE (19,330), P19_I00065, 6/6 firsts.')
