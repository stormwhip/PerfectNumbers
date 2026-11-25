"""Discover cross-index grafts: re-use the OWNER subtree of an entirely different
(p,e) on each shared forced root. Rebuild the recipient's exact A and all valuations.
Unlike arithmetic index lift, this requires NO divisibility between the two indices.
Only independent replay on the target certifies anything.
"""
import argparse,json,sys,gzip,math,random
from collections import defaultdict
from pathlib import Path
from functools import lru_cache
H=Path(__file__).resolve().parent;R=H.parent;W=R.parent.parent;sys.path[:0]=[str(R/'Nov25/Boost'),str(W/'NightCache/flint-lib')]
from BoostScore import load,minimum,sigma
from flint import fmpz

def grab(f):
    try:
        if f.stat().st_size>6000000:return []
        raw=f.read_bytes();d=json.loads(gzip.decompress(raw) if f.suffix=='.gz' else raw)
        if isinstance(d,dict) and 'rows' in d and isinstance(d['rows'],list):ds=d['rows']
        elif isinstance(d,dict) and 'row' in d and isinstance(d['row'],dict):
            v=d['row'];ds=[dict(p=3,e=v['e'],roots=v['roots'],owners=v['edges'],head=v['head'])]
        else:ds=[d]
        return [(tuple(d.get('roots',d.get('P'))),dict(d['owners'])) for d in ds if isinstance(d,dict) and 'owners' in d and d.get('roots',d.get('P'))]
    except (KeyError,TypeError,ValueError,EOFError):return []

def build(out):
    by=defaultdict(dict); pats=[(R,'NightLowRoute/Release/Forest*.gz'),(R,'NightSevenForest/Release/Forest*.gz'),(R,'MiddayForest/Forest*.gz'),(R,'Midday/Packets/Forest*.gz'),(R,'MiddayDirected/Directed*.gz'),(R,'MiddayThree/Forest*.gz'),(R,'Nov25/Forests/*.gz'),(W,'overnight/Research/NightLowRoute/CacheD*.json'),(W,'overnight/Research/NightLowRoute/Intra*.json'),(W,'overnight/Research/NightSevenForest/seed*.json'),(W,'MiddayScratch/Deep/*.json'),(W,'MiddayScratch/Second/*.json'),(W,'MiddayScratch/Advanced/*.json')]
    for folder,pat in pats:
        for f in folder.glob(pat):
            for roots,ow in grab(f):
                kid=defaultdict(list)
                for q,z in ow.items():kid[z].append(q)
                for z in roots:
                    if not kid[z]:continue
                    ql=[z];edges=[];seen={z}
                    while ql:
                        w=ql.pop()
                        for t in kid[w]:
                            if t not in seen:seen.add(t);edges.append((t,w));ql.append(t)
                    if edges:by[z][hash(tuple(sorted(edges)))]=edges
    out.write_bytes(gzip.compress(json.dumps({str(z):list(v.values()) for z,v in by.items()},separators=(',',':')).encode(),mtime=0));print('families',len(by),'pieces',sum(map(len,by.values())),flush=True)

def merge(subs,K,pA):
    ow={}
    for z,edges in subs:
        valid={z}
        for q,w in edges:
            if w not in valid or q in K or pA%q==0:continue
            if q not in ow:ow[q]=w;valid.add(q)
            elif ow[q]==w:valid.add(q)
    return ow

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--bank',type=Path,required=True);ap.add_argument('--build',action='store_true');ap.add_argument('--out',type=Path);ap.add_argument('--rounds',type=int,default=12);ap.add_argument('--part',type=int,default=0);ap.add_argument('--parts',type=int,default=1);a=ap.parse_args()
    if a.build:return build(a.bank)
    store={int(z):v for z,v in json.loads(gzip.decompress(a.bank.read_bytes())).items()};a.out.mkdir(exist_ok=True,parents=True);rng=random.Random(101);ds=json.loads((R/'Nov25/Delta.json').read_bytes());cs=sorted({(r['root'],e) for r in ds['remaining_shards'] for e in r['remaining_actuals']});
    for i,(p,e) in enumerate(cs):
        if i%a.parts!=a.part:continue
        if any(f.exists() for f in (H/'Packets'/f'Forest{p}x{e}.json.gz',R/'MiddayForest'/f'Forest{p}x{e}.json.gz',R/'MiddayDirected'/f'Directed{p}x{e}.json.gz',R/'MiddayThree'/f'Forest{e}.json.gz' if p==3 else H/'impossible')):continue
        A=sigma(p,e);raw=json.loads((W/f'MiddayScratch/Factors/{p}x{e}.json').read_bytes());K={q for q,v in raw if q>2 and A%q==0 and fmpz(q).is_probable_prime()};
        if not K:continue
        choices=[]
        for z in sorted(K):
            es=store.get(z,[])
            if not es:continue
            es=sorted(es,key=len,reverse=True);es=es[:8]+rng.sample(es[8:],min(4,len(es[8:])))
            choices.append((z,es))
        if not choices:continue
        row=dict(p=p,e=e,roots=sorted(K),owners=[],head=115);best=-math.inf;bestrow=None
        def trial(sel):
            nonlocal best,bestrow
            o=merge(sel,K,p*A);r=dict(row,owners=sorted(o.items()));v=minimum(r)
            if v>best:best=v;bestrow=dict(r,scout=v)
            return v
        sel=[(z,es[0]) for z,es in choices];trial(sel)
        for j,(z,es) in enumerate(choices):
            if len(es)<=1:continue
            vv=[]
            for ed in es:vv.append(trial(sel[:j]+[(z,ed)]+sel[j+1:]))
            sel[j]=(z,es[vv.index(max(vv))])
        for _ in range(a.rounds):
            if best>2400.02:break
            rng.shuffle(sel);trial(sel)
        (a.out/f'{p}x{e}.json').write_text(json.dumps(bestrow,separators=(',',':')),encoding='utf8');print(p,e,round(best,2),len(K),len(choices),flush=True);sigma.cache_clear()
if __name__=='__main__':main()
