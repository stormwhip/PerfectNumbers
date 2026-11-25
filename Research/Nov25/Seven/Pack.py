"""Assemble self-contained root-7/11 packets from graph proposals and ECPP data.

The pinned replay is the authoritative arithmetic; cache contents are not trusted.
"""
import argparse
import gzip
from hashlib import sha256
import json
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Scout import H,HIST,PIN,pc
from Replay import proof,B

R=H.parents[1]
ROOT=HIST.parents[2]
CACHE=ROOT/'NightCache'


def read(p):
    y=p.read_bytes();return json.loads(gzip.decompress(y) if p.suffix=='.gz' else y)


def candidates(paths):
    for d in paths:
        if d.is_dir():yield d


def valid(q,rows):
    if not isinstance(rows,list) or not rows:return False
    try:
        for row in rows:
            if q!=row[0]:return False
            q=pc.level(*row)
        return type(q)==int and pc.prime64(q)
    except (TypeError,ValueError,IndexError,OverflowError):return False


def lookup(q,db,paths):
    rows=db.get(str(q))
    if valid(q,rows):return rows
    h=sha256(str(q).encode()).hexdigest()[:24]
    for d in paths:
        for name in (h+'.json',h+'.json.gz','Prime'+h+'.json'):
            f=d/name
            if f.is_file():
                rows=read(f)
                if valid(q,rows):return rows
    return None


def gather_historical():
    db=read(R/'OrderSupplyNext/OrderPrimeProofs.json.gz')
    for f in PIN.glob('*.json.gz'):
        data=read(f)
        db.update(data.get('ecpp',{}))
    return db


def pack(src,extras=()):
    src=Path(src); row={k:v for k,v in read(src).items() if k in ('p','e','roots','owners','head','den','rho')}
    db=gather_historical();paths=list(candidates([H/'cert',*extras,CACHE/'ecpp-local',R/'NightOrder/ECPP',R/'EveningTree/ECPP',R/'NightLowRoute/CertCache',ROOT/'upstream/Research/OrderSupplyNext/certs',HIST.parent/'NightLowRoute/CertCache']))
    names=set(row['roots'])|dict(row['owners']).keys(); ecpp={}; missing=[]
    for q in sorted(names):
        if q<2**64:
            if not pc.prime64(q):raise ValueError(f'composite small node {q}')
        else:
            rows=lookup(q,db,paths)
            if rows is None:missing.append(q)
            else:ecpp[str(q)]=rows
    if missing:
        out=H/(src.stem+'.missing.json');out.write_text(json.dumps(missing)+'\n',encoding='utf8')
        print('Missing',len(missing),'of',len(names),'nodes:',out,flush=True)
        return
    out=H/(src.stem+'.pack.json.gz'); data=dict(rows=[row],ecpp=ecpp)
    vals=proof(row,ecpp); den=row.get('den',1); m=min(vals.values()); floors={k:(len(str(v))-1)//den for k,v in vals.items()}
    if m<=B**den:
        print('OPEN exact',row['p'],row['e'],floors,flush=True)
        return
    out.write_bytes(gzip.compress(json.dumps(data,separators=(',',':')).encode(),mtime=0)); print('PASS exact',row['p'],row['e'],floors,'nodes',len(names),'ECPP',len(ecpp),'packet',out,flush=True)
    return out

if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--cache',type=Path,action='append',default=[]);a.add_argument('src',nargs='+'); y=a.parse_args()
    for s in y.src:pack(s,y.cache)
