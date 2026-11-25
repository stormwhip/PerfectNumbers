"""Canonical 3/112 joint proof, using the exact two terminal anchor exponents."""
import gzip,json,sys,subprocess,hashlib
from pathlib import Path
H=Path(__file__).resolve().parent;T=H.parent/'MiddayTerminal';q=526256453012063980796131127321354599535039

def check():
 if not __debug__:raise RuntimeError('no -O')
 x=H/'Complement112.json.gz';y=T/'Leaves112x12x16.json.gz';a=json.loads(gzip.decompress(x.read_bytes()));b=json.loads(gzip.decompress(y.read_bytes()));assert (a['e'],a['pivot'],a['tail'],sorted(a['omitted']))==(112,q,23,[12,16]);assert (b['p'],b['e'])==(3,112) and sorted(l['x'] for l in b['leaves'])==[[[q,12]],[[q,16]]]
 subprocess.run([sys.executable,'-I','-S','-B',str(H/'Complement.py'),str(x)],check=True);subprocess.run([sys.executable,'-I','-S','-B',str(T/'RootSlices.py'),y.name],check=True);print('PASS complete (3,112) canonical',*(hashlib.sha256(z.read_bytes()).hexdigest() for z in (x,y)));return 3,112
if __name__=='__main__':check()
