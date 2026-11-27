"""Optional discovery-side sealing of exact masked assertions on tree holes."""
from Domain import *
from Search import catalog
from hashlib import sha256
from subprocess import run


def main():
    full=json.loads(gzip.decompress((H/'Thirteen262.json.gz').read_bytes())); raw=json.loads(SCOUT.read_bytes())['unresolved']
    def holes(t,rows):
        if t['type']=='open':return {tuple(rows)}
        if t['type']!='split':return set()
        return set.union(set(),*(holes(v,rows+[(t['q'],int(f))]) for f,v in t['cases'].items()))
    pending=set.union(set(),*(holes(t,[(P,E),(Q,int(f))]) for f,t in full['cases'].items()))
    cases={}
    from flint import fmpz
    for p in (H/'trials').glob('*-*-*-*.json'):
        tag,m,f,i=p.stem.split('-');m,f,i=map(int,(m,f,i)); t=json.loads(p.read_bytes())
        if m==0 or t['score']<2400:continue
        r=tuple(map(tuple,raw[str(f)][i][0]));s=state(r,m)
        if r not in pending:continue
        k,o,h=map(t.get,('roots','owners','head'));forest=C.Forest(s,k,o,h)
        if forest.lower()[0]<=B or not all(fmpz(q).is_probable_prime() for q in set(k)|dict(o).keys()):continue
        seen={q for q,_,_ in forest.memo};active=[edge for edge in o if edge[0] in seen]
        if C.Forest(s,k,active,h).lower()[0]>B:o=active
        y=dict(roots=k,owners=o,head=h); key=(m,r)
        if key not in cases or len(o)<len(cases[key]['owners']):cases[key]=y
    from Discover import Finder,Bank
    finder=Finder(Bank(Path('E:/PerfectNumbers/Build/Night2400/FactorData')),24)
    for m in ALL:
        for r in pending:
            if (m,r) in cases:continue
            s=state(r,m)
            if dead(s):cases[m,r]=None;continue
            roots=roots_for(r,s,finder)
            if abundance(s,roots)<=2:continue
            for q in [z for z in roots if z not in s.present][::-1]:
                others=[z for z in roots if z!=q]
                if abundance(s,others)>2:roots=others
            cases[m,r]={'kind':'abundance','roots':roots}
    full_masks=[m for m in ALL if all((m,r) in cases for r in pending)]
    labels=sorted({q for leaf in cases.values() if leaf is not None for q in [*leaf['roots'],*dict(leaf.get('owners',[]))] if q>=2**64 and str(q) not in full['ecpp']})
    _,known=catalog();todo=[q for q in labels if str(q) not in known]
    if todo:
        cmd=['wsl','--exec','/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr/bin/gp-2.17','-q','-f','-s','128M']
        text='default(nbthreads,1);\n'+''.join(f'print(primecert({q}));\n' for q in todo)
        p=run(cmd,input=text.encode(),capture_output=True,timeout=900,check=True)
        cert=[json.loads(s) for s in p.stdout.splitlines() if s.strip()];assert len(cert)==len(todo)
        known.update({str(q):c for q,c in zip(todo,cert)})
    out=H/'Masks262.json.gz'; data=dict(cases=[(m,r,t) for (m,r),t in sorted(cases.items())],ecpp={str(q):known[str(q)] for q in labels},full_masks=full_masks)
    packet=gzip.compress(json.dumps(data,separators=(',',':'),sort_keys=True).encode(),mtime=0);out.write_bytes(packet)
    print('CASES',[(m,r[1][1],r[-1]) for m,r,_ in data['cases']],'ECPP',len(labels),'SHA256',sha256(packet).hexdigest(),flush=True)

if __name__=='__main__':main()
