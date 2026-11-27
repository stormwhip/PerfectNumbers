"""Exact canonical root (7,438) and forced-pivot mask enumeration."""
from functools import cache
from math import prod
from fractions import Fraction
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent; REPO=H.parents[2]; R=REPO/'Research'
sys.path[:0]=[str(R/'Session20261126'),str(R/'FinalSprint'),str(R/'Nov25/Compose')]
from PivotCheck import C,B,floor10
P,E,Q=7,438,572749682520506652634407616247
A=C.sigma(P,E); ORDER=tuple(C.ORDER)
FRONT=json.loads((R/'Session20261126/OpenSupport.json').read_bytes())['rows']['7:438']
ALL=list(range(2,256,4))
SCOUT=Path('E:/PerfectNumbers/Build/Night2400/Scout7x438F6.json')


def groups(m):
    assert m in ALL
    return tuple(q for i,q in enumerate(ORDER) if i>=2 and m>>i&1),tuple(q for i,q in enumerate(ORDER) if i>=2 and not m>>i&1)


def state(rows,m=None):
    if m is None:return C.State(rows)
    yes,no=groups(m);return C.State(rows,yes,no)


def dead(s):
    return s.conflict or s.base>B or prod(C.sigma(z,f) for z,f in s.rows.items())>2*s.X


def expand(rows,q,m=None):
    s=state(rows,m)
    assert not dead(s) and q not in s.rows and q not in s.bad and s.D%q==0
    f=v=C.valuation(s.D,q); scale=s.base//q**v; out=[]
    while scale*q**f<=B:
        if s.possible(q,f,v) and not dead(state(rows+[(q,f)],m)):out.append(f)
        f+=1
    return out,f


@cache
def earliest(q,f,sp,bad):
    f+=((1-f)%4 if sp else f%2); step=4 if sp else 2
    while not C.permitted(q,f,bad):f+=step
    return f


def abundance(s,roots=()):
    r=(set(roots)|set(s.present))-s.rows.keys();assert all(q in s.present or s.D%q==0 for q in r)
    h={q:max(1,C.valuation(s.D,q)) for q in r}
    def av(q,f):return Fraction(C.sigma(q,f),q**f)
    k={q:av(q,earliest(q,v,False,s.bad)) for q,v in h.items()}
    b=Fraction(prod(C.sigma(q,f) for q,f in s.rows.items()),s.X)*prod(k.values());al=[b]
    if not s.fixed_euler:
        for q,v in h.items():
            if C.euler(q,s.bad):al.append(b/k[q]*av(q,earliest(q,v,True,s.bad)))
    return min(al)


def roots_for(rows,s,finder,extra=()):
    f={q for p,e in rows for q in finder.factors(p,e)}|set(s.present)|set(extra)
    return sorted(q for q in f if q not in s.rows and q not in s.bad and (q in s.present or s.D%q==0))
