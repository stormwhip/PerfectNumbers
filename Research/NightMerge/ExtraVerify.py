"""Strict offline replay of ECM-discovered test factors; each must divide a geometric sum."""
import argparse,gzip,json,sys,hashlib
from pathlib import Path
from functools import cache
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R/'EveningTree'));import IndependentTree as I
@cache
def prime(z):
    if z<2**64:return I.ec.prime64(z)
    k=hashlib.sha256(str(z).encode()).hexdigest()[:24];rows=json.loads(gzip.decompress((H/'ECPP'/(k+'.json.gz')).read_bytes()));n=z
    for row in rows:
        if row[0]!=n:return False
        n=I.ec.level(*row)
    return I.ec.prime64(n)
def verify(rows):
    eligible={(s['root'],e) for s in json.loads((R/'EveningMerge/Audit.json').read_text())['remaining_shards'] for e in s['remaining_actuals']};proof=set()
    for r in rows:
        p,e,fs=r['p'],r['e'],r['fs'];edges=r['witness']
        if (p,e) not in eligible or p not in (7,11,13,19,31) or e%2 or (p,e) in proof or len(fs)!=len(set(fs)) or {z for _,_,z in edges}!=set(fs):raise ValueError('invalid scope')
        for z,f,q in edges:
            if z<=1 or q<=2 or f<1 or pow(z,f+1,q*(z-1))!=1 or not prime(q):raise ValueError('invalid sigma witness')
        # A listed z is a trial divisor, not forced globally: the independent proof only uses z if z|D in this node.
        t=I.Proof(p,e,fs,False,True);t.depth_limit=r['depth']
        if not t.prove():raise ValueError('unresolved tree')
        proof.add((p,e));print('verified',p,e,dict(t.stats),flush=True)
    return proof
if __name__=='__main__':
    if not __debug__:raise SystemExit('Run without -O')
    ap=argparse.ArgumentParser();ap.add_argument('file',nargs='?',default='ExtraAnchors.json');a=ap.parse_args();verify(json.loads((H/a.file).read_text()))
