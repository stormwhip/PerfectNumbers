"""Local discovery; optional indexed factors require the explicitly supplied read-only discovery directory."""
from Domain import *
from math import log10
from fractions import Fraction
from itertools import product
from pathlib import Path

H = Path(__file__).resolve().parent
U, V = 232955070372754085071, 255153692787972397812167227080247511906799034201829146831207531709920886827180456213124673685864777790858521
F2 = [3, 7, 43, 121909, 14644051, 22753985580739682448512055047868836831212984820263, 25827259]
F4 = [5, 11, 761, U, V, 25827259]


def seed(extra=()):
    old, _, _ = inputs()
    return dict(old['ecpp'], **{str(rows[0][0]): rows for rows in json.loads((H/'ECMF4.json').read_bytes())}, **dict(extra))


def base_graphs(old):
    rs = {r['f']: r for r in old['rows']}
    seq = [rs[f] for f in (8, 14, 24, 6, 18, 22, 10, 12, 16, 20)]
    return [t['owners'] for t in seq] + [[edge for t in seq for edge in t['owners']]]


def trim(s, rs, es):
    reach = set(rs); own = {}
    es = [(q,z) for q,z in es if q not in s.rows and q not in reach and q not in s.bad and s.D % q]
    while True:
        old = len(own)
        for q,z in es:
            if q not in reach and z in reach:
                reach.add(q); own[q] = z
        if old == len(own):
            break
    return sorted(own.items())


@cache
def first(q, lo, odd, bad):
    s = 4 if odd else 2
    f = lo + ((1-lo)%4 if odd else lo%2)
    while not C.permitted(q,f,bad):
        f += s
    return f


def bound(s, roots):
    aff = {q: max(1, C.valuation(s.D, q)) for q in roots}
    norm = {q: first(q, h, False, s.bad) for q,h in aff.items()}
    odd = {q: first(q,h,True,s.bad) for q,h in aff.items() if not s.fixed_euler and C.euler(q,s.bad)}
    def abundance(q,f): return Fraction(C.sigma(q,f),q**f)
    a = Fraction(prod(C.sigma(q,f) for q,f in s.rows.items()), s.X) * prod(abundance(q,f) for q,f in norm.items())
    lows = [a] + [a*abundance(q,f)/abundance(q,norm[q]) for q,f in odd.items()]
    return min(lows), norm, odd


def roots(s, f):
    return sorted((s.present | {q for q in F2+F4 if s.D % q == 0}) - s.rows.keys())


if __name__ == '__main__':
    old, _, missing = inputs(); graphs = base_graphs(old)
    ecpp = seed(); assert all(prime_chain(q,ecpp) for q in set(F2+F4+[Q]))
    assert C.sigma(Q,4) == 5*11*761*U*V
    for m in missing:
        f = next(f for f in branches(m)[0] if f in (2,4)); a,b = groups(m); s = C.State(feasible(f)[0],a,b); k = roots(s,f)
        d,ns,os = bound(s,k); candidates=[]
        if d <= 2:
            for idx in [0,1,2,10]:
                es = trim(s,k,graphs[idx]); ff = C.Forest(s,k,es,384,record=True); x,y=ff.lower(); candidates.append((floor10(x),idx,[(q,h) for q,h,r in ff.witness(y)]))
        print(m,f,float(d),max(candidates,default=None),flush=True)
