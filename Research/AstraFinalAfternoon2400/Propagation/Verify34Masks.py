"""Close five exact (7,34) firsts by a complete 3-support partition."""
from functools import cache
from hashlib import sha256
from math import prod
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Verify34Forest import child_domain,exact_state,C,B,prime64,level,q,P,F,PACKS
from VerifyForest import abgt2
from Full48Eight import independently
from Propagation import sigma

SCOPES=((2,2),(2,4),(8,2),(8,4),(9,0),(21,0))
DIRECT={9:(5,17,31,811),14:(5,61,151,907,4723),21:(11,17,23,89)}
EXPECTED={2,8,9,14,21}


def replay():
    assert __debug__
    A=sigma(7,34);assert prod(F)==A and all(prime64(p) for p in (3,7,19,*F))
    assert q%4==1 and 3%4==3
    domain,tail=child_domain(P,(19,),q);assert len(domain)==78 and tail==217
    assert EXPECTED<=set(map(int,domain)) and not EXPECTED&set().union(*map(set,PACKS.values()))
    # These firsts force 3 directly; the first 14 is then entirely abundant.
    assert all(sigma(q,f)%3==0 for f in (2,8,14))
    for f,values in DIRECT.items():
        assert all(prime64(v) and sigma(q,f)%v==0 for v in values)
        P0=P+[(q,f),(3,2)]
        labels=(set(F)|set(values))-{p for p,k in P0}
        assert abgt2(P0+[(p,2 if p%4==3 else 1) for p in labels])
    raw=(H/'Reserved438x12-orbit48root34m.json.gz').read_bytes()
    pack=json.loads(gzip.decompress(raw));assert set(pack)=={'records','ecpp'}
    used=set();seen=[];cert=pack['ecpp'];low=None
    @cache
    def prime(p):
        if p<2**64:return prime64(p)
        n=p; k=str(p);used.add(k)
        for r in cert[k]:assert n==r[0];n=level(*r)
        return prime64(n)
    for z in pack['records']:
        assert set(z)=={'P','bad','tree','roots','present','lo'}
        R=list(map(tuple,z['P']));f=R[1][1];base=P+[(q,f)]
        assert R[:2]==base and base==domain[str(f)]
        b=tuple(z['bad']); p=tuple(z['present']); h=dict(z['lo'])
        assert b[0]==19 and len(b)==len(set(b))
        if f in (9,21):
            mode=0;assert R==base and 3 in b and not p and not h
        elif R==base+[(3,2)]:
            assert f in (2,8) and not p and not h;mode=2
        else:
            assert f in (2,8) and R==base and p==(3,) and h=={3:4};mode=4
        seen.append((f,mode))
        mask=set(b)-{19}
        if mode==0:mask.remove(3) # 3 absence is this support assumption alone.
        fixed=dict(R)
        all_sigma=prod(sigma(a,k) for a,k in R)
        known=set(z['roots']);assert not known&fixed.keys()
        assert all(prime(a) and all_sigma%a==0 for a in known)
        for a in known:fixed[a]=2 if a%4==3 else 1
        fixed.update(h)
        for a in mask:
            assert prime(a) and a not in fixed
            assert abgt2(list(fixed.items())+[(a,2 if a%4==3 else 1)])
        T=z['tree'];assert set(T)=={'type','roots','owners','head'} and T['type']=='forest'
        r,e,M=(T[k] for k in ('roots','owners','head'))
        S=C.State(R,absent=b[1:],present=p,lo=h);good,X,D,n=exact_state(R,b)
        assert good and not S.conflict and set(p)<=set(r) and (S.X,S.D)==(X,D)
        C.validate_forest(S,r,e,M,prime)
        a=C.Forest(S,r,e,M).lower()[0];d=independently(R,b,r,e,M,p,h)
        v=min(a,d);assert v>B
        low=v if low is None else min(low,v)
        print('PASS (7,34) mask',f,mode,'floor',len(str(v))-1,'local bans',len(mask),flush=True)
    assert tuple(seen)==SCOPES and used==set(cert)
    print('PASS full firsts',sorted(EXPECTED),'by 6 forests and 3 abundance cuts; ECPP',len(used),
          'minimum millionths',low*10**6//B,'sha256',sha256(raw).hexdigest(),flush=True)
    return EXPECTED.copy()

if __name__=='__main__':replay()
