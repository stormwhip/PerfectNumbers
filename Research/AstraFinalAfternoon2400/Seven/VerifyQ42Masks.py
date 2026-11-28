"""Exact support disjunctions below canonical 7^12,Q^42; both integer forest evaluators."""
from hashlib import sha256
from functools import cache
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from VerifyForest import Q,C,B,sig,abgt2,known_scope,exact_state,child_domain
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
        elif h in (2,6,10) and present==(3,) and lo=={3:{2:1200,6:450,10:900}[h]}:
            assert len(P)==3 and abgt2([(7,12),(3,2),(5,1)])
            assert bad==((19,5,11) if h==10 else (19,5))
            if h==10:
                assert all(C.pc.prime64(q) for q in (11,19,23,43))
                assert sig(Q,42)%43==sig(173,h)%23==sig(11,2)%19==0
                assert 11%4==43%4==3
                assert abgt2([(7,12),(3,4),(43,2),(23,1),(11,4)])
            mode='even-high-three'
        elif h in (2,6,10) and P==[(7,12),(Q,42),(173,h),(3,2)]:
            assert bad==(19,5,11) and not present and not lo
            assert all(C.pc.prime64(q) for q in (3,5,7,11,13,43))
            assert sig(3,2)==13 and sig(Q,42)%43==sig(11,2)%19==0
            assert 11%4==3 and abgt2([(7,12),(3,2),(5,1)])
            assert abgt2([(7,12),(3,2),(43,2),(13,1),(11,4)])
            mode='even-three-two'
        elif h==6 and P==[(7,12),(Q,42),(173,h),(3,6)]:
            assert not present and not lo and bad==(19,5)
            assert abgt2([(7,12),(3,2),(5,1)])
            mode='even-three-six'
        elif h in (2,6) and P==[(7,12),(Q,42),(173,h),(3,4)]:
            assert not present and not lo
            assert all(C.pc.prime64(q) for q in (3,5,7,11,19,43,*bad))
            assert sig(3,4)==121 and sig(11,2)%19==0 and sig(Q,42)%43==0
            assert 11%4==43%4==3 and abgt2([(7,12),(3,2),(5,1)])
            assert bad[:2]==(19,5) and len(set(bad))==len(bad) and all(q not in (3,7,11,Q,43,173) for q in bad[2:])
            assert all(abgt2([(7,12),(173,h),(3,4),(11,4),(43,2),(q,1)]) for q in bad[2:])
            mode='even-three-four'
        else:raise AssertionError((P,bad,present,lo))
        k=(h,mode);assert k not in done;done.add(k)
        s=C.State(P,present=present,absent=bad[1:],lo=lo);assert s.bad==bad and not s.conflict and exact_state(P,bad)[0]
        stats=[0,0,0];mins=[]
        def walk(P,t,pres,lows):
            if t['type']=='split':
                assert not pres and not lows and set(t)=={'type','q','cases'} and prime(t['q'])
                kids,tail=child_domain(P,bad,t['q']); assert set(kids)==set(t['cases']);stats[0]+=1
                for k in kids:walk(kids[k],t['cases'][k],(),{})
                return
            assert t['type']=='forest' and set(t)=={'type','roots','owners','head'}
            s=C.State(P,present=pres,absent=bad[1:],lo=lows);assert s.bad==bad and not s.conflict
            K,E,n=t['roots'],t['owners'],t['head']; C.validate_forest(s,K,E,n,prime);assert set(pres)<=set(K)
            a=C.Forest(s,K,E,n).lower()[0]; b=independently(P,bad,K,E,n,pres,lows)
            assert min(a,b)>B;mins.append(min(a,b)*10**6//B);stats[1]+=1;stats[2]+=len(K)+len(E)
        walk(P,r['tree'],present,lo)
        print(h,mode,'splits, forests, vertices',stats,'strict millionths',min(mins),flush=True)
    assert used==set(d['ecpp']) and done and (expect is None or done==expect)
    print('PASS',path.name,sorted(done),'ECPP',len(used),'SHA256',sha256(raw).hexdigest(),flush=True)
    return done

if __name__=='__main__':
    for p in sys.argv[1:]:verify(Path(p))
