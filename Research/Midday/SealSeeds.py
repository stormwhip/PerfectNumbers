"""Optional discovery-side certifier. Exact replay, not search scores, decides acceptance."""
from pathlib import Path
import argparse,gzip,json,sys,hashlib,subprocess
from concurrent.futures import ThreadPoolExecutor
from functools import cache
H=Path(__file__).resolve().parent; R=H.parent;W=R.parent.parent
sys.path.insert(0,str(R/'Nov25/Boost'));import Pack
sys.path.insert(0,str(R/'MiddayForest'));from Verify import verify

def main():
    ap=argparse.ArgumentParser();ap.add_argument('seeds',type=Path);ap.add_argument('--cert',type=Path,required=True);ap.add_argument('--output',type=Path,required=True);ap.add_argument('--gp',required=True);ap.add_argument('--workers',type=int,default=4);ap.add_argument('--part',type=int,default=0);ap.add_argument('--parts',type=int,default=1);a=ap.parse_args();a.cert.mkdir(parents=True,exist_ok=True);a.output.mkdir(parents=True,exist_ok=True)
    Pack.DIRS=(a.cert,R/'MiddayForest/Scratch/cert',R/'MiddayDirected/cert',*Pack.DIRS);Pack.database()
    @cache
    def witness(q):
        c=Pack.chain(q)
        if c:return c
        path=a.cert/(hashlib.sha256(str(q).encode()).hexdigest()[:24]+'.json');cmd=['wsl','-d','Ubuntu','--',a.gp,'-fq'];data=f'default(parisizemax,750000000);default(nbthreads,1);\nprint(primecert({q}));\n'
        try:
            ret=subprocess.run(cmd,input=data,text=True,encoding='utf-8',errors='replace',capture_output=True,timeout=200,check=True);rows=json.loads(ret.stdout)
            if Pack.verify_chain(q,rows):path.write_text(json.dumps(rows,separators=(',',':')),encoding='utf8');return rows
        except (ValueError,OSError,subprocess.SubprocessError):pass
        print('missing',len(str(q)),str(q)[:15],flush=True);return None
    fs=[]
    for f in sorted(a.seeds.glob('*.json')):
        d=json.loads(f.read_bytes())
        if d.get('scout',0)>2400 and not (a.output/f'Forest{d["p"]}x{d["e"]}.json.gz').exists():fs.append(d)
    fs=fs[a.part::a.parts];print('queue',len(fs),flush=True)
    with ThreadPoolExecutor(a.workers) as pool:
        for d in fs:
            row={k:d[k] for k in ('p','e','roots','owners','head')};p,e=row['p'],row['e']; vals=sorted(z for z in (set(row['roots'])|dict(row['owners']).keys()) if z>=2**64);cs={str(q):v for q,v in zip(vals,pool.map(witness,vals)) if v};
            if len(cs)!=len(vals):continue
            name=a.output/f'Forest{p}x{e}.json.gz';temp=a.output/f'Unverified{p}x{e}.tmp';temp.write_bytes(gzip.compress(json.dumps(dict(rows=[row],ecpp=cs),separators=(',',':')).encode(),mtime=0))
            try:ans=verify(temp)
            except ValueError as ex:print('open/rejected',p,e,ex,flush=True);continue
            temp.replace(name);print('PASS',*ans,flush=True)
if __name__=='__main__':main()
