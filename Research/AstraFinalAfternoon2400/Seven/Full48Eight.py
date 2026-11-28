"""Complete canonical (7,48) t^8 with three integer-forest support cases."""
from functools import cache
import gzip,json
from hashlib import sha256
from math import gcd,prod
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from VerifyForest import C,B,S48,abgt2,sig,exact_state,val,known_scope
P0=[(7,48),(S48,8)]

def independently(P,bad,roots,edges,head,present,lo):
    ok,X,D,fixed_euler=exact_state(P,bad); assert ok
    banned=prod(bad); pool=X*D*prod(set(roots)|{z for z,_ in edges})
    K=[(p,max(1,val(D,p),lo.get(p,0))) for p in roots]
    kids={p:[] for p in roots}
    for p,q in edges:kids[p]=[]
    for p,q in edges:kids[q].append(p)
    @cache
    def solve(p,k):
        a=b=B+1
        for odd in (False,True):
            if odd and (fixed_euler or p%4!=1 or gcd(p+1,banned)>1):continue
            e=k+((1-k)%4 if odd else k%2); step=4 if odd else 2; n=0
            while n<head and (ph:=p**e)<(b if odd else a):
                s=(p*ph-1)//(p-1)
                if gcd(s,banned)==1:
                    n+=1; s//=1+int(odd); d=s
                    while (g:=gcd(d,pool))>1:d//=g
                    sub=[solve(q,val(s,q)) for q in kids[p] if s%q==0]
                    z=ph*d*prod(x for x,y in sub)
                    if not odd:
                        a=min(a,z)
                        if not fixed_euler:z=min([z]+[z//x*y for x,y in sub])
                    b=min(b,z)
                e+=step
            if not odd:a=min(a,p**e)
            b=min(b,p**e)
        return a,a if fixed_euler else b
    X*=D//prod(p**val(D,p) for p,h in K)
    r=[solve(p,h) for p,h in K]; a=X*prod(u for u,v in r)
    return min([a]+[a//u*v for u,v in r])


def verify(path):
    assert __debug__; data=path.read_bytes(); pack=json.loads(gzip.decompress(data)); assert set(pack)=={'records','ecpp'}
    seen=set(); bins=set()
    @cache
    def prime(n):
        assert type(n)==int and n>2
        q=n
        if q>=2**64:
            k=str(q);seen.add(k)
            for row in pack['ecpp'][k]:assert row[0]==q;q=C.pc.level(*row)
        return C.pc.prime64(q)
    assert all(prime(q) for q in (3,5,7,11,13,19,29,61,S48)) and known_scope(P0,(19,))=='48'
    assert sig(7,48)%29==sig(S48,8)%61==0
    # Whenever 3 occurs, it has at least exponent two. 5 gives excess.
    u=[(7,48),(29,1),(61,1),(3,2)]
    assert abgt2(u+[(5,1)])
    # If 11 occurs it is ordinary, and its square emits forbidden 19.
    assert 3%4==11%4==3 and sig(11,2)%19==0
    u1=[(7,48),(29,1),(61,1),(3,4),(11,4)]
    assert abgt2(u1) and sig(3,2)==13 and abgt2(u+[(11,4),(13,1)])
    # Thus if 3 occurs, 5 and 11 are absent. 3^4 is then impossible since
    # its geometric sum is 121. The exact domains are v3=0, v3=2, v3>=6 even.
    assert sig(3,4)==11*11
    for r in pack['records']:
        assert not r['unresolved']; P=list(map(tuple,r['P'])); bad=tuple(r['bad']); present=tuple(r.get('present',())); lo=dict(r.get('lo',()))
        assert all(prime(q) for q,h in P)
        if bad==(19,3):
            k=0; assert P==P0 and not present and not lo and set(r)=={'P','bad','tree','unresolved'}
        elif P==P0+[(3,2)]:
            k=2; assert bad==(19,5,11) and not present and not lo and set(r)=={'P','bad','tree','unresolved'}
        else:
            k=6; assert P==P0 and bad==(19,5,11) and present==(3,) and lo=={3:6} and set(r)=={'P','bad','present','lo','tree','unresolved'}
        assert k not in bins; bins.add(k)
        s=C.State(P,present=present,absent=bad[1:],lo=lo); t=r['tree']; assert s.bad==bad and exact_state(P,bad)[0] and not s.conflict
        assert set(t)=={'type','roots','owners','head'} and t['type']=='forest'
        rt,es,head=t['roots'],t['owners'],t['head']; C.validate_forest(s,rt,es,head,prime); assert not set(present)-set(rt)
        a=C.Forest(s,rt,es,head).lower()[0]; b=independently(P,bad,rt,es,head,present,lo)
        assert min(a,b)>B
        print('v3 case',k,'strict millionths',min(a,b)*10**6//B,'vertices',len(rt)+len(es),flush=True)
    assert bins=={0,2,6} and seen==set(pack['ecpp'])
    print('PASS complete (7,48) first v_t=8; ECPP',len(seen),'SHA256',sha256(data).hexdigest(),flush=True)

if __name__=='__main__':verify(H/'Forest48Eight.json.gz')
