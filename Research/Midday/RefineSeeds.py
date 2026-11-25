"""Offline secondary discovery: change ownership of emitted labels on weak exact cells."""
from SeedScan import *
import random
from BoostScore import minimum

def search(builder,start,seconds,rng):
    import time
    deadline=time.monotonic()+seconds;bestrow=start.copy();r=start.copy();p,e=r['p'],r['e'];base=p*sigma(p,e);roots=set(r['roots']);best=minimum(r);i=0;tried=defaultdict(int)
    while time.monotonic()<deadline and best<2400.04:
        ow=dict(r['owners']); V=roots|ow.keys();v,tr=scorer(r);m=min(v,key=v.get);cur=v[m];state=tr(m);tr.clear(); switches=[];adds={};score=lambda o:minimum(dict(r,owners=sorted(o.items())))
        def cycle(z,q):
            while z in ow and z!=q:z=ow[z]
            return z==q
        items=[(z,f) for z,(c,f,k,w) in state.items() if w is not False and (f+1)*z.bit_length()<14000];rng.shuffle(items);items.sort(key=lambda zf:tried[zf]);
        for z,f in items:
            tried[z,f]+=1
            hs=builder.hints(z,f);S=arithmetic(z,f);g=math.gcd(S,math.prod(ow));qs=set(hs)
            if g>1:qs.update(q for q in ow if g%q==0)
            for q in qs:
                if base%q==0 or q in roots:continue
                if q not in ow:adds.setdefault(q,z)
                elif ow[q]!=z and not cycle(z,q):switches.append((q,z))
        cand=[]
        if adds:cand.append((score(ow|adds),ow|adds));
        rng.shuffle(switches);switches.sort(key=lambda qz:qz[0] in state,reverse=True)
        for q,z in switches[:35]:
            if time.monotonic()>deadline:break
            o=ow|{q:z};cand.append((score(o),o))
        if not cand:break
        a,o=max(cand,key=lambda x:x[0]);r=dict(r,owners=sorted(o.items()))
        if a>best:best=a;bestrow=r.copy();i=0
        elif a<=cur+1e-6:
            i+=1
            if i%2==0 and len(cand)>1:r=dict(bestrow,owners=sorted(rng.choice(cand)[1].items()))
            if i>6:break
    return best,bestrow

def main():
    ap=argparse.ArgumentParser();ap.add_argument('folder',type=Path);ap.add_argument('--bank',type=Path,required=True);ap.add_argument('--out',type=Path,required=True);ap.add_argument('--above',type=float,default=1650);ap.add_argument('--seconds',type=int,default=45);ap.add_argument('--min-only',action='store_true');ap.add_argument('--part',type=int,default=0);ap.add_argument('--parts',type=int,default=1);a=ap.parse_args(); a.out.mkdir(parents=True,exist_ok=True);b=Builder(a.bank);todo=[]
    for f in a.folder.glob('*.json'):
        d=json.loads(f.read_bytes());s=d.get('scout',0)
        if a.above<s<2400.01:todo.append((s,d['p'],d['e'],d))
    for s,p,e,d in sorted(todo,reverse=True)[a.part::a.parts]:
        if a.min_only:b.build(p,e,d['roots'],65,a.out,head=96,start=d);continue
        d['head']=max(90,d['head']);w,win=search(b,d,a.seconds,random.Random(p*10000+e));f=a.out/f'{p}x{e}.json';f.write_text(json.dumps(dict(win,scout=w),separators=(',',':')));print(p,e,round(s,2),round(w,2),flush=True);sigma.cache_clear()
if __name__=='__main__':main()
