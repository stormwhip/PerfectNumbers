"""No projection: require all 31 compatible firsts at canonical exact 7^36 exactly once."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;N=H.parents[1]/'Night2400';sys.path.insert(0,str(N));from VerifyFibers import verify
if __name__=='__main__':
 assert __debug__
 names=[N/'Fibers7x36.json.gz',N/'E8/Fibers7x36ComplementFour.json.gz',H/'Seven36Two.json.gz',H/'Seven36Twelve.json.gz',H/'Seven36Sixteen.json.gz']
 vs=[verify(n) for n in names];dom=set(vs[0]['domain'])
 assert all(v['domain']==vs[0]['domain'] and v['key']==[7,36] and v['pivot']=='4805345109492315767981401' for v in vs)
 sets=[set(v['covered']) for v in vs];assert [len(x) for x in sets]==[24,4,1,1,1] and sets[1:]==[{1,4,6,18},{2},{12},{16}] and sum(map(len,sets))==len(set.union(*sets))==len(dom)==31 and set.union(*sets)==dom
 print('FULL canonical (7,36) all 31 firsts; singleton P7_I00011.',flush=True)
