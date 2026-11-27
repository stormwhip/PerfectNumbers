"""Seal only complete selected first-pivot subtrees from the authorized discovery handoff."""
from Search import catalog
from Domain import *
from subprocess import run
from hashlib import sha256
import argparse


def main(fibers,out,reuse):
    src=json.loads(SCOUT.read_bytes()); all0=src['tree']; assert all0['type']=='split' and all0['q']==Q
    _,known=catalog(); labels={Q}; stats={'forests':0,'splits':0,'new':0}; missing={tuple(tuple(a) for a in r):(int(f),i) for f in src['unresolved'] for i,(r,_) in enumerate(src['unresolved'][f])}
    if reuse:known.update(json.loads(gzip.decompress(reuse.read_bytes()))['ecpp'])
    def walk(rows,t):
        if t is None:
            f,i=missing[tuple(rows)]; s=state(rows); viable=[]
            for p in sorted((H/'trials').glob(f'*-0-{f}-{i}.json')):
                d=json.loads(p.read_bytes()); k,o,h=map(d.get,('roots','owners','head'))
                if C.Forest(s,k,o,h).lower()[0]>B:viable.append((len(o),d))
            if not viable:return {'type':'open'}
            t=min(viable,key=lambda u:u[0])[1];t=dict(type='forest',**{k:t[k] for k in ('roots','owners','head')});stats['new']+=1
        if t['type']=='split':
            q=t['q']; labels.add(q); stats['splits']+=1
            fs,_=expand(rows,q); assert set(map(str,fs))==set(t['cases'])
            return dict(type='split',q=q,cases={str(f):walk(rows+[(q,f)],t['cases'][str(f)]) for f in fs})
        assert t['type']=='forest' and set(t)=={'type','roots','owners','head'}
        k,o,h=map(t.get,('roots','owners','head')); s=state(rows); ff=C.Forest(s,k,o,h)
        assert ff.lower()[0]>B
        used={q for q,_,_ in ff.memo}
        a=[e for e in o if e[0] in used]
        if len(a)<len(o) and C.Forest(s,k,a,h).lower()[0]>B:o=a
        labels.update(k);labels.update(dict(o));stats['forests']+=1
        return dict(type='forest',roots=k,owners=o,head=h)
    cases={str(f):walk([(P,E),(Q,f)],all0['cases'][str(f)]) for f in fibers}
    qs=sorted(q for q in labels if q>=2**64)
    for q in qs:
        if str(q) in known:continue
        key=sha256(str(q).encode()).hexdigest()[:24]
        blob=run(['git','cat-file','blob',f'49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec:Research/NightOrder/ECPP/{key}.json.gz'],capture_output=True,cwd=REPO)
        if blob.returncode==0:known[str(q)]=json.loads(gzip.decompress(blob.stdout))
    gen=[q for q in qs if str(q) not in known];print('STATS',stats,'ECPP',len(qs),'GEN',len(gen),flush=True)
    if gen:
        cmd=['wsl','--exec','/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr/bin/gp-2.17','-q','-f','-s','128M']
        text='default(nbthreads,1);\n'+''.join(f'print(primecert({q}));\n' for q in gen)
        r=run(cmd,input=text.encode(),capture_output=True,check=True,timeout=1000)
        a=[json.loads(v) for v in r.stdout.splitlines() if v.strip()];assert len(a)==len(gen),r.stderr
        known.update({str(q):v for q,v in zip(gen,a)})
    ecpp={}
    for q in qs:
        n=q;c=known[str(q)];assert c
        for lev in c:
            assert lev[0]==n;n=C.pc.level(*lev)
        assert C.pc.prime64(n);ecpp[str(q)]=c
    assert all(C.pc.prime64(q) for q in labels if q<2**64)
    out=out.resolve();assert out.is_relative_to(H)
    out.write_bytes(gzip.compress(json.dumps(dict(p=P,e=E,pivot=Q,cases=cases,ecpp=ecpp),separators=(',',':'),sort_keys=True).encode(),mtime=0))
    print(out.name,sha256(out.read_bytes()).hexdigest(),flush=True)

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('--fibers',type=int,nargs='+',required=True);ap.add_argument('--out',type=Path,default=H/'Nineteen372.json.gz');ap.add_argument('--reuse',type=Path);a=ap.parse_args();main(a.fibers,a.out,a.reuse)
