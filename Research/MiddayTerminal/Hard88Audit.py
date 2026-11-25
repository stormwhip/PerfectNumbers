"""Independent cold check of the two exact v_Q=30,36 root-three-88 leaves.
The remaining legal exponents at Q need their separate complement packet.
"""
from pathlib import Path
import sys,gzip,json,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Audit import replay,W,logs,split,primeproduct,chunks;import Common

def check(fn):
 raw=(H/fn).read_bytes();d=json.loads(gzip.decompress(raw));p,e=d['p'],d['e'];Q=5042939439565996049162197;assert (p,e)==(3,88) and ((3**89-1)//2)%Q==0;V=d['base'];cs=d['ecpp'];es=[];wanted={q for q in V if q>=2**64}
 for leaf in d['leaves']:wanted|={q for q,c in leaf['extend'] if q>=2**64 and q not in Common.bank()}
 assert set(map(int,cs))==wanted;Common.chain.cache_clear();Common.dataset=lambda:{'rows':{'3:88':V},'ecpp':cs};assert Common.chain(Q)
 for l in d['leaves']:
  assert (l['root'],l['e'],l['lower'])==(3,88,[]) and set(l['extra'])<=set(Common.ORDER[:Common.ORDER.index(3)]) and len(l['x'])==1 and l['x'][0][0]==Q;f=l['x'][0][1];assert f in (30,36) and f not in es;es.append(f);u,*_=replay(**l);unit=W*logs(10)[1];assert u>2400*unit;print('Q exponent',f,u//unit,flush=True);split.cache_clear();primeproduct.cache_clear();chunks.cache_clear()
 assert sorted(es)==[30,36];print(fn,hashlib.sha256(raw).hexdigest(),'ECPP',len(cs),'exact canonical 3/88 given Q exponent 30 or 36 only',flush=True)
if __name__=='__main__':
 if not __debug__:raise SystemExit('Do not use -O')
 for n in sys.argv[1:]:check(n)
