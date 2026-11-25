"""Discovery: a common finite forest portfolio split on Euler label or a donor's exact exponent.
Unlike maximizing scalar minima, a different proved bound may win on every branch.
"""
import argparse,json,math,sys
from pathlib import Path
from functools import lru_cache
H=Path(__file__).resolve().parent;R=H.parent;W=R.parent.parent
sys.path.insert(0,str(R/'Nov25/Boost'));from BoostScore import load,sigma,arithmetic,nonsupport,valuation,ORDER,admissible

def make(row):
    p,e=row['p'],row['e'];A=sigma(p,e);K=row['roots'];P=dict(row['owners']);V=set(K)|P.keys();U=p*A*math.prod(P);cs={z:valuation(A,z) for z in K};base=e*math.log10(p)+math.log10(A)-sum(c*math.log10(z) for z,c in cs.items());kids={z:[] for z in V};ban=ORDER[:ORDER.index(p)];head=max(60,row.get('head',6));L={z:math.log10(z) for z in V}
    for q,z in P.items():kids[z].append(q)
    @lru_cache(None)
    def costs(z,f):
        S=arithmetic(z,f);return math.log10(nonsupport(S,U)),[(q,v) for q in kids[z] if (v:=valuation(S,q))]
    # Pair: ordinary cost and map of deltas for a specified Euler label.
    @lru_cache(None)
    def rec(z,h):
        no=math.inf; opt={};special=math.inf
        for sp in (False,True):
            if sp and (z%4!=1 or any((z+1)%b==0 for b in ban)):continue
            f=h+((1-h)%4 if sp else h%2);cnt=0;step=4 if sp else 2
            while True:
                if not admissible(z,f,ban):f+=step;continue
                if cnt>=head or f*L[z]>=(special if sp else no):
                    if sp:special=min(special,f*L[z]);
                    else:no=min(no,f*L[z]);
                    break
                cnt+=1;rem,sub=costs(z,f);v=f*L[z]+rem;active=[]
                for q,c in sub:
                    a,w=rec(q,c);v+=a;active.append(w)
                if sp:special=min(special,v)
                else:
                    no=min(no,v)
                    for w in active:
                        for t,delta in w.items():opt[t]=min(opt.get(t,math.inf),v+delta)
                f+=step
        opt[z]=min(opt.get(z,math.inf),special);return no,{t:v-no for t,v in opt.items() if v<no}
    g=base;ds={}
    for z,c in cs.items():
        a,d=rec(z,c);g+=a;ds.update(d)
    rec.cache_clear();costs.cache_clear();return g,ds

def main():
    ap=argparse.ArgumentParser();ap.add_argument('p',type=int);ap.add_argument('e',type=int);ap.add_argument('--limit',type=int,default=18);a=ap.parse_args();p,e=a.p,a.e;files=[]
    for pat in (f'overnight/Research/NightLowRoute/*{p}_{e}.json',f'overnight/Research/NightSevenForest/*{p}_{e}.json',f'nov25-until-1000-scratch/Research/Nov25/*/*-{p}x{e}-*.json',f'MiddayScratch/*/{p}x{e}.json',f'MiddayStudy/Research/MiddayForest/Scratch/trial-{p}-{e}.json',f'MiddayStudy/Research/MiddayDirected/best-{p}-{e}.json'):
        files.extend(W.glob(pat))
    allm=[];labels=set();seen=set()
    for path in files:
        try:r=load(path);key=tuple(map(tuple,sorted(r['owners']))),tuple(r['roots'])
        except (ValueError,KeyError,TypeError,AttributeError):continue
        if key in seen or (r['p'],r['e'])!=(p,e):continue
        seen.add(key);g,d=make(r);allm.append((g,d,path));labels.update(d)
    if not allm:return
    worst=sorted((max(g+d.get(z,0) for g,d,f in allm),z) for z in labels|{0});print(p,e,len(allm),len(labels),'floor',round(worst[0][0],3),'open',sum(v<2400 for v,z in worst),'worst',[(round(v,2),str(z)[:22]) for v,z in worst[:4]],flush=True)
if __name__=='__main__':main()
