"""Final t² residual; prove exact 27 child coverage, local bans and dual forests."""
from functools import cache
from hashlib import sha256
from math import prod
from pathlib import Path
from collections import Counter
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from Verify48Masks import lemma,BASE,C,B,abgt2,exact_state,independently,prime64,level
from Verify48Price import P,T,SMALL,ROOTS,PIVOT
from VerifyForest import child_domain
from Propagation import sigma,val
R=PIVOT[2]; A=116161286042101
PARENT=BASE+[(R,12),(3,2)]
BAD=(19,5,11,17,23)
EXPECT=(2,6,8,10,12,16,18,20,22,28,30,32,36,38,40,42,46,48,50,52,56,58,60,62,66,68,70)


def verify(path=H/'Reserved438x12-orbit48finalsq.json.gz'):
    assert __debug__;lemma()
    raw=path.read_bytes();obj=json.loads(gzip.decompress(raw));assert set(obj)=={'records','ecpp'}
    cert=obj['ecpp'];used=set()
    @cache
    def prime(p):
        if p<2**64:return prime64(p)
        u=p;s=str(p);used.add(s)
        for step in cert[s]:assert u==step[0];u=level(*step)
        return prime64(u)
    assert all(prime(p) for p in (P,T,R,3,A,13,157,*SMALL,*ROOTS[2]))
    assert prod(SMALL)*T==sigma(P,48) and prod(ROOTS[2])==sigma(T,2)
    f=sigma(R,12)
    assert f%(13*157*A)==0 and sigma(3,2)==13
    H0=dict(PARENT)
    compelled=(set(SMALL)|set(ROOTS[2])|{13,157,A})-H0.keys()
    for q in compelled:H0[q]=2 if q%4==3 else 1
    assert all(abgt2(list(H0.items())+[(q,2 if q%4==3 else 1)]) for q in (17,23))
    # Every legal assignment under BAD is enumerated at the exact prefix,
    # with arbitrary Euler position. The h classes may have gaps.
    kids,tail=child_domain(PARENT,BAD,A)
    assert tuple(map(int,kids))==EXPECT and tail==143
    rec=[];mins=[];vertices=0
    for x in obj['records']:
        assert set(x)=={'P','bad','tree','unresolved'} and not x['unresolved']
        P0=list(map(tuple,x['P']));assert P0[:-1]==PARENT and P0[-1][0]==A
        h=P0[-1][1];assert kids[str(h)]==P0 and h not in rec;rec.append(h)
        bad=tuple(x['bad']);assert bad[:len(BAD)]==BAD and len(bad)==len(set(bad))
        z=x['tree'];assert set(z)=={'type','roots','owners','head'} and z['type']=='forest'
        roots,edges,head=(z[k] for k in ('roots','owners','head'))
        assert all(prime(p) for p in roots)
        # Additional masks can use only actual compulsory support at THIS
        # exact prefix. Root minima are independently charged at 1 or 2.
        all_em=prod(sigma(p,e) for p,e in P0); floor=dict(P0)
        forced=(set(roots)|compelled)-floor.keys()
        assert all(all_em%p==0 and prime(p) for p in forced)
        for p in forced:floor[p]=2 if p%4==3 else 1
        for q in bad[len(BAD):]:
            assert prime(q) and q not in floor
            assert abgt2(list(floor.items())+[(q,2 if q%4==3 else 1)]),(h,q)
        ok,X,D,n=exact_state(P0,bad);assert ok
        st=C.State(P0,absent=bad[1:]);assert not st.conflict and (st.X,st.D)==(X,D)
        C.validate_forest(st,roots,edges,head,prime)
        a=C.Forest(st,roots,edges,head).lower()[0]; b=independently(P0,bad,roots,edges,head,(),{})
        L=min(a,b);assert L>B
        mins.append(L);vertices+=len(roots)+len(edges)
        print('final square leaf',h,'floor',len(str(L))-1,'local bans',len(bad)-len(BAD),flush=True)
    assert tuple(rec)==EXPECT and used==set(cert)
    print('PASS last t^2 residual, children',len(rec),'strict tail',tail,'vertices',vertices,'ECPP',len(used),
          'minimum millionths',min(mins)*10**6//B,'sha256',sha256(raw).hexdigest(),flush=True)
    return tuple(PARENT)

if __name__=='__main__':verify()
