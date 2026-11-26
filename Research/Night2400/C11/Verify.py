"""Cold complete pivot-4 fiber of (19,46), independent of other packets."""
from fractions import Fraction
from functools import cache
import gzip,json
from hashlib import sha256
from math import prod
from pathlib import Path
import sys

H=Path(__file__).resolve().parent; R=H.parents[1]
sys.path[:0]=[str(H),str(R/'Session20261126')]
from PivotCheck import C,B,exact_leaf,floor10
from PrefixPrice import excludes

KEY=(19,46); Q=70169234660105574400577005075855017842743056666917902427141
ORDER=(19,7,11,31,13,3,5,17)
DOMAIN=['1','2','4','5','6','8','9','10','12','13','14','16','17','18']


def dead(s):return s.conflict or s.base>B or prod(C.sigma(q,f) for q,f in s.rows.items())>2*s.X


def split(p,q):
    s=C.State(p);assert not dead(s) and q not in s.rows and q not in s.bad and s.D%q==0
    h=C.valuation(s.D,q); x=s.base//q**h; f=h; k={}; direct=[]; illegal=[]
    while x*q**f<=B:
        if not s.possible(q,f,h):illegal.append(f)
        elif dead(C.State(p+[(q,f)])):direct.append(f)
        else:k[str(f)]=p+[(q,f)]
        f+=1
    return k,direct,illegal,f


def abund(s,k):
    def ratio(q,odd):
        f=max(1,C.valuation(s.D,q)); f+=(1-f)%4 if odd else f%2
        while not C.permitted(q,f,s.bad):f+=4 if odd else 2
        return Fraction(C.sigma(q,f),q**f)
    a={q:ratio(q,False) for q in k}
    v=Fraction(prod(C.sigma(q,f) for q,f in s.rows.items()),s.X)*prod(a.values())
    return min([v,*[v/a[q]*ratio(q,True) for q in k if not s.fixed_euler and C.euler(q,s.bad)]])


def prime_book(book):
    used=set()
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
    return prime,used


def check_support(p,rows,prime):
    assert set(rows)==set(map(str,range(1,256,2)))
    counts=[0,0]; min_ab=None
    for m in range(1,256,2):
        yes=tuple(q for j,q in enumerate(ORDER[1:],1) if m>>j&1); no=tuple(q for q in ORDER[1:] if q not in yes)
        s=C.State(p,yes,no); r=rows[str(m)]
        if r['type']=='direct': assert set(r)=={'type'} and dead(s);counts[0]+=1;continue
        assert r['type']=='abundance' and set(r)=={'type','roots'} and not dead(s)
        k=r['roots']; assert sorted(set(k))==k and all(q not in s.rows and q not in s.bad and prime(q) and (q in yes or s.D%q==0) for q in k)
        val=abund(s,k); assert val>2;counts[1]+=1;min_ab=val if min_ab is None else min(min_ab,val)
    return counts,None if min_ab is None else (min_ab.numerator*10**9)//min_ab.denominator


def verify():
    assert __debug__ and C.ORDER==ORDER and Q.bit_length()==196
    raw=(H/'Fiber4.json.gz').read_bytes();d=json.loads(gzip.decompress(raw));book=d['ecpp'];prime,used=prime_book(book)
    assert set(d)=={'p','e','pivot','f','tree','support','ecpp'} and (d['p'],d['e'],d['pivot'],d['f'])==(*KEY,Q,4)
    assert all(prime(q) for q in (*ORDER,Q)); pre,direct,illegal,tail=split([KEY],Q)
    assert (list(pre),len(direct),len(illegal),tail)==(DOMAIN,15,10,40)
    print('FIRST LIVE',list(pre),'direct',direct,'incompatible',illegal,'tail',tail,flush=True)
    covered_support=set(); stats=[0,0,0];floors=[]
    def walk(p,t):
        s=C.State(p);assert not dead(s)
        if t['type']=='split':
            assert set(t)=={'type','q','cases'} and prime(t['q']); k,a,_,_=split(p,t['q']); assert set(k)==set(t['cases'])
            stats[0]+=1;stats[1]+=len(a)
            for f,ks in k.items():walk(ks,t['cases'][f])
        elif t['type']=='forest':
            assert set(t)=={'type','roots','owners','head'};k,o,h=(t[x] for x in ('roots','owners','head'))
            C.validate_forest(s,k,o,h,prime);a=C.Forest(s,k,o,h).lower()[0];b=exact_leaf(p,k,o,h);assert min(a,b)>B
            stats[2]+=1;floors.append(floor10(min(a,b)))
        else:
            assert t['type']=='support' and set(t)=={'type','id'} and t['id'] not in covered_support
            assert all(prime(q) for q,_ in p)
            counts,min_ab=check_support(p,d['support'][t['id']],prime);assert counts==[124,4]
            print('PASS support',p,counts,'minimum abundancy ppb',min_ab,flush=True)
            covered_support.add(t['id'])
    walk(pre['4'],d['tree']);assert used==set(book) and covered_support==set(d['support'])=={'1','2'}
    assert stats[0]==4 and stats[2]==47
    print('FULL EXACT FIBER 4, splits/direct/forests',stats,'minimum floor',min(floors),'SHA256',sha256(raw).hexdigest(),flush=True)

def deep():
    assert __debug__ and C.ORDER==ORDER
    raw=(H/'DeepLeaves.json.gz').read_bytes();d=json.loads(gzip.decompress(raw));prime,used=prime_book(d['ecpp'])
    assert set(d)=={'p','e','pivot','paths','ecpp'} and (d['p'],d['e'],d['pivot'])==(*KEY,Q)
    assert all(prime(q) for q in (*ORDER,Q)); seen=set(); counts={6:[0,0],10:[0,0]}
    for key,r in d['paths'].items():
        p=list(map(tuple,r['parts'])); tag=tuple(f for q,f in p)
        assert key==','.join(map(str,tag)) and tag not in seen and p[0]==KEY and p[1][0]==Q and tag[1] in counts
        seen.add(tag); s=C.State(p); assert not dead(s) and all(prime(q) for q,_ in p)
        for j in range(1,len(p)):
            q,f=p[j]; live,*_=split(p[:j],q); assert live[str(f)]==p[:j+1]
        if r['type']=='support':
            assert set(r)=={'parts','type','masks'}; ct,ppm=check_support(p,r['masks'],prime); assert sum(ct)==128
            counts[tag[1]][0]+=1; receipt=(ct,ppm)
        else:
            assert r['type']=='price' and set(r)=={'parts','type','targets','receipt'}
            v=excludes(p,s.bad,r['targets']);assert list(v)==r['receipt'];counts[tag[1]][1]+=1;receipt=v
        print('PASS conditional path',tag,receipt,flush=True)
    assert used==set(d['ecpp']) and counts=={6:[6,8],10:[10,0]}
    print('CONDITIONAL deep leaf counts',counts,'SHA256',sha256(raw).hexdigest(),flush=True)


if __name__=='__main__':
    if sys.argv[1:]==['--deep']:deep()
    else:
        assert not sys.argv[1:]
        verify()
