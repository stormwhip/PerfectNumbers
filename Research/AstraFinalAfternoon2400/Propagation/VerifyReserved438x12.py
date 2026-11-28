"""Verify exact Euler-reserved factor forests at canonical (7,438), t^12."""
from functools import cache
from math import gcd, prod
from pathlib import Path
import gzip, json, sys
H=Path(__file__).resolve().parent
R=H.parents[1]
sys.path[:0]=[str(H),str(R/'RootFiveNext')]
from Propagation import part, sigma, val, outside_progression
from PrimeCheck import level, prime64
from Verify438x22 import p,r,t,B,T,replay_euler,exact

LOW=2*T-1
MOD=4*T
ACCEPTED_CORE=(12,14,16,18,20,24)


def replay(path, expected):
    pack=json.loads(gzip.decompress(path.read_bytes()))
    assert set(pack)=={'records','ecpp'}
    docs=pack['records']; ecpp=pack['ecpp']; seen=set(); mins=[]; stats=[0,0]
    assert [tuple(doc['P'][-1]) for doc in docs]==[(r,h) for h in expected]

    @cache
    def prime(x):
        if x==t:return True  # separately authenticated by replay_euler
        if x<2**64:return prime64(x)
        y=x; k=str(x); rows=ecpp[k]; assert rows
        seen.add(k)
        for row in rows:
            assert row[0]==y; y=level(*row)
        return prime64(y)

    @cache
    def without_q(block):
        """Lower bound for the exact part of block coprime to the Euler prime."""
        upper=block//LOW
        if upper==0:return block
        residue=block*pow(LOW,-1,MOD)%MOD or MOD
        return block if residue>upper or (residue+MOD>upper and block%residue) else residue

    def forest(P,D,tree):
        assert set(tree)=={'type','roots','owners','head'} and tree['type']=='reserve'
        head=tree['head']; assert type(head)==int and 1<=head<=4096
        roots=tree['roots']; assert len(roots)==len(set(roots)) and all(D%z==0 for z in roots)
        owners={q:w for q,w in tree['owners']}; assert len(owners)==len(tree['owners'])
        assert not (set(roots)&owners.keys())
        nodes=set(roots)|owners.keys(); bases={q for q,h in P}
        assert all(q%MOD!=LOW and q not in bases and q!=19 and prime(q) for q in nodes)
        assert all(w in nodes and D%q!=0 and q!=w for q,w in owners.items())
        kids={z:[] for z in nodes}
        for q,w in owners.items():kids[w].append(q)
        done=set(); stack=list(roots)
        while stack:
            z=stack.pop(); assert z not in done; done.add(z); stack.extend(kids[z])
        assert done==nodes
        stats[0]+=1; stats[1]+=len(nodes)
        X=prod(q**h for q,h in P); pool=X*D*prod(nodes)
        left=D//part(D,prod(roots))

        @cache
        def lower(q,v):
            h=v+v%2; best=B+1; visited=0
            while q**h<best and visited<head:
                Q=q**h; s=sigma(q,h)
                if s%19:
                    visited+=1
                    cleaned=s//part(s,pool)
                    value=Q*without_q(cleaned)*prod(lower(z,val(s,z)) for z in kids[q] if s%z==0)
                    best=min(best,value)
                h+=2
            return min(best,q**h)

        @cache
        def audit(q,v):
            # A distinct recursion, pure progression divisor testing instead
            # of a single cached residual transform. Remove only exact support.
            k=v+v%2; hits=0; candidates=[]; floor=B+1; pw=q**k
            while hits<head and pw<floor:
                em=(pw*q-1)//(q-1)
                if gcd(em,19)==1:
                    hits+=1; rem=em
                    while (g:=gcd(rem,pool))>1:rem//=g
                    top=rem//LOW
                    x=rem*LOW%MOD or MOD  # LOW inverse is LOW
                    if x<=top and (x+MOD<=top or rem%x==0):rem=x
                    v1=pw*rem
                    for z in kids[q]:
                        if em%z==0: v1*=audit(z,val(em,z))
                    candidates.append(v1);floor=min(floor,v1)
                k+=2;pw*=q*q
            return min([B+1,pw,*candidates])

        assert pow(LOW,2,MOD)==1
        a=X*LOW*without_q(left)*prod(lower(q,val(D,q)) for q in roots)
        b=X*LOW*without_q(left)*prod(audit(q,val(D,q)) for q in roots)
        assert min(a,b)>B
        mins.append(min(a,b)*10**6//B)

    # The shipped release has one forest per h and no splits.
    for doc in docs:
        P=list(map(tuple,doc['P'])); assert len(P)==3 and P[:2]==[(p,438),(t,12)]
        X,S,D,c,bad=exact(P)
        assert not bad and all(q%MOD!=LOW and h%2==0 and prime(q) for q,h in P)
        forest(P,D,doc['tree'])
        print(P[-1][1],'strict minimum millionths',mins[-1],flush=True)
    assert seen==set(ecpp)
    print('PASS t^12 secondary fibers',list(expected),'forests, vertices',stats,'ECPP',len(seen),'min scaled bound',min(mins),flush=True)

if __name__=='__main__':
    assert __debug__
    replay_euler()
    args=tuple(map(int,sys.argv[1:])) or ACCEPTED_CORE
    assert len(args)==len(set(args)) and all(2<=h<=26 and h%2==0 and h!=22 for h in args)
    replay(H/('Reserved438x12-'+'-'.join(map(str,args))+'.json.gz'),args)
