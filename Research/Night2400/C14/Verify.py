"""Cold exact complete fibers of (19,312) with explicit support split."""
from fractions import Fraction
from functools import cache
import gzip,json
from hashlib import sha256
from math import prod
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;R=H.parents[1]
sys.path[:0]=[str(H),str(R/'Session20261126'),str(R/'Nov25/Compose')]
from PivotCheck import C,B,exact_leaf,floor10
from IndependentForest import replay
from PrefixPrice import excludes
KEY=(19,312); Q=1481866508237449
ORDER=(19,7,11,31,13,3,5,17)


def dead(s):return s.conflict or s.base>B or prod(C.sigma(q,f) for q,f in s.rows.items())>2*s.X


def split(p,q):
    s=C.State(p); assert not dead(s) and q not in s.rows and q not in s.bad and s.D%q==0
    h=C.valuation(s.D,q);a=s.base//q**h;k={};d=[];i=[];f=h
    while a*q**f<=B:
        if not s.possible(q,f,h):i.append(f)
        elif dead(C.State(p+[(q,f)])):d.append(f)
        else:k[str(f)]=p+[(q,f)]
        f+=1
    return k,d,i,f


def book_reader(book):
    used=set()
    @cache
    def prime(q):
        assert type(q) is int and q>2
        n=q
        if n>=2**64:
            used.add(str(q)); chain=book[str(q)];assert chain
            for row in chain:
                assert row[0]==n and n>=2**64
                n=C.pc.level(*row)
        assert C.pc.prime64(n);return True
    return prime,used


def support(p,masks,book,prime):
    assert set(masks)==set(map(str,range(1,256,2)))
    r=[0,0,0]; floors=[]
    for m in range(1,256,2):
        yes=tuple(q for i,q in enumerate(ORDER[1:],1) if m>>i&1); no=tuple(q for q in ORDER[1:] if q not in yes);s=C.State(p,yes,no);t=masks[str(m)]
        if t['type']=='direct':assert set(t)=={'type'} and dead(s);r[0]+=1;continue
        assert not dead(s);k=t['roots']
        if t['type']=='abundance':
            assert set(t)=={'type','roots'} and sorted(set(k))==k
            assert all(prime(q) and q not in s.rows and q not in s.bad and (q in yes or s.D%q==0) for q in k)
            def ratio(q,odd):
                e=max(1,C.valuation(s.D,q)); e+=(1-e)%4 if odd else e%2
                while not C.permitted(q,e,s.bad):e+=4 if odd else 2
                return Fraction(C.sigma(q,e),q**e)
            a={q:ratio(q,False) for q in k};v=Fraction(prod(C.sigma(q,e) for q,e in p),s.X)*prod(a.values())
            assert min([v,*[v/a[q]*ratio(q,True) for q in k if not s.fixed_euler and C.euler(q,s.bad)]])>2
            r[1]+=1;continue
        assert t['type']=='forest' and set(t)=={'type','roots','owners','head'};o,h=t['owners'],t['head']
        C.validate_forest(s,k,o,h,prime); x=C.Forest(s,k,o,h).lower()[0];assert x>B
        certs={str(z):book[str(z)] for z in {q for q,_ in p}|set(k)|set(dict(o)) if z>=2**64}
        y=replay(dict(assigned=p,present=yes,absent=no,leaf=dict(kind='forest',roots=k,owners=o,head=h),ecpp=certs))
        r[2]+=1;floors.append(min(floor10(x),y))
    print('SUPPORT EXACT',tuple(f for q,f in p),r,'minimum forest',min(floors,default=None),flush=True)


def packet(f):
    raw=(H/f'Fiber{f}.json.gz').read_bytes();d=json.loads(gzip.decompress(raw)); book=d['ecpp'];prime,used=book_reader(book)
    assert set(d)=={'p','e','pivot','cases','ecpp'} and (d['p'],d['e'],d['pivot'])==(*KEY,Q) and set(d['cases'])=={str(f)}
    assert __debug__ and C.ORDER==ORDER and Q.bit_length()==51 and all(prime(q) for q in (*ORDER,Q))
    dom,ds,il,tail=split([KEY],Q);assert (len(dom),len(ds),len(il),tail)==(40,40,26,107)
    stats=[0,0,0,0,0]; floors=[]
    def go(p,t):
        s=C.State(p);assert not dead(s)
        if t['type']=='split':
            assert set(t)=={'type','q','cases'} and prime(t['q']);a,b,_,_=split(p,t['q']);assert set(a)==set(t['cases'])
            stats[0]+=1;stats[1]+=len(b)
            for e,part in a.items():go(part,t['cases'][e])
        elif t['type']=='support':
            assert set(t)=={'type','masks'} and all(prime(q) for q,_ in p)
            support(p,t['masks'],book,prime);stats[4]+=1
        elif t['type']=='forest':
            assert set(t)=={'type','roots','owners','head'};k,o,h=(t[z] for z in ('roots','owners','head'))
            C.validate_forest(s,k,o,h,prime);a=C.Forest(s,k,o,h).lower()[0];b=exact_leaf(p,k,o,h);assert min(a,b)>B
            stats[2]+=1;floors.append(floor10(min(a,b)))
        else:
            assert t=={'type':'price','targets':[0,1]} and p==[KEY,(Q,36),(160883,30)]
            a=excludes(p,s.bad,[0,1]);assert a==(10,[7476,3792,0]);stats[3]+=1
            print('PRICE DEEP 36',a,flush=True)
    go(dom[str(f)],d['cases'][str(f)]);assert used==set(book)
    print('COMPLETE',f,'splits/direct/forests/price/support',stats,'forest min',min(floors,default=None),'SHA256',sha256(raw).hexdigest(),flush=True)

if __name__=='__main__':
    assert not sys.argv[1:]
    for f in (8,36):packet(f)
