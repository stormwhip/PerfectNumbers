"""Unconditional projection within its canonical root-13 class, no other support precondition."""
from pathlib import Path
import json,gzip,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Check import run, require

def verify(path=None):
 if not __debug__:raise ValueError('do not run with -O')
 d=json.loads(gzip.decompress((Path(path) if path else H/'Batch4_13x136d5.json.gz').read_bytes()));require((d['p'],d['e'])==(13,136));r=run(d,split_five=True);require(r['closed'] and not r['opened']);print('PASS local root',r['p'],r['e'],'forest terminals',r['terminals'],'exact splits',r['split'],'unresolved',len(r['opened']),flush=True);return {(13,136)}
if __name__=='__main__':verify(sys.argv[1] if len(sys.argv)>1 else None)
