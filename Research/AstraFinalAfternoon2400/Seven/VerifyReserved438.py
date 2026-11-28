"""Authenticate the Euler-exponent-one prerequisite and independently replay reserved forests."""
from functools import cache
import gzip
from hashlib import sha256
import json
from math import gcd, isqrt, prod
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
R=H.parents[1]
sys.path.insert(0,str(H))
from VerifyForest import C, B, known_scope, sig, val
from ReservedForest import reserve
sys.path.insert(0,str(R/'FinalNight2400/Seven'))
from Verify438 import prove_prime

T=572749682520506652634407616247
M=T**9
LOW=2*M-1
MOD=4*M
BASE=[(7,438),(T,10)]
PACKS={'d':[14,20,44,48,56,60,62,82], 'e':[10,18,32,40,46,124], 'f':[4,6,24,80], 'g':[8,26], 'h':[2]}

def rule(first=10):
    """Exact source domain, without any incoming weighted price / Hensel table."""
    assert first in (10,12)
    prove_prime(T)
    X=7**438*T**first; A0=sig(7,438); A=A0//T; D=sig(T,first)
    m=T**(first-1); low=2*m-1; mod=4*m
    assert val(A0,T)==1 and D%T==1 and gcd(X,A*D)==1 and gcd(A,D)==1
    assert T>5100 and 3**5100>B and (T-1)%4==2
    assert [d for d in range(3,5101,2) if (T-1)%d==0]==[439]
    # h+1<=5100<T: no LTE length shift or order-one source. Ordinary
    # order is 439; any Euler source of order 439 or 878 needs length >=878.
    z=3; c1=0
    while X*z**438<=B:
        if z not in (7,T,19) and pow(z,439,T)==1:
            if C.pc.prime64(z):
                c1+=1
                assert X*(A*D//z**val(A*D,z))*z**438>B
        z+=2
    q=5; c2=0
    while X*q**877<=B:
        if q not in (7,T,19) and pow(q,878,T)==1 and pow(q,2,T)!=1:
            if C.pc.prime64(q): c2+=1
        q+=4
    assert c2==0
    # Thus Euler's q+1 supplies all 9 residual t units. Since q≡1 mod4,
    # q≡LOW mod MOD. q cannot divide A by the complete cofactor interval.
    inv=pow(low,-1,mod)
    k=A*inv%mod or mod; upper=A//low
    assert upper<k or (upper-k<mod and A%k!=0)
    # If q|D, then ord_q(T) divides first+1, odd, so (T/q)=1; reciprocity for
    # q≡1 mod4 and q≡−1 mod T (T≡3 mod4) instead gives (T/q)=−1.
    assert T%4==3 and X*A*D*low**5>B
    print('Euler rule: ordinary candidate hits, endpoint, Euler hits, endpoint:',c1,z,c2,q,flush=True)


def independent(P,roots,edges,head,m=M):
    """Second evaluator: division over the whole cofactor progression, no shared rebate code."""
    X=prod(p**h for p,h in P); D=prod(sig(p,h) for p,h in P)
    factors={p for p,h in P}
    def strip(a,F):
        for p in F:
            while a%p==0:a//=p
        return a
    D=strip(D,factors); children={p:[] for p in roots}
    for q,p in edges:children[q]=[]
    for q,p in edges:children[p].append(q)
    low=2*m-1; mod=4*m; inv=pow(low,-1,mod)
    @cache
    def without_q(z):
        # An output factor can use q no more than once since q||N.
        lim=z//low; k=z*inv%mod or mod
        if lim<k:return z
        if k+mod>lim and z%k:return z
        return k
    @cache
    def lower(p,v):
        h=v+v%2; used=0; candidates=[]
        best=B+1
        while used<head and (ph:=p**h)<best:
            S=sig(p,h)
            if S%19:
                used+=1
                cleaned=S
                pool=X*D*prod(children)
                while (g:=gcd(cleaned,pool))>1:cleaned//=g
                candidates.append(ph*without_q(cleaned)*prod(lower(q,val(S,q)) for q in children[p] if S%q==0))
                best=min(best,candidates[-1])
            h+=2
        # Match an unconditional monotone tail, even with no admitted finite cell.
        return min(candidates+[p**h])
    return X*low*without_q(strip(D,roots))*prod(lower(p,val(D,p)) for p in roots)


def verify(kind):
    path=H/f'Forest438{kind}.json.gz'; raw=path.read_bytes(); data=json.loads(gzip.decompress(raw))
    assert set(data)=={'records','ecpp'}; used=set(); tested=[]
    @cache
    def prime(p):
        q=p
        if q>=2**64:
            k=str(p); used.add(k)
            for step in data['ecpp'][k]:assert step[0]==q; q=C.pc.level(*step)
        return C.pc.prime64(q)
    for r in data['records']:
        assert set(r)=={'P','bad','tree','unresolved'} and r['bad']==[19] and not r['unresolved']
        P=list(map(tuple,r['P'])); assert len(P)==3 and P[:2]==BASE and P[-1][0]==67 and all(prime(p) for p,h in P)
        assert known_scope(P,(19,))=='438'; tested.append(P[-1][1]); n=r['tree']; assert set(n)=={'roots','owners','head','type'} and n['type']=='reserve'
        roots=n['roots']; es=n['owners']; head=n['head']; C.validate_forest(C.State(P),roots,es,head,prime)
        assert all(p%MOD!=LOW for p in set(roots)|{q for q,_ in es})
        a=reserve(P,roots,es,head,(19,),M,exact_one=True)
        b=independent(P,roots,es,head)
        assert min(a,b)>B
        print(P[-1][1],'strict minimum millionths',min(a,b)*10**6//B,flush=True)
    assert tested==PACKS[kind] and used==set(data['ecpp'])
    print('PASS 438'+kind,tested,'ECPP',len(used),'SHA256',sha256(raw).hexdigest(),flush=True)

if __name__=='__main__':
    assert __debug__; rule()
    for kind in sys.argv[1:] or PACKS:verify(kind)
