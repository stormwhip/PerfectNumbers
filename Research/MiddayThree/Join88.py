"""Combine the two exact low-root terminal leaves with their strict complement."""
import gzip,json,sys,subprocess,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;T=H.parent/'MiddayTerminal';q=5042939439565996049162197

def check():
 if not __debug__:raise RuntimeError('no -O')
 x=H/'Complement88.json.gz';y=T/'Leaves88x30x36.json.gz';a=json.loads(gzip.decompress(x.read_bytes()));b=json.loads(gzip.decompress(y.read_bytes()));assert (a['e'],a['pivot'],a['tail'],sorted(a['omitted']))==(88,q,41,[30,36]);assert (b['p'],b['e'])==(3,88) and sorted(l['x'] for l in b['leaves'])==[[[q,30]],[[q,36]]]
 subprocess.run([sys.executable,'-I','-S','-B',str(H/'Complement.py'),str(x)],check=True);subprocess.run([sys.executable,'-I','-S','-B',str(T/'Hard88Audit.py'),y.name],check=True);print('PASS complete (3,88) canonical',*(hashlib.sha256(z.read_bytes()).hexdigest() for z in (x,y)));return 3,88
if __name__=='__main__':check()
