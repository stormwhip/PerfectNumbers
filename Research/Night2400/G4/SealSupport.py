"""Optional construction of the finite abundance-only support addendum."""
from Domain import *
from Search import catalog,extra_factors
from Support import projected_tree
from hashlib import sha256
from subprocess import run
import argparse


def main(packet):
    from Discover import Finder,Bank
    finder=Finder(Bank(Path('E:/PerfectNumbers/Build/Night2400/FactorData')),25)
    tree=json.loads(gzip.decompress(packet.read_bytes())); gaps=projected_tree(tree)
    cases=[r for f in sorted(gaps) for r in gaps[f]]
    masks={}; labels=set()
    for m in FRONT:
        a=[]; good=True
        for assignment in cases:
            s=state(assignment,m)
            if dead(s): a.append(None);continue
            extra={z for q,f in assignment for z in extra_factors().get((q,f),())}
            k=roots_for(assignment,s,finder,extra)
            if abundance(s,k)<=2:good=False;break
            for q in [z for z in k if z not in s.present][::-1]:
                kk=[z for z in k if z!=q]
                if abundance(s,kk)>2:k=kk
            a.append(k)
        if good:
            masks[str(m)]=a;labels.update(q for z in a if z for q in z if q>=2**64)
    assert masks
    _,known=catalog();known.update(tree['ecpp'])
    missing=[q for q in sorted(labels) if str(q) not in known]
    if missing:
        cmd=['wsl','--exec','/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr/bin/gp-2.17','-q','-f','-s','128M']
        proc=run(cmd,input=('default(nbthreads,1);\n'+''.join(f'print(primecert({q}));\n' for q in missing)).encode(),capture_output=True,check=True,timeout=180)
        chains=[json.loads(s) for s in proc.stdout.splitlines() if s.strip()];assert len(chains)==len(missing)
        known.update({str(q):r for q,r in zip(missing,chains)})
    raw=gzip.compress(json.dumps(dict(masks=masks,ecpp={str(q):known[str(q)] for q in sorted(labels)}),sort_keys=True,separators=(',',':')).encode(),mtime=0)
    (H/'Support372.json.gz').write_bytes(raw)
    print('support masks',sorted(map(int,masks)),'ECPP',len(labels),'SHA256',sha256(raw).hexdigest())

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('tree',type=Path);main(a.parse_args().tree)
