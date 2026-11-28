"""Independent exact Q-square cutoff at (19,222), first1 second42."""
import gzip,json,sys
from hashlib import sha256
from math import lcm,prod
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Forest import PR
from Check31Domains import B,state,split
from CheckSevenForestDomains import sig
T=7579985624053; R=3705121363; P=((19,222),(T,1),(R,42))

def main():
    assert __debug__
    p=H.parent/'Nineteen/Root222F1G42.json';raw=p.read_bytes()
    assert sha256(raw).hexdigest()=='4e16d8317bdc6aa27638ca32db16844eca70ce4526cb355519bae85228bb83bc'
    d=json.loads(raw); assert tuple(map(tuple,d['prefix']))==P and T%4==1
    q=d['pivot'];m=q
    steps=d['ecpp'];assert q>10**381 and len(steps)==50
    for a in steps:assert a[0]==m;m=PR['level'](*a)
    assert all(PR['prime64'](p) for p in (m,19,T,R))
    assert sig(R,42)%q==0
    r,tail=split(P,q,());assert not r and tail==4
    x,y,b=state(P+((q,2),),()); assert lcm(x,y)>B
    print('PASS independent commitment, 50 ECPP levels and exact sole legal raw even head, size tail 4')

if __name__=='__main__':main()
