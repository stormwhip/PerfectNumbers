"""Independent A78 delta and separate 64-mask support partition. Stdlib only."""
import gzip
import json
import subprocess
import sys
from collections import Counter
from fractions import Fraction
from functools import cache
from math import gcd, isqrt, prod
from pathlib import Path

B = 10**2400
Q = 16148168401
BASE = '82a52f1ac637641249dd9b7a5cab7de6acc14da6'
DIR = Path('Research/Night2400/A')


def sigma(p,e):
    return (p**(e+1)-1)//(p-1)


def v(n,p):
    h = 0
    while n%p == 0:
        n //= p
        h += 1
    return h


def data(compressed):
    def unique(pairs):
        d = dict(pairs)
        assert len(d) == len(pairs)
        return d
    return json.loads(gzip.decompress(compressed), object_pairs_hook=unique)


def fixed(prefix, banned):
    X = prod(q**e for q,e in prefix)
    S = prod(sigma(q,e) for q,e in prefix)
    D = S >> v(S,2)
    reasons = set()
    if any(D%p == 0 for p in banned):
        reasons.add('forbidden')
    if sum(e%2 for q,e in prefix)>1 or any(e%2 and (q%4,e%4)!=(1,1) for q,e in prefix):
        reasons.add('Euler')
    for q,e in prefix:
        h = v(D,q)
        if h>e:
            reasons.add('overflow')
        D //= q**h
    if X*D>B:
        reasons.add('size')
    if S>2*X:
        reasons.add('ratio')
    return X,S,D,reasons


def ratio(p,e):
    return Fraction(sigma(p,e),p**e)


def delta():
    path = DIR/'Fibers12.json.gz'
    old = data(subprocess.check_output(['git','show',f'{BASE}:{path.as_posix()}']))
    d = data(path.read_bytes())
    assert old['pivot']==d['pivot']==Q and old['pair']==d['pair']==[7,12]
    assert all(d['cases'][k]==obj for k,obj in old['cases'].items())
    assert all(d['ecpp'][k]==obj for k,obj in old['ecpp'].items())
    assert d['cases'].keys()-old['cases'].keys()=={'28'}
    print('UNCHANGED',len(old['cases']),len(old['ecpp']),'new ECPP',len(d['ecpp'])-len(old['ecpp']))
    t = d['cases']['28']
    p = t['q']
    pref = ((7,12),(Q,28))
    X,S,D,reasons = fixed(pref,(19,))
    assert not reasons and p not in (7,19,Q) and D%p==0
    h=v(D,p)
    tail=X*(D//p**h)
    e=h
    live=[]
    while tail*p**e <= B:
        ch = pref+((p,e),)
        why=fixed(ch,(19,))[3]
        if not why:
            live.append(e)
        print('P28 CASE',e,'contradictions',sorted(why))
        e+=1
    assert tail*p**(e-1)<=B<tail*p**e
    print('P28 DOMAIN',h,e-1,'TAIL',e,'LIVE',live,'pivot',p)
    assert set(map(str,live))==t['cases'].keys() and live == [1,2]
    a=t['cases']['1']
    r=t['cases']['2']
    assert a=={'type':'abundance','forced':[3,5]} and r['type']=='forest'
    ch=pref+((p,1),)
    x,s,out,why=fixed(ch,(19,))
    assert not why and p%4==1 and out%15==0
    loss=Fraction(s,x)*ratio(3,2)*ratio(5,2)
    assert loss>2
    print('P28 ABUNDANCE','compelled 3^2 5^2','lower ratio exceeds', (loss.numerator*10**12//loss.denominator),'e-12','positive numerator bits',(loss-2).numerator.bit_length())


def stripped(x,P):
    while (g:=gcd(x,P))!=1:
        x//=g
    return x


def forest(X,D,yes,no,t):
    roots=t['roots']; parents=dict(t['owners']); head=t['head']
    labels=set(roots)|parents.keys()
    assert t['type']=='forest' and 1<=head<=1024 and len(roots)==len(set(roots)) and len(parents)==len(t['owners'])
    assert not set(roots)&parents.keys() and set(parents.values())<=labels and not labels&no
    assert labels.isdisjoint((7,Q,110563,226741)) and yes<=set(roots)
    assert all(p in yes or D%p==0 for p in roots)
    assert all(p not in yes and D%p for p in parents)
    children={p:[] for p in labels}
    for child,parent in parents.items():
        children[parent].append(child)
    visited=set()
    def visit(p):
        assert p not in visited
        visited.add(p)
        for c in children[p]: visit(c)
    for r in roots: visit(r)
    assert visited==labels
    pool=X*D*prod(labels)
    ban=prod(no)
    @cache
    def bound(p,incoming):
        f=incoming+(incoming%2)
        qf=p**f
        n=0
        best=B+1
        while n<head and qf<best:
            S=(p*qf-1)//(p-1)
            if gcd(S,ban)==1:
                n+=1
                out=stripped(S,pool)
                a=qf*out
                for c in children[p]:
                    if S%c==0:
                        a*=bound(c,v(S,c))
                best=min(best,a)
            f+=2
            qf*=p*p
        return min(best,qf)
    roots_v={p:v(D,p) for p in roots}
    rest=D//prod(p**h for p,h in roots_v.items())
    return X*rest*prod(bound(p,max(h,1)) for p,h in roots_v.items())


def support():
    pref=((7,12),(Q,1),(110563,2),(226741,2))
    flags=(3,5,11,13,17,31)
    d=data((DIR/'SupportLeaf12.json.gz').read_bytes())
    assert tuple(map(tuple,d['prefix']))==pref
    assert all(all(q%d for d in range(2,isqrt(q)+1)) for q in (*dict(pref),*flags,19))
    assert sigma(7,12)==Q and (Q+1)%110563==0 and sigma(110563,2)%226741==0
    assert sum(e%2 for p,e in pref)==1
    masks=[]
    types=Counter()
    for i in range(64):
        yes={p for j,p in enumerate(flags) if (i>>j)&1}
        no={19}|(set(flags)-yes)
        X,S,D,why=fixed(pref,no)
        if why:
            typ='direct'; detail=sorted(why)
        else:
            lower=Fraction(S,X)
            exps=[]
            for p in sorted(yes):
                h=max(1,v(D,p)); h+=h%2
                while any(sigma(p,h)%q==0 for q in no):
                    assert p**h<=B
                    h+=2
                assert p**h<=B
                lower*=ratio(p,h)
                exps.append((p,h))
            if lower>2:
                typ='abundance'; detail=exps
            else:
                typ='forest'; masks.append(i)
                L=forest(X,D,yes,no,d['masks'][str(i)])
                assert L>B
                detail=len(str(L))-1
        print('MASK',i,typ,detail,flush=True)
        types[typ]+=1
    assert types=={'direct':32,'abundance':23,'forest':9}
    assert set(map(str,masks))==d['masks'].keys() and masks==[1,5,9,17,25,33,37,41,49]
    print('SUPPORT',dict(types),'FOREST MASKS',masks,flush=True)


if __name__=='__main__':
    assert __debug__ and sys.argv[1:] in (['delta'],['support'])
    {'delta':delta,'support':support}[sys.argv[1]]()
