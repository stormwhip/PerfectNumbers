"""Targeted discovery from untrusted owner hints; no historical code imports."""
import argparse
from collections import defaultdict
from functools import cache
import gzip
from hashlib import sha256
import json
import mmap
from pathlib import Path
import struct
import sys
from time import monotonic

sys.path.insert(0,str(Path(__file__).resolve().parent))
from Compose import B, ORDER, pc, sigma, valuation, nonsupport, permitted, euler, State, Forest

H = Path(__file__).resolve().parent
D = Path('E:/PerfectNumbers/overnight/Research/NightLowRoute')
CACHE = Path('E:/PerfectNumbers/NightCache')
BEST = {(13,10):'Intra', (13,12):'Back', (13,22):'Back', (19,16):'Back', (19,22):'QFine', (31,10):'QFine', (31,6):'QFine'}


@cache
def read(f):
    raw = f.read_bytes()
    return json.loads(gzip.decompress(raw) if f.suffix=='.gz' else raw)


class Facts:
    """Read-only adapter for the existing Ochem factor-hint index."""
    def __init__(self):
        with (CACHE/'facts.idx').open('rb') as i, (CACHE/'facts.dat').open('rb') as d:
            self.idx = mmap.mmap(i.fileno(),0,access=mmap.ACCESS_READ)
            self.dat = mmap.mmap(d.fileno(),0,access=mmap.ACCESS_READ)
        self.count=len(self.idx)//32

    def lookup(self,p,h):
        a=14695981039346656037
        b=1099511628211^0x9e3779b97f4a7c15
        mask=2**64-1
        for c in f'{p} {h}'.encode():
            a=((a^c)*1099511628211)&mask
            b=((b^c)*0xbf58476d1ce4e5b9)&mask
            b^=b>>31
        lo,hi=0,self.count
        while lo<hi:
            mid=(lo+hi)//2
            xy=struct.unpack_from('<QQ',self.idx,mid*32)
            if xy<(a,b):lo=mid+1
            else:hi=mid
        if lo==self.count:return ()
        x,y,o,n=struct.unpack_from('<QQQI',self.idx,lo*32)
        return tuple(map(int,self.dat[o:o+n].split())) if (x,y)==(a,b) else ()


