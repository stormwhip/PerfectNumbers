"""One scoped canonical-key union; no complete-repository regression claim."""
import subprocess,sys
from pathlib import Path
H=Path(__file__).resolve().parent;repo=H.parents[2];history=H.parents[1]/'Night2400'/'C'/'Verify.py'
def replay(p):
 print('REPLAY',p.name,flush=True);subprocess.run([sys.executable,'-I','-S','-B','-X','int_max_str_digits=0',str(p)],cwd=repo,check=True)
if __name__=='__main__':
 assert __debug__;replay(history) # historical full first domain and 8/10/12
 sys.path.insert(0,str(H));from ExactTwo import verify;from CheckDeep import verify_row
 verify(420);verify_row(420,2);verify_row(420,4);print('PASS complete first 2',flush=True)
 for p in ['Verify.py','Four420.py','One420.py','SecondaryFour.py','SecondaryTwo.py']:replay(H/p)
 print('PASS COMPLETE (19,420), P19_I00080, firsts 2,4,6,8,10,12; all 6.')
