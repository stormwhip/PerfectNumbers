"""Cold low-fiber proof of (11,12), without inherited verdicts."""
from collections import Counter
from fractions import Fraction
from functools import cache
import gzip
from hashlib import sha256
import json
from math import prod
from pathlib import Path
import sys

H=Path(__file__).resolve().parent; R=H.parents[1]
sys.path[:0]=[str(H),str(R/'Session20261126')]
from PivotCheck import C,B,floor10
from IndependentRoot11 import replay

KEY=(11,12); Q=3158528101
ORDER=(19,7,11,31,13,3,5,17); MASKS=tuple(range(4,256,8))
HOLES=(36,44,52,60,100,164,172,180,188)
EXPECTED={1:({28,140,156},[0,0,3]),2:(set(MASKS)-set(HOLES),[16,7,0]),4:(set(MASKS),[24,4,4]),5:(set(MASKS),[16,0,16]),8:(set(MASKS)-set(HOLES),[16,7,0])}


def dead(s):return s.conflict or s.base>B or prod(C.sigma(q,f) for q,f in s.rows.items())>2*s.X


def domain():
    s=C.State([KEY]); assert not dead(s) and C.valuation(s.D,Q)==1
    f=1; scale=s.base//Q; live=[]; direct=[]; invalid=[]
    while scale*Q**f<=B:
        if not s.possible(Q,f,1):invalid.append(f)
        elif dead(C.State([KEY,(Q,f)])):direct.append(f)
        else:live.append(f)
        f+=1
    assert (len(live),len(direct),len(invalid),f)==(77,78,96,252)
    return live


def abundance(s,roots):
    """Minimum among permitted listed Euler placements, or no listed one."""
    def ratio(q,odd):
        f=max(1,C.valuation(s.D,q)); f+=(1-f)%4 if odd else f%2
        while not C.permitted(q,f,s.bad): f+=4 if odd else 2
        return Fraction(C.sigma(q,f),q**f)
    terms={q:ratio(q,False) for q in roots}; base=Fraction(s.S,s.X)*prod(terms.values())
    return min([base,*[base/terms[q]*ratio(q,True) for q in roots if not s.fixed_euler and C.euler(q,s.bad)]])


def verify():
    assert __debug__ and ORDER==C.ORDER and Q.bit_length()==32
    assert C.sigma(*KEY)==1093*Q and C.State([KEY]).bad==(19,7)
    src=(H/'Support11x12.json.gz').read_bytes(); d=json.loads(gzip.decompress(src))
    assert set(d)=={'p','e','pivot','cases','ecpp'} and (d['p'],d['e'],d['pivot'])==(*KEY,Q)
    book=d['ecpp']; used=set()
    @cache
    def prime(q):
        assert type(q) is int and q>2
        x=q
        if x>=2**64:
            used.add(str(q)); chain=book[str(q)]; assert chain
            for a in chain:
                assert a[0]==x and x>=2**64
                x=C.pc.level(*a)
        assert C.pc.prime64(x); return True
    assert all(prime(q) for q in (*ORDER,1093,Q)); live=domain()
    print('DOMAIN 77; direct 78; incompatible 96; tail >=252',flush=True)
    assert set(d['cases'])==set(map(str,EXPECTED)) and set(EXPECTED)<=set(live)
    for f,(masks,expected) in sorted(EXPECTED.items()):
        p=[KEY,(Q,f)]; rows=d['cases'][str(f)]; counts=[0,0,0]; floors=[]
        assert set(rows)==set(map(str,masks))
        for m in sorted(masks):
            yes=tuple(q for i,q in enumerate(ORDER[3:],3) if m>>i&1); no=tuple(q for q in ORDER[3:] if q not in yes)
            s=C.State(p,yes,no); t=rows[str(m)]
            if t['type']=='direct': assert set(t)=={'type'} and dead(s); counts[0]+=1
            elif t['type']=='abundance':
                k=t['roots']; assert set(t)=={'type','roots'} and sorted(set(k))==k and not dead(s)
                assert all(prime(q) and q not in s.rows and q not in s.bad and (q in yes or s.D%q==0) for q in k)
                assert abundance(s,k)>2; counts[1]+=1
            else:
                assert t['type']=='forest' and set(t)=={'type','roots','owners','head'} and not dead(s)
                k,o,h=(t[z] for z in ('roots','owners','head')); C.validate_forest(s,k,o,h,prime)
                a=C.Forest(s,k,o,h).lower()[0]; assert a>B
                ec={str(q):book[str(q)] for q in set(k)|set(dict(o)) if q>=2**64}
                b=replay(dict(assigned=p,present=yes,absent=no,leaf=dict(kind='forest',roots=k,owners=o,head=h),ecpp=ec))
                floors.append(min(floor10(a),b)); counts[2]+=1
        assert counts==expected
        print('PASS',f,'masks',len(masks),'direct/abundance/forest',counts,'min forest floor',min(floors,default=None),'mask gaps',sorted(set(MASKS)-masks),flush=True)
    assert used==set(book)
    print('FULL FIBERS', [4,5], 'SHA256',sha256(src).hexdigest(),flush=True)

if __name__=='__main__':verify()
