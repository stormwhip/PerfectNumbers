"""Seal strict trial cutoffs and elementary abundancy leaves; discovery only."""
from Search import *
from hashlib import sha256
from subprocess import run


def main():
    from Discover import Finder,Bank
    ap=argparse.ArgumentParser();ap.add_argument('--db',type=Path,required=True);ap.add_argument('--out',type=Path,default=H/'Nineteen432.json.gz');ap.add_argument('--reuse',type=Path);ns=ap.parse_args()
    find=Finder(Bank(ns.db),27);_,known=catalog()
    if ns.reuse:known.update(json.loads(gzip.decompress(ns.reuse.read_bytes()))['ecpp'])
    extra={int(f):v for f,v in json.loads((H/'FactorSeeds.json').read_bytes()).items()}
    choices={}; masksets={}; cells={}; labels={Q}
    seen_files=sorted((H/'trials').glob('*.json'))
    for filename in seen_files:
        parts=filename.stem.split('-')
        if len(parts)!=3:continue
        tag,m,f=parts;m,f=int(m),int(f)
        try:t=json.loads(filename.read_bytes())
        except json.JSONDecodeError:continue  # another bounded trial may still be writing old-format scratch
        k,o,h=t['roots'],t['owners'],t['head']
        if t['score']<2400:continue
        s=state([(P,E),(Q,f)],m)
        ff=C.Forest(s,k,o,h);x=ff.lower()[0]; assert x>B,(m,f,t['score'])
        active={q for q,_,_ in ff.memo}
        small=[edge for edge in o if edge[0] in active]
        if len(small)<len(o) and C.Forest(s,k,small,h).lower()[0]>B:o=small
        if (m,f) not in choices or len(o)<len(choices[m,f]['owners']):choices[m,f]={'kind':'forest','roots':k,'owners':o,'head':h}
    special_path=H/'trials/Special.json'
    special=None
    if special_path.exists():
        t=json.loads(special_path.read_bytes());k,o,h=map(t.get,('roots','owners','head'))
        ss=state([(P,E),(Q,16),(5,1)],113); ff=C.Forest(ss,k,o,h)
        if ff.lower()[0]>B:
            active={q for q,_,_ in ff.memo}; es=[edge for edge in o if edge[0] in active]
            if C.Forest(ss,k,es,h).lower()[0]>B:o=es
            special={'kind':'euler5','roots':k,'owners':o,'head':h}
    all_f=set()
    for m in ALL:
        fs,tail=expand([(P,E)],Q,m);assert tail==69;all_f.update(fs)
        s=state([(P,E)],m);rr=sorted(set(s.present))
        if abundance(s,rr)>2:
            cells[str(m)]={'root':rr,'cases':{}};masksets[m]=set();continue
        cs={}
        for f in fs:
            t=state([(P,E),(Q,f)],m);roots=sorted((set(t.present)|set(find.factors(Q,f))|set(extra.get(f,())))-t.rows.keys()-set(t.bad))
            assert all(t.D%q==0 or q in t.present for q in roots)
            if abundance(t,roots)>2:
                # Remove dispensable labels before asking for certificates.
                for q in roots.copy()[::-1]:
                    if q in t.present:continue
                    trial=[z for z in roots if z!=q]
                    if abundance(t,trial)>2:roots=trial
                r={'kind':'abundance','roots':roots}
            elif f in (20,24,26,30,32,34) and C.Forest(t,roots,[],64).lower()[0]>B:
                r={'kind':'forest','roots':roots,'owners':[],'head':64}
            elif (m,f) in choices:r=choices[m,f]
            elif (m,f)==(113,16) and special is not None:r=special
            else:continue
            cs[str(f)]=r;labels.update(r['roots']);labels.update(dict(r.get('owners',[])))
        masksets[m]=set(fs)-set(map(int,cs));cells[str(m)]={'root':None,'cases':cs}
    full=sorted(f for f in all_f if all(f not in s for s in masksets.values()));print('FULL',full,'leaves',sum(len(v['cases']) for v in cells.values()),'number open',sum(map(len,masksets.values())),flush=True)
    needed=sorted(q for q in labels if q>=2**64)
    for q in needed:
        if str(q) in known:continue
        key=sha256(str(q).encode()).hexdigest()[:24]
        obj=f'49b19bbdf6c46ac3cdd4cb0da2b6b08e1360fdec:Research/NightOrder/ECPP/{key}.json.gz'
        pr=run(['git','cat-file','blob',obj],capture_output=True,cwd=REPO)
        if pr.returncode==0:known[str(q)]=json.loads(gzip.decompress(pr.stdout))
    missing=[q for q in needed if str(q) not in known]; print('labels',len(needed),'generate',len(missing),'bits',max(map(int.bit_length,missing),default=0),flush=True)
    if missing:
        cmd=['wsl','--exec','/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr/bin/gp-2.17','-q','-f','-s','128M']; script='default(nbthreads,1);\n'+''.join(f'print(primecert({q}));\n' for q in missing)
        p=run(cmd,input=script.encode(),capture_output=True,cwd=REPO,timeout=1100,check=True)
        rs=[json.loads(x) for x in p.stdout.splitlines() if x.strip()];assert len(rs)==len(missing),p.stderr
        known.update({str(q):r for q,r in zip(missing,rs)})
    ecpp={}
    for q in needed:
        a=known[str(q)];n=q;assert a
        for r in a:
            assert r[0]==n;n=C.pc.level(*r)
        assert C.pc.prime64(n);ecpp[str(q)]=a
    packet=ns.out.resolve();assert packet.is_relative_to(H); payload=json.dumps(dict(masks=cells,full_fibers=full,ecpp=ecpp),sort_keys=True,separators=(',',':')).encode()
    temp=packet.with_suffix('.tmp'); temp.write_bytes(gzip.compress(payload,mtime=0));temp.replace(packet)
    print('SHA256',sha256(packet.read_bytes()).hexdigest(),flush=True)

if __name__=='__main__':main()
