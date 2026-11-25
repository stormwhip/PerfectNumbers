"""Extend ReleaseFive by one cold-replayed numerical premise. No discovery files."""
from pathlib import Path
import sys,subprocess,gzip,json,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Common
from Audit import replay,W,logs

def main():
 if not __debug__:raise SystemExit('Do not run with -O')
 args=sys.argv[1:];assert args in ([],['--baseline'],['--only-new'])
 if args!=['--only-new']:subprocess.run([sys.executable,'-I','-S','-B',str(H/'ReleaseFive.py'),*args],check=True)
 # Explicitly disallow any dependency on the research-only nomination store.
 def forbidden():raise ValueError('research input requested')
 Common.dataset=forbidden
 fn=H/'New-FourAdaptive.json.gz';raw=fn.read_bytes();d=json.loads(gzip.decompress(raw));assert (d['root'],d['e'],d['extra'],d['x'],d['lower'])==(0,0,[3,5,11,13],[],[[7,1],[17,1],[19,1],[23,1]])
 u,*_=replay(**d);unit=W*logs(10)[1];assert u>2400*unit and u//unit==2429
 print(fn.name,hashlib.sha256(raw).hexdigest(),u//unit,flush=True);print('Using the three five-prime theorems and {3,5,7}, absence of 3,5,11,13 forces 7,17,19,23: contradiction. PROVED: {3,5,11,13}. Complete canonical exponents/shards credited: 0/0.',flush=True)
if __name__=='__main__':main()
