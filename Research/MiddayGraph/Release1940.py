"""Full canonical 19^40 certificate: final cells split by 13 and 31 support."""
from pathlib import Path
import sys,gzip,json
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Check import run,require

def verify(path=None):
 if not __debug__:raise ValueError('do not run with -O')
 d=json.loads(gzip.decompress((Path(path) if path else H/'Next19x40d2.json.gz').read_bytes()));require((d['p'],d['e'])==(19,40));r=run(d,support_plan=(13,31));require(r['closed'] and not r['opened']);print('PASS local root',r['p'],r['e'],'forest terminals',r['terminals'],'exact splits',r['split'],'unresolved',len(r['opened']),flush=True);return {(19,40)}
if __name__=='__main__':verify(sys.argv[1] if len(sys.argv)>1 else None)
