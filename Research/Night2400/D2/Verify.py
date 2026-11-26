"""Cold-verification of all 64 supports at 7^28 || N with 19 absent."""
from pathlib import Path
from fractions import Fraction
from functools import cache
from hashlib import sha256
from math import gcd, prod
import argparse, gzip, json, sys

H=Path(__file__).resolve().parent
R=H.parents[1]
sys.path[:0]=[str(R/'Session20261126'),str(R/'FinalSprint/Support')]
from PivotCheck import C, floor10
from ForestMasks import factory as independent

S8=(19,7,11,31,13,3,5,17)
P,E=7,28
X=P**E
A=(P**(E+1)-1)//(P-1)
ROOTS=(59,127540261,71316922984999)
B=10**2400


def groups(m):
    assert type(m)==int and m in range(2,256,4)
    return tuple(q for i,q in enumerate(S8) if q!=P and m>>i&1),tuple(q for i,q in enumerate(S8) if not m>>i&1)


def abundance(need,banned):
    """Small exponent-free support exclusions, minimizing optional Euler placement."""
    assert set(need).isdisjoint(banned) and 19 in banned
    def lower(q,start,odd):
        f=start; step=4 if odd else 2
        while any(pow(q,f+1,b*(q-1))==1 for b in banned):
            f+=step
        n=q**f
        return Fraction((q*n-1)//(q-1),n)
    listed=sorted(set(need)|set(ROOTS)); even={q:lower(q,2,False) for q in listed}
    base=Fraction(A,X)*prod(even.values());opts=[base]
    for q in listed:
        if q%4==1 and gcd(q+1,prod(banned))==1:
            opts.append(base/even[q]*lower(q,1,True))
    return min(opts)


def trim_old(roots, owners, need, banned):
    rr=sorted(set(roots)|set(need));seen=set(rr);out={}
    edges=[(q,z) for q,z in owners if q not in banned and q not in seen and q!=P and A%q]
    while True:
        n=len(out)
        for q,z in edges:
            if z in seen and q not in seen:
                out[q]=z;seen.add(q)
        if n==len(out):return rr,sorted(out.items())


def run(packet, projected=False):
    if not __debug__:raise RuntimeError('assertions required; do not use -O')
    assert tuple(C.ORDER)==S8 and C.pc.prime64(P) and prod(ROOTS)==A
    assert all(C.pc.prime64(q) for q in set(ROOTS)|set(S8))
    old=json.loads(gzip.decompress((R/'FinalSprint/Support/Root7x28.json.gz').read_bytes()))
    front=json.loads((R/'Session20261126/OpenSupport.json').read_bytes());assert front['order']==list(S8)
    projected_masks=set(front['rows']['7:28']);assert len(projected_masks)==26
    old_masks=set(map(int,old['closed']));assert len(old_masks)==13 and old_masks<=projected_masks
    raw=packet.read_bytes();data=json.loads(gzip.decompress(raw));assert set(data)=={'cases','ecpp'}
    assert not set(old['ecpp'])&set(data['ecpp'])
    table=dict(old['ecpp'],**data['ecpp']); seen=set()
    @cache
    def prime(z):
        assert type(z)==int and z>2
        n=z
        if z>=2**64:
            chain=table[str(z)];assert chain
            for row in chain:
                assert row[0]==n;n=C.pc.level(*row)
            seen.add(str(z))
        assert C.pc.prime64(n)
        return True
    old_row=old['row']; assert (old_row['p'],old_row['e'])==(P,E) and old_row['roots']==list(ROOTS)
    cases=data['cases']; used=set(); counts={'old':0,'new':0,'abundance':0}; floors={k:[] for k in counts}; covered=[]
    for m in range(2,256,4):
        if projected and m not in projected_masks:continue
        need,banned=groups(m); assert banned[0]==19
        state=C.State([(P,E)],need,banned[1:]);assert not state.conflict
        if m in old_masks:
            r,o=trim_old(old_row['roots'],old_row['owners'],need,banned)
            h=old_row['head'];source='old'
        elif str(m) in cases:
            row=cases[str(m)];assert set(row)=={'roots','owners','head'}
            r,o,h=map(row.get,('roots','owners','head'));source='new';used.add(str(m))
        else:
            z=abundance(need,banned);assert z>2,('open mask',m)
            counts['abundance']+=1;floors['abundance'].append(z.numerator*10**6//z.denominator);covered.append(m)
            print('PASS',m,'abundance',floors['abundance'][-1],flush=True)
            continue
        C.validate_forest(state,r,o,h,prime)
        x=C.Forest(state,r,o,h).lower()[0]
        y=independent(dict(p=P,e=E,roots=r,owners=o,head=h),need)(banned)
        assert min(x,y)>B,('forest underpriced',m,floor10(x),floor10(y))
        counts[source]+=1;floors[source].append(floor10(min(x,y)));covered.append(m)
        print('PASS',m,source,'floor',floors[source][-1],flush=True)
    assert used==set(cases) and seen-set(old['ecpp'])==set(data['ecpp'])
    if not projected:
        assert counts=={'old':13,'new':27,'abundance':24}
    assert set(covered)==(projected_masks if projected else set(range(2,256,4)))
    assert (projected_masks-old_masks)<=set(map(int,cases))
    print('VERIFIED',(P,E),'masks',len(covered),counts,'floors',{k:min(f,default=None) for k,f in floors.items()},'new ECPP',len(data['ecpp']),'SHA256',sha256(raw).hexdigest(),flush=True)


if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--packet',type=Path,default=H/'Seven28.json.gz');ap.add_argument('--projection-only',action='store_true');ns=ap.parse_args();run(ns.packet,ns.projection_only)
