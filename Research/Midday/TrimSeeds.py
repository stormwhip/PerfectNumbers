"""Remove subtrees in batches before spending time proving the labels prime."""
import sys,json,math,argparse,random,time,gzip
from pathlib import Path
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R/'Nov25/Boost'));from BoostScore import minimum,sigma

def compact(d,sec=12):
    p,e=d['p'],d['e'];ow=dict(d['owners']);roots=set(d['roots']);d={k:v for k,v in d.items() if k in ('p','e','head','roots','owners')};d['head']=max(d['head'],128);deadline=time.monotonic()+sec;best=minimum(d);target=2400.02
    if best<=target:return None
    def trylose(batch):
        nonlocal ow,roots,best
        drop=set(batch);old=-1
        while len(drop)!=old:old=len(drop);drop.update(q for q,z in ow.items() if z in drop)
        n={q:z for q,z in ow.items() if q not in drop};rr=roots-drop
        if not rr:return False
        a=minimum(dict(d,owners=list(n.items()),roots=sorted(rr)))
        if a<=target:return False
        ow=n;roots=rr;best=a;return True
    for group in (sorted(roots|ow.keys(),key=lambda z:-z.bit_length()),sorted(ow),sorted(roots,reverse=True)):
        queue=[group]
        while queue and time.monotonic()<deadline:
            batch=[z for z in queue.pop() if z in roots or z in ow]
            if not batch or trylose(batch):continue
            if len(batch)>1:
                j=len(batch)//2;queue.extend([batch[j:],batch[:j]])
    return dict(d,roots=sorted(roots),owners=sorted(ow.items()),scout=best)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('folders',type=Path,nargs='+');ap.add_argument('--out',type=Path,required=True);ap.add_argument('--seconds',type=float,default=9);ap.add_argument('--part',type=int,default=0);ap.add_argument('--parts',type=int,default=1);a=ap.parse_args();a.out.mkdir(parents=True,exist_ok=True);todo={}
    for folder in a.folders:
        for f in folder.glob('*.json'):
            try:d=json.loads(f.read_bytes());p,e,s=d['p'],d['e'],d['scout']
            except (ValueError,KeyError,TypeError):continue
            if s>2400 and (p,e) not in todo or s>todo.get((p,e),{}).get('scout',math.inf):todo[p,e]=d
    for (p,e),d in sorted(todo.items()):
        if (p*171+e)%a.parts!=a.part:continue
        dest=a.out/f'{p}x{e}.json';
        if dest.exists() or (H/'Packets'/f'Forest{p}x{e}.json.gz').exists() or (R/'MiddayDirected'/f'Directed{p}x{e}.json.gz').exists() or (R/'MiddayForest'/f'Forest{p}x{e}.json.gz').exists():continue
        x=compact(d,a.seconds);sigma.cache_clear()
        if x:
            dest.write_text(json.dumps(x,separators=(',',':')),encoding='utf8');print(p,e,len(d['owners']),len(x['owners']),round(x['scout'],2),flush=True)
if __name__=='__main__':main()
