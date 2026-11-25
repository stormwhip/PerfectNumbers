"""Exact support-only exclusions on the frozen Midday frontier.

Run from the repository root: python -I -S -B Research/SupportSplit/Verify.py
No third-party dependency, no factorization assumptions, no full shard credit.
"""
from fractions import Fraction as F
from functools import lru_cache
from hashlib import sha1
from math import isqrt
from pathlib import Path
import json

ROOTS=(19,7,11,31,13,3,5,17)
B=10**2400
P=10000
sieve=bytearray(b'\1')*(P+1)
sieve[:2]=b'\0\0'
for n in range(2,isqrt(P)+1):
    if sieve[n]:
        sieve[n*n::n]=b'\0'*((P-n*n)//n+1)
PRIMES=tuple(i for i in range(3,P+1,2) if sieve[i])

@lru_cache(None)
def sigma(r,f):
    return (r**(f+1)-1)//(r-1)

@lru_cache(None)
def abundance(r,f):
    return F(sigma(r,f),r**f)

@lru_cache(None)
def small_factors(n):
    d={}
    for q in PRIMES:
        if q*q>n:
            break
        if n%q==0:
            v=0
            while n%q==0:
                n//=q
                v+=1
            d[q]=v
    if n in PRIMES:
        d[n]=1
    return tuple(d.items())

@lru_cache(None)
def min_exp(r,c,odd,ban):
    if odd and r%4!=1:
        return None
    step=4 if odd else 2
    f=1 if odd else 2
    f+=step*max(0,(c-f+step-1)//step)
    for g in range(f,f+step*40,step):
        if all(pow(r,g+1,q*(r-1))!=1 for q in ban):
            return g
    # A capped search must never be mistaken for an impossibility proof.
    return f

def masks(p):
    tail=ROOTS[ROOTS.index(p)+1:]
    for b in range(1<<len(tail)):
        s=frozenset([p]+[q for j,q in enumerate(tail) if b>>j&1])
        if all(s.intersection((3,5,q)) for q in (7,11,13)):
            yield s

@lru_cache(None)
def component(r,f):
    S=sigma(r,f)
    while S%2==0:
        S//=2
    return S,small_factors(S)

def leaf(p,e,s,fixed=(),tails=()):
    """True only for a proved impossible conditional state."""
    assert len(dict(fixed))==len(fixed) and p not in dict(fixed)
    assert len(dict(tails))==len(tails) and p not in dict(tails)
    assert not set(dict(fixed)).intersection(dict(tails))
    ban=tuple(q for q in ROOTS if q not in s)
    fixed=dict(((p,e),)+tuple(fixed))
    tails=dict(tails)
    assert all(r in PRIMES and f>0 for r,f in fixed.items())
    assert all(r in PRIMES and f>0 for r,f in tails.items())
    if any(r in ban for r in fixed):
        return True
    odd=sum(f%2 for f in fixed.values())
    if odd>1 or any(f%2 and (r%4!=1 or f%4!=1) for r,f in fixed.items()):
        return True
    fac={r:1 for r in s}
    incoming={}
    R=1
    N0=1
    I0=F(1)
    for r,f in fixed.items():
        S,factors=component(r,f)
        if any(S%q==0 for q in ban):
            return True
        R*=S
        N0*=r**f
        I0*=abundance(r,f)
        for q,v in factors:
            incoming[q]=incoming.get(q,0)+v
    for q,v in incoming.items():
        fac[q]=max(fac.get(q,0),v)
    for r,f in fixed.items():
        if fac.get(r,0)>f:
            return True
        fac.pop(r,None)
        while R%r==0:
            R//=r
    ar=[F(1)]
    sr=[F(1)]
    for r,c in fac.items():
        while R%r==0:
            R//=r
        c=max(c,tails.get(r,0))
        f=min_exp(r,c,False,ban)
        a=abundance(r,f)
        I0*=a
        N0*=r**f
        g=min_exp(r,c,True,ban)
        if not odd and g is not None:
            ar.append(abundance(r,g)/a)
            sr.append(F(r**g,r**f))
    return I0*min(ar)>2 or N0*R*min(sr)>B

def states(r,cap=8):
    for f in range(1,cap+1):
        if f%2==0 or (r%4==1 and f%4==1):
            yield ((r,f),),()
    yield (),((r,cap+1),)

def check_split(p,e,s,r):
    assert r in s and r!=p
    return all(leaf(p,e,s,f,t) for f,t in states(r))

WITNESSES=[
    (19,2,(3,11,13,17,19,31),13),
    (19,4,(3,11,13,17,19,31),13),
    (19,20,(3,5,13,19),13),
    (19,24,(5,7,11,13,17,19,31),5),
    (19,28,(5,7,11,13,17,19,31),5),
    (19,34,(5,7,11,13,17,19,31),5),
    (19,54,(3,11,13,17,19,31),13),
    (19,92,(3,11,13,17,19,31),13),
]
EXPECTED={19:(70,7000,3263),7:(59,3068,1269),11:(34,816,266),
          31:(17,204,25),13:(27,162,9),3:(37,148,1)}

def main():
    if not __debug__:
        raise RuntimeError("Assertions must be enabled")
    root=Path(__file__).resolve().parents[2]
    raw=(root/"Research/Midday/Delta.json").read_bytes()
    assert sha1(b"blob "+str(len(raw)).encode()+b"\0"+raw).hexdigest()=="3a7b6812aafed3dddd228c34ed9575324d242887"
    d=json.loads(raw)
    pairs={(x["root"],e) for x in d["remaining_shards"] for e in x["remaining_actuals"]}
    assert len(pairs)==244 and all(e%2==0 for p,e in pairs)
    assert d["open"]==204
    base=set()
    universe=set()
    for p,(n,nt,nc) in EXPECTED.items():
        es=sorted(e for q,e in pairs if q==p)
        assert len(es)==n
        cases={(p,e,s) for e in es for s in masks(p)}
        dead={(p,e,s) for p,e,s in cases if leaf(p,e,s)}
        assert (len(cases),len(dead))==(nt,nc)
        universe.update(cases)
        base.update(dead)
        print(p,len(cases),len(dead))
    extra=set()
    for p,e,sp,r in WITNESSES:
        s=frozenset(sp)
        key=(p,e,s)
        assert key in universe-base-extra
        assert check_split(p,e,s,r)
        extra.add(key)
    p,e,s=31,8,frozenset((3,5,13,31))
    key=(p,e,s)
    assert key in universe-base-extra
    pending=[]
    for f,t in states(5):
        if not leaf(p,e,s,f,t):
            pending.append((f,t))
            assert all(leaf(p,e,s,f+g,t+u) for g,u in states(13))
    assert pending==[(((5,2),),())]
    extra.add(key)
    assert len(universe)==11398 and len(base)==4833 and len(extra)==9
    # Independent proof that the entire 15|(e+1) family excludes 5.
    A=sigma(19,14)
    factors=(3,31,127,151,211,911,2460181)
    product=1
    for q in factors:
        product*=q
    assert A==product
    K=abundance(19,14)
    for q in (31,127,151,211,911):
        assert q in PRIMES and q%4==3
        K*=abundance(q,2)
    assert 13 in PRIMES and sigma(3,2)%13==0
    assert 11 in PRIMES and sigma(3,4)%11==0
    assert K*abundance(3,2)*abundance(5,1)*abundance(13,1)>2
    assert K*abundance(3,4)*abundance(5,1)*abundance(11,1)>2
    assert K*abundance(3,6)*abundance(5,1)>2
    for e in (14,44):
        live={s for p,f,s in universe-base-extra if p==19 and f==e}
        assert len(live)==8 and all(3 in s and 31 in s and 5 not in s for s in live)
    fully_closed=[(p,e) for p,e in sorted(pairs)
                  if all((p,e,s) in base|extra for s in masks(p))]
    assert fully_closed==[]
    print(json.dumps({"cases":len(universe),"base":len(base),"extra":len(extra),
                      "remaining":len(universe-base-extra),"new_actuals":fully_closed}))
if __name__=="__main__":
    main()
