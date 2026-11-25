"""Discovery: counterexample-guided ownership, alternative exponent witnesses, and a restart bank.
Only a sealed integer packet proves a pair. No inference from a local optimum or failed run.
"""
from RefineSeeds import *
from BoostScore import load
import time,hashlib

def inventory(banks,p,e):
    opts=[]
    for folder in banks:
        for name in (f'{p}x{e}.json',f'best-{p}-{e}.json',f'trial-{p}-{e}.json',f'CacheD{p}_{e}.json',f'Intra{p}_{e}.json',f'QFine{p}_{e}.json',f'seed{p}_{e}.json'):
            f=folder/name
            if not f.exists():continue
            try:r=load(f);r['head']=max(115,r['head']); v=minimum(r)
            except (KeyError,ValueError,TypeError):continue
            opts.append((v,r))
    return sorted(opts,key=lambda t:-t[0])

class Engine(Builder):
    def __init__(self,bank):
        super().__init__(bank);F=R/'MiddayForest/Scratch/Factors';D=R/'MiddayDirected';self.hintdirs=(F,D/'factors');
        for file in (D/'ecm').glob('*.receipt'):
            t=json.loads(file.read_bytes());self.edges.setdefault(t['z'],[]).extend(t['hits'])
    @lru_cache(16384)
    def candidates(self,z,f):
        if (f+1)*z.bit_length()>18000:return ()
        qs=set(self.hints(z,f));n=arithmetic(z,f);name=hashlib.sha256(f'{z}^{f+1}'.encode()).hexdigest()[:26]+'.json'
        for folder in self.hintdirs:
            ff=folder/name
            if ff.is_file():
                d=json.loads(ff.read_bytes());a=d.get('hints',[]) if isinstance(d,dict) else d;qs.update(q for q in a if q>2 and n%q==0 and pr(q))
        return sorted(qs)

def improve(r,b,secs,seed,save):
    rng=random.Random(seed);p,e=r['p'],r['e'];best=minimum(r);bestrow=r.copy();A=p*sigma(p,e);end=time.monotonic()+secs;K=set(r['roots']);candidates=defaultdict(set);it=0;stale=0
    def value(o):return minimum(dict(r,owners=sorted(o.items())))
    while time.monotonic()<end and best<2400.02:
        it+=1;o=dict(r['owners']);V=set(o)|K;v,tr=scorer(r);m=min(v,key=v.get);cur=v[m];states=tr(m);U=math.prod(o);cells=[(z,f) for z,(h,f,_,who) in states.items() if who is not False];more=[]
        if stale>=1:
            for mode in sorted(v,key=v.get)[1:]:
                if v[mode]<cur+150:more.extend((z,f) for z,(h,f,_,who) in tr(mode).items() if who is not False)
            if cells:
                z,f=rng.choice(cells);av,at=scorer(r,exclude={z:{f}});mm=min(av,key=av.get);more.extend((k,a) for k,(_,a,_,who) in at(mm).items() if who is not False);at.clear()
        tr.clear();adds={};switch=[]
        for z,f in dict.fromkeys(cells+more):
            S=arithmetic(z,f);g=math.gcd(S,U);hs=set(b.candidates(z,f));
            if g>1:hs.update(q for q in o if g%q==0)
            for q in hs:
                if A%q==0 or q in K:continue
                candidates[q].add(z)
                if q not in o:adds.setdefault(q,z);continue
                if o[q]==z:continue
                x=z
                while x in o and x!=q:x=o[x]
                if x!=q:switch.append((q,z))
        tested=[]
        if adds:
            nxt=o|adds;tested.append((value(nxt),nxt))
        rng.shuffle(switch);switch.sort(key=lambda qz:(qz[0] in states,qz[1] in states),reverse=True)
        for q,z in switch[:min(35,7+stale*5)]:
            if time.monotonic()>=end:break
            no=o|{q:z};tested.append((value(no),no))
        if not tested or stale>4:
            o=dict(bestrow['owners']);nons=[q for q in o if q in states and q not in K] or list(o)
            if not nons:break
            drop=set(rng.sample(nons,min(len(nons),rng.randint(1,4))));prev=0
            while len(drop)!=prev:prev=len(drop);drop.update(q for q,z in o.items() if z in drop)
            no={q:z for q,z in o.items() if q not in drop};tested=[(value(no),no)];stale=0
        val,no=max(tested,key=lambda t:t[0]);r=dict(r,owners=sorted(no.items()))
        if val>best+1e-5:best=val;bestrow=r.copy();save(best,bestrow);stale=0
        else:stale+=1
    return best

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bank',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--min',type=float,default=1400);ap.add_argument('--seconds',type=int,default=20);ap.add_argument('--part',type=int,default=0);ap.add_argument('--parts',type=int,default=1);ap.add_argument('--seed',type=int,default=11);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);engine=Engine(a.bank);folders=[*(W/'MiddayScratch'/name for name in ('Seeds','Second','Deep','Refined','Advanced','Rebuilt','Super')),R/'MiddayDirected',R/'MiddayForest/Scratch',W/'overnight/Research/NightLowRoute',W/'overnight/Research/NightSevenForest'];ds=json.loads((R/'Nov25/Delta.json').read_bytes());cases={(s['root'],e) for s in ds['remaining_shards'] for e in s['remaining_actuals']};todo=[]
    for ix,(p,e) in enumerate(sorted(cases)):
        if ix%a.parts!=a.part:continue
        if any(f.exists() for f in (H/'Packets'/f'Forest{p}x{e}.json.gz',R/'MiddayForest'/f'Forest{p}x{e}.json.gz',R/'MiddayDirected'/f'Directed{p}x{e}.json.gz')):continue
        opts=inventory(folders,p,e)
        if not opts:continue
        v,r=opts[0]
        if v>a.min:todo.append((v,p,e,r))
        sigma.cache_clear()
    for v,p,e,r in sorted(todo,reverse=True):
        f=a.out/f'{p}x{e}.json';
        def save(s,x):f.write_text(json.dumps(dict(x,scout=s),separators=(',',':')),encoding='utf8')
        save(v,r);b=improve(r,engine,a.seconds,a.seed+100*p+e,save);print(p,e,round(v,1),round(b,1),flush=True);sigma.cache_clear()
if __name__=='__main__':main()
