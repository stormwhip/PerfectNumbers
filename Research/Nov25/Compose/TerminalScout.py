"""Focused terminal scout: no conclusions depend on floating solver success."""
import argparse
from collections import defaultdict
from math import prod
from pathlib import Path
import sys
from time import monotonic

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Scout import Sources,D,BEST,read
from Compose import State,ORDER,B,sigma,valuation
from Terminal import model,solve,price,DYADIC,L,log_bounds


def ranked(s,src,limit=28,layers=2):
    roots,_=src.init(s)
    initial=set(roots)|set(s.present)
    touch={q for q in initial if q not in s.rows and q not in s.bad}
    explicit={q:min(limit,64) for q in touch}
    pending=set(touch);E=set()
    for stage in range(layers):
        follow=set()
        for q in sorted(pending):
            for f in range(1,max(explicit[q],36 if q<L else 0)+1):
                if not s.possible(q,f,0):continue
                for a in src.divisors(q,f):
                    if a in s.bad or a in s.rows:continue
                    E.add((q,a))
                    if a not in explicit:
                        explicit[a]=0
                        follow.add(a)
        pending=follow
        if stage+1<layers:
            # Keep expansion tight around anchors. All other receiving bases
            # retain even/Euler tail cells and can still participate as targets.
            pending={q for q in pending if q.bit_length()<120}
            for q in pending:
                explicit[q]=min(8,limit)
    return explicit,E


def data(s,src,limit,layers,usearchive):
    promoted,E=ranked(s,src,limit,layers)
    if usearchive:
        for (q,f),T in src.archive_factors.items():
            if q>=L or q in s.rows or q in s.bad or f>36 or not s.possible(q,f,0):continue
            for a in T:
                if a in s.rows or a in s.bad or not src.prime(a):continue
                if a>=L:promoted.setdefault(a,0)
                E.add((q,a))
    return sorted(promoted.items()),sorted(E)


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('pairs',nargs='+')
    ap.add_argument('--support',default='3,5,17')
    ap.add_argument('--mask',type=int,action='append')
    ap.add_argument('--exact',default='')
    ap.add_argument('--pivot',type=int)
    ap.add_argument('--f',action='append',type=int)
    ap.add_argument('--tail',type=int,help='assume pivot has at least this exponent')
    ap.add_argument('--facts',action='store_true')
    ap.add_argument('--archive',action='store_true')
    ap.add_argument('--limit',default=20,type=int)
    ap.add_argument('--layers',default=2,type=int)
    ap.add_argument('--save-branches',type=Path,help='write only locally certified, explicitly conditional leaf data')
    a=ap.parse_args()
    for t in a.pairs:
        p,e=map(int,t.split(':'));start=monotonic()
        src=Sources(p,e,True,a.facts)
        split=[int(q) for q in a.support.split(',') if q and int(q) not in ORDER[:ORDER.index(p)] and int(q)!=p]
        exact=[tuple(map(int,t.split(':'))) for t in a.exact.split(',') if t]
        for mask in a.mask if a.mask is not None else range(1<<len(split)):
            yes=tuple(q for i,q in enumerate(split) if mask>>i&1)
            no=tuple(q for q in split if q not in yes)
            s0=State([(p,e),*exact],yes,no)
            for f in a.f or (0,):
                ff=([(a.pivot,f)] if f and a.pivot else [])
                lo={a.pivot:a.tail} if a.tail else None
                s=State([(p,e),*exact,*ff],yes,no,lo)
                if s.conflict or s.base>B:
                    print(t,yes,no,ff,'direct',flush=True)
                    continue
                promoted,E=data(s,src,a.limit,a.layers,a.archive)
                print(t,yes,no,ff,'launch',len(promoted),len(E),'time',round(monotonic()-start,2),flush=True)
                m=model(s,promoted,E,src.prime)
                if a.pivot and f and not s0.possible(a.pivot,f,valuation(s0.D,a.pivot)):
                    raise ValueError('nonapplicable branch')
                nominal,exactscore,w=solve(m)
                print(t,yes,no,ff,'score',(nominal,exactscore),'vars',len(m[0]),'rows',len(m[1]),'time',round(monotonic()-start,2),flush=True)
                if w is not None and price(m,w)>2400*DYADIC*log_bounds(10)[1] and a.save_branches and not a.tail:
                    import gzip,json
                    K={str(q):src.cert[str(q)] for q,h in promoted if q>=2**64}
                    leaf={'kind':'terminal','promoted':promoted,'edges':E,'weights':w}
                    packet={'assigned':list(s.rows.items()),'present':yes,'absent':no,'leaf':leaf,'ecpp':K}
                    a.save_branches.mkdir(exist_ok=True,parents=True)
                    spec='-'.join(map(str,split)) or 'none'
                    tag='-'.join(f'{q}x{v}' for q,v in exact) or 'bare'
                    path=a.save_branches/f'T{p}x{e}-s{spec}-m{mask}-{tag}-f{f}.json.gz'
                    path.write_bytes(gzip.compress(json.dumps(packet,separators=(',',':')).encode(),mtime=0))


if __name__=='__main__':
    main()
