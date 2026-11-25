"""Optional, offline ordinary forest discovery. Not a proof verifier.
Build the published data-v1 index with Sources/Cpp/BuildIndex.cpp, then run:
python Research/Session20261126/Discover.py --index PATH --out OUT --head 128
Requires python-flint (candidate selection only). Outputs resumable per-key trials.
"""
import argparse, json, math, mmap, struct, sys
from functools import lru_cache
from pathlib import Path
from flint import fmpz
HERE=Path(__file__).resolve().parent;R=HERE.parent
sys.path.insert(0,str(R/'Nov25/Boost'));import BoostScore as bs
MASK=(1<<64)-1
class Bank:
    def __init__(self,folder):
        self.fi=(folder/'facts.idx').open('rb');self.fd=(folder/'facts.dat').open('rb')
        self.index=mmap.mmap(self.fi.fileno(),0,access=mmap.ACCESS_READ);self.values=mmap.mmap(self.fd.fileno(),0,access=mmap.ACCESS_READ)
        if len(self.index)!=1322332128 or len(self.values)!=745826778:raise ValueError('unexpected data-v1 index size')
    @lru_cache(16384)
    def get(self,p,n):
        a=14695981039346656037;b=1099511628211^0x9e3779b97f4a7c15
        for z in f'{p} {n}'.encode():
            a=((a^z)*1099511628211)&MASK;b=((b^z)*0xbf58476d1ce4e5b9)&MASK;b^=b>>31
        lo=0;hi=len(self.index)//32
        while lo<hi:
            m=(lo+hi)//2;u,v,i,k=struct.unpack_from('<QQQI',self.index,m*32)
            if (a,b)==(u,v):return tuple(int(q) for q in self.values[i:i+k].split() if q.isdigit())
            if (a,b)<(u,v):hi=m
            else:lo=m+1
        return ()
@lru_cache(2048)
def ds(n):return sorted({x for k in range(1,math.isqrt(n)+1) if n%k==0 for x in (k,n//k)})
@lru_cache(4096)
def phi(p,n):return (p**n-1)//math.prod(phi(p,d) for d in ds(n)[:-1])
class Finder:
    def __init__(self,db,bits):self.db=db;self.bits=bits
    @lru_cache(8192)
    def factors(self,p,f):
        out=set()
        for d in ds(f+1)[1:]:
            u=phi(p,d)
            for v in self.db.get(p,d):
                if v>1 and u%v==0 and fmpz(v).is_probable_prime():
                    out.add(v)
                    while u%v==0:u//=v
            if u>1 and fmpz(u).is_probable_prime():out.add(u)
            elif u>1 and u.bit_length()<=90:out.update(int(v) for v,h in fmpz(u).factor())
            elif u>1 and self.bits and u.bit_length()<=4400:
                out.update(int(v) for v,h in fmpz(u).factor_smooth(self.bits,0) if v.is_probable_prime())
        return sorted(out-{2})
    def run(self,p,e,a):
        stem=f'{p}x{e}';dest=a.out/(stem+'.json');done=a.out/(stem+'.done');A=bs.sigma(p,e)
        if done.exists():return
        roots=self.factors(p,e);best=0;ow={};seen=set()
        if dest.exists():
            old=json.loads(dest.read_bytes());assert (old['p'],old['e'])==(p,e);roots=sorted(set(roots)|set(old['roots']));ow=dict(old['owners']);best=old['score']
        for _ in range(a.steps if roots else 0):
            r=dict(p=p,e=e,roots=roots,head=a.head,owners=sorted(ow.items()));vs,tr=bs.scorer(r);m=min(vs.values());add={}
            if m>best:
                best=m;tmp=dest.with_suffix('.tmp');tmp.write_text(json.dumps(dict(r,score=m),separators=(',',':')),encoding='utf8');tmp.replace(dest)
            if m<=2400.01:
                for mode,score in sorted(vs.items(),key=lambda x:x[1]):
                    if score>m+100:break
                    for z,(_,f,_,child) in tr(mode).items():
                        if child is False or (z,f) in seen or z.bit_length()*(f+1)>16000:continue
                        seen.add((z,f))
                        for q in self.factors(z,f):
                            if q!=p and A%q and q not in ow:add.setdefault(q,z)
            tr.clear()
            if not add:break
            ow.update(add)
        done.write_text(json.dumps({'pair':[p,e],'best':best,'head':a.head,'steps':a.steps,'smooth_bits':a.smooth_bits,'status':'DISCOVERY_ONLY'}),encoding='utf8');bs.sigma.cache_clear();print(stem,best,flush=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--index',type=Path,required=True);ap.add_argument('--out',type=Path,required=True,help='use a separate output directory per parameter set');ap.add_argument('--head',type=int,default=128);ap.add_argument('--steps',type=int,default=90);ap.add_argument('--smooth-bits',type=int,default=0);ap.add_argument('--root',type=int);ap.add_argument('--exponent',type=int);a=ap.parse_args();assert 1<=a.head<=512 and a.steps>0;a.out.mkdir(exist_ok=True,parents=True);d=json.loads((R/'Midday/Delta.json').read_bytes());finder=Finder(Bank(a.index),a.smooth_bits)
    for p,e in sorted({(s['root'],e) for s in d['remaining_shards'] for e in s['remaining_actuals']}):
        if (a.root is None or a.root==p) and (a.exponent is None or a.exponent==e):finder.run(p,e,a)
