"""Optional discovery-side PARI ECPP witness export; never used by replay."""
import argparse
from concurrent.futures import ThreadPoolExecutor
import gzip
from hashlib import sha256
import json
from pathlib import Path
import subprocess
import sys
from time import monotonic

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from ForestDiscovery import pc, read


def valid(q,rows):
    if not isinstance(rows,list) or not rows:return False
    try:
        for row in rows:
            if q!=row[0]:return False
            q=pc.level(*row)
        return pc.prime64(q)
    except (TypeError,ValueError,IndexError):
        return False


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--history',type=Path,required=True)
    ap.add_argument('--output',type=Path,required=True)
    ap.add_argument('--cache',type=Path,action='append',default=[])
    ap.add_argument('--gp',required=True,help='path to GP; WSL Linux path when --wsl is given')
    ap.add_argument('--wsl')
    ap.add_argument('--minutes',type=int,default=18)
    ap.add_argument('--workers',type=int,default=3)
    ap.add_argument('seeds',nargs='+')
    a=ap.parse_args();a.output.mkdir(exist_ok=True,parents=True);deadline=monotonic()+a.minutes*60
    bank=read(H.parent/'OrderSupplyNext/OrderPrimeProofs.json.gz')
    cmd=(['wsl','-d',a.wsl,'--'] if a.wsl else [])+[a.gp,'-fq']
    todo=set()
    for n in a.seeds:
        name=Path(n)
        x=read(name if name.is_file() else a.history/(n+'.json'))
        if isinstance(x,list):
            todo.update(q for q in x if type(q) is int and q>=2**64)
        else:
            roots=x.get('P',x.get('roots'))
            todo.update(q for q in {*roots,*dict(x['owners'])} if q>=2**64)
    paths=[a.output,a.history/'CertCache',H.parent/'NightOrder/ECPP',H.parent/'EveningTree/ECPP',*a.cache]
    waiting=[]
    for q in sorted(todo):
        s=sha256(str(q).encode()).hexdigest()[:24];dest=a.output/(s+'.json');rows=bank.get(str(q))
        if rows is None:
            for d in paths:
                f=next((d/filename for filename in (s+'.json',s+'.json.gz','Prime'+s+'.json') if (d/filename).is_file()),None)
                if f is not None:
                    rows=read(f)
                    break
        if rows is not None:
            if not dest.exists():dest.write_text(json.dumps(rows,separators=(',',':')),encoding='utf-8')
        else:waiting.append((q,dest))
    print('selected',len(todo),'fresh',len(waiting),'workers',a.workers,flush=True)
    def make(item):
        q,dest=item
        if dest.is_file():return
        remaining=deadline-monotonic()
        if remaining<=1:return
        gp=f'default(parisizemax,1000000000); default(nbthreads,1);\nc=primecert({q}); if(c && primecertisvalid(c),print(c), print(0));\n'
        try:
            r=subprocess.run(cmd,input=gp,text=True,encoding='utf-8',errors='replace',capture_output=True,timeout=min(90,remaining),check=True)
            rows=json.loads(r.stdout)
            if not valid(q,rows):
                print('unverified',q,flush=True);return
            dest.write_text(json.dumps(rows,separators=(',',':')),encoding='utf-8')
            print('certified',len(str(q)),len(rows),q,flush=True)
        except (subprocess.SubprocessError,ValueError) as e:
            print('failed',q,type(e).__name__,flush=True)
    with ThreadPoolExecutor(a.workers) as pool:
        list(pool.map(make,waiting))
    print('cert files available',len(list(a.output.glob('*.json'))),flush=True)

if __name__=='__main__':main()
