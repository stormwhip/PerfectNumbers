"""Arithmetic discovery for the exact 7^28 support partition."""
from pathlib import Path
from fractions import Fraction
from math import prod, gcd, log10
from collections import defaultdict
import gzip, json, sys
H = Path(__file__).resolve().parent
REPO = H.parents[2]
R = REPO/'Research'
sys.path[:0] = [str(R/'Session20261126'),str(R/'FinalSprint'),str(R/'Nov25/Compose')]
from PivotCheck import C, B, floor10
S8 = tuple(C.ORDER)
P,E,Q = 7,28,71316922984999
A = C.sigma(P,E)
SEEDS = (59,127540261,Q)
assert prod(SEEDS)==A and all(C.pc.prime64(q) for q in SEEDS)
OLD = json.loads(gzip.decompress((R/'FinalSprint/Support/Root7x28.json.gz').read_bytes()))
FRONT = json.loads((R/'Session20261126/OpenSupport.json').read_bytes())['rows']['7:28']
MISSING = sorted(set(FRONT)-set(map(int,OLD['closed'])))


def support(m):
    assert type(m)==int and m&3==2 and 0<m<256
    return tuple(q for i,q in enumerate(S8) if (m>>i&1) and q!=P), tuple(q for i,q in enumerate(S8) if not m>>i&1 and q!=19)


def st(rows,m):
    present,absent = support(m)
    return C.State(rows,present,absent)


def shape(s,roots,es=OLD['row']['owners']):
    K=sorted(set(roots)|set(s.present)-s.rows.keys());seen=set(K); out={}
    es=[(q,z) for q,z in es if q not in s.bad and q not in seen and q not in s.rows and s.D%q]
    while True:
        n=len(out)
        for q,z in es:
            if z in seen and q not in seen:
                out[q]=z;seen.add(q)
        if n==len(out):return K,sorted(out.items())


def abundancy(s,roots):
    def least(q,H,sp):
        f=H+((1-H)%4 if sp else H%2); step=4 if sp else 2
        while not C.permitted(q,f,s.bad):f+=step
        return Fraction(C.sigma(q,f),q**f),f
    if s.conflict:return Fraction(3),None
    roots=sorted(set(roots)|set(s.present)-s.rows.keys());H={q:max(1,C.valuation(s.D,q)) for q in roots}
    assert all(q in s.present or s.D%q==0 for q in roots)
    evens={q:least(q,v,False) for q,v in H.items()}; A0=Fraction(prod(C.sigma(q,f) for q,f in s.rows.items()),s.X)*prod(a for a,f in evens.values());alts=[(A0,None)]
    if not s.fixed_euler:
        for q,v in H.items():
            if C.euler(q,s.bad):alts.append((A0/evens[q][0]*least(q,v,True)[0],q))
    return min(alts,key=lambda v:v[0])


def palette(s, base=SEEDS):
    return sorted(set(q for q in base if s.D%q==0)|set(s.present)-s.rows.keys())


def extend(s,q):
    assert q not in s.rows and s.D%q==0 and q not in s.bad
    f=v=C.valuation(s.D,q);scale=s.base//q**v
    cases=[]
    while scale*q**f<=B:
        if s.possible(q,f,v):
            rows=list(s.rows.items())+[(q,f)];m=C.State(rows,s.present,s.bad[1:]);assert m.bad==s.bad
            if not m.conflict and m.base<=B and prod(C.sigma(z,j) for z,j in rows)<=2*m.X:
                cases.append((f,m))
        f+=1
    return cases,f


if __name__=='__main__':
    print('historical',sorted(OLD['closed'],key=int),'initial',len(FRONT),'residual',MISSING,flush=True)
    for m in MISSING:
        s=st([(P,E)],m); r,o=shape(s,SEEDS); f=C.Forest(s,r,o,512,record=True); v,w=f.lower();
        cases,tail=extend(s,Q)
        print(m,s.present,s.bad,float(abundancy(s,r)[0]),floor10(v),[(q,h) for q,h,_ in f.witness(w)][:15], 'tail',tail, 'cases',[a for a,t in cases],flush=True)
