"""Exact (13,372), q^2: replay the last three masks of the root fiber.

The five disjoint peer masks are replayed by C5/Verify.py, not assumed closed
by this file. Every one of the 36 live (mask, secondary valuation) cells is
covered. The other primary valuations are out of scope.
"""
from functools import cache
import gzip
from hashlib import sha256
import json
from pathlib import Path
import sys

H = Path(__file__).resolve().parent
sys.path.insert(0,str(H/'C5'))
from Verify import KEY, Q, MASKS, C, B, abundance, dead, forest, partitions

R = 1451320277645395737847
RESIDUAL = (48,112,176)


def replay(path):
    if not __debug__: raise RuntimeError('assertions required')
    raw=path.read_bytes();d=json.loads(gzip.decompress(raw))
    assert set(d)=={'cases','ecpp'} and set(d['cases'])==set(map(str,RESIDUAL))
    assert set(RESIDUAL)<set(MASKS)
    used=set()

    @cache
    def prime(q):
        assert type(q) is int and q>2
        n=q
        if q>=2**64:
            k=str(q);used.add(k);chain=d['ecpp'][k];assert chain
            for row in chain:
                assert row[0]==n and n>=2**64
                n=C.pc.level(*row)
        assert C.pc.prime64(n)
        return True

    assert all(prime(q) for q in (*C.ORDER,Q,R))
    base,_,_,tail=partitions([KEY],Q)
    assert '2' in base and tail==78
    counts={'forest':0,'abundance':0}; minima=[]
    for m in RESIDUAL:
        yes=tuple(q for i,q in enumerate(C.ORDER[5:],5) if m>>i&1)
        no=tuple(q for q in C.ORDER[5:] if q not in yes)
        cases, direct, illegal, last=partitions(base['2'],R,yes,no)
        assert set(cases)==set(d['cases'][str(m)]) and last==73
        for j, P in cases.items():
            node=d['cases'][str(m)][j]
            if node['type']=='abundance':
                s=C.State(P,yes,no); roots=node['roots']
                assert not dead(s) and set(node)=={'type','roots'} and roots==sorted(set(roots))
                assert all(prime(z) and z not in s.rows and z not in s.bad and (z in yes or s.D%z==0) for z in roots)
                assert abundance(s,roots)>2
            else:
                minima.append(forest(P,node,prime,yes,no,d['ecpp']))
            counts[node['type']]+=1
        print('PASS mask',m,'secondary live',list(map(int,cases)),'direct',direct,'illegal',illegal,'tail',last,flush=True)
    assert used==set(d['ecpp']) and counts=={'forest':34,'abundance':2}
    return {'key':list(KEY),'primary':2,'confirmed_masks':list(RESIDUAL),
            'joint_all_masks':list(MASKS),'counts':counts,'min_forest_floor':min(minima),
            'ecpp':len(used),'sha256':sha256(raw).hexdigest()}


if __name__=='__main__':
    print(json.dumps(replay(Path(sys.argv[1]))),flush=True)
