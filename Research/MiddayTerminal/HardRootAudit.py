"""Replay a single exact-root/anchor leaf independent of any other anchor exponents.
No global claim here: the other exponents must be covered separately.
"""
from pathlib import Path
import sys,gzip,json,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Audit import replay,W,logs;import Common

def check(fn):
 raw=(H/fn).read_bytes();d=json.loads(gzip.decompress(raw));p,e=d['p'],d['e'];Q=46509804063632583432467217805311362636553293639540930405531;assert (p,e)==(3,148);assert ((3**149-1)//2)%Q==0;assert len(d['leaves'])==1;row=d['leaves'][0];assert row['root']==p and row['e']==e and row['x']==[[Q,6]] and row['lower']==[] and set(row['extra'])<=set(Common.ORDER[:Common.ORDER.index(p)]);V=d['base'];proof=d['ecpp'];wanted={q for q in V if q>=2**64}|{q for q,c in row['extend'] if q>=2**64 and q not in Common.bank()};assert set(map(int,proof))==wanted
 Common.chain.cache_clear();Common.dataset=lambda:{'rows':{f'{p}:{e}':V},'ecpp':proof};assert Common.chain(Q);u,*_=replay(**row);unit=W*logs(10)[1];assert u>2400*unit;print(fn,hashlib.sha256(raw).hexdigest(),'ECPP',len(proof),'canonical 3/148 given anchor exponent 6 only',u//unit,flush=True)
if __name__=='__main__':
 if not __debug__:raise SystemExit('no -O')
 for name in sys.argv[1:]:check(name)
