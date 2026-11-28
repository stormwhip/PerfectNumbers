"""New canonical 7^438,t^12 exact lower 27431 exponents, reserved Euler forest."""
from functools import cache
from hashlib import sha256
import gzip,json,sys
from pathlib import Path

H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from VerifyForest import C, B, child_domain
from VerifyReserved438 import T, rule, independent
from ReservedForest import reserve
PREF=[(7,438),(T,12)]; R=27431; M=T**11


def verify(path,expected,delegated=()):
    external=set(delegated); reached=set()
    raw=path.read_bytes(); d=json.loads(gzip.decompress(raw)); assert set(d)=={'records','ecpp'}
    used=set();tested=[]
    @cache
    def prime(p):
        q=p
        if q>=2**64:
            k=str(p);used.add(k)
            for step in d['ecpp'][k]: assert step[0]==q; q=C.pc.level(*step)
        return C.pc.prime64(q)
    assert prime(R) and R%4==3
    dom,tail=child_domain(PREF,(19,),R)
    assert list(map(int,dom))==list(range(2,111,2))
    print('t12 direct pivot',R,'size tail',tail,'live',len(dom),flush=True)
    def walk(P,t,counts,millionths):
        assert all(h%2==0 and p%(4*M)!=2*M-1 for p,h in P)
        if t['type']=='delegated':
            assert set(t)=={'type'}
            key=tuple(sorted(P)); assert key in external and key not in reached
            reached.add(key); counts[3]+=1
            return
        if t['type']=='split-q1':
            assert set(t)=={'q','cases','type'} and prime(t['q']) and t['q']%(4*M)!=2*M-1
            ks,tail=child_domain(P,(19,),t['q'])
            # The actual Euler prime is outside this congruence-excluded pivot.
            ks={k:P2 for k,P2 in ks.items() if int(k)%2==0}
            assert set(t['cases'])==set(ks); counts[0]+=1; counts[2]=max(counts[2],tail)
            for k in ks:walk(ks[k],t['cases'][k],counts,millionths)
            return
        assert set(t)=={'roots','owners','head','type'} and t['type']=='reserve'
        K=t['roots']; E=t['owners']; head=t['head']; C.validate_forest(C.State(P),K,E,head,prime)
        assert all(p%(4*M)!=2*M-1 for p in set(K)|{q for q,_ in E})
        a=reserve(P,K,E,head,(19,),M,exact_one=True); b=independent(P,K,E,head,M)
        assert min(a,b)>B; counts[1]+=1; millionths.append(min(a,b)*10**6//B)
    for r in d['records']:
        assert set(r)=={'P','bad','tree','unresolved'} and r['bad']==[19] and not r['unresolved']
        P=list(map(tuple,r['P'])); assert len(P)==3 and P[:-1]==PREF and P[-1][0]==R and all(prime(p) for p,h in P)
        h=P[-1][1]; assert h in (2,4,6,8) and str(h) in dom; tested.append(h)
        counts=[0,0,0,0]; millionths=[];walk(P,r['tree'],counts,millionths)
        print(h,'splits, forests, max raw tail, delegated',counts,'strict minimum millionths',min(millionths,default=None),flush=True)
    assert tested==expected and used==set(d['ecpp']) and reached==external
    print('PASS',path.name,tested,'ECPP',len(used),'SHA256',sha256(raw).hexdigest(),flush=True)

PACKS={'a':[4,6], 'b':[8], 'c':[2]}
def square_external():
    sys.path.insert(0,str(H.parent/'Propagation'))
    from VerifyReserved438x12 import verify_h2_cuts
    base=PREF+[(R,2),(752487193,22)]
    required={tuple(sorted(base+[(50047294070406095227,h)])) for h in (2,10,12)}
    required.update(tuple(sorted(PREF+[(R,2),(752487193,h)])) for h in (46,52))
    verified=verify_h2_cuts()
    assert required<=verified
    return required

if __name__=='__main__':
    assert __debug__; rule(12)
    for tag in sys.argv[1:] or PACKS:
        verify(H/f'Forest438t12{tag}.json.gz',PACKS[tag],square_external() if tag=='c' else ())
