"""Combine exactly one omitted branch with the canonical terminal proof.
This orchestrator runs fixed files in isolated child processes so no private
modules named Audit/Common are accidentally reused between proof suites.
"""
import subprocess,sys,gzip,json,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;T=H.parent/'MiddayTerminal';q=46509804063632583432467217805311362636553293639540930405531

def check():
 if not __debug__:raise RuntimeError('no -O')
 x=H/'Complement148.json.gz';y=T/'Leaf148x6.json.gz';d=json.loads(gzip.decompress(x.read_bytes()));s=json.loads(gzip.decompress(y.read_bytes()));assert d['e']==148 and d['pivot']==q and d['omitted']==[6] and s['p']==3 and s['e']==148 and len(s['leaves'])==1 and s['leaves'][0]['x']==[[q,6]]
 subprocess.run([sys.executable,'-I','-S','-B',str(H/'Complement.py'),str(x)],check=True);subprocess.run([sys.executable,'-I','-S','-B',str(T/'HardRootAudit.py'),y.name],check=True);print('PASS complete (3,148) canonical, exact terminal + complementary forest',*(hashlib.sha256(p.read_bytes()).hexdigest() for p in [x,y]));return 3,148
if __name__=='__main__':check()
