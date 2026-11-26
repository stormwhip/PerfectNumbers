"""Offline replay of partial first-pivot fibers, not necessarily of the root pair."""
from pathlib import Path
from functools import cache
from math import prod
import gzip,json,sys

H=Path(__file__).resolve().parent
R=H.parents[1]
sys.path[:0]=[str(R/'Session20261126'),str(R/'FinalSprint')]
from PivotCheck import C,B,exact_leaf,floor10
from JointValuation import excludes

Q=16148168401
PAIR=(7,12)
BANNED=(19,)


def verify(path):
    d=json.loads(gzip.decompress(path.read_bytes()))
    assert set(d)=={'pair','pivot','ecpp','cases'} and tuple(d['pair'])==PAIR and d['pivot']==Q
    used=set()
    forests=splits=direct=prices=0
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
    def cases(parts,q):
        nonlocal direct
        s=C.State(parts)
        assert prime(q) and not dead(parts,s) and s.D%q==0 and q not in s.rows and q not in s.bad
        c=C.valuation(s.D,q); f=c; n=s.base
        while n<=B:
            if s.possible(q,f,c):
                p2=parts+[(q,f)]
                if dead(p2,C.State(p2)):
                    direct+=1
                else:
                    yield str(f),p2
            f+=1
            n*=q
    def walk(parts,node):
        nonlocal forests,splits,prices
        s=C.State(parts)
        assert not dead(parts,s)
        if node['type']=='forest':
            assert set(node)=={'type','roots','owners','head'}
            roots,owners,head=node['roots'],node['owners'],node['head']
            C.validate_forest(s,roots,owners,head,prime)
            v=min(C.Forest(s,roots,owners,head).lower()[0],exact_leaf(parts,roots,owners,head))
            assert v>B,parts
            forests+=1
            return floor10(v)
        if node['type']=='price':
            assert set(node)=={'type','targets'}
            excludes(parts,s.bad,node['targets'])
            prices+=1
            return 2400
        assert node['type']=='split' and set(node)=={'type','q','cases'}
        splits+=1
        expected=dict(cases(parts,node['q']))
        assert set(expected)==set(node['cases'])
        return min((walk(expected[f],r) for f,r in node['cases'].items()),default=2400)
    assert __debug__ and C.ORDER[:C.ORDER.index(PAIR[0])]==BANNED
    assert C.sigma(*PAIR)==Q and prime(Q)
    live=dict(cases([PAIR],Q))
    assert len(live)==83 and direct==84
    k=7**12
    assert k*Q**234<=B<k*Q**235
    claims=d['cases']
    assert claims and claims.keys()<=live.keys()
    for f in sorted(claims,key=int):
        floor=walk(live[f],claims[f]);print('PASS',int(f),floor,flush=True)
    assert used==set(d['ecpp'])
    pending=sorted(map(int,live.keys()-claims.keys()))
    print('PARTITION live',len(live),'covered',len(claims),'uncovered',len(pending),'forests',forests,'splits',splits,'direct',direct,'prices',prices,'ECPP',len(used),flush=True)
    print('UNCOVERED',pending,flush=True)
    return pending

if __name__=='__main__':
    verify(Path(sys.argv[1]) if len(sys.argv)>1 else H/'Fibers12.json.gz')
