"""Seal marked trial graphs and prune unused ECPP data (discovery only)."""
from Domain import *
from hashlib import sha256
from subprocess import run
import argparse


def main(projection_only):
    cases={}; labels=set()
    for m in range(2,256,4):
        s=st([(P,E)],m);a,_=abundancy(s,SEEDS)
        if m in map(int,OLD['closed']):continue
        if m in MISSING or (a<=2 and not projection_only):
            pref='base' if m in MISSING else 'extra'
            path=H/'trials'/f'{pref}-{m}.json';t=json.loads(path.read_bytes());k,o,h=t['roots'],t['owners'],t['head'];assert C.Forest(s,k,o,h).lower()[0]>B,m
            cases[str(m)]=dict(roots=k,owners=o,head=h)
            labels.update(k);labels.update(dict(o))
    ecpp=OLD['ecpp'].copy(); wanted=sorted(q for q in labels if q>=2**64 and str(q) not in ecpp)
    known={}
    for q in wanted:
        code=sha256(str(q).encode()).hexdigest()[:24]
        blob=run(['git','cat-file','blob',f'49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec:Research/NightOrder/ECPP/{code}.json.gz'],capture_output=True,cwd=REPO)
        if blob.returncode==0:known[str(q)]=json.loads(gzip.decompress(blob.stdout))
    gen=[q for q in wanted if str(q) not in known];print('new labels',len(wanted),'generate',len(gen),flush=True)
    if gen:
        cmd=['wsl','--exec','/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr/bin/gp-2.17','-f','-q','-s','128M']
        ask='default(nbthreads,1);\n'+''.join(f'print(primecert({q}));\n' for q in gen)
        proc=run(cmd,input=ask.encode(),capture_output=True,timeout=900,cwd=REPO,check=True)
        arr=[json.loads(line) for line in proc.stdout.splitlines() if line.strip()];assert len(arr)==len(gen),proc.stderr
        known.update({str(q):a for q,a in zip(gen,arr)})
    for q,a in known.items():
        n=int(q);assert a
        for lev in a:
            assert lev[0]==n;n=C.pc.level(*lev)
        assert C.pc.prime64(n)
    packet=H/('Seven28Projected.json.gz' if projection_only else 'Seven28.json.gz')
    packet.write_bytes(gzip.compress(json.dumps(dict(cases=cases,ecpp=known),separators=(',',':'),sort_keys=True).encode(),mtime=0))
    print(len(cases),packet.name,sha256(packet.read_bytes()).hexdigest(),flush=True)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--projection-only',action='store_true');main(a.parse_args().projection_only)
