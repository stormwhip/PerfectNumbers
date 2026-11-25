"""Independently reconstruct exact hard anchor slices with signed coverage only for
listed e,Q,f. All other local exponents require separately verified complements."""
from pathlib import Path
import sys,gzip,json,hashlib
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Audit import replay,W,logs,split,primeproduct,chunks;import Common
SPECS={96:(48845962828028421155731228333,[12]),112:(526256453012063980796131127321354599535039,[12,16])}

def check(file):
 raw=(H/file).read_bytes();d=json.loads(gzip.decompress(raw));p,e=d['p'],d['e'];assert p==3 and e in SPECS;Q,known=SPECS[e];assert ((3**(e+1)-1)//2)%Q==0;V=d['base'];proof=d['ecpp'];target={q for q in V if q>=2**64};got=[]
 for x in d['leaves']:target|={q for q,c in x['extend'] if q>=2**64 and q not in Common.bank()}
 assert set(map(int,proof))==target;Common.chain.cache_clear();Common.dataset=lambda:{'rows':{f'3:{e}':V},'ecpp':proof};assert Common.chain(Q)
 for x in d['leaves']:
  assert (x['root'],x['e'],x['lower'])==(p,e,[]) and len(x['x'])==1 and x['x'][0][0]==Q and set(x['extra'])<=set(Common.ORDER[:Common.ORDER.index(3)]);f=x['x'][0][1];assert f in known and f not in got;got.append(f);v,*_=replay(**x);unit=W*logs(10)[1];assert v>2400*unit;print(e,f,v//unit,flush=True);split.cache_clear();primeproduct.cache_clear();chunks.cache_clear()
 assert sorted(got)==known;print(file,hashlib.sha256(raw).hexdigest(),'conditional exact anchor exponents only',flush=True)
if __name__=='__main__':
 if not __debug__:raise SystemExit('Do not run with -O')
 for file in sys.argv[1:]:check(file)
