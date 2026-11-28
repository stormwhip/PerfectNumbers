"""Replay sealed conditional forest packets; null endpoints are never exclusions."""
from collections import Counter
import argparse
from functools import cache
from hashlib import sha256
import gzip,json,sys
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parents[1]
sys.path[:0]=[str(H),str(R/'Session20261126')]
from Replay import B, P, BANNED, key, split, state, valuation, ledger
from PivotCheck import C, exact_leaf


def verify(filename, *, details=False):
    raw=filename.read_bytes();packet=json.loads(gzip.decompress(raw))
    assert set(packet)=={'e','pivot','cases','ecpp'}
    e,t=packet['e'],packet['pivot'];primers=packet['ecpp'];used=set();counts=Counter()
    @cache
    def prime(z):
        assert type(z)==int and z>2
        q=z
        if q>=2**64:
            assert primers[str(q)];used.add(str(q))
            for a in primers[str(q)]:
                assert a[0]==q
                q=C.pc.level(*a)
        assert C.pc.prime64(q)
        return True
    open_rows=[]
    def visit(row,n):
        if n is None:
            counts['open']+=1;open_rows.append(row);return False
        assert state(row)[-1]
        kind=n['type'];counts[kind]+=1
        if kind in ('price6','joint6'):
            assert e==6 and set(n)=={'type'}
            from PriceLeaf6 import allowed,joint
            return (allowed if kind=='price6' else joint)(row)
        if kind=='price2_316':
            assert e==2 and set(n)=={'type'}
            from PriceTwo316 import check
            assert check(row)['excluded']
            return True
        if kind=='price2_400':
            assert e==2 and row==((31,2),(331,400)) and set(n)=={'type'}
            from PricedTwo import check
            assert not check(400)['residual']
            return True
        if kind=='forest':
            assert set(n)=={'type','roots','owners','head'}
            s=C.State(list(row));k,o,h=n['roots'],n['owners'],n['head']
            assert (s.X,s.S,s.D)==state(row)[:3] and not s.conflict
            C.validate_forest(s,k,o,h,prime)
            assert C.Forest(s,k,o,h).lower()[0]>B and exact_leaf(list(row),k,o,h)>B
            return True
        assert kind=='split' and set(n)=={'type','q','cases'}
        z=n['q'];assert prime(z)
        children,_=split(row,z);cs={str(r[-1][1]):r for r in children}
        assert set(cs)==set(n['cases'])
        return all([visit(r,n['cases'][f]) for f,r in cs.items()])
    if t is None:
        assert set(packet['cases'])=={str(e)}
        cs=[((P,e),)]
    else:
        assert prime(t)
        cs,tail=split(((P,e),),t)
        k=key(e)
        if k[0]==t:assert (cs,tail)==k[1:]
    assert set(packet['cases'])=={str(r[-1][1]) for r in cs}
    good=[];bad=[]
    for r in cs:
        f=r[-1][1]
        (good if visit(r,packet['cases'][str(f)]) else bad).append(f)
        if details:print('first',f,'open' if f in bad else 'excluded',flush=True)
    assert used==set(primers)
    summary=dict(key=[P,e],pivot=t,sha256=sha256(raw).hexdigest(),closed=good,
                 open=bad,ecpp=len(used),checks=counts)
    if details:summary['open_prefixes']=open_rows
    print(json.dumps(summary),flush=True)
    return good,bad


if __name__=='__main__':
    assert __debug__;ledger()
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--require-complete',action='store_true',help='fail if any first remains open')
    ap.add_argument('--details',action='store_true',help='include the complete residual prefix list')
    ap.add_argument('paths',nargs='+',type=Path)
    a=ap.parse_args()
    for path in a.paths:
        good,bad=verify(path,details=a.details)
        if a.require_complete:
            assert good and not bad,('certificate is not complete',bad)
