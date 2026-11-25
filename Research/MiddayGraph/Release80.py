"""Exact 13^80 certificate. Binary supports are exhaustively included and excluded."""
from pathlib import Path
import sys,gzip,json
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Check import run,require

def verify(path=None):
 if not __debug__:raise ValueError('do not run with -O')
 d=json.loads(gzip.decompress((Path(path) if path else H/'EcmC13x80d3.json.gz').read_bytes()));require((d['p'],d['e'])==(13,80));r=run(d,support_plan=(37,43));require(r['closed'] and not r['opened']);print('PASS local root',r['p'],r['e'],'forest terminals',r['terminals'],'exact splits',r['split'],'unresolved',len(r['opened']),flush=True);return {(13,80)}
if __name__=='__main__':verify(sys.argv[1] if len(sys.argv)>1 else None)
