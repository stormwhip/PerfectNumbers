"""Discovery only: terminal residual LP conditioned on exact assigned factor components.

Use full sigma product modulo assigned support; a fixed component may contain
Euler or permit it elsewhere. Prices relax all multiplicities not represented
by a disjoint anonymous charge or an explicit forced-prime row.
"""
import gzip
from functools import cache
import json
from math import gcd, log, log10, prod
from pathlib import Path
import sys
from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE=Path(__file__).resolve().parent; R=HERE.parents[1]
sys.path.insert(0,str(R/'Session20261122'/'Python'))
from TerminalCertificate import odd_primes, sigma, allowed
from TerminalPilot import bank, vp, supply, BAD


def solve(xs, pref=(), count_supply=False, noref=False):
    e=xs[0][1]
    cfg={p:f for p,f in xs}; gone=set(cfg); early=any(f%2 for f in cfg.values())
    X=prod(p**f for p,f in xs); S=prod(sigma(p,f) for p,f in xs); D=S//gcd(2*X,S)
    if X*D>10**2400 or gcd(D,X*prod(BAD))>1 or vp(S)>e:
        return ('arithmetic',)
    E,promoted,blocks=bank(); base={p:32 for p in odd_primes(5000) if p not in BAD};
    base.update({p:max(f,base.get(p,0)) for p,f in promoted.items() if p not in BAD})
    groups={};opts={};C=[];ab=[];eu=[];unit=[]
    E={key:v for key,v in E.items() if not (early and key[1]%2)}
    for p,f,q in E:
        base[p]=max(f,base.get(p,0));base.setdefault(q,0)
    for q in pref:
        base.setdefault(q,0)
    for p in gone:base.pop(p,None)
    forced={};D0=D
    for p in base:
        c=vp(D0,p)
        if c:
            D0//=p**c
            forced[p]=c
    def add(p,f,odd,exact):
        if exact and f<forced.get(p,0):return
        j=len(C);groups.setdefault(p,[]).append((j,f,odd,exact));
        if exact:opts[p,f]=j
        C.append(max(f,forced.get(p,0))*log10(p))
        ab.append(log(sigma(p,f)/p**f) if exact else log(1+1/(p-1)))
        if odd:eu.append(j)
        unit.append(supply(p,f) if exact else (5 if p%5==1 else 5+vp(p+1) if odd and p%5==4 else 0))
    for p,cap in sorted(base.items()):
        for f,d,odd in [(2,2,False),(1,4,True)]:
            if odd and (early or p%4!=1 or not allowed(p,1,BAD)):continue
            for j in range(f,cap+1,d):
                if allowed(p,j,BAD):add(p,j,odd,True)
            j=f+d*max(0,(cap-f)//d+1)
            while not allowed(p,j,BAD):j+=d
            add(p,j,odd,False)
    occupied=prod(base)*X*D0; used={}; refund=[]
    for (p,f),(V,L) in blocks.items():
        if (p,f) not in opts:continue
        support=occupied*prod(v for q,v in used.items() if q!=p)
        while (g:=gcd(V,support))>1:V//=g
        if V<=1:continue
        used[p]=V*used.get(p,1)
        j=opts[p,f];C[j]+=log10(V);ab[j]+=int(log(V)/log(L))*log(1+1/(L-1))
        if __import__('math').isqrt(V)**2!=V:
            C[j]+=log10(L)
            if not early and V%4==1 and not noref:
                k=len(C); C.append(-log10(L)); ab.append(0);unit.append(0);eu.append(k);refund.append(([(k,1),(j,-1)],0))
            elif not early and V%4==1 and noref:
                C[j]-=log10(L)
        unit[j]+=log10(V)/(4*log10(5001))
    tail=len(C);C.extend([1,0,0]);ab.extend([0,1,0]);unit.extend([0,0,1]);L=5001
    if not early:
        j=len(C);eu.append(j);C.append(log10(L));ab.append(log(1+1/(L-1)));unit.append(e)
    target=log(2)-log(S/X)-int(log(D0)/log(L))*log(1+1/(L-1))
    rows=[(list(enumerate(-v for v in ab)), -target), ([(tail,-1),(tail+1,2*log10(L)/log(1+1/(L-1)))],0)]
    if count_supply:
        rows.extend((([(tail,-1),(tail+2,4*log10(L))],0), ([(j,-u) for j,u in enumerate(unit) if u], -(e-vp(S)-log10(D0)/(4*log10(L))))))
    if not early:rows.append(([(j,1) for j in eu],1))
    rows += [([(j,1) for j,*_ in g],1) for g in groups.values()]
    rows += [([(j,-1) for j,*_ in groups[p]],-1) for p in forced]
    for (p,f,q),c in E.items():
        if q in gone or (p,f) not in opts:continue
        i=opts[p,f]; rows.append(([(i,1)]+[(j,-1) for j,jf,od,ex in groups[q] if (not od or not f%2) and (not ex or jf>=c)],0))
    rows.extend(refund)
    rr=[];cc=[];vv=[];rhs=[]
    for i,(terms,b) in enumerate(rows):
        rhs.append(b)
        for j,v in terms:rr.append(i);cc.append(j);vv.append(v)
    z=linprog(C,A_ub=coo_matrix((vv,(rr,cc)),shape=(len(rows),len(C))).tocsr(),b_ub=rhs,bounds=[(0,None) if tail<=j<tail+3 else (0,1) for j in range(len(C))],method='highs')
    return (round(log10(X*D0)+z.fun,3),len(C),len(rows),len(forced)) if z.success else (z.message,)


if __name__=='__main__':
    H=R.parents[1]/'overnight'/'Research'/'NightFive'
    for e in (48,52,42,40,30,28):
        d=json.loads((H/f'ConditionForest{e}.json').read_bytes())
        for a,v in d.items():
            xs=[(int(p),f) for p,f in v['x']]
            print(e,a,solve(xs,v['roots']),flush=True)
