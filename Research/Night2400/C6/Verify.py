"""Cold exact first-fiber support proofs for (13,310), independent of C5."""
from fractions import Fraction
from functools import cache
import gzip
from hashlib import sha256
import json
from math import prod
from pathlib import Path
import sys

H = Path(__file__).resolve().parent
R = H.parents[1]
sys.path[:0] = [str(R/'Session20261126'), str(R/'Nov25/Compose'), str(R/'FinalSprint')]
from PivotCheck import C, B, floor10
from IndependentForest import replay
from JointValuation import excludes

KEY = (13, 310)
Q = 5424477432443
ORDER = (19, 7, 11, 31, 13, 3, 5, 17)
MASKS = tuple(16+32*i for i in range(8))
DOMAIN = [2,6,10,12,16,18,20,22,28,32,36,38,40,42,46,48,50,52,56,58,60,66]


def dead(s):
    return s.conflict or s.base>B or prod(C.sigma(z,h) for z,h in s.rows.items())>2*s.X


def domain():
    s=C.State([KEY]); assert not dead(s) and C.valuation(s.D,Q)==1
    scale=s.base//Q; f=1; live,direct,illegal=[],[],[]
    while scale*Q**f<=B:
        if not s.possible(Q,f,1): illegal.append(f)
        elif dead(C.State([KEY,(Q,f)])): direct.append(f)
        else: live.append(f)
        f+=1
    assert live==DOMAIN and len(direct)==23 and len(illegal)==90 and f==136
    return live,direct,illegal,f


def abundance(s,roots):
    def ratio(z,odd):
        h=max(1,C.valuation(s.D,z)); h+=(1-h)%4 if odd else h%2
        while not C.permitted(z,h,s.bad): h+=4 if odd else 2
        return Fraction(C.sigma(z,h),z**h)
    ev={q:ratio(q,False) for q in roots}; base=Fraction(s.S,s.X)*prod(ev.values())
    vals=[base,*[base/ev[q]*ratio(q,True) for q in roots if not s.fixed_euler and C.euler(q,s.bad)]]
    return min(vals)


def verify():
    assert __debug__ and C.ORDER==ORDER and Q.bit_length()==43
    raw=(H/'Support13x310.json.gz').read_bytes(); d=json.loads(gzip.decompress(raw))
    assert set(d)=={'p','e','pivot','cases','ecpp'} and (d['p'],d['e'])==KEY and d['pivot']==Q
    pairs=d['cases']; book=d['ecpp']; used=set()

    @cache
    def prime(q):
        assert type(q) is int and q>2
        n=q
        if n>=2**64:
            used.add(str(q)); rows=book[str(q)]; assert rows
            for a in rows:
                assert a[0]==n and n>=2**64
                n=C.pc.level(*a)
        assert C.pc.prime64(n)
        return True

    assert all(prime(q) for q in (*ORDER,Q))
    live,direct,illegal,tail=domain()
    print('DOMAIN',live,'DIRECT',direct,'INCOMPATIBLE',len(illegal),'TAIL >=',tail,flush=True)
    assert set(pairs)=={'6','10','12'}
    for f in (6,10,12):
        rows=pairs[str(f)]; p=[KEY,(Q,f)]
        assert set(rows)==set(map(str,MASKS)) and f in live
        for m in MASKS:
            yes=tuple(q for i,q in enumerate(ORDER[5:],5) if m>>i&1)
            no=tuple(q for q in ORDER[5:] if q not in yes)
            s=C.State(p,yes,no); t=rows[str(m)]
            if t['type']=='direct': assert set(t)=={'type'} and dead(s); receipt='direct'
            elif t['type']=='abundance':
                k=t['roots']; assert set(t)=={'type','roots'} and sorted(set(k))==k and not dead(s)
                assert all(prime(q) and q not in s.rows and q not in s.bad and (q in yes or s.D%q==0) for q in k)
                assert abundance(s,k)>2; receipt='abundance'
            else:
                assert t['type']=='forest' and set(t)=={'type','roots','owners','head'} and not dead(s)
                k,o,h=(t[a] for a in ('roots','owners','head'))
                C.validate_forest(s,k,o,h,prime)
                x=C.Forest(s,k,o,h).lower()[0]; assert x>B
                certs={str(q):book[str(q)] for q in set(k)|set(dict(o)) if q>=2**64}
                y=replay(dict(assigned=p,present=yes,absent=no,leaf=dict(kind='forest',roots=k,owners=o,head=h),ecpp=certs))
                receipt=min(floor10(x),y)
            print('PASS',f,'mask',m,receipt,flush=True)
    assert used==set(book)
    covered=set(map(int,pairs))
    print('COVERED',sorted(covered),'OPEN',sorted(set(live)-covered),'SHA256',sha256(raw).hexdigest(),flush=True)


if __name__=='__main__': verify()
