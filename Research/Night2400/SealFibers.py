"""Discovery helper: seal a selected exact subtree using existing or PARI ECPP.

Only explicit known repository paths and --cache are read. No network. The
output is accepted only after running the frozen arithmetic via VerifyFibers.
"""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess

from VerifyFibers import C, R


def vals(t):
    if t is None: raise ValueError('requested fiber has an unresolved leaf')
    if t['type']=='split':
        yield t['q']
        for z in t['cases'].values(): yield from vals(z)
    elif t['type']=='forest':
        yield from t['roots']; yield from (q for q,_ in t['owners'])
    elif t['type']!='price': raise ValueError(t['type'])


def load(f):
    raw=f.read_bytes()
    return json.loads(gzip.decompress(raw) if f.suffix=='.gz' else raw)


def valid(q,rows):
    if not isinstance(rows,list): return False
    try:
        for row in rows:
            if q!=row[0]:return False
            q=C.pc.level(*row)
        return C.pc.prime64(q)
    except (ValueError,TypeError,IndexError,OverflowError):return False


def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('input',type=Path);p.add_argument('output',type=Path);p.add_argument('--fiber',nargs='+',type=int,required=True)
    p.add_argument('--price',action='append',nargs='+',type=int,default=[],help='one first-fiber valuation followed by target indices')
    p.add_argument('--cache',required=True,type=Path);p.add_argument('--gp',required=True);p.add_argument('--wsl',default='Ubuntu')
    p.add_argument('--workers',default=3,type=int);p.add_argument('--timeout',default=120,type=int)
    a=p.parse_args(); x=load(a.input); pivot=x['tree']['q']; replacement={str(v[0]):{'type':'price','targets':v[1:]} for v in a.price}
    cases={str(v):(replacement[str(v)] if str(v) in replacement else x['tree']['cases'][str(v)]) for v in a.fiber}
    labels={pivot};
    for t in cases.values():labels.update(vals(t))
    for q in labels:
        if q<2**64 and not C.pc.prime64(q):raise ValueError(f'nonprime small label {q}')
    labels=sorted(q for q in labels if q>=2**64)
    book=load(R/'OrderSupplyNext/OrderPrimeProofs.json.gz')
    for d in (R/'Session20261126',R/'FinalSprint'):
        for f in (*d.glob('Tree*.json.gz'),*d.glob('JointTree*.json.gz')):
            for q,rows in load(f)['ecpp'].items():
                if q in {str(z) for z in labels}:book.setdefault(q,rows)
    a.cache.mkdir(parents=True,exist_ok=True)
    cmd=(['wsl','-d',a.wsl,'--'] if a.wsl else [])+[a.gp,'-fq']

    def prove(q):
        h=sha256(str(q).encode()).hexdigest()[:24]
        for qid in (str(q),h):
            rows=book.get(qid)
            if valid(q,rows):return str(q),rows
        for d in (a.cache,R/'NightOrder/ECPP',R/'EveningTree/ECPP'):
            for name in (h+'.json',h+'.json.gz','Prime'+h+'.json'):
                f=d/name
                if f.is_file():
                    rows=load(f)
                    if valid(q,rows):return str(q),rows
        data=f'default(parisizemax,1000000000); default(nbthreads,1); print(primecert({q}));\n'
        out=subprocess.run(cmd,input=data,text=True,encoding='utf-8',errors='replace',capture_output=True,timeout=a.timeout,check=True)
        rows=json.loads(out.stdout)
        if not valid(q,rows):raise ValueError(f'could not certify {q}')
        (a.cache/(h+'.json')).write_text(json.dumps(rows,separators=(',',':')),encoding='utf-8')
        return str(q),rows

    with ThreadPoolExecutor(max_workers=a.workers) as pool: chains=dict(pool.map(prove,labels))
    row={'p':x['p'],'e':x['e'],'pivot':pivot,'cases':cases,'ecpp':chains}
    target=a.output.with_suffix('.tmp');target.write_bytes(gzip.compress(json.dumps(row,separators=(',',':')).encode(),mtime=0));target.replace(a.output)
    print('sealed',a.output,'labels',len(labels),'sha256',sha256(a.output.read_bytes()).hexdigest(),flush=True)


if __name__=='__main__':main()
