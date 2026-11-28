"""Exact support disjunctions below canonical 7^12,Q^42; both integer forest evaluators."""
from hashlib import sha256
from functools import cache
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from VerifyForest import Q,C,B,sig,abgt2,known_scope,exact_state
from Full48Eight import independently


def odd_scope(P,bad,present,lo):
    base=[(7,12),(Q,42),(173,1)]; assert P[:3]==base
    assert all(C.pc.prime64(q) for q in (3,5,7,11,13,17,19,23,29,31,37,43,173,Q))
    assert sig(7,12)==Q and sig(Q,42)%43==0 and sig(173,1)==2*3*29
    G=base+[(29,2),(43,2)]
    if P==base:
        assert present==(3,) and lo=={3:4} and bad==(19,5,11,13)
        for q in bad[1:]:assert abgt2(G+[(3,4),(q,2)])
        return 'odd-high'
    assert P==base+[(3,2)] and not present and not lo and bad==(19,5,11,17,23,31,37)
    assert sig(3,2)==13
    for q in bad[1:]:assert abgt2(G+[(3,2),(13,2),(q,2)])
    return 'odd-two'


def verify(path,expect=None):
    assert __debug__; raw=path.read_bytes(); d=json.loads(gzip.decompress(raw));assert set(d)=={'records','ecpp'}
    used=set(); done=set()
    @cache
    def prime(q):
        y=q
        if q>=2**64:
            k=str(q);used.add(k)
            for s in d['ecpp'][k]:assert s[0]==y; y=C.pc.level(*s)
        return C.pc.prime64(y)
    for r in d['records']:
        assert set(r)=={'P','bad','present','lo','tree','unresolved'} and not r['unresolved']
        P=list(map(tuple,r['P'])); bad=tuple(r['bad']);present=tuple(r['present']);lo=dict(r['lo']);assert len(lo)==len(r['lo'])
        assert all(prime(q) for q,h in P) and known_scope(P[:3],(19,))=='12R'; h=P[2][-1]
        if h==1: mode=odd_scope(P,bad,present,lo)
        elif bad==(19,3):
            assert len(P)==3 and not present and not lo;mode='no3'
        elif present==(3,) and lo=={3:2}:
            assert len(P)==3 and bad==(19,5) and abgt2([(7,12),(3,2),(5,1)]);mode='yes3'
        else:raise AssertionError((P,bad,present,lo))
        k=(h,mode);assert k not in done;done.add(k)
        s=C.State(P,present=present,absent=bad[1:],lo=lo);assert s.bad==bad and not s.conflict and exact_state(P,bad)[0]
        t=r['tree'];assert t['type']=='forest' and set(t)=={'type','roots','owners','head'}
        K,E,n=t['roots'],t['owners'],t['head']; C.validate_forest(s,K,E,n,prime);assert set(present)<=set(K)
        a=C.Forest(s,K,E,n).lower()[0]; b=independently(P,bad,K,E,n,present,lo)
        assert min(a,b)>B
        print(h,mode,'vertices',len(K)+len(E),'strict millionths',min(a,b)*10**6//B,flush=True)
    assert used==set(d['ecpp']) and done and (expect is None or done==expect)
    print('PASS',path.name,sorted(done),'ECPP',len(used),'SHA256',sha256(raw).hexdigest(),flush=True)
    return done

if __name__=='__main__':
    for p in sys.argv[1:]:verify(Path(p))
