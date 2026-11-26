"""Independent exact size, parity and forbidden-emission partitions for B."""
from collections import Counter
from pathlib import Path
from math import gcd,isqrt,prod
import gzip,json,sys

B=10**2400
BAN=(19,7,11,31,13)
Z=prod(BAN)
Q=797161
P=((3,12),)


def sigma(p,f):return (p**(f+1)-1)//(p-1)

def v(n,p):
    e=0
    while n%p==0:
        n//=p;e+=1
    return e

def state(P):
    X=prod(p**f for p,f in P)
    S=prod(sigma(p,f) for p,f in P)
    D=S>>v(S,2)
    if gcd(D,Z)>1:return X,S,D,'forbidden'
    if S>2*X:return X,S,D,'abundant'
    for p,f in P:
        m=v(D,p)
        if m>f:return X,S,D,'overflow'
        D//=p**m
    return X,S,D,'size' if X*D>B else None

def expand(P,q):
    X,S,D,why=state(P)
    assert why is None and q not in (*BAN,*dict(P)) and D%q==0
    v0=v(D,q)
    L=X*(D//q**v0)
    e=v0
    w=X*D
    live=set(); no=Counter()
    while w<=B:
        if e%2 and ((q%4,e%4)!=(1,1) or any(h%2 for p,h in P)):
            why='Euler'
        else:
            why=state(P+((q,e),))[3]
        if why is None:live.add(e)
        else:no[why]+=1
        e+=1; w*=q
    assert len(live)+sum(no.values())==e-v0 and L*q**(e-1)<=B<L*q**e
    return live,e,no

def key_check(pairs):
    d=dict(pairs);assert len(d)==len(pairs);return d

def main(files):
    assert sigma(3,12)==Q and all(Q%d for d in range(2,isqrt(Q)+1))
    live,tail,why=expand(P,Q)
    assert len(live)==100 and tail==406
    archive=set()
    for name in ('Session20261126/LowBranches','FinalSprint/LowBranches','FinalSprint/LowBranches/Wave2','FinalSprint/LowBranches/Wave3','FinalSprint/LowBranches/Wave4'):
        with gzip.open(Path('Research')/name/'Branches.json.gz','rt',encoding='utf-8') as f:
            records=json.load(f,object_pairs_hook=key_check)['roots']
        for e,q,data in records:
            if (e,q)==(12,Q):
                a=set(map(int,data))
                assert a<=live and not a&archive
                archive|=a
    assert live-archive=={1,2,66,96}
    print('FIRST',len(live),'tail',tail,'exclusions',dict(why),'uncovered',sorted(live-archive),flush=True)
    for file in files:
        with gzip.open(file,'rt',encoding='utf-8') as s:d=json.load(s,object_pairs_hook=key_check)
        f=d['f']; t=d['tree']; q=t['q']
        assert f in live-archive and q=={1:398581,2:22996651,66:5897}[f]
        pref=P+((Q,f),)
        kids,tail,why=expand(pref,q)
        covered={int(e) for e in t['cases']}
        assert covered<=kids
        count=Counter()
        def walk(P,t):
            typ=t['type'];count[typ]+=1
            if typ=='split':
                q=t['q'];kids,tail,why=expand(P,q)
                assert set(map(str,kids))==t['cases'].keys()
                print('SPLIT',P,'pivot',q,'live',len(kids),'tail',tail,'excluded',dict(why),flush=True)
                for e in kids:walk(P+((q,e),),t['cases'][str(e)])
            elif typ=='supplier-split':
                # Exact supplier-option enumeration is left to the candidate's cold run.
                for k,row in t['cases'].items():walk(P+(tuple(map(int,k.split(':'))),),row)
            else:assert typ in ('joint-valuation','forest','order-budget')
        for e in covered:walk(pref+((q,e),),t['cases'][str(e)])
        print('SECONDARY',f,q,'live',len(kids),'covered',len(covered),'raw_open',sorted(kids-covered),'tail',tail,'pruned',dict(why),'counts',dict(count),'ecpp',len(d['ecpp']),flush=True)

if __name__=='__main__':
    assert __debug__
    main(sys.argv[1:])
