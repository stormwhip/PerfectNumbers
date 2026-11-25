"""Read-only experimental forest scorer. Floating scores are discovery only."""
import argparse
from functools import cache, lru_cache
import json
import math
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
HIST=H.parents[2].parent/'overnight/Research/NightSevenForest'
PIN=H.parents[1]/'NightSevenForest/Release'
sys.path.insert(0,str(PIN))
from Replay import sigma, nonsupport, valuation, pc
CASES=((11,220),(7,234),(11,132),(7,252))

def load(p,e):
    return json.loads((HIST/f'seed{p}_{e}.json').read_bytes())

@lru_cache(maxsize=12000)
def arithmetic(z,f):
    return sigma(z,f)//(2 if f%2 else 1)


def scorer(row,prices=None,exclude=None):
    p,e=row['p'],row['e']; roots=row['roots']; ow=dict(row['owners']); nodes=set(roots)|ow.keys(); A=sigma(p,e)
    cap=row.get('head',32); prices=prices or {}; exclude=exclude or {}; banned=(19,7) if p==11 else (19,)
    kids={z:[] for z in nodes}
    for q,z in ow.items():kids[z].append(q)
    U=p*A*math.prod(ow)
    load={z:valuation(A,z) for z in roots}; log={z:math.log10(z) for z in nodes};
    price_log=[(z,w*log[z]) for z,w in prices.items() if w and z in nodes]; price_prod=math.prod(z for z,w in price_log)
    @cache
    def valid(z,f):
        return f not in exclude.get(z,()) and all((f+1)%b if z%b==1 else pow(z,f+1,b)!=1 for b in banned)
    @cache
    def costs(z,f):
        S=arithmetic(z,f); rem=nonsupport(S,U); charge=math.log10(rem)
        if math.gcd(price_prod,S)>1:
            charge+=sum(w*valuation(S,q) for q,w in price_log if S%q==0)
        return charge,tuple((q,valuation(S,q)) for q in kids[z] if S%q==0)
    @cache
    def node(z,h,mode):
        # mode 0: none, 1: at most one, 2: here, 3: at most one strictly below
        if mode==1:
            x=node(z,h,3); y=node(z,h,2)
            return min(x,y,key=lambda n:n[0])
        if mode==2 and (z%4!=1 or any((z+1)%b==0 for b in banned)):
            return math.inf,None,None
        f=h+((1-h)%4 if mode==2 else h%2); step=4 if mode==2 else 2; tested=0
        best=(math.inf,None,None)
        per=log[z]*(1-prices.get(z,0))
        while True:
            if not valid(z,f):f+=step;continue
            if tested>=cap:
                return min(best,(f*per,f,False),key=lambda n:n[0])
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
    b=e*math.log10(p)+math.log10(A)-sum(h*(1-prices.get(z,0))*log[z] for z,h in load.items())
    zs={z:node(z,load[z],0)[0] for z in roots}; f0=b+sum(zs.values())
    modes={-1:f0}; mode_dict={-1:(0,None)}
    for z in roots:
        modes[z]=f0-zs[z]+node(z,load[z],2)[0];mode_dict[z]=(2,z)
    w=min(roots,key=lambda z:node(z,load[z],3)[0]-zs[z]);modes[0]=f0-zs[w]+node(w,load[w],3)[0];mode_dict[0]=(3,w)
    def trace(m):
        if not math.isfinite(modes[m]):raise ValueError('cannot trace an impossible Euler mode')
        kind,w=mode_dict[m]; states={};
        def visit(z,h,k):
            if k==1:k=min((2,3),key=lambda x:node(z,h,x)[0]);
            _,f,who=node(z,h,k);states[z]=(h,f,k,who)
            if who is not False:
                for q,c in costs(z,f)[1]:visit(q,c,1 if q==who else 0)
        for z in roots:visit(z,load[z],kind if z==w else 0)
        return states
    return modes,trace


def summarize(row):
    values,trace=scorer(row); norm={k:round(v,3) for k,v in values.items() if math.isfinite(v)}
    p,e=row['p'],row['e']; A=sigma(p,e); ow=dict(row['owners']);U=p*A*math.prod(ow)
    m=min(values,key=values.get); states=trace(m); K=set(states)
    print(p,e,norm,'chosen',m,'active',len(states),flush=True)
    carry={z:valuation(A,z) for z in K|{p}}
    for z,(h,f,k,w) in states.items():
        if w is False:continue
        S=arithmetic(z,f)
        for q in carry:
            if S%q==0:carry[q]+=valuation(S,q)
    losses=[]; unowned=[]; euler=[]
    for z,(h,f,k,w) in states.items():
        c=carry[z]; n=max(c,h); lo=n+((1-n)%4 if k==2 else n%2)
        if lo>f:losses.append((round((lo-f)*math.log10(z),2),z,h,f,c))
        if k==2:euler.append((z,h,f))
        if w is False:print('tail',z,h,f,k,flush=True);continue
        S=arithmetic(z,f);R=nonsupport(S,U);miss=S//R//math.gcd(S//R,A*p)
        if miss>1:unowned.append((round(math.log10(miss),2),z,f))
    print('extra active forced',sum(a for a,*_ in losses), sorted(losses,reverse=True)[:20],'Euler',euler,'p carry',carry[p],flush=True)
    print('nonroot known smooth outputs',sorted(unowned,reverse=True)[:20],flush=True)
    print('big components',sorted(((round(f*math.log10(z),2),z,h,f,round(math.log10(nonsupport(arithmetic(z,f),U)),2)) for z,(h,f,k,w) in states.items()),reverse=True)[:20],flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--cases',nargs='*',default=[]);a=ap.parse_args()
    for p,e in (tuple(map(int,x.split('x'))) for x in a.cases or [f'{p}x{e}' for p,e in CASES]):summarize(load(p,e))