class Sources:
    def export(self, path, p, e, tree):
        def used(t):
            k=t['kind']
            if k=='forest':
                yield from t['roots']; yield from dict(t['owners'])
            elif k=='abundance':
                yield from t['support']
            elif k=='terminal':
                yield from dict(t['promoted'])
            elif k=='exp':
                yield t['q']
                for x in t['cells'].values():yield from used(x)
                yield from used(t['tail'])
            elif k=='support':
                yield t['q'];yield from used(t['yes']);yield from used(t['no'])
        cert={str(q):self.cert[str(q)] for q in set(used(tree)) if q>=2**64}
        raw=json.dumps(dict(p=p,e=e,tree=tree,ecpp=cert),separators=(',',':')).encode()
        path.write_bytes(gzip.compress(raw,mtime=0))

    def __init__(self,p,e,bank,facts=False):
        self.facts = Facts() if facts else None
        self.seed = read(D/(BEST[p,e]+f'{p}_{e}.json'))
        self.pres = defaultdict(dict)
        self.cert = {}
        if (D/f'Minimum{p}_{e}.json').is_file():
            for q,_,o in read(D/f'Minimum{p}_{e}.json')['branches']:
                self.pres[q] = dict(o)
        self.children = defaultdict(set)
        self.branch = {}
        if (p,e)==(31,6):
            self.branch.update({(917087137,int(a.stem.split('_')[1])):a for a in D.glob('A6_*.json')})
        self.certcache = (D/'CertCache', D.parent/'NightOrder/ECPP', D.parent/'EveningTree/ECPP', CACHE/'ecpp-local', Path.home()/'AppData/Local/Temp/perfect-nov25-primes', H/'ecpp')
        seedfiles = [f for f in D.glob(f'*{p}_{e}.json') if 'Profile' not in f.name and 'Wide' not in f.name]
        for f in seedfiles:
            r = read(f)
            if 'owners' in r:
                for q,z in r['owners']:
                    self.children[z].add(q)
        for o in self.pres.values():
            for q,z in o.items():
                self.children[z].add(q)
        released = [*D.joinpath('Release').glob('Forest*.gz'), *H.parents[0].joinpath('Forests').glob('*.gz')]
        for f in released:
            data = read(f)
            self.cert.update(data['ecpp'])
            if bank:
                for r in data['rows']:
                    for q,z in r['owners']:
                        self.children[z].add(q)
        if bank:
            self.archive_factors = defaultdict(set)
            for name in ('Original','Replacement'):
                f = H.parents[1]/f'Session20261122/Certificates/Terminal{name}.json.gz'
                for p,e,q,k in read(f)['edges']:
                    self.archive_factors[p,e].add(q)
        else:
            self.archive_factors = defaultdict(set)
        self.ready = {}
        self.missing=set()

    def prime(self,q):
        if q not in self.ready:
            yes = False
            if q<2**64:
                yes = pc.prime64(q)
            else:
                rows = self.cert.get(str(q))
                if rows is None:
                    h=sha256(str(q).encode()).hexdigest()[:24]
                    filename=next((d/n for d in self.certcache for n in (h+'.json',h+'.json.gz','Prime'+h+'.json') if (d/n).is_file()),None)
                    if filename is not None:
                        rows = read(filename)
                if rows is None:
                    self.missing.add(q)
                if rows:
                    z=q
                    try:
                        for row in rows:
                            if z!=row[0]:
                                break
                            z = pc.level(*row)
                        else:
                            yes = pc.prime64(z)
                    except (ValueError,TypeError,IndexError):
                        yes = False
                    if yes:
                        self.cert[str(q)] = rows
            self.ready[q] = yes
        return self.ready[q]

    def grow(self,roots,seed,s):
        """Reachable known parents only; can safely discard unproved labels."""
        K=set(roots); pending=defaultdict(list)
        for q,z in seed.items():
            if q not in K and q not in s.bad and q not in s.rows and s.D%q and q not in s.present:
                pending[z].append(q)
        used=set(K); o={}; work=list(K)
        while work:
            z=work.pop()
            for q in pending[z]:
                if q not in used and self.prime(q):
                    used.add(q)
                    o[q]=z
                    work.append(q)
        return o

    @cache
    def divisors(self,z,f):
        S=sigma(z,f)
        K={q for q in self.children.get(z,()) if q>2 and not S%q and self.prime(q)}
        K.update(q for q in self.archive_factors.get((z,f),()) if self.prime(q))
        if self.facts:
            for h in range(2,f+2):
                if (f+1)%h==0:
                    K.update(q for q in self.facts.lookup(z,h) if q>2 and not S%q and self.prime(q))
        Z=nonsupport(S,2)
        for q in K:
            Z=nonsupport(Z,q)
        if self.prime(Z):
            K.add(Z)
        return K

    def init(self,s):
        z0=self.seed
        seeds=dict(z0['owners'])
        for q in s.present:
            seeds.update(self.pres[q])
        for z,f in s.rows.items():
            if filename:=self.branch.get((z,f)):
                for q,a in read(filename)['owners']:
                    seeds[q]=a
                    self.children[a].add(q)
                self.divisors.cache_clear()
        roots={q for q in s.present if q not in s.rows}
        pool=set(z0['P'])|set(seeds)
        for p,e in s.rows.items():
            pool.update(self.divisors(p,e))
        for q in pool:
            if not s.D%q and self.prime(q):
                roots.add(q)
        return sorted(roots),self.grow(roots,seeds,s)

    def bound(self,s,head,rounds):
        if s.conflict:
            return B+1,None,[]
        roots,owners=self.init(s)
        assert all(q in roots for q in s.lo)
        best=0; rec=None; witness=[]
        for i in range(rounds+1):
            F=Forest(s,roots,owners,head,record=True)
            b,z=F.lower()
            w=[] if b>B else list(F.witness(z))
            if b>best:
                best,rec,witness=b,{'roots':roots,'owners':sorted(owners.items()),'head':head},w
            if b>B or i==rounds:
                break
            add={}
            for p,e,C in w:
                if C<=1:
                    continue
                for q in self.divisors(p,e):
                    if q not in F.V and q not in s.rows and q not in s.present and q not in s.bad and s.D%q:
                        add.setdefault(q,p)
            if not add:
                break
            owners.update(add)
        return best,rec,witness


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pairs',nargs='+')
    ap.add_argument('--bank',action='store_true')
    ap.add_argument('--facts',action='store_true')
    ap.add_argument('--mask',type=int,action='append')
    ap.add_argument('--head',type=int,default=120)
    ap.add_argument('--rounds',type=int,default=8)
    ap.add_argument('--support',default='3,5,17')
    ap.add_argument('--exact',default='')
    ap.add_argument('--pivot',type=int)
    ap.add_argument('--maxf',type=int,default=12)
    ap.add_argument('--f',type=int,action='append',help='discovery only: filter exact cells')
    ap.add_argument('--save',type=Path,help='write portable positive exact or unsplit cells only')
    ap.add_argument('--verbose',action='store_true')
    a=ap.parse_args()
    for t in a.pairs:
        p,e=map(int,t.split(':'));start=monotonic()
        x=Sources(p,e,a.bank,a.facts)
        exact=[tuple(map(int,t.split(':'))) for t in a.exact.split(',') if t]
        avail=[int(q) for q in a.support.split(',') if q and int(q) not in ORDER[:ORDER.index(p)] and int(q)!=p]
        for mask in range(1<<len(avail)) if a.mask is None else a.mask:
            yes=tuple(q for i,q in enumerate(avail) if mask>>i&1)
            no=tuple(q for q in avail if q not in yes)
            s=State([(p,e),*exact],yes,no)
            cells=[(s,None)]
            if a.pivot is not None:
                z=a.pivot
                assert x.prime(z) and z not in s.rows and (s.D%z==0 or z in s.present)
                v=valuation(s.D,z)
                cells=[(State([(p,e),*exact,(z,f)],yes,no),f) for f in range(1,a.maxf+1) if s.possible(z,f,v)]
                cells.append((State([(p,e),*exact],yes,no,{z:a.maxf+1}),'tail'))
            for s,f0 in cells:
                if a.f is not None and (f0 if isinstance(f0,int) else 0) not in a.f:
                    continue
                b,row,w=x.bound(s,a.head,a.rounds)
                print(t,'yes',yes,'no',no,'pivot',a.pivot,'exp',f0,'bound',b>B,'log',len(str(b))-1,'nodes',len(row['owners']) if row else 0,'time',round(monotonic()-start,1),flush=True)
                if w and a.verbose:
                    print('  witness', sorted((z,f,len(str(C))-1) for z,f,C in w if z in row['roots'] or z<101),flush=True)
                if a.save and b>B and not s.lo:
                    leaf={'kind':'direct'} if row is None else {'kind':'forest',**row}
                    q0=(() if row is None else (*row['roots'],*dict(row['owners'])))
                    K={str(q):x.cert[str(q)] for q in set(q0)|s.rows.keys() if q>=2**64}
                    data=dict(assigned=list(s.rows.items()),present=yes,absent=no,leaf=leaf,ecpp=K)
                    a.save.mkdir(exist_ok=True,parents=True)
                    tag='-'.join(f'{q}x{f}' for q,f in list(s.rows.items())[1:]) or 'bare'
                    f=a.save/f'F{p}x{e}-m{mask}-{tag}.json.gz'
                    f.write_bytes(gzip.compress(json.dumps(data,separators=(',',':')).encode(),mtime=0))


if __name__=='__main__':
    main()
