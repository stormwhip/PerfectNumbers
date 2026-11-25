"""Scout historical (untrusted) graph proposals with cached primality witnesses.

This script never imports or runs code from the historical workspace. The
released ForestPackets adapter must replay any positive packet separately.
"""
import argparse
from concurrent.futures import ProcessPoolExecutor
import gzip
from hashlib import sha256
import json
import os
from pathlib import Path
import sys
from time import monotonic

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
sys.path.insert(0,str(H.parent/'NightLowRoute/Release'))
from ForestReplay import proof, B, pc
from Ledger import load_baseline, obligations

CASES=('HDir31_26','HDir19_86','QFine19_120','NoExtra13_38','QFine13_76',
       'CacheD13_34','Long231_32','NoExtra13_50','CacheD31_396')

def read(path):
    path=Path(path)
    data=path.read_bytes()
    return json.loads(gzip.decompress(data) if path.suffix=='.gz' else data)


def each(job):
    path,certdir,out=map(Path,job)
    x=read(path);p,e=x['p'],x['e'];start=monotonic()
    def report(why,**kw):
        r=dict(source=path.name,p=p,e=e,status=why,seconds=round(monotonic()-start,2),**kw)
        print(json.dumps(r),flush=True)
        return r
    # Discovery metadata, including floating "floor", is never supplied to proof.
    r=dict(p=p,e=e,roots=x['P'],owners=x['owners'],head=x['head']);cs={};missing=[];nset={*r['roots'],*dict(r['owners'])}
    for q in sorted(nset):
        if q<2**64:
            if not pc.prime64(q):return report('composite-small',candidate=q)
            continue
        h=sha256(str(q).encode()).hexdigest()[:24]
        f=certdir/(h+'.json')
        if f.is_file():cs[str(q)]=read(f)
        else:missing.append(q)
    if missing:
        # Safe speculative loss: remove unproved child and its entire subtree.
        # A root prime is merely a known sigma factor, and can likewise be omitted.
        lose=set(missing)
        while True:
            l=len(lose);lose.update(q for q,w in r['owners'] if w in lose)
            if len(lose)==l:break
        r['roots']=[q for q in r['roots'] if q not in lose]
        r['owners']=[[q,w] for q,w in r['owners'] if q not in lose]
        cs={str(q):v for q,v in ((int(k),u) for k,u in cs.items()) if q not in lose}
    try:
        vals=proof(r,cs);m=min(vals.values());floor=len(str(m))-1
    except (ValueError,KeyError,RecursionError) as ex:
        return report('rejected',why=str(ex),missing=len(missing))
    if m<=B:
        return report('open',floor=floor,missing=len(missing),modes={str(k):len(str(v))-1 for k,v in vals.items() if v<=B})
    pkt=out/f'{p}x{e}-{path.stem}.json.gz'
    pkt.write_bytes(gzip.compress(json.dumps(dict(rows=[r],ecpp=cs),separators=(',',':')).encode(),mtime=0))
    return report('candidate',floor=floor,missing=len(missing),packet=str(pkt),edges=len(r['owners']),ecpp=len(cs))


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--history',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--cert-cache',type=Path)
    ap.add_argument('--workers',type=int,default=4)
    ap.add_argument('cases',nargs='*')
    a=ap.parse_args();a.output.mkdir(exist_ok=True,parents=True)
    active=obligations(load_baseline()['remaining_shards']); jobs=[]
    for n in a.cases or CASES:
        f=a.history/(n+'.json'); d=read(f)
        if (d['p'],d['e']) not in active:raise ValueError('old or invalid claim')
        jobs.append((f,a.cert_cache or a.history/'CertCache',a.output))
    if a.workers==1:
        records=list(map(each,jobs))
    else:
        with ProcessPoolExecutor(a.workers) as pool:records=list(pool.map(each,jobs))
    (a.output/'survey.json').write_text(json.dumps(records,indent=1)+'\n',encoding='utf-8',newline='\n')

if __name__=='__main__':
    if not __debug__:raise SystemExit('do not use -O')
    main()
