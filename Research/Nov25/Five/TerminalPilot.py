"""Exploratory SciPy terminal LP for root 5; scores never constitute proof."""
from functools import cache
import gzip
from math import gcd, log, log10, prod
from pathlib import Path
import json
import sys

from scipy.optimize import linprog
from scipy.sparse import coo_matrix

HERE=Path(__file__).resolve().parent
R=HERE.parents[1]
sys.path.insert(0,str(R/'Session20261122'/'Python'))
from TerminalCertificate import allowed,odd_primes,sigma
BAD=(3,7,11,13,19,31)
B=10**2400


def vp(n,q=5):
    j=0
    while n%q==0:
        n//=q; j+=1
    return j


def supply(p,f):
    return vp(f+1) if p%5==1 else (vp(p+1)+vp(f+1) if p%5==4 and f%2 else 0)


@cache
def bank():
    files=R/'Session20261122'/'Certificates'
    raw=[json.load(gzip.open(files/f'Terminal{x}.json.gz','rt')) for x in ('Original','Replacement')]
    ext=json.loads((R/'NightUniform'/'ThreeAvoid.json').read_bytes())['cases'][0]
    E={}
    for p,e,q,c in [row for src in raw for row in src['edges']]+ext['new']:
        k=p,e,q
        if p not in BAD+(5,) and q not in BAD+(5,) and allowed(p,e,BAD):
            E[k]=max(c,E.get(k,0))
    promoted=dict(ext['promoted'])
    blocks={(p,e):(n,l) for p,e,n,l in ext['blocks']}
    return E,promoted,blocks


def solve(e,s=None,include_blocks=True,cut=32,root_factors=()):
    A=sigma(5,e)
    E,promoted,blocks=bank()
    cap=10**2400//5**e
    ordinary_only=s is not None
    Y=5**s if ordinary_only else 1
    Q=2*Y-1 if ordinary_only else 1
    assert not ordinary_only or s>0
    E={k:v for k,v in E.items() if not (ordinary_only and k[1]%2)}
    base={p:cut for p in odd_primes(5000) if p not in BAD+(5,)}
    base.update({p:max(f,base.get(p,0)) for p,f in promoted.items() if p not in BAD+(5,)})
    base.update({p:max(f,base.get(p,0)) for p,f,_ in E})
    for _,_,q in E:
        base.setdefault(q,0)
    for p in root_factors:
        base[p]=max(cut,base.get(p,0))
    covered=prod(base)
    R0=A; forced={}
    for p in base:
        c=vp(R0,p)
        if c:
            R0//=p**c
            forced[p]=c
    groups={};opts={};C=[];ab=[];U=[];V=[];special=[]
    def add(p,f,odd,exact):
        if exact and f<forced.get(p,0):return
        j=len(C); groups.setdefault(p,[]).append((j,f,odd,exact));opts[p,f]=j if exact else opts.get((p,f),j)
        C.append(max(f,forced.get(p,0))*log10(p));ab.append(log(sigma(p,f)/p**f) if exact else log(1+1/(p-1)));U.append(supply(p,f) if exact else 0)
        V.append(supply(p,f) if exact else (5 if p%5==1 else 5+vp(p+1) if odd and p%5==4 else 0))
        if odd:special.append(j)
    for p,fin in sorted(base.items()):
        for i,d,odd in ((2,2,False),(1,4,True)):
            if odd and (ordinary_only or p%4!=1 or not allowed(p,1,BAD)):continue
            for f in range(i,fin+1,d):
                if allowed(p,f,BAD):add(p,f,odd,True)
            f=i+d*max(0,(fin-i)//d+1)
            while not allowed(p,f,BAD):f+=d
            add(p,f,odd,False)
    if include_blocks:
        used={}
        for (p,f),(u,L) in blocks.items():
            if f>base.get(p,0) or (p,f) not in opts or (ordinary_only and f%2):continue
            if p in forced or p in BAD+(5,):continue
            # Keep coactive supports disjoint and remove all root / explicit overlap.
            U0=covered*A
            while (g:=gcd(u,U0))>1:u//=g
            U1=prod(v for x,v in used.items() if x!=p)
            while (g:=gcd(u,U1))>1:u//=g
            used[p]=u*used.get(p,1)
            j=opts[p,f];C[j]+=log10(u)
            # Their actual excess log-cost stays in the generic tail; credit
            # the portion already installed by the rough cofactor.
            V[j]+=log10(u)/(4*log10(5001))
            ab[j]+=int(log(u)/log(L))*log(1+1/(L-1)) if u>1 else 0
    tail=len(C);L=5001
    # Ordinary tail log-budget z and its separate abundance/supply ceilings.
    C += [1,0,0];ab += [0,1,0]; U += [0,0,0];V += [0,0,1]
    if not ordinary_only:
        special.append(len(C)); C.append(log10(L));ab.append(log(1+1/(L-1)));U.append(0);V.append(e)
    L0 = 100001
    rr=[(list(enumerate(-x for x in ab)), -(log(2)-log(5/4) - (log(R0)/log(L0))*log(1+1/(L0-1)) - (1/(Q-1) if ordinary_only else 0)))]
    rr.append(([(tail,-1),(tail+1,2*log10(L)/log(1+1/(L-1)))],0))
    rr.append(([(tail,-1),(tail+2,4*log10(L))],0))
    G=log(R0)/(4*log(L))
    rr.append(([(j,-u) for j,u in enumerate(V) if u],-(e-(s or 0)-G)))
    if ordinary_only:
        rr.append(([(j,u) for j,u in enumerate(U) if u],e-s))
    else:
        rr.append(([(j,1) for j in special],1))
    rr += [([(j,1) for j,*_ in g],1) for g in groups.values()]
    rr += [([(j,-1) for j,*_ in groups[p]],-1) for p in forced]
    for (p,f,q),c in E.items():
        assert (p,f) in opts or f<forced.get(p,0)
        if (p,f) not in opts:continue
        rr.append(([(opts[p,f],1)]+[(j,-1) for j,a,o,x in groups[q] if (not o or not f%2) and (not x or a>=c)],0))
    ii=[];jj=[];vv=[];d=[]
    for i,(terms,b) in enumerate(rr):
        for j,v in terms:
            ii.append(i);jj.append(j);vv.append(v)
        d.append(b)
    z=linprog(C,A_ub=coo_matrix((vv,(ii,jj)), shape=(len(rr),len(C))).tocsr(),b_ub=d,
              bounds=[(0,None) if tail<=j<tail+3 else (0,1) for j in range(len(C))],method='highs')
    assert z.success, z.message
    # Rough A can overlap a donor and Euler; in this particular late window q>A's
    # internal valuation cap, but not necessarily q>A. Separate source fee not yet applied.
    offset=log10(5**e*R0*Q)
    return len(C),len(rr),round(offset+z.fun,3),round(z.fun,3)


if __name__=='__main__':
    for s in (445,460,475,490,505,520):
        print(520,s,solve(520,s,True),flush=True)
