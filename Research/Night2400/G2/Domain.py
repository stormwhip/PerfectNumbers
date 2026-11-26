"""Exact first-pivot partitions for (19,432)."""
from functools import cache
from math import prod, gcd, log10
from pathlib import Path
from fractions import Fraction
import gzip,json,sys
H=Path(__file__).resolve().parent; REPO=H.parents[2]; R=REPO/'Research'
sys.path[:0]=[str(R/'Session20261126'),str(R/'FinalSprint'),str(R/'Nov25/Compose')]
from PivotCheck import C,B,floor10
P,E,Q=19,432,11842464881317660217
A=C.sigma(P,E); ORDER=tuple(C.ORDER)
FRONT=json.loads((R/'Session20261126/OpenSupport.json').read_bytes())['rows']['19:432']
ALL=list(range(1,256,2))


def groups(m):
    assert m in ALL
    return tuple(q for i,q in enumerate(ORDER) if i>=1 and m>>i&1),tuple(q for i,q in enumerate(ORDER) if i>=1 and not m>>i&1)


def state(rows,m):
    yes, no = groups(m)
    return C.State(rows,yes,no)


def dead(s):
    return s.conflict or s.base>B or prod(C.sigma(z,f) for z,f in s.rows.items())>2*s.X


def expand(rows,q,m):
    s=state(rows,m); assert not dead(s) and q not in s.rows and q not in s.bad and s.D%q==0
    f=v=C.valuation(s.D,q); scale=s.base//q**v; out=[]
    while scale*q**f<=B:
        if s.possible(q,f,v):
            t=state(rows+[(q,f)],m)
            if not dead(t):out.append(f)
        f+=1
    return out,f


@cache
def earliest(q,f,sp,bad):
    f+=((1-f)%4 if sp else f%2); step=4 if sp else 2
    while not C.permitted(q,f,bad):f+=step
    return f


def abundance(s,roots=()):
    r=set(roots)|set(s.present)-s.rows.keys();assert all(q in s.present or s.D%q==0 for q in r)
    h={q:max(1,C.valuation(s.D,q)) for q in r}
    def av(q,f):return Fraction(C.sigma(q,f),q**f)
    k={q:av(q,earliest(q,v,False,s.bad)) for q,v in h.items()}
    b=Fraction(prod(C.sigma(q,f) for q,f in s.rows.items()),s.X)*prod(k.values());al=[b]
    if not s.fixed_euler:
        for q,v in h.items():
            if C.euler(q,s.bad):al.append(b/k[q]*av(q,earliest(q,v,True,s.bad)))
    return min(al)


if __name__=='__main__':
    from Discover import Finder,Bank
    find=Finder(Bank(Path('E:/PerfectNumbers/Build/Night2400/FactorData')),26)
    allf=set()
    for m in ALL:
        s=state([(P,E)],m);fs,t=expand([(P,E)],Q,m); allf.update(fs); print('MASK',m,groups(m),'rootab',float(abundance(s,(Q,))),'f',fs,'tail',t,flush=True)
    for f in sorted(allf):
        qs=find.factors(Q,f);print('PIVOT',f,'factors',qs,'cofactor bits',(C.sigma(Q,f)//prod(q**C.valuation(C.sigma(Q,f),q) for q in qs)).bit_length(),flush=True)
        pairs=[]
        for m in ALL:
            s=state([(P,E),(Q,f)],m)
            if not dead(s):
                qs1=[q for q in qs if q not in s.rows and q not in s.bad and s.D%q==0]
                a=abundance(s,qs1);pairs.append((m,round(float(a),6),floor10(s.base)))
        print('LIVE',f,pairs,flush=True)
