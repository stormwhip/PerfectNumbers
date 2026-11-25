"""Exact state-terminal linear relaxation. Only numerical discovery invokes SciPy.

All exact options emit every odd sigma factor outside the explicit support;
these emissions are paid with multiplicity even if anonymous factors overlap.
"""
from collections import defaultdict
from functools import cache
from math import gcd, prod
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Compose import need,pc,sigma,permitted,euler,sig_odd,nonsupport,valuation
sys.path.insert(0,str(H.parents[1]/'Session20261122/Python'))
from RoadblockDual import SCALE,log_bounds,odd_primes

DYADIC=2**24
L=5001
BLOCK_LIMIT=160


def intlog(n,r):
    k=0
    while n>=r:
        n//=r
        k+=1
    return k


@cache
def cutoff_support():
    return tuple(odd_primes(L-1))


def model(s,promoted,edges,prime,logs=log_bounds):
    # Exact fixed components already impose all their sigma valuations.
    need(not s.conflict,'state conflict: use direct')
    base={q:36 for q in cutoff_support() if q not in s.bad and q not in s.rows}
    need(len(dict(promoted))==len(promoted),'duplicate promotions')
    for q,h in promoted:
        need(q not in s.rows and q not in s.bad and prime(q) and type(h)==int and 0<=h<=BLOCK_LIMIT,'promotion')
        base[q]=max(base.get(q,0),h)
    for q in s.present|s.lo.keys():
        if q not in s.rows:
            base.setdefault(q,0)
    # For each emitting option only consider nominated explicit receiving primes.
    # Omitting any nonroot receiver is a relaxation, never an assertion of absence.
    targets=defaultdict(set)
    for r,q in edges:
        need(r in base and q in base and r!=q and q not in targets[r],'edge')
        targets[r].add(q)
    U=prod(base)*prod(s.rows)
    D0=nonsupport(s.D,U)
    need(gcd(D0,prod(cutoff_support()))==1,'residual smooth prime')
    hroot={q:valuation(s.D,q) for q in base}
    capacities={q:f-valuation(s.S,q) for q,f in s.rows.items()}
    need(all(v>=0 for v in capacities.values()),'exact capacity')
    group={}; costs=[]; abund=[]; special=[]; emissions=defaultdict(list)
    # Active fixed Euler means every other prime is ordinary.
    for q,cap in sorted(base.items()):
        g=group[q]=[]
        lo=logs(q)[0]; ab=logs(q,q-1)[1]
        low=max(hroot[q],s.lo.get(q,1))
        for sp in (False,True):
            if sp and (s.fixed_euler or not euler(q,s.bad)):
                continue
            start,step=(1,4) if sp else (2,2)
            f=start+max(0,-((start-low)//step))*step
            while not permitted(q,f,s.bad):
                f+=step
            while True:
                j=len(costs)
                cost=f*lo; benefit=ab; exact=f<=cap
                if exact:
                    A=sig_odd(q,f)
                    C=nonsupport(A,U)
                    cost+=logs(C)[0]
                    benefit=logs(sigma(q,f),q**f)[1]+intlog(C,L)*logs(L,L-1)[1]
                    for r in targets[q]|s.rows.keys():
                        if (v:=valuation(A,r)):
                            emissions[r].append((j,v))
                g.append((j,f,sp,exact));costs.append(cost);abund.append(benefit)
                if sp:special.append(j)
                if not exact:
                    break
                f+=step
                while not permitted(q,f,s.bad):
                    f+=step
    tail=len(costs); tail_h=logs(L,L-1)[1]; tail_cost=logs(L)[0]
    costs.append(2*tail_cost*SCALE//tail_h);abund.append(SCALE)
    if not s.fixed_euler:
        special.append(len(costs));costs.append(tail_cost);abund.append(tail_h)
    free=sum(logs(sigma(q,f),q**f)[1] for q,f in s.rows.items())+intlog(D0,L)*tail_h
    rows=[(list(enumerate(-u for u in abund)),free-logs(2)[0])]
    if not s.fixed_euler:
        rows.append(([(j,SCALE) for j in special],SCALE))
    # Tail valuations can be larger than the modeled minimum. This deliberately
    # loose upper cap still exceeds every exponent allowed by N <= 10^2400.
    caps={q:max(f for j,f,sp,exact in G)+intlog(10**2400,q) for q,G in group.items()}
    for q,G in group.items():
        if emissions[q]:
            rows.append(([(j,SCALE*v) for j,v in emissions[q]]+[(j,-SCALE*(f if exact else caps[q])) for j,f,sp,exact in G],-SCALE*hroot[q]))
    for q in s.rows:
        if emissions[q]:
            rows.append(([(j,SCALE*v) for j,v in emissions[q]],SCALE*capacities[q]))
    # Strengthen aggregate capacity by each emitter's binary implication.
    # Its receiver may be in an unpriced exponent tail, which remains valid.
    for q,G in group.items():
        for j,v in emissions[q]:
            rows.append(([(j,SCALE)]+[(k,-SCALE) for k,a,sp,ex in G if not ex or a>=v+hroot[q]],0))
    required={q for q in group if hroot[q] or q in s.present or q in s.lo}
    gp=[(q,tuple(j for j,*_ in g)) for q,g in group.items()]
    if not s.fixed_euler:
        gp.append((0,(tail+1,)))
    base_cost=logs(s.X*D0)[0]
    return costs,rows,gp,required,tail,base_cost


def price(d,weights):
    costs,rows,gp,required,tail,offset=d
    red=[DYADIC*v for v in costs]
    cst=DYADIC*offset;old=-1
    for i,w in weights:
        need(type(i)==type(w)==int and old<i<len(rows) and w>0,'bad dual')
        for j,a in rows[i][0]:
            red[j]+=w*a
        cst-=w*rows[i][1];old=i
    need(red[tail]>=0,'negative unbounded-tail coefficient')
    return cst + sum(min(red[j] for j in g) if q in required else min(0,*(red[j] for j in g)) for q,g in gp)


def solve(d):
    from scipy.optimize import linprog
    from scipy.sparse import coo_matrix
    costs,rows,gp,required,tail,offset=d
    rr=[];cc=[];vv=[];rhs=[]
    rrws=rows+[( [(j,SCALE) for j in g], SCALE) for q,g in gp]
    rrws+=[( [(j,-SCALE) for j in g], -SCALE) for q,g in gp if q in required]
    for i,(t,b) in enumerate(rrws):
        rhs.append(b/SCALE)
        for j,a in t:
            rr.append(i);cc.append(j);vv.append(a/SCALE)
    C=[c/SCALE for c in costs]
    z=linprog(C,A_ub=coo_matrix((vv,(rr,cc)),shape=(len(rrws),len(C))).tocsr(),b_ub=rhs,bounds=[(0,None) if i==tail else (0,1) for i in range(len(C))],method='highs',options={'threads':1})
    if not z.success:
        return z.message,None,None
    ww=[max(0,round(-float(x)*DYADIC)) for x in z.ineqlin.marginals[:len(rows)]]
    # Only the abundance row contains the unbounded tail variable.
    ww[0]=min(ww[0],costs[tail]*DYADIC//SCALE)
    weights=[(i,w) for i,w in enumerate(ww) if w]
    v=price(d,weights)
    return round((offset/SCALE+z.fun)/(log_bounds(10)[1]/SCALE),5),v/(DYADIC*log_bounds(10)[1]),weights
