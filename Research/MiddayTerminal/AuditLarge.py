"""Cold verification of a minimal nomination dictionary, without any research data.
The extra field supplies only prime chains; Common.chain rechecks all ECPP links.
"""
from pathlib import Path
import sys,gzip,json,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Audit import replay,W,logs;import Common

def check(name):
 raw=(H/name).read_bytes();p=json.loads(gzip.decompress(raw));d=p['args'];assert d['root']==d['e']==0;Common.chain.cache_clear();Common.dataset=lambda:{'rows':{},'ecpp':p['ecpp']};want={str(q) for q,c in d['extend'] if q>=2**64 and q not in Common.bank()};assert set(p['ecpp'])==want
 u,*_=replay(**d);unit=W*logs(10)[1];assert u>2400*unit;print(name,hashlib.sha256(raw).hexdigest(),len(want),'ECPP',u//unit,'absent',d['extra'],'present',d['lower'],flush=True);return d,u//unit
if __name__=='__main__':
 if not __debug__:raise SystemExit('Do not run with -O')
 for fn in sys.argv[1:]:check(fn)
