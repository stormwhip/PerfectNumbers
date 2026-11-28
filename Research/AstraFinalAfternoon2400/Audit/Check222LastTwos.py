"""Independent two-terminal audit at (19,222), first 2, second 22."""
from fractions import Fraction
from functools import cache
import gzip,json,sys
from hashlib import sha256
from pathlib import Path
from math import prod,lcm
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Check31Domains import state,split,vp,B
from Check31Forest import PR,forest
from CheckSevenForestDomains import sig
T=7579985624053;R=3705121363;Q=2032322226061
P=((19,222),(T,2),(R,22)); home=H.parent/'Nineteen'


def run():
    assert __debug__
    live,tail=split(P,Q,()); assert tail==114
    hist=json.loads(gzip.decompress((home.parents[1]/'FinalNight2400/Root222/ThirdForests.json.gz').read_bytes()))['cases']['2:22']
    assert hist['q']==Q and live.keys()=={int(k) for k in hist['children']}|set(hist['left'])
    assert set(hist['left'])=={1,2,4,18,28}
    for name,j,bans,count,digest in [
        ('Plain222J2.json.gz',2,(),111,'e23cd70133042e8b236f6989f74c9f1c7447a09957a264045a01e7bad76e3785'),
        ('Mask222J4.json.gz',4,(7,11),21,'02c74f80b8112d0e4a9b3fdb1f36b118e3f3d7ed450837a194f1f3517fdc7b27')]:
        raw=(home/name).read_bytes();assert sha256(raw).hexdigest()==digest
        d=json.loads(gzip.decompress(raw));rows=tuple(map(tuple,d['prefix']));assert rows==live[j]
        K,E,H0=d['forest'];vertices=set(K)|{q for q,_ in E};used=set()
        @cache
        def prime(q):
            if q>=2**64:
                k=str(q); used.add(k)
                for row in d['ecpp'][k]:assert row[0]==q;q=PR['level'](*row)
            assert PR['prime64'](q)
        for label in vertices|dict(rows).keys()|set(bans):prime(label)
        assert len(used)==count and used==d['ecpp'].keys()
        if bans:
            x,y,ok=state(rows,());assert ok
            D=lcm(x,y)//x;assert len(K)==len(set(K)) and all(D%v==0 for v in K)
            assert set(bans).isdisjoint(K) and set(bans).isdisjoint(dict(rows))
            # Abundance increasing with exponent separately. Ignore global
            # Euler uniqueness for the lower bound (relaxes only).
            alpha=prod(Fraction(sig(p,h),p**h) for p,h in rows)
            for p in K:
                a=vp(D,p);h=a if p%4==1 or a%2==0 else a+1
                alpha*=Fraction(sig(p,h),p**h)
            for p in bans:assert alpha*Fraction(sig(p,2),p**2)>2
        val=forest(rows,dict(roots=K,owners=E,head=H0),bans);assert val>B
        print('PASS independent exact domain, local bans',bans,'and forest at third',j,'ECPP',count,flush=True)

if __name__=='__main__':run()
