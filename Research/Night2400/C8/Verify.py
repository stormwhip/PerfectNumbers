"""Cold partial proof for (31,352); no other Night2400 directory is loaded."""
from fractions import Fraction
from functools import cache
import gzip,json
from hashlib import sha256
from math import prod
from pathlib import Path
import sys

H=Path(__file__).resolve().parent; R=H.parents[1]
sys.path[:0]=[str(H),str(R/'Session20261126'),str(R/'Nov25/Compose')]
from PivotCheck import C,B,exact_leaf,floor10
from IndependentForest import replay
from PrefixPrice import excludes

KEY=(31,352); Q=1797674429773
DOMAIN=[1,2,4,6,10,12,13,14,16,18,20,21,22,24,25,28,30,32,33,34,36,37,38,40,42,45,46,48,50,52,54]
SPLITS={4:([4,6,10,12,16,18],[22,24,28,30,34,36,40,42],43),6:([1,2,5,10,12],[16,18,21,22,25,28],29),10:([1,4],[6,9],12),30:([],[2],3),33:([2],[4],5),45:([6],[10,12],14),48:([1,2],[5],6),50:([],[],2),54:([],[1],2)}
PRICES={25:(24,[0,0,0]),37:(16,[0,0,0]),38:(15,[7816,5598,0]),40:(13,[9678,4442,0]),42:(12,[11480,3346,0]),46:(9,[14520,1718,0]),52:(6,[18087,269,0])}
ORDER=(19,7,11,31,13,3,5,17); MASKS=tuple(range(8,256,16))


def dead(s):return s.conflict or s.base>B or prod(C.sigma(q,f) for q,f in s.rows.items())>2*s.X


def split(parts,q):
    s=C.State(parts); assert not dead(s) and q not in s.rows and q not in s.bad and s.D%q==0
    h=C.valuation(s.D,q); scale=s.base//q**h; f=h; kids={}; direct=[]; invalid=[]
    while scale*q**f<=B:
        if not s.possible(q,f,h):invalid.append(f)
        elif dead(C.State(parts+[(q,f)])):direct.append(f)
        else:kids[str(f)]=parts+[(q,f)]
        f+=1
    return kids,direct,invalid,f


def abundance(s,roots):
    def ratio(q,odd):
        f=max(1,C.valuation(s.D,q)); f+=(1-f)%4 if odd else f%2
        while not C.permitted(q,f,s.bad): f+=4 if odd else 2
        return Fraction(C.sigma(q,f),q**f)
    terms={q:ratio(q,False) for q in roots}; base=Fraction(s.S,s.X)*prod(terms.values())
    return min([base,*[base/terms[q]*ratio(q,True) for q in roots if not s.fixed_euler and C.euler(q,s.bad)]])


def load(name):
    raw=(H/name).read_bytes(); d=json.loads(gzip.decompress(raw)); assert (d['p'],d['e'],d['pivot'])==(*KEY,Q)
    book=d['ecpp'];used=set()
    @cache
    def prime(q):
        assert type(q) is int and q>2
        x=q
        if x>=2**64:
            used.add(str(q)); chain=book[str(q)];assert chain
            for a in chain:
                assert a[0]==x and x>=2**64
                x=C.pc.level(*a)
        assert C.pc.prime64(x);return True
    return d,book,used,prime,sha256(raw).hexdigest()


def forest(p,t,prime,yes=(),no=(),book=None):
    k,o,h=(t[a] for a in ('roots','owners','head'));s=C.State(p,yes,no)
    assert set(t)=={'type','roots','owners','head'} and t['type']=='forest' and not dead(s)
    C.validate_forest(s,k,o,h,prime);x=C.Forest(s,k,o,h).lower()[0];assert x>B
    if book is None:
        y=exact_leaf(p,k,o,h);assert y>B;return floor10(min(x,y))
    needed={str(q):book[str(q)] for q in set(k)|set(dict(o)) if q>=2**64}
    y=replay(dict(assigned=p,present=yes,absent=no,leaf=dict(kind='forest',roots=k,owners=o,head=h),ecpp=needed))
    return min(floor10(x),y)


def support():
    d,book,used,prime,digest=load('Support2.json.gz');p=[KEY,(Q,2)]
    assert set(d)=={'p','e','pivot','f','cases','ecpp'} and d['f']==2
    assert set(d['cases'])==set(map(str,MASKS)) and all(prime(q) for q in (*ORDER,Q))
    counts=[0,0,0]; floors=[]
    for m in MASKS:
        yes=tuple(z for i,z in enumerate(ORDER[4:],4) if m>>i&1); no=tuple(z for z in ORDER[4:] if z not in yes)
        s=C.State(p,yes,no);t=d['cases'][str(m)]
        if t['type']=='direct':assert set(t)=={'type'} and dead(s);counts[0]+=1
        elif t['type']=='abundance':
            k=t['roots'];assert set(t)=={'type','roots'} and sorted(set(k))==k and not dead(s)
            assert all(prime(q) and q not in s.rows and q not in s.bad and (q in yes or s.D%q==0) for q in k)
            assert abundance(s,k)>2;counts[1]+=1
        else:floors.append(forest(p,t,prime,yes,no,book));counts[2]+=1
    assert used==set(book) and counts==[8,2,6]
    print('PASS 2 support',counts,'min forest floor',min(floors),'SHA256',digest,flush=True)


def verify():
    assert __debug__ and ORDER==C.ORDER and Q.bit_length()==41 and C.pc.prime64(KEY[0]) and C.pc.prime64(Q)
    domain,direct,invalid,tail=split([KEY],Q)
    assert list(map(int,domain))==DOMAIN and len(direct)==33 and len(invalid)==47 and tail==112
    print('DOMAIN',DOMAIN,'direct',direct,'incompatible',len(invalid),'tail >=',tail,flush=True)
    assert '2' in domain;support();covered={2}
    d,book,used,prime,digest=load('Fibers31x352.json.gz')
    assert set(d)=={'p','e','pivot','cases','ecpp'} and set(d['cases'])==set(map(str,SPLITS))
    for f,expected in sorted(SPLITS.items()):
        p=domain[str(f)];t=d['cases'][str(f)];assert t['type']=='split' and set(t)=={'type','q','cases'} and prime(t['q'])
        a,b,_,end=split(p,t['q']);assert (list(map(int,a)),b,end)==expected and set(a)==set(t['cases'])
        floors=[forest(pp,t['cases'][g],prime) for g,pp in a.items()]
        print('PASS',f,'split',expected,'min forest floor',min(floors,default=None),flush=True);covered.add(f)
    assert used==set(book);print('TREE SHA256',digest,flush=True)
    for f,expected in PRICES.items():
        p=domain[str(f)]; got=excludes(p,C.State(p).bad,[0,1]);assert got==expected
        print('PASS',f,'price',got,flush=True);covered.add(f)
    print('COVERED',sorted(covered),'OPEN',sorted(set(DOMAIN)-covered),flush=True)


if __name__=='__main__':verify()
