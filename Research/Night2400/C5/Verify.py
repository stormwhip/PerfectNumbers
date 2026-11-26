"""Cold proof for the separately covered exact fibers of (13,372)."""
import gzip
import json
from functools import cache
from fractions import Fraction
from math import prod
from pathlib import Path
import sys

H = Path(__file__).resolve().parent
R = H.parents[1]
sys.path[:0] = [str(R/'Session20261126'),str(R/'Nov25/Compose')]
from PivotCheck import C, B, exact_leaf, floor10
from IndependentForest import replay

KEY = (13,372)
Q = 438552673580231875649
MASKS = tuple(16 + 32*i for i in range(8))


def dead(s):
    return s.conflict or s.base>B or prod(C.sigma(z,f) for z,f in s.rows.items())>2*s.X


def partitions(P,q,yes=(),no=()):
    s=C.State(P,yes,no)
    assert not dead(s) and q not in s.rows and q not in s.bad and s.D%q==0
    h=C.valuation(s.D,q); scale=s.base//q**h; f=h
    live={}; direct=[]; illegal=[]
    while scale*q**f<=B:
        if not s.possible(q,f,h):illegal.append(f)
        elif dead(C.State(P+[(q,f)],yes,no)):direct.append(f)
        else:live[str(f)]=P+[(q,f)]
        f+=1
    return live,direct,illegal,f


def abundance(s,roots):
    def ratio(z,odd):
        h=max(1,C.valuation(s.D,z));h+=(1-h)%4 if odd else h%2
        while not C.permitted(z,h,s.bad):h+=4 if odd else 2
        return Fraction(C.sigma(z,h),z**h)
    even={z:ratio(z,False) for z in roots};base=Fraction(s.S,s.X)*prod(even.values())
    return min([base,*[base/even[z]*ratio(z,True) for z in roots if not s.fixed_euler and C.euler(z,s.bad)]])


def book_reader(book):
    used=set()
    @cache
    def prime(q):
        assert type(q) is int and q>2
        n=q
        if n>=2**64:
            used.add(str(q)); chain=book[str(q)]; assert chain
            for row in chain:
                assert row[0]==n and n>=2**64
                n=C.pc.level(*row)
        assert C.pc.prime64(n)
        return True
    return prime,used


def forest(P,node,prime,yes=(),no=(),book=None):
    s=C.State(P,yes,no)
    assert not dead(s) and set(node)=={'type','roots','owners','head'} and node['type']=='forest'
    roots,owners,head=(node[n] for n in ('roots','owners','head'))
    C.validate_forest(s,roots,owners,head,prime)
    a=C.Forest(s,roots,owners,head).lower()[0]
    assert a>B
    if not yes and not no:
        b=exact_leaf(P,roots,owners,head); assert b>B
        return min(floor10(a),floor10(b))
    labels={z for z,_ in P}|set(roots)|set(dict(owners))|set(yes)|set(s.bad)
    b=replay(dict(assigned=P,present=yes,absent=no,leaf=dict(kind='forest',roots=roots,owners=owners,head=head),ecpp={str(z):book[str(z)] for z in labels if z>=2**64}))
    return min(floor10(a),b)


def tree(path, expected):
    d=json.loads(gzip.decompress(path.read_bytes()))
    assert set(d)=={'p','e','pivot','ecpp','cases'} and (d['p'],d['e'])==KEY and d['pivot']==Q
    prime,used=book_reader(d['ecpp']); assert prime(KEY[0]) and Q.bit_length()==69 and prime(Q)
    domain,direct,illegal,tail=partitions([KEY],Q)
    assert len(domain)==25 and tail==78
    print('DOMAIN',list(map(int,domain)),'DIRECT',direct,'INCOMPATIBLE',illegal,'TAIL >=',tail,flush=True)
    assert set(d['cases'])==set(expected)
    def go(P,node):
        if node['type']=='forest':return (1,0,0,forest(P,node,prime))
        assert node['type']=='split' and set(node)=={'type','q','cases'} and prime(node['q'])
        child,dead0,_,_=partitions(P,node['q']); assert set(child)==set(node['cases'])
        res=[go(RR,node['cases'][f]) for f,RR in child.items()]
        return sum(x[0] for x in res),1+sum(x[1] for x in res),len(dead0)+sum(x[2] for x in res),min(x[3] for x in res)
    covered=set()
    for f in expected:
        print('PASS first',f,'forests/splits/direct/min-floor',go(domain[f],d['cases'][f]),flush=True)
        covered.add(f)
    assert used==set(d['ecpp'])
    return set(domain),covered


def support(path,f,masks):
    d=json.loads(gzip.decompress(path.read_bytes())); assert set(d)=={'pivot','cases','ecpp','f'} and d['pivot']==Q and d['f']==f
    prime,used=book_reader(d['ecpp']);P=[KEY,(Q,f)];assert all(prime(q) for q in [Q,*C.ORDER]); assert set(d['cases'])==set(map(str,masks))
    for mask in masks:
        yes=tuple(q for i,q in enumerate(C.ORDER[5:],5) if mask>>i&1); no=tuple(q for q in C.ORDER[5:] if q not in yes)
        s=C.State(P,yes,no);node=d['cases'][str(mask)]
        if node['type']=='direct':assert set(node)=={'type'} and dead(s); lb='direct'
        elif node['type']=='abundance':
            roots=node['roots'];assert set(node)=={'type','roots'} and not dead(s) and sorted(set(roots))==roots
            assert all(prime(q) and q not in s.rows and q not in s.bad and (q in yes or s.D%q==0) for q in roots)
            assert abundance(s,roots)>2;lb='abundance'
        else:lb=forest(P,node,prime,yes,no,d['ecpp'])
        print('PASS',f,'mask',mask,lb,flush=True)
    assert used==set(d['ecpp'])


def verify_all():
    assert __debug__
    domain,covered=tree(H/'Fibers13x372.json.gz',('1','4','6'))
    domain8,covered8=tree(H/'Fiber8.json.gz',('8',)); assert domain8==domain
    covered |= covered8
    assert '16' in domain and '2' in domain
    support(H/'Support16.json.gz',16,MASKS);covered.add('16')
    partial=(16,80,144,208,240)
    support(H/'Support2.json.gz',2,partial)
    print('PARTIAL 2:',list(partial),'OPEN MASKS:',sorted(set(MASKS)-set(partial)),flush=True)
    print('COVERED',sorted(map(int,covered)),'OUTSIDE THIS PACKET',sorted(map(int,domain-covered)),flush=True)
    return set(map(int,domain)),set(map(int,covered)),set(partial)


if __name__=='__main__':
    verify_all()
