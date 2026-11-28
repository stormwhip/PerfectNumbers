"""Independent reconstruction and capacity-DP replay of final j=16 under (19,222), f1,g2."""
import gzip,json,sys
from hashlib import sha256
from pathlib import Path
H=Path(__file__).resolve().parent; sys.path.insert(0,str(H))
from Check31Domains import split,B
from Check31Forest import PR,forest
R=H.parent
T,U,Q=7579985624053,3705121363,3789992812027
P=((19,222),(T,1),(U,2))

def z(p):return json.loads(gzip.decompress(p.read_bytes()))

def main():
    assert __debug__
    name=R/'Nineteen/Root222F1G2.json.gz';t=name.read_bytes()
    assert sha256(t).hexdigest()=='4224ec34fe814bf643e791f9f709ce2cbcb1c0873b515caf8acef663ec9f15fb'
    p=json.loads(gzip.decompress(t));r=tuple(map(tuple,p['prefix'])); live,tail=split(P,Q,())
    assert tail==144 and r==live[16] and T%4==1
    old=z(R.parent/'FinalNight2400/Root222/ThirdForests.json.gz')['cases']['1:2']; assert old['q']==Q
    prev=set(old['left']); removed=set(map(int,old['children']))
    assert prev=={2,4,12,16,18,42} and prev|removed==live.keys() and not prev&removed
    for k in ('Forest222.json.gz','Forest222Stage2.json.gz','Forest222Stage3.json.gz'):
        more=set(z(R/'Nineteen'/k)['windows']['1:2']['closed']); assert more<=prev;prev-=more
    assert prev=={16}
    K,O,head=p['forest']; labels=set(K)|{q for q,_ in O}|dict(r).keys(); check=set()
    for q in labels:
        if q>=2**64:
            key=str(q); check.add(key)
            path=p['ecpp'][key]; assert path
            for step in path: assert step[0]==q;q=PR['level'](*step)
        assert PR['prime64'](q)
    assert len(check)==178 and check==p['ecpp'].keys()
    assert forest(r,dict(roots=K,owners=O,head=head),())>B
    print('PASS independent f1:g2 complete third-domain subtraction, last j16 strict ordinary forest, 178 ECPP')

if __name__=='__main__':main()
