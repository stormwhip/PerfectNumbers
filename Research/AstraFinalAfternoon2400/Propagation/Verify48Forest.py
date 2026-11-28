"""Strict two-recurrence forest replay for newly excluded (7,48) exact rows."""
from functools import cache
from hashlib import sha256
from math import gcd,prod
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent; R=H.parents[1]
sys.path[:0]=[str(H),str(R/'Session20261126'),str(R/'Night2400/A'),str(R/'RootFiveNext')]
from PivotCheck import C, B
from MaskedForest import exact_absence_bound
from PrimeCheck import prime64,level
from Propagation import sigma,val,part
from Verify48Price import P,T,domain,PIVOT,PUBLISH
from Verify48Overlap import EXTRA


def replay(path, expected=None):
    data=path.read_bytes(); z=json.loads(gzip.decompress(data)); assert set(z)=={'records','ecpp'}
    seen=set();pre=[]; ec=z['ecpp']
    @cache
    def prime(q):
        if q<2**64:return prime64(q)
        s=str(q); n=q; seen.add(s)
        for step in ec[s]: assert n==step[0];n=level(*step)
        return prime64(n)
    assert prime(P) and prime(T) and val(sigma(P,48),T)==1
    for row in z['records']:
        assert set(row)=={'P','bad','tree','unresolved'} and row['bad']==[19] and not row['unresolved']
        rows=list(map(tuple,row['P'])); assert len(rows)==3 and rows[0]==(P,48) and rows[1][0]==T
        f=rows[1][1]; q,h=rows[2]; assert f in (2,10) and q==PIVOT[f]
        assert all(prime(p) for p,e in rows) and q%4==3 and h not in set(PUBLISH[f])|EXTRA[f].keys()
        assert h in domain(rows[:2],q)[0]
        tag=f,h; assert tag not in pre; pre.append(tag)
        t=row['tree']; assert set(t)=={'type','roots','owners','head'} and t['type']=='forest'
        roots,edges,head=(t[k] for k in ('roots','owners','head')); s=C.State(rows)
        assert not s.conflict and s.bad==(19,)
        C.validate_forest(s,roots,edges,head,prime)
        a=C.Forest(s,roots,edges,head).lower()[0]
        b=exact_absence_bound(rows,roots,edges,head,(19,),B)
        assert min(a,b)>B
        floor=len(str(min(a,b)))-1
        print('48 forest',tag,'roots/owners',len(roots),len(edges),'decimal floor',floor,
              'scaled millionths (clipped)',min(10**12,min(a,b)*10**6//B),flush=True)
    assert seen==set(ec) and pre
    if expected is not None:assert pre==list(expected)
    print('PASS (7,48) forest cuts',pre,'ECPP',len(seen),'sha256',sha256(data).hexdigest(),flush=True)
    return {tuple([(P,48),(T,f),(PIVOT[f],h)]) for f,h in pre}

def forest_file(tag):
    return H/f'Reserved438x12-{tag}.json.gz'

PACKS={
 'orbit48':[(10,h) for h in (84,86,88,90,94,96)],
 'orbit48ten':[(10,h) for h in (38,44,48,50,54,56,60,62,64,66,68,70,72,74,76,78,80,82)],
 'orbit48tenlow':[(10,h) for h in (14,20,22,24,26,32,34)],
 'orbit48tenfresh':[(10,h) for h in (30,40)],
 'orbit48tennested':[(10,h) for h in (8,18)],
 'orbit48tenhard':[(10,h) for h in (4,6,12,16,28,42,52,58)],
 'orbit48tenhard10':[(10,10)],
 'orbit48tenhardfinal':[(10,h) for h in (2,36,46)],
 'orbit48sq':[(2,h) for h in range(32,73,2)],
 'orbit48sqmid':[(2,h) for h in (14,20,24,26,28,30)],
}

if __name__=='__main__':
    assert __debug__
    proved=set()
    for tag in sys.argv[1:] or tuple(PACKS):
        e=replay(forest_file(tag),PACKS[tag]);assert not proved&e;proved|=e
