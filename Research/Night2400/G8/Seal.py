"""Seal exact masked trees and reusable size leaves; discovery inputs are not proof dependencies."""
from Search import *
from hashlib import sha256
from subprocess import run

SECOND={6:3032394642737237,10:159387017168296185666158069,12:284483325856762389425983276524293,22:41350417582353391035540171793853418700038798850109580339617,52:765692473186112212513185113}
SECOND.update({int(f):q for f,q in json.loads((H/'ShortSplits.json').read_bytes()).items()})


def main(out,reuse=None):
    from Discover import Finder,Bank
    find=Finder(Bank(Path('E:/PerfectNumbers/Build/Night2400/FactorData')),25)
    _,known=catalog()
    if reuse:known.update(json.loads(gzip.decompress(reuse.read_bytes()))['ecpp'])
    ks=extras(); options={}; shared={}; cases={}; labels={Q}
    deep={int(f):[list(map(tuple,r)) for r in rows] for f,rows in json.loads((H/'DeepSeeds.json').read_bytes()).items()}
    from flint import fmpz
    for p in sorted((H/'trials').glob('*.json')):
        tag,m,f,idx=p.stem.split('-');m,f,idx=map(int,(m,f,idx));d=json.loads(p.read_bytes());k,o,h=map(d.get,('roots','owners','head'))
        if d['score']<2400:continue
        if not all(fmpz(q).is_probable_prime() for q in set(k)|dict(o).keys()):continue
        rows=deep[f][idx] if tag.startswith('split') else [(P,E),(Q,f)]
        st=state(rows,m or None);ft=C.Forest(st,k,o,h)
        assert ft.lower()[0]>B,(tag,m,f,idx)
        touched={q for q,_,_ in ft.memo}; a=[e for e in o if e[0] in touched]
        if len(a)<len(o) and C.Forest(st,k,a,h).lower()[0]>B:o=a
        key=(m,tuple(rows));leaf=dict(type='forest',roots=k,owners=o,head=h)
        if key not in options or len(o)<len(options[key]['owners']):options[key]=leaf
    def mark(r):
        labels.update(r['roots']);labels.update(dict(r.get('owners',[])))
        return r
    def walk(rows,m):
        s=state(rows,m); assert not dead(s)
        if (0,tuple(rows)) in options:
            key=';'.join(f'{q}:{f}' for q,f in rows)
            shared[key]=dict(rows=rows,leaf=mark(options[0,tuple(rows)]));return dict(type='shared',key=key)
        k=roots_for(rows,s,find,{z for q,f in rows for z in ks.get((q,f),())})
        if abundance(s,k)>2:
            for q in [z for z in k if z not in s.present][::-1]:
                a=[v for v in k if v!=q]
                if abundance(s,a)>2:k=a
            return mark(dict(type='abundance',roots=k))
        if (m,tuple(rows)) in options:return mark(options[m,tuple(rows)])
        q=SECOND.get(rows[-1][1]) if len(rows)==2 else None
        if q:
            labels.add(q); fs,_=expand(rows,q,m)
            return dict(type='split',q=q,cases={str(f):walk(rows+[(q,f)],m) for f in fs})
        return {'type':'open'}
    for m in ALL:
        f0,_=expand([(P,E)],Q,m)
        root=state([(P,E)],m); rs=sorted(set(root.present))
        if abundance(root,rs)>2:
            cases[str(m)]={'root':mark(dict(type='abundance',roots=rs)),'cases':{}}
        else:cases[str(m)]={'root':None,'cases':{str(f):walk([(P,E),(Q,f)],m) for f in f0}}
    for d in shared.values():labels.update(q for q,_ in d['rows'])
    need=sorted(q for q in labels if q>=2**64)
    for q in need:
        if str(q) in known:continue
        key=sha256(str(q).encode()).hexdigest()[:24]
        proc=run(['git','cat-file','blob',f'49b19bbd:Research/NightOrder/ECPP/{key}.json.gz'],capture_output=True,cwd=REPO)
        if proc.returncode==0:known[str(q)]=json.loads(gzip.decompress(proc.stdout))
    todo=[q for q in need if str(q) not in known];print('shared',list(shared),'cert',len(need),'new',len(todo),flush=True)
    if todo:
        cmd=['wsl','--exec','/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr/bin/gp-2.17','-q','-f','-s','128M']
        text='default(nbthreads,1);\n'+''.join(f'print(primecert({q}));\n' for q in todo)
        proc=run(cmd,input=text.encode(),capture_output=True,check=True,timeout=1000)
        a=[json.loads(s) for s in proc.stdout.splitlines() if s.strip()];assert len(a)==len(todo),proc.stderr
        known.update({str(q):r for q,r in zip(todo,a)})
    d=dict(cases=cases,shared=shared,ecpp={str(q):known[str(q)] for q in need})
    raw=gzip.compress(json.dumps(d,separators=(',',':'),sort_keys=True).encode(),mtime=0)
    out=out.resolve();assert out.is_relative_to(H) and out.parent.is_dir();out.write_bytes(raw);print(out.name,sha256(raw).hexdigest(),flush=True)

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('--out',type=Path,default=H/'Thirteen508.json.gz');a.add_argument('--reuse',type=Path);ns=a.parse_args();main(ns.out,ns.reuse)
