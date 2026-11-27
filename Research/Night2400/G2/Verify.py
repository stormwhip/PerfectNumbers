"""Exact masked pivot coverage for (19,432); no trial or factor bank is used."""
from pathlib import Path
from functools import cache
from fractions import Fraction
from hashlib import sha256
from math import gcd,prod
import argparse,gzip,json,sys

H=Path(__file__).resolve().parent
R=H.parents[1]
sys.path[:0]=[str(R/'Session20261126')]
from PivotCheck import C,floor10

O=(19,7,11,31,13,3,5,17)
P,E,Q=19,432,11842464881317660217
B=10**2400


def sigma(p,e):return (p**(e+1)-1)//(p-1)


def val(n,z):
    v=0
    while n%z==0:n//=z;v+=1
    return v


def trim(n,pool):
    while (g:=gcd(n,pool))>1:n//=g
    return n


def legal(q,f,banned):return all(pow(q,f+1,b*(q-1))!=1 for b in banned)


def domain(banned):
    a=sigma(P,E); x=P**E; cap=val(a,Q); scale=x*(a//Q**cap); f=cap; out={}
    while scale*Q**f<=B:
        if f%2==0 or Q%4==f%4==1:
            z=a*sigma(Q,f); s=z//(1+f%2); xx=x*Q**f
            if val(s,Q)<=f and val(s,P)<=E and gcd(s,prod(banned))==1 and z<=2*xx and xx*trim(s,P*Q)<=B:
                out[f]=[(P,E),(Q,f)]
        f+=1
    assert scale*Q**(f-1)<=B<scale*Q**f
    return out,f


def second(rows,need,banned,roots,edges,head):
    """Independent recurrence with states deriving ordinary and one optional Euler cost."""
    fixed=dict(rows); s=prod(sigma(q,f)//(1+f%2) for q,f in rows)
    d=trim(s,prod(fixed)); x=prod(q**f for q,f in rows)
    parent=dict(edges); kids={q:[] for q in (*roots,*parent)}
    for q,z in edges:kids[z].append(q)
    children_product={p:prod(zs) for p,zs in kids.items()}
    pool=x*d*prod(parent)*prod(set(need)-fixed.keys()); locked=any(f%2 for f in fixed.values())
    # Alternate arithmetic recognizes bans from a congruence, not Compose.permitted.
    @cache
    def allowed(p,f):return legal(p,f,banned)
    @cache
    def costs(q,h):
        even,flex= B+1,B+1
        for odd in (0,1):
            if odd and (locked or q%4!=1 or not allowed(q,1)):continue
            step=2+2*odd; f=h+((1-h)%4 if odd else h%2); remaining=head
            while remaining and q**f<(flex if odd else even):
                if allowed(q,f):
                    remaining-=1; z=sigma(q,f)//(1+odd)
                    common=gcd(z,children_product[q])
                    subs=[costs(p,val(z,p)) for p in kids[q] if common%p==0] if common>1 else []
                    n=q**f*trim(z,pool)*prod(a for a,_ in subs)
                    if not odd:
                        even=min(even,n);n=min([n]+[n//a*b for a,b in subs])
                    flex=min(flex,n)
                f+=step
            tail=q**f
            if not odd:even=min(even,tail)
            flex=min(flex,tail)
        return even,flex
    heights=[(q,val(d,q)) for q in roots];children=[costs(q,max(1,v)) for q,v in heights]
    n=x*(d//prod(q**v for q,v in heights))*prod(a for a,_ in children)
    return min([n]+[n//a*b for a,b in children])


def abundance(rows,need,banned,roots,prime,minima=None):
    locked=any(f%2 for q,f in rows)
    x=prod(q**f for q,f in rows); raw=prod(sigma(q,f) for q,f in rows)
    d=trim(raw//(1+locked),prod(q for q,_ in rows)); fixed=dict(rows)
    assert sorted(set(roots))==roots and all(prime(q) and q not in fixed and q not in banned and (q in need or d%q==0) for q in roots)
    minima={} if minima is None else minima
    assert set(minima)<=set(roots) and all(type(v)==int and v>0 for v in minima.values())
    def least(q,odd):
        h=max(1,val(d,q),minima.get(q,0));f=h+((1-h)%4 if odd else h%2)
        while not legal(q,f,banned):f+=2+2*odd
        return Fraction(sigma(q,f),q**f)
    es={q:least(q,0) for q in roots};b=Fraction(raw,x)*prod(es.values()); candidates=[b]
    if not locked:
        candidates += [b/es[q]*least(q,1) for q in roots if q%4==1 and legal(q,1,banned)]
    a=min(candidates);assert a>2,('abundance not strict',rows,need,banned)
    return a.numerator*10**6//a.denominator


def verify(packet):
    if not __debug__: raise RuntimeError('assertions required')
    raw=packet.read_bytes();d=json.loads(gzip.decompress(raw));assert set(d)=={'ecpp','masks','full_fibers'}
    assert O==tuple(C.ORDER)
    used=set()
    @cache
    def prime(q):
        assert type(q)==int and q>2
        n=q
        if q>=2**64:
            rows=d['ecpp'][str(q)];assert rows
            for z in rows:
                assert z[0]==n;n=C.pc.level(*z)
            used.add(str(q))
        assert C.pc.prime64(n)
        return True
    assert prime(Q) and all(prime(q) for q in O) and val(sigma(P,E),Q)==1 and Q%4==1 and (Q+1)%3==0
    all_m=set(range(1,256,2));projection=json.loads((R/'Session20261126/OpenSupport.json').read_bytes());assert projection['order']==list(O)
    front=set(projection['rows']['19:432']);assert len(front)==55 and front<=all_m
    assert set(map(int,d['masks']))==all_m
    seen_f={};minima={'forest':[],'abundance':[],'euler5':[]};all_possible=set();open_m=[]; summary={}; raw_pairs=raw_projected=0
    def check_forest(rows,need,banned,k,o,h):
        s=C.State(rows,need,banned);assert not s.conflict and s.base<=B
        C.validate_forest(s,k,o,h,prime)
        a,b=C.Forest(s,k,o,h).lower()[0],second(rows,need,banned,k,o,h)
        assert min(a,b)>B,('underpriced',rows,need,floor10(a),floor10(b))
        return floor10(min(a,b))
    for m in sorted(all_m):
        need=tuple(q for i,q in enumerate(O) if m>>i&1 and q!=P);banned=tuple(q for i,q in enumerate(O) if not m>>i&1)
        assert P not in banned
        live,tail=domain(banned);assert tail==69
        all_possible.update(live)
        raw_pairs+=len(live)
        if m in front:raw_projected+=len(live)
        cell=d['masks'][str(m)]
        assert set(cell)=={'root','cases'}
        if cell['root'] is not None:
            assert not cell['cases']; a=abundance([(P,E)],need,banned,cell['root'],prime)
            minima['abundance'].append(a)
            summary[m]=[]
            print('MASK',m,'ROOT ABUNDANCE',a,flush=True)
            continue
        for sf,leaf in cell['cases'].items():
            f=int(sf);assert str(f)==sf and f in live
            rows=live[f]; kind=leaf['kind'];k=leaf['roots']
            if kind=='abundance':
                assert set(leaf)=={'kind','roots'};lb=abundance(rows,need,banned,k,prime)
            elif kind=='euler5':
                assert (m,f)==(113,16) and set(leaf)=={'kind','roots','owners','head'}
                assert 5 in need and 7 in banned and all(not exponent%2 for _,exponent in rows)
                # The only admissible positive exponent of 5 below 6 is 1.
                assert not legal(5,2,banned) and not legal(5,4,banned) and not legal(5,5,banned)
                # All exponents at least 6, regardless of Euler placement, contradict abundancy.
                assert abundance(rows,need,banned,[3,5,13,409],prime,{5:6})>2_000_000
                lb=check_forest(rows+[(5,1)],need,banned,k,leaf['owners'],leaf['head'])
            else:
                assert kind=='forest' and set(leaf)=={'kind','roots','owners','head'}
                lb=check_forest(rows,need,banned,k,leaf['owners'],leaf['head'])
            minima[kind].append(lb);seen_f[f]=seen_f.get(f,0)+1
        residual=sorted(set(live)-set(map(int,cell['cases'])))
        summary[m]=residual
        if residual:open_m.append(m)
        print('MASK',m,'branches',len(live),'proved',len(cell['cases']),'remaining',residual,flush=True)
    assert set(used)==set(d['ecpp'])
    full=sorted(f for f in all_possible if all(f not in v for v in summary.values()))
    assert full==d['full_fibers']
    assert all_possible=={1,2,4,5,6,8,9,10,12,13,14,16,17,18,20,21,22,24,25,26,28,29,30,32,33,34}
    assert (raw_pairs,raw_projected)==(2440,1006)
    print('VERIFIED',(P,E),'full fibers',full,'closed masks',sorted(all_m-set(open_m)),'projected closed',sorted(front-set(open_m)),'individual leaves',seen_f,'forest count/min',(len(minima['forest'])+len(minima['euler5']),min(minima['forest']+minima['euler5'],default=None)),'forced Euler5',len(minima['euler5']),'abundance count/min ppm',(len(minima['abundance']),min(minima['abundance'],default=None)),'remaining',len(open_m),'masks',sum(map(len,summary.values())),'cells; projected',sum(len(summary[m]) for m in front),'SHA256',sha256(raw).hexdigest(),flush=True)


if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--packet',type=Path,default=H/'Nineteen432.json.gz');verify(p.parse_args().packet)
