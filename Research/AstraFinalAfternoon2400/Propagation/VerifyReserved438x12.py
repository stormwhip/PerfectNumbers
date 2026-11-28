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
from Verify438x22 import p,r,t,B,T,replay_euler,exact,price_cut
from Propagation import odd_price,screened_prime

LOW=2*T-1
MOD=4*T
ACCEPTED_CORE=(12,14,16,18,20,24)


def replay(path, expected, exact_prefixes=False):
    pack=json.loads(gzip.decompress(path.read_bytes()))
    assert set(pack)=={'records','ecpp'}
    docs=pack['records']; ecpp=pack['ecpp']; seen=set(); mins=[]; stats=[0,0]
    if exact_prefixes:
        assert [[tuple(x) for x in doc['P']] for doc in docs]==expected
    else:
        assert [tuple(doc['P'][2]) for doc in docs]==[(r,h) for h in expected]

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

    def may(z): return z not in (p,r,t,19) and screened_prime(z)

    @cache
    def U(h):
        assert gcd(3*p,r*((r-1)//2))==1
        return odd_price(p,438,2,1,B,5100,may)[0]*odd_price(r,h,4,1,B,5100,may)[0]

    splits=prices=0
    def walk(P,tree):
        nonlocal splits,prices
        X,S,D,c,bad=exact(P)
        assert not bad and all(q%MOD!=LOW and h%2==0 and prime(q) for q,h in P)
        if tree['type']=='reserve':return forest(P,D,tree)
        if tree['type']=='credits':
            assert set(tree)=={'type','labels'}
            z=tree['labels']; assert len(z)==len(set(z)) and not ({q for q,h in P}&set(z))
            assert all(q<LOW and q!=19 and D%q==0 and prime(q) for q in z)
            statistics=price_cut(P,z,U(P[2][1]),prime); prices+=1
            print('price leaf',P[2:],statistics,flush=True)
            return
        assert set(tree)=={'type','anchor','cases'} and tree['type']=='split'
        q=tree['anchor']; cases=tree['cases']; splits+=1
        assert prime(q) and q%MOD!=LOW and q!=19 and all(q!=x for x,h in P) and D%q==0
        v=val(D,q); k=v+v%2; keys=[]
        # Multiply LOW into the parent tail only if q_Euler is known
        # coprime to the entire paid parent D. Do the same in each child.
        extra=LOW if outside_progression(D,LOW,MOD,LOW,B//X) else 1
        while X*(D//q**v)*q**k*extra<=B:
            F=P+[(q,k)]; X1,S1,D1,c1,invalid=exact(F)
            if not invalid and (not outside_progression(D1,LOW,MOD,LOW,B//X1) or X1*D1*LOW<=B):
                keys.append(str(k));walk(F,cases[str(k)])
            k+=2
        assert set(keys)==set(cases)

    for doc in docs:
        P=list(map(tuple,doc['P'])); assert (exact_prefixes or len(P)==3) and P[:2]==[(p,438),(t,12)]
        i=len(mins);walk(P,doc['tree'])
        print(P[2:],'strict minimum millionths across unpriced leaves',min(mins[i:],default=None),flush=True)
    assert seen==set(ecpp)
    print('PASS t^12 secondary fibers',list(expected),'forests, vertices',stats,'splits',splits,'prices',prices,'ECPP',len(seen),'min scaled bound',min(mins,default=None),flush=True)
    return {tuple(sorted(map(tuple,doc['P']))) for doc in docs}


def verify_h2_cuts(tags=('sub2','price2','high2')):
    """Authenticate the exact leaves and return their canonical sorted prefixes.

    Callers must select their own non-overlapping subset and verify each
    delegated leaf is actually reached by their exhaustive exact tree.
    """
    assert __debug__
    replay_euler()
    base=[(p,438),(t,12),(r,2)]; a=752487193; c=50047294070406095227
    cases={'sub2':[base+[(a,28)],base+[(a,22),(c,2)]],
           'price2':[base+[(a,22),(c,k)] for k in (8,10,12)],
           'high2':[base+[(a,k)] for k in (46,52)]}
    assert len(tags)==len(set(tags)) and set(tags)<=cases.keys()
    return set().union(*(replay(H/f'Reserved438x12-{tag}.json.gz',cases[tag],True) for tag in tags))

if __name__=='__main__':
    assert __debug__
    if sys.argv[1:] in (['sub2'],['price2'],['high2']):
        verify_h2_cuts(tuple(sys.argv[1:]))
    else:
        replay_euler()
        args=tuple(map(int,sys.argv[1:])) or ACCEPTED_CORE
        assert len(args)==len(set(args)) and all(2<=h<=26 and h%2==0 and h!=22 for h in args)
        replay(H/('Reserved438x12-'+'-'.join(map(str,args))+'.json.gz'),args)
