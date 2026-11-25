"""Standalone stdlib replay for arbitrary subsets of the original eight roots. Uses the original PINNED certified terminal archive to regenerate factor-edge/primality guarantees; may safely discard original variable restrictions when forbidden set shrinks. Every retained edge filtered against NEW support. Requires only already tracked `Session20261122` files, not SciPy/NumPy. Outputs-only lower bounds; no published shard unless mapped independently."""
from pathlib import Path
from math import gcd
import sys,json,gzip,argparse,hashlib
R=Path(__file__).resolve().parents[1];T=R/'Session20261122';sys.path.insert(0,str(T/'Python'));from TerminalCertificate import allowed,build_model,DYADIC,verify;from RoadblockDual import SCALE,odd_primes,log_bounds
ROOTS={3,5,7,11,13,17,19,31}

def main():
    a=argparse.ArgumentParser();a.add_argument('packet',type=Path);o=a.parse_args();data=json.loads(o.packet.read_text());arc=json.load(gzip.open(T/'Certificates/TerminalOriginal.json.gz','rt'));verify(arc);before=set();den=DYADIC*log_bounds(10)[1]
    for r in data:
        bad=r['forbidden'];assert len(set(bad))==len(bad) and set(bad)<=ROOTS and tuple(sorted(bad)) not in before;before.add(tuple(sorted(bad)));L=r['L'];cut=r['cut'];assert L==arc['limit'] and cut==arc['cutoff'];base=set(odd_primes(L))-set(bad);edges=[tuple(x) for x in arc['edges'] if x[0] in base and x[2] not in bad and x[1]<=cut and allowed(x[0],x[1],bad)];C,rows,tail=build_model(bad,L,cut,edges);w=[0]*len(rows);last=-1
        for j,v in r['weights']:
            if type(j)!=int or type(v)!=int or not last<j<len(rows) or v<0:raise ValueError('bad dual weight')
            w[j]=v;last=j
        reduced=[c*DYADIC for c in C];z=0
        for v,(terms,d) in zip(w,rows):
            if not v:continue
            z-=v*d
            for j,a in terms:reduced[j]+=a*v
        if reduced[tail]<0:raise ValueError('negative tail')
        z+=sum(min(0,v) for j,v in enumerate(reduced) if j!=tail)
        if z!=r['lb'] or z<=2400*den:raise ValueError('insufficient lower bound')
        print('avoid',bad,'certified lower exponent (rounded down)',z*10**6//den)
if __name__=='__main__':
    if not __debug__:raise SystemExit('disable -O')
    main()
