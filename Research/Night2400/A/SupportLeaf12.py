"""Exact support partition of one fixed-Euler leaf of (7,12)."""
from fractions import Fraction
from functools import cache
from math import gcd,prod
from pathlib import Path
import gzip,json,sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Verify import C,B,floor10

PREFIXES=(
    ((7,12),(16148168401,1),(110563,2),(226741,2)),
    ((7,12),(16148168401,2),(200741603328100897,1)),
)
U=(3,5,11,13,17,31)


def independent(s,roots,owners,head):
    """No Euler coupon remains. Rebuild all products and even exponent tails."""
    assert s.fixed_euler
    K=set(roots)
    needed=s.present-s.rows.keys()
    assert needed<=K
    ban=prod(s.bad)
    X=prod(q**f for q,f in s.rows.items())
    D=prod(((q**(f+1)-1)//(q-1))//(1+f%2) for q,f in s.rows.items())
    assert gcd(D,ban)==1
    for q in s.rows:
        while D%q==0:
            D//=q
    assert D==s.D
    pool=X*D*prod(needed)*prod(q for q,p in owners)
    kids={q:[] for q in K|dict(owners).keys()}
    for q,p in owners:
        kids[p].append(q)
    def vp(n,p):
        v=0
        while n%p==0:
            n//=p
            v+=1
        return v
    @cache
    def node(q,h):
        best=B+1;f=h+h%2;count=0
        while count<head and q**f<best:
            T=(q**(f+1)-1)//(q-1)
            if gcd(T,ban)==1:
                count+=1;u=T
                while (g:=gcd(u,pool))>1:
                    u//=g
                n=q**f*u*prod(node(p,vp(T,p)) for p in kids[q] if T%p==0)
                best=min(best,n)
            f+=2
        return min(best,q**f)
    vals=[vp(D,q) for q in roots]
    base=X*(D//prod(q**v for q,v in zip(roots,vals)))
    return base*prod(node(q,max(1,v)) for q,v in zip(roots,vals))


def verify(path):
    assert __debug__
    d=json.loads(gzip.decompress(path.read_bytes()))
    assert set(d)=={'prefix','masks','ecpp'}
    P=tuple(map(tuple,d['prefix']));assert P in PREFIXES
    assert C.ORDER[:C.ORDER.index(7)]==(19,)
    assert set(U).isdisjoint(dict(P))
    assert C.sigma(7,12)==P[1][0]
    assert all(C.sigma(*left)%right[0]==0 for left,right in zip(P,P[1:]))
    assert sum(f%2 for q,f in P)==1
    seen=set()
    @cache
    def prime(q):
        assert type(q)==int and q>2
        z=q
        if q>=2**64:
            for row in d['ecpp'][str(q)]:
                assert row[0]==z
                z=C.pc.level(*row)
            seen.add(str(q))
        assert C.pc.prime64(z)
        return True
    assert all(prime(q) for q in [*dict(P),*U])
    A=prod(Fraction(C.sigma(q,f),q**f) for q,f in P)
    covered=set();direct=abundance=0
    for mask in range(1<<len(U)):
        present={q for i,q in enumerate(U) if mask>>i&1}
        s=C.State(P,present,tuple(q for q in U if q not in present))
        if s.conflict or s.base>B or A>2:
            direct+=1
            continue
        v=A
        for q in present:
            h=max(1,C.valuation(s.D,q)); f=h+h%2
            while q**f<=B and not s.possible(q,f,h):
                f+=2
            assert q**f<=B
            v*=Fraction(C.sigma(q,f),q**f)
        if v>2:
            abundance+=1
            continue
        key=str(mask);t=d['masks'][key]
        assert set(t)=={'type','roots','owners','head'} and t['type']=='forest'
        roots,owners,head=t['roots'],t['owners'],t['head']
        assert present<=set(roots)
        C.validate_forest(s,roots,owners,head,prime)
        n=min(C.Forest(s,roots,owners,head).lower()[0],independent(s,roots,owners,head))
        assert n>B
        covered.add(key)
        print('PASS SUPPORT',mask,floor10(n),flush=True)
    assert covered==set(d['masks']) and seen==set(d['ecpp'])
    assert direct==32 and abundance==23 and len(covered)==9
    print('SUPPORT LEAF',P,'direct',direct,'abundance',abundance,'forests',len(covered),'ECPP',len(seen),flush=True)
    return P

if __name__=='__main__':
    verify(Path(sys.argv[1]) if len(sys.argv)>1 else H/'SupportLeaf12.json.gz')
