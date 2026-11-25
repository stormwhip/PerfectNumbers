"""Try abundance-priced fixed forests on explicit conditional cells."""
from pathlib import Path
from time import monotonic
import argparse,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Scout import Sources
from Compose import State,ORDER
from Weighted import weighted,log_bounds


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pair');ap.add_argument('--mask',type=int,action='append');ap.add_argument('--f',type=int,action='append');ap.add_argument('--pivot',type=int)
    ap.add_argument('--support',default='3,5,17');ap.add_argument('--exact',default='');ap.add_argument('--rounds',type=int,default=3);ap.add_argument('--head',type=int,default=100);ap.add_argument('--mu',type=int,action='append')
    ap.add_argument('--save',type=Path)
    a=ap.parse_args();p,e=map(int,a.pair.split(':'));src=Sources(p,e,True,True);t=monotonic()
    S=tuple(int(z) for z in a.support.split(',') if z and int(z) not in (*ORDER[:ORDER.index(p)],p)); assigned=[tuple(map(int,z.split(':'))) for z in a.exact.split(',') if z]
    for m in a.mask or range(1<<len(S)):
        yes=tuple(q for i,q in enumerate(S) if m>>i&1);no=tuple(q for q in S if q not in yes)
        for f in a.f or (0,):
            exact=[(a.pivot,f)] if f and a.pivot else []
            s=State([(p,e),*assigned,*exact],yes,no)
            b,row,w=src.bound(s,a.head,a.rounds)
            if row is None or b>10**2400:
                print(a.pair,m,f,'direct/forest',len(str(b))-1,flush=True);continue
            print(a.pair,m,f,'raw',len(str(b))-1,'weighted launching',round(monotonic()-t,1),flush=True)
            for mu in a.mu or (500,1000,2000,4000,8000,16000):
                z=weighted(s,row['roots'],dict(row['owners']),a.head,mu)
                print(a.pair,m,f,'mu',mu,'lowerlog',z//log_bounds(10)[1],'time',round(monotonic()-t,1),flush=True)
                if a.save and z>2400*log_bounds(10)[1]:
                    import gzip,json
                    K={str(q):src.cert[str(q)] for q in set(row['roots'])|dict(row['owners']).keys()|s.rows.keys() if q>=2**64}
                    tracked=dict(kind='weighted',mu=mu,**row)
                    d=dict(assigned=list(s.rows.items()),present=yes,absent=no,leaf=tracked,ecpp=K)
                    a.save.mkdir(exist_ok=True,parents=True)
                    name=f'W{p}x{e}-s'+'-'.join(map(str,S))+f'-m{m}-f{f}-mu{mu}.json.gz'
                    out=a.save/name
                    out.write_bytes(gzip.compress(json.dumps(d,separators=(',',':')).encode(),mtime=0))

if __name__=='__main__':main()
