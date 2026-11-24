"""Fail-closed verification of the frozen 19-pair result. No discovery data, earlier counts, or current working directory dependencies. Python >=3.10; run without -O."""
import sys,json,gzip,hashlib,time
from pathlib import Path
import replay as R
EXPECTED={7:(1048,1050,1060,1062,1068,1090,1092,1102),11:(730,760),19:(708,718,726,732),31:(576,586,590,606,612)}
D=Path(__file__).resolve().parent
if __name__=='__main__':
 if not __debug__:raise RuntimeError('cannot run with assertions disabled')
 sys.setrecursionlimit(30000);t=time.time();inputrows=json.loads((D/'input.json').read_bytes());data={(a['p'],a['e']):a for a in inputrows};assert len(data)==len(inputrows)
 p11=json.loads((D/'leaf-packet.json').read_bytes());p31=json.loads(gzip.decompress((D/'root31-576.json.gz').read_bytes()));assert len(p11)==28 and len(p31)==296 and not (p11.keys()&p31.keys());R.pack={**p11,**p31};used=set();levels=0;total=0
 for p,exps in EXPECTED.items():
  for e in exps:
   R.checked.clear();row=R.run(data[p,e],0);assert not row['outside'] and not row['inside'],(p,e,'OPEN',row['outside'][:1],row['first']);assert sum(row['counts'].values())==e+1
   assert R.checked==(set(p11) if (p,e)==(11,760) else set(p31) if (p,e)==(31,576) else set()),(p,e,'incomplete/unexpected lattice coverage');used.update(R.checked);levels+=e+1;total+=1;R.cand.cache_clear();R.root.cache_clear();print(p,e,'PASS',e+1,len(R.checked),flush=True)
 assert total==19 and used==set(R.pack);print('VERIFIED',total,'complete exponents;',levels,'s levels;',len(used),'checked polynomial leaves;',round(time.time()-t,1),'seconds')
