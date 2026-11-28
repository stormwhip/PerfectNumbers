"""Independent, exact final residual branch and compact forest arithmetic for first t² of (7,48)."""
from fractions import Fraction
from functools import cache
from hashlib import sha256
from math import prod
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Check31Domains import B,geometric as G,split
from Check31Forest import PR,forest
from Check48StrongScopes import P,T,R
Q=116161286042101
PARENT=((P,48),(T,2),(R,12),(3,2))
BAD=(19,5,11,17,23)
EXPECT=(2,6,8,10,12,16,18,20,22,28,30,32,36,38,40,42,46,48,50,52,56,58,60,62,66,68,70)


def forced_factors():
    """Check the exact products for both compact fixed emissions."""
    a=(29,3529,4733,1074473,13473433)
    b=(61,1965401149,600424816906741)
    assert prod(a)*T==G(P,48) and prod(b)*R==G(T,2)
    return set(a+b)|{13,157,Q}


def main():
    assert __debug__
    f=H.parent/'Propagation/Reserved438x12-orbit48finalsq.json.gz'
    raw=f.read_bytes(); data=json.loads(gzip.decompress(raw)); ecpp=data['ecpp']; checked=set()
    @cache
    def prime(n):
        if n>=2**64:
            key=str(n); w=ecpp[key]; assert w
            checked.add(key)
            for row in w:
                assert row[0]==n; n=PR['level'](*row)
        assert PR['prime64'](n)
    assert all(PR['prime64'](p) for p in (P,T,R,Q,*BAD,3))
    compelled=forced_factors()
    fixed=dict(PARENT)
    Y=prod(G(p,h) for p,h in PARENT)
    for q in compelled:
        prime(q)
        assert Y%q==0 and q not in fixed
    def abund(rows):return prod(Fraction(G(p,h),p**h) for p,h in rows.items())
    def ceil(p):return 2 if p%4==3 else 1
    minimum={**fixed,**{p:ceil(p) for p in compelled}}
    for p in (17,23):
        assert p not in minimum and abund({**minimum,p:ceil(p)})>2
    live,tail=split(PARENT,Q,BAD)
    assert tuple(live)==EXPECT and tail==143
    took=set(); smallest=None; vertices=0
    for r in data['records']:
        row=tuple(map(tuple,r['P'])); h=row[-1][1]
        assert h not in took and row==live[h] and not r['unresolved']
        took.add(h)
        bans=tuple(r['bad']); leaf=r['tree']
        assert bans[:len(BAD)]==BAD and len(set(bans))==len(bans)
        fixed=dict(row); out=prod(G(p,e) for p,e in row)
        labels=(compelled|set(leaf['roots']))-fixed.keys()
        for p in labels:
            prime(p); assert out%p==0
        for p,_ in leaf['owners']:prime(p)
        lower={**fixed,**{p:ceil(p) for p in labels}}
        for p in bans[len(BAD):]:
            prime(p); assert p not in lower and abund({**lower,p:ceil(p)})>2
        bound=forest(row,leaf,bans)
        assert bound>B
        smallest=bound if smallest is None else min(smallest,bound)
        vertices+=len(leaf['roots'])+len(leaf['owners'])
    assert took==live.keys() and checked==ecpp.keys()
    print('PASS independent final t^2 residual','raw tail',tail,'children',len(took),
          'strict millionths',smallest*10**6//B,'vertices',vertices,'ECPP',len(checked),'sha256',sha256(raw).hexdigest(),flush=True)


if __name__=='__main__':main()
