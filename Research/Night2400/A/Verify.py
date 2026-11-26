"""Offline replay of partial first-pivot fibers, not necessarily of the root pair."""
from pathlib import Path
from functools import cache
from fractions import Fraction
from math import prod
import gzip,json,sys

H=Path(__file__).resolve().parent
R=H.parents[1]
sys.path[:0]=[str(H),str(R/'Session20261126')]
from PivotCheck import C,B,exact_leaf,floor10
from Price12 import enough
from MaskedForest import exact_absence_bound

Q=16148168401
PAIR=(7,12)
BANNED=(19,)


def verify(path):
    d=json.loads(gzip.decompress(path.read_bytes()))
    assert tuple(d['pair'])==PAIR and d['pivot']==Q
    assert set(d) in ({'pair','pivot','ecpp','cases'}, {'pair','pivot','ecpp','prefix','tree'})
    used=set()
    forests=splits=direct=prices=abundance=0
    @cache
    def prime(q):
        assert type(q)==int and q>2
        z=q
        if q>=2**64:
            used.add(str(q))
            for row in d['ecpp'][str(q)]:
                assert row[0]==z
                z=C.pc.level(*row)
        assert C.pc.prime64(z)
        return True
    def dead(parts,s):
        return s.conflict or s.base>B or prod(C.sigma(q,f) for q,f in parts)>2*s.X
    def cases(parts,q,absent=()):
        nonlocal direct
        s=C.State(parts,absent=absent)
        assert prime(q) and not dead(parts,s) and s.D%q==0 and q not in s.rows and q not in s.bad
        c=C.valuation(s.D,q); f=c; n=s.base
        while n<=B:
            if s.possible(q,f,c):
                p2=parts+[(q,f)]
                if dead(p2,C.State(p2,absent=absent)):
                    direct+=1
                else:
                    yield str(f),p2
            f+=1
            n*=q
    def walk(parts,node,absent=()):
        nonlocal forests,splits,prices,abundance
        s=C.State(parts,absent=absent)
        assert not dead(parts,s)
        if node['type']=='forest':
            assert set(node)=={'type','roots','owners','head'}
            roots,owners,head=node['roots'],node['owners'],node['head']
            C.validate_forest(s,roots,owners,head,prime)
            check=(exact_absence_bound(parts,roots,owners,head,s.bad,B) if absent else exact_leaf(parts,roots,owners,head))
            v=min(C.Forest(s,roots,owners,head).lower()[0],check)
            assert v>B,parts
            forests+=1
            return floor10(v)
        if node['type']=='abundance':
            assert set(node)=={'type','forced'}
            forced=node['forced']
            assert forced and len(forced)==len(set(forced))
            assert all(prime(q) and q not in s.rows and q not in s.bad and s.D%q==0 for q in forced)
            fixed=prod(Fraction(C.sigma(q,f),q**f) for q,f in parts)
            modes=[None]+([q for q in forced if C.euler(q,s.bad)] if not s.fixed_euler else [])
            for mode in modes:
                lower=fixed
                for q in forced:
                    h=C.valuation(s.D,q)
                    f=h+((1-h)%4 if q==mode else h%2)
                    while q**f<=B and not s.possible(q,f,h):
                        f+=4 if q==mode else 2
                    if q**f>B:
                        break
                    lower*=Fraction(C.sigma(q,f),q**f)
                else:
                    assert lower>2
            abundance+=1
            return 2400
        if node['type'] in ('no-three','no-five'):
            assert set(node)=={'type','tree'} and not absent
            banned,present=(3,5) if node['type']=='no-three' else (5,3)
            assert prime(3) and prime(5) and banned not in s.rows and (present in s.rows or s.D%present==0)
            # 3 is never Euler; even its square and a single 5 are strictly abundant with 7^12.
            assert Fraction(C.sigma(*PAIR),7**12)*Fraction(C.sigma(3,2),9)*Fraction(C.sigma(5,1),5)>2
            t=C.State(parts,absent=(banned,))
            if dead(parts,t):
                abundance+=1
                return 2400
            return walk(parts,node['tree'],(banned,))
        if node['type']=='support-abundance':
            assert set(node)=={'type'}
            S=(3,5,11,13,17,31)
            assert all(prime(q) for q in S)
            fixed=prod(Fraction(C.sigma(q,f),q**f) for q,f in parts)
            for mask in range(1<<len(S)):
                Y={q for i,q in enumerate(S) if mask>>i&1}
                t=C.State(parts,Y,tuple(set(absent)|{q for q in S if q not in Y}))
                if dead(parts,t):
                    continue
                V=sorted(Y-t.rows.keys())
                modes=[None]+([q for q in V if C.euler(q,t.bad)] if not t.fixed_euler else [])
                for mode in modes:
                    lower=fixed
                    for q in V:
                        h=max(1,C.valuation(t.D,q))
                        f=h+((1-h)%4 if q==mode else h%2)
                        while q**f<=B and not t.possible(q,f,h):
                            f+=4 if q==mode else 2
                        if q**f>B:
                            break
                        lower*=Fraction(C.sigma(q,f),q**f)
                    else:
                        assert lower>2
            abundance+=1
            return 2400
        if node['type']=='exact-packet':
            assert set(node)=={'type','name'} and not absent and node['name']=='Exact1x2'
            assert tuple(parts)==(PAIR,(Q,1),(110563,2))
            assert verify(H/'Exact1x2.json.gz')==tuple(parts)
            return 2400
        if node['type']=='support-packet':
            assert set(node)=={'type','name'} and not absent
            known={
                'SupportLeaf12':((7,12),(Q,1),(110563,2),(226741,2)),
                'SupportLeaf2':((7,12),(Q,2),(200741603328100897,1)),
            }
            key=node['name'];assert tuple(parts)==known[key]
            from SupportLeaf12 import verify as verify_support
            assert verify_support(H/(key+'.json.gz'))==tuple(parts)
            return 2400
        if node['type']=='price':
            assert set(node)=={'type'} and len(parts)==2 and parts[0]==PAIR and parts[1][0]==Q and s.bad==BANNED
            enough(parts[1][1])
            prices+=1
            return 2400
        assert node['type']=='split' and set(node)=={'type','q','cases'}
        splits+=1
        expected=dict(cases(parts,node['q'],absent))
        assert set(expected)==set(node['cases'])
        return min((walk(expected[f],r,absent) for f,r in node['cases'].items()),default=2400)
    assert __debug__ and C.ORDER[:C.ORDER.index(PAIR[0])]==BANNED
    assert C.sigma(*PAIR)==Q and prime(Q)
    live=dict(cases([PAIR],Q))
    assert len(live)==83 and direct==84
    k=7**12
    assert k*Q**234<=B<k*Q**235
    if 'prefix' in d:
        parts=[tuple(x) for x in d['prefix']]
        assert parts in [
            [PAIR,(Q,1),(110563,2)],
            [PAIR,(Q,4),(222942691488419051165955167217344876341,18)],
            [PAIR,(Q,4),(222942691488419051165955167217344876341,10),(6818005862120741597,22)],
            [PAIR,(Q,42),(173,1)],
            [PAIR,(Q,42),(173,4)],
            [PAIR,(Q,42),(173,6)],
            [PAIR,(Q,42),(173,48)],
        ]
        assert parts[:2]==live[str(parts[1][1])]
        for j,(q,f) in enumerate(parts[2:],2):
            around=dict(cases(parts[:j],q))
            assert around[str(f)]==parts[:j+1]
        floor=walk(parts,d['tree'])
        assert used==set(d['ecpp'])
        print('PASS EXACT PREFIX',parts,'floor',floor,'forests',forests,'splits',splits,'direct',direct,'prices',prices,'abundance',abundance,'ECPP',len(used),flush=True)
        return tuple(parts)
    claims=d['cases']
    assert claims and claims.keys()<=live.keys()
    for f in sorted(claims,key=int):
        floor=walk(live[f],claims[f]);print('PASS',int(f),floor,flush=True)
    assert used==set(d['ecpp'])
    pending=sorted(map(int,live.keys()-claims.keys()))
    print('PARTITION live',len(live),'covered',len(claims),'uncovered',len(pending),'forests',forests,'splits',splits,'direct',direct,'prices',prices,'abundance',abundance,'ECPP',len(used),flush=True)
    print('UNCOVERED',pending,flush=True)
    return pending

if __name__=='__main__':
    verify(Path(sys.argv[1]) if len(sys.argv)>1 else H/'Fibers12.json.gz')
