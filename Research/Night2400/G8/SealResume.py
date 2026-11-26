"""Seal the final exact f=6 forest using the local trial graph, not proof code."""
from pathlib import Path
import gzip,json,subprocess
from hashlib import sha256
from Domain import P,E,Q,C,B

H=Path(__file__).resolve().parent

def main():
    src=json.loads((H/'trials/splitresume-0-6-1.json').read_bytes())
    s=C.State([(P,E),(Q,6),(3032394642737237,4)])
    k,o,h=map(src.get,('roots','owners','head')); forest=C.Forest(s,k,o,h)
    assert forest.lower()[0]>B
    active={q for q,_,_ in forest.memo}; oo=[pair for pair in o if pair[0] in active]
    if C.Forest(s,k,oo,h).lower()[0]>B:o=oo
    n=sorted(q for q in set(k)|dict(o).keys() if q>=2**64)
    old=json.loads(gzip.decompress((H/'Thirteen508.json.gz').read_bytes()))['ecpp']; missing=[q for q in n if str(q) not in old]
    if missing:
        gp='/mnt/e/PerfectNumbers/Build/Night2400/LinuxTools/usr/bin/gp-2.17'; text='default(nbthreads,1);\n'+''.join(f'print(primecert({q}));\n' for q in missing)
        out=subprocess.run(['wsl','--exec',gp,'-f','-q','-s','128M'],input=text.encode(),capture_output=True,check=True,timeout=480)
        cert=[json.loads(a) for a in out.stdout.splitlines() if a.strip()];assert len(cert)==len(missing) and all(cert)
        old.update({str(q):a for q,a in zip(missing,cert)})
    if not all(C.pc.prime64(q) for q in set(k)|dict(o).keys() if q<2**64):raise AssertionError('not prime64')
    raw=gzip.compress(json.dumps(dict(roots=k,owners=o,head=h,ecpp={str(q):old[str(q)] for q in n}),separators=(',',':'),sort_keys=True).encode(),mtime=0)
    (H/'Resume6.json.gz').write_bytes(raw); print('labels',len(n),'generated',len(missing),'SHA256',sha256(raw).hexdigest())

if __name__=='__main__':main()
