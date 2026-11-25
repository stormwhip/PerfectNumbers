"""Discovery floats only; ordinary low-root modes mirror ForestReplay."""
from functools import lru_cache
import json, math, sys
from pathlib import Path

H=Path(__file__).resolve().parent
R=H.parents[1]
ROOT=R.parent.parent
HIST=ROOT/'overnight/Research/NightLowRoute'
PIN=R/'NightLowRoute/Release'
sys.path.insert(0,str(PIN))
from ForestReplay import B,R as ORDER,pc,sigma,valuation,nonsupport,proof

@lru_cache(maxsize=12000)
def arithmetic(z,f):
    return sigma(z,f)//(2 if f%2 else 1)

@lru_cache(maxsize=160000)
def admissible(z,f,ban):
    return all((f+1)%b if z%b==1 else pow(z,f+1,b)!=1 for b in ban)

def load(path):
    x=json.loads(path.read_bytes()); p,e=x.get('p'),x.get('e'); A=sigma(p,e)
    roots=x.get('roots',x.get('P'))
    if not roots or any(A%q or not q%2 for q in roots):raise ValueError('invalid unconditional roots')
    row=dict(p=p,e=e,roots=sorted(set(roots)),owners=x['owners'],head=x.get('head',6))
    for k in ('den','rho'):
        if k in x:row[k]=x[k]
    owners=dict(row['owners']); seen=set(roots)
    kids={q:[] for q in seen|owners.keys()}
    for q,z in owners.items():
        if A*p%q==0 or z not in kids:raise ValueError('bad owner edge')
        kids[z].append(q)
    queue=list(seen)
    while queue:
        for q in kids[queue.pop()]:
            if q in seen:raise ValueError('bad graph')
            seen.add(q);queue.append(q)
    if seen!=set(kids):raise ValueError('unreachable')
    return row

def scorer(row,prices=None,exclude=None):
    p,e=row['p'],row['e']; roots=row['roots']; ow=dict(row['owners']); nodes=set(roots)|ow.keys(); A=sigma(p,e)
    cap=row['head']; prices=prices or {}; exclude=exclude or {}; banned=ORDER[:ORDER.index(p)]
    kids={z:[] for z in nodes}
    for q,z in ow.items():kids[z].append(q)
    U=p*A*math.prod(ow)
    load={z:max(1,valuation(A,z)) for z in roots}; log={z:math.log10(z) for z in nodes}
    price_log=[(z,w*log[z]) for z,w in prices.items() if w and z in nodes]; price_prod=math.prod(z for z,w in price_log)
    @lru_cache(None)
    def odd(z):return z%4==1 and all((z+1)%b for b in banned)
    @lru_cache(None)
    def costs(z,f):
        S=arithmetic(z,f); rem=nonsupport(S,U); charge=math.log10(rem)
        if math.gcd(price_prod,S)>1:
            charge+=sum(w*valuation(S,q) for q,w in price_log if S%q==0)
        return charge,tuple((q,valuation(S,q)) for q in kids[z] if S%q==0)
    @lru_cache(None)
    def node(z,h,mode):
        if mode==1:return min((node(z,h,3),node(z,h,2)),key=lambda n:n[0]) if odd(z) else node(z,h,3)
        if mode==2 and not odd(z):return math.inf,None,None
        f=h+((1-h)%4 if mode==2 else h%2); step=4 if mode==2 else 2; tested=0
        best=(math.inf,None,None); per=log[z]*(1-prices.get(z,0))
        while True:
            if not admissible(z,f,banned) or f in exclude.get(z,()):f+=step;continue
            if tested>=cap:return min(best,(f*per,f,False),key=lambda n:n[0])
            if f*per>=best[0]:return best
            tested+=1
            charge,sub=costs(z,f); m=f*per+charge; disc=0; who=None
            for q,c in sub:
                no=node(q,c,0)[0];m+=no
                if mode==3:
                    alt=node(q,c,1)[0]
                    if no-alt>disc:disc=no-alt;who=q
            if m-disc<best[0]:best=(m-disc,f,who)
            f+=step
    base=e*math.log10(p)+math.log10(A)-sum(h*(1-prices.get(z,0))*log[z] for z,h in load.items())
    zs={z:node(z,load[z],0)[0] for z in roots}; f0=base+sum(zs.values())
    modes={-1:f0}; mode_dict={-1:(0,None)}
    for z in roots:
        if odd(z):
            modes[z]=f0-zs[z]+node(z,load[z],2)[0];mode_dict[z]=(2,z)
    w=min(roots,key=lambda z:node(z,load[z],3)[0]-zs[z]);modes[0]=f0-zs[w]+node(w,load[w],3)[0];mode_dict[0]=(3,w)
    def trace(m):
        kind,w=mode_dict[m]; states={}
        def visit(z,h,k):
            if k==1:k=min((3,2),key=lambda x:node(z,h,x)[0])
            low,f,who=node(z,h,k); states[z]=(h,f,k,who)
            if who is not False:
                for q,c in costs(z,f)[1]:visit(q,c,1 if q==who else 0)
        for z in roots:visit(z,load[z],kind if z==w else 0)
        return states
    def clear():
        costs.cache_clear();node.cache_clear();odd.cache_clear()
    trace.clear=clear
    return modes,trace

def minimum(row,prices=None,exclude=None):
    v,t=scorer(row,prices,exclude); t.clear();return min(v.values())