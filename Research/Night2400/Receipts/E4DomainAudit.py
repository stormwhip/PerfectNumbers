"""Stdlib-only verification of the exact E4 split structure, scope and size tails."""
import gzip
import json
from collections import Counter
from math import prod
from pathlib import Path

B = 10**2400
Q = 1169407471026387018305554817094515359
R = 120298224779693
ROOT = ((7,420),)
DEEP = ROOT+((Q,6),(R,4),(614161368508213374837480973511596661304038630932974761,4),(31,2),(331,2),(5233,2),(42073,4))
DOMAIN = [2,4,6,10,12,14,16,18,20,22]
N = Path('Research/Night2400/E4/Fibers7x420Complete.json.gz')


def no_duplicates(pairs):
    d=dict(pairs)
    assert len(d)==len(pairs)
    return d


def sigma(q,e):
    return (q**(e+1)-1)//(q-1)


def v(n,q):
    e=0
    while n%q==0:
        n//=q
        e+=1
    return e


def accounting(P):
    X=prod(q**e for q,e in P)
    S=prod(sigma(q,e) for q,e in P)
    D=S >> v(S,2)
    reasons=[]
    if D%19==0:
        reasons.append('ban')
    for q,e in P:
        a=v(D,q)
        if a>e: reasons.append('incoming')
        D//=q**a
    if X*D>B: reasons.append('size')
    if S>2*X: reasons.append('abundancy')
    return X,S,D,reasons


def independent_domain(P,q):
    X,S,D,reasons=accounting(P)
    assert not reasons and q not in (19,*dict(P)) and D%q==0
    first=v(D,q)
    K=X*(D//q**first)
    e=first
    multiplier=q**e
    live=[]; direct={}; parity=[]; ban=[]
    while K*multiplier<=B:
        if e%2 and ((q%4,e%4)!=(1,1) or any(f%2 for p,f in P)):
            parity.append(e)
        elif sigma(q,e)%19==0:
            ban.append(e)
        else:
            why=accounting(P+((q,e),))[3]
            if why: direct[e]=why
            else: live.append(e)
        e+=1
        multiplier*=q
    assert K*q**(e-1)<=B<K*q**e
    assert len(live)+len(direct)+len(parity)+len(ban)==e-first
    print('DOMAIN',P,'pivot',q,'valuation',first,'tail',e,'tail_floor',len(str(K*q**e))-1,'live',live,'direct',direct,'parity',parity,'ban',ban,flush=True)
    return live,direct,e


def main():
    with gzip.open(N,'rt',encoding='utf-8') as f:
        d=json.load(f,object_pairs_hook=no_duplicates)
    assert (d['p'],d['e'],d['pivot'])==(7,420,Q)
    with Path('Research/Session20261126/Delta.json').open(encoding='utf-8') as f:
        shards=json.load(f)['remaining_shards']
    rows=[r for r in shards if r['root']==7 and 420 in r['remaining_actuals']]
    assert len(rows)==1 and rows[0]['id']=='P7_I00081' and rows[0]['remaining_actuals']==[420] and rows[0]['index']==81
    print('SHARD',rows[0],flush=True)
    count=Counter(); prices={}; deepest=False
    def walk(P,t):
        nonlocal deepest
        typ=t['type']; count[typ]+=1
        assert not accounting(P)[3]
        if typ=='forest':
            assert set(t)=={'type','roots','owners','head'}
        elif typ=='price':
            assert set(t)=={'type','targets'}
            prices[P]=t['targets']
        else:
            assert typ=='split' and set(t)=={'type','q','cases'}
            kids,direct,tail=independent_domain(P,t['q']); count['direct']+=len(direct)
            assert set(map(str,kids))==t['cases'].keys()
            if P==DEEP:
                assert t['q']==284860058207025151 and kids==list(range(2,23,2)) and tail==45
                deepest=True
            for e in kids:
                walk(P+((t['q'],e),),t['cases'][str(e)])
    live,direct,tail=independent_domain(ROOT,Q)
    assert live==DOMAIN and set(map(str,live))==d['cases'].keys() and tail==48
    assert sorted(direct)==[24,28,30,32,34,36,38,40,42,46]
    count['direct']+=len(direct)
    for e in live:
        walk(ROOT+((Q,e),),d['cases'][str(e)])
    assert deepest and prices=={ROOT+((Q,6),(R,30)):[0,1,2], ROOT+((Q,22),):[1]}
    print('TALLY',dict(count),'PRICES',prices,'ECPP',len(d['ecpp']))


if __name__=='__main__':
    assert __debug__
    main()
