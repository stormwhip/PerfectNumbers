"""Independent exact branch verifier. No size bound; no conditional H closure if one branch survives.
python -I -S -B Verify.py [repository for ledger projection]
"""
from math import isqrt
from fractions import Fraction as F
from functools import cache
from pathlib import Path
import sys,json,importlib.util,hashlib
P8={3,5,7,11,13,17,19,31};RULES=[((3,7,13,19,31),13),((3,5,19,31),5),((3,5,13,19),5)]
@cache
def prime(p):return p>=2 and all(p%j for j in range(2,isqrt(p)+1))
@cache
def sigma(p,f):return (p**(f+1)-1)//(p-1)
@cache
def ab(p,f):return F(sigma(p,f),p**f)
@cache
def factors(n):
    original=n;res={};assert n%2==1
    for u in range(3,10000,2):
        if u*u>n:break
        while n%u==0:n//=u;res[u]=res.get(u,0)+1
    if 1<n<10**8 and prime(n):res[n]=res.get(n,0)+1
    for u,v in res.items():assert u%2==1 and prime(u) and original%u**v==0
    return res

def minimal(p,c,step,ban):
    f=max(1,c);f+=((0 if step==2 else 1)-f)%step
    for j in range(12):
        g=f+step*j
        if all(pow(p,g+1,z*(p-1))!=1 for z in ban):return g
    return f+12*step

def leaf(s,fx,lo):
    ban=P8-s;incoming={};ab0=F(1);odd=0
    for p,f in fx.items():
        assert f>0 and prime(p)
        odd+=f%2;assert not f%2 or p%4==f%4==1
        n=sigma(p,f);ab0*=ab(p,f)
        if any(n%z==0 for z in ban):return 'ban'
        n//=n&-n
        for z,c in factors(n).items():incoming[z]=incoming.get(z,0)+c
    if odd>1:return 'two Euler primes'
    if any(incoming.get(p,0)>f and p!=19 for p,f in fx.items()):return 'incoming'
    coupon=[F(1)]
    for p in s|set(incoming):
        if p in fx:continue
        c=max(1,lo.get(p,0),incoming.get(p,0));h=minimal(p,c,2,ban);v=ab(p,h);ab0*=v
        if odd==0 and p%4==1:coupon.append(ab(p,minimal(p,c,4,ban))/v)
    return 'abundance' if ab0*min(coupon)>2 else None

def branch(s,fx,lo,sequence):
    if leaf(s,fx,lo):return []
    if not sequence:return [(fx,lo)]
    p,cap=sequence[0];assert p in s and p not in fx and p not in lo and cap>=1
    bins=[({**fx,p:h},lo) for h in range(1,cap+1) if h%2==0 or p%4==h%4==1]+[(fx,{**lo,p:cap+1})]
    return [z for a,b in bins for z in branch(s,a,b,sequence[1:])]

def theorem():
    assert __debug__ and sigma(19,2)==3*127
    for H,r in RULES:
        S=set(H);single=branch(S,{19:2},{},[(r,12)])
        assert single==[({19:2,r:1},{})]
        double=branch(S,{19:2},{},[(r,12),(3,12)])
        if H!=(3,5,19,31):assert double==[({19:2,r:1,3:2},{})]
        else:assert double==[({19:2,r:1,3:6},{}),({19:2,r:1,3:12},{}),({19:2,r:1},{3:13})]
        print('e=2 mod 3',H,'surviving Euler prime and source exponents',double)

def ledger(repo):
    R=Path(repo)/'Research';D=R/'Session20261126';base=json.loads((R/'Midday/Delta.json').read_bytes());orig={(z['root'],e) for z in base['remaining_shards'] for e in z['remaining_actuals']};assert len(orig)==244
    spec=importlib.util.spec_from_file_location('FrozenSupport',R/'SupportSplit/Verify.py');sv=importlib.util.module_from_spec(spec);spec.loader.exec_module(sv)
    prior={(p,e,tuple(sorted(h))) for p,e,h,q in sv.WITNESSES}|{(31,8,(3,5,13,31))};live={(p,e,tuple(sorted(h))) for p,e in orig for h in sv.masks(p) if not sv.leaf(p,e,h)}-prior;assert len(live)==6556
    packet={(p,e,tuple(h)) for p,e,h in json.loads((D/'Support/Ledger.json').read_bytes())};hit={a for a in live if not set(a[2])&{3,5,17,19}};old=packet|hit;assert len(old)==413 and old<=live
    filtered={a for a in live-old if a[0]==19 and (a[1]+1)%3==0 and a[2] in {h for h,_ in RULES}};assert len(filtered)==14
    now=(D/'Delta.json').read_bytes();full=set(map(tuple,json.loads(now)['new_actuals']));all_full={a for a in live if a[:2] in full};livebefore=live-old-all_full
    assert {a[:2] for a in livebefore}==orig-full
    print(json.dumps(dict(frozen_open_masks=len(live),known_conditional_exclusions=len(old),new_complete_mask_exclusions=0,sharpened_mask_cells=len(filtered),full_actuals=len(full),surviving_sharpened_cells=sorted(filtered&livebefore),open_triples=len(livebefore),open_actuals=len(orig-full),delta_sha256=hashlib.sha256(now).hexdigest())))
if __name__=='__main__':
    theorem()
    if len(sys.argv)>1:ledger(sys.argv[1])
