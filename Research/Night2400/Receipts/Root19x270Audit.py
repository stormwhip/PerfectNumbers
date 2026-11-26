"""Rebuild exact domain of root 19 exponent 270 and all internal splits."""
from collections import Counter
from pathlib import Path
from math import prod, gcd
import gzip,json

B=10**2400
Q=107499032325771819886598832053082701603

def sig(p,e):return (p**(e+1)-1)//(p-1)

def val(n,p):
    h=0
    while n%p==0:
        n//=p;h+=1
    return h

def state(P):
    X=prod(p**f for p,f in P); S=prod(sig(p,f) for p,f in P)
    D=S>>val(S,2)
    excess=False
    for p,f in P:
        h=val(D,p)
        excess |= h>f
        D//=p**h
    return X,S,D,excess

def domain(P,r):
    X,S,D,bad=state(P)
    assert r not in dict(P) and not bad and S<=2*X and X*D<=B and D%r==0
    h=val(D,r); base=X*(D//r**h)
    feasible=[]; skipped=[]; direct=[]
    f=h
    while base*r**f<=B:
        if f%2 and ((r%4,f%4)!=(1,1) or any(e%2 for p,e in P)):
            skipped.append(f)
        else:
            N,S,O,overflow=state(P+((r,f),))
            if overflow or N*O>B or S>2*N:
                direct.append(f)
            else:
                feasible.append(f)
        f+=1
    assert base*r**(f-1)<=B<base*r**f
    print('DOMAIN',P,r,'from',h,'tail',f,'live',feasible,'parity',skipped,'direct',direct,flush=True)
    return f,feasible,direct

def unique(pairs):
    d=dict(pairs);assert len(d)==len(pairs);return d

if __name__=='__main__':
    assert __debug__
    p=Path('Research/Night2400/Fibers19x270.json.gz')
    d=json.loads(gzip.decompress(p.read_bytes()),object_pairs_hook=unique)
    assert (d['p'],d['e'],d['pivot'])==(19,270,Q)
    root=((19,270),)
    tail,live,direct=domain(root,Q)
    covered=sorted(map(int,d['cases'])); opened=sorted(set(live)-set(covered))
    assert (tail,covered,opened)==(46,[2,6,8,14,18,20,22],[4,10,12,16])
    counter=Counter(direct=len(direct)); prices=[]
    def visit(P,t):
        tp=t['type'];counter[tp]+=1
        if tp=='split':
            _,kids,dead=domain(P,t['q']);counter['direct']+=len(dead)
            assert set(map(str,kids))==t['cases'].keys()
            for f in kids:visit(P+((t['q'],f),),t['cases'][str(f)])
        elif tp=='price':
            assert P==root+((Q,18),) and t['targets']==[0,1]
            X,S,D,overflow=state(P)
            assert gcd(X,D)==1 and not overflow
            prices.append([f-val(S,q) for q,f in P])
        else: assert tp=='forest'
    for e in covered:visit(root+((Q,e),),d['cases'][str(e)])
    assert len(prices)==1
    print('COUNTS',dict(counter),'open',opened,'ECPP',len(d['ecpp']),'price caps',prices)
