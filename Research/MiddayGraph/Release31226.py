"""Complete exact 31^226 certificate. No auxiliary support condition."""
from pathlib import Path
import json,gzip,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Check import run,require

def verify(path=None):
 if not __debug__:raise ValueError('do not run with -O')
 d=json.loads(gzip.decompress((Path(path) if path else H/'Next31x226d2.json.gz').read_bytes()));require((d['p'],d['e'])==(31,226));r=run(d);require(r['closed'] and not r['opened']);print('PASS local root',r['p'],r['e'],'forest terminals',r['terminals'],'exact splits',r['split'],'unresolved',len(r['opened']),flush=True);return {(31,226)}
if __name__=='__main__':verify(sys.argv[1] if len(sys.argv)>1 else None)
