"""Exact masked pivot coverage for (7,882); no trial or factor bank is used."""
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
P,E,Q=7,882,21193
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


def live(rows,banned):
    x=prod(q**f for q,f in rows);raw=prod(sigma(q,f) for q,f in rows);locked=sum(f%2 for q,f in rows)
    if locked>1 or any(f%2 and q%4!=1 or f%2 and f%4!=1 for q,f in rows):return None
    s=raw//(1+locked)
    if gcd(s*prod(q for q,_ in rows),prod(banned))>1 or raw>2*x or any(val(s,q)>f for q,f in rows):return None
    d=trim(s,prod(q for q,_ in rows))
    return (x*d,d,locked) if x*d<=B else None


def split(rows,q,banned,prime):
    base,d,locked=live(rows,banned)
    assert prime(q) and q not in dict(rows) and q not in banned and d%q==0
    v=val(d,q);scale=base//q**v;f=v;children={}
    while scale*q**f<=B:
        if f%2==0 or (not locked and q%4==f%4==1):
            t=rows+[(q,f)]
            if live(t,banned):children[str(f)]=t
        f+=1
    assert scale*q**(f-1)<=B<scale*q**f
    return children,f


def verify(packet):
    if not __debug__:raise RuntimeError('assertions required')
    raw=packet.read_bytes();d=json.loads(gzip.decompress(raw));assert set(d)=={'cases','shared','ecpp'}
    used=set()
    @cache
    def prime(q):
        assert type(q)==int and q>2
        n=q
        if q>=2**64:
            chain=d['ecpp'][str(q)];assert chain
            for row in chain:assert row[0]==n;n=C.pc.level(*row)
            used.add(str(q))
        assert C.pc.prime64(n)
        return True
    assert tuple(C.ORDER)==O and tuple(C.ORDER[:C.ORDER.index(P)])==(19,)
    assert all(prime(q) for q in O) and prime(Q) and Q%4==1 and val(sigma(P,E),Q)==1
    cosmos,base_tail=split([(P,E)],Q,(19,),prime)
    targets=set(map(int,cosmos))
    assert len(targets)==70 and base_tail==212
    counts={'forest':0,'abundance':0,'split':0,'shared':0}; floors=[]; remaining={}; all_live=0
    shared=d['shared']; reused=set()
    def check_forest(rows,need,banned,leaf):
        assert set(leaf)=={'type','roots','owners','head'} and leaf['type']=='forest'
        q,o,h=map(leaf.get,('roots','owners','head')); s=C.State(rows,need,banned[1:]); assert s.bad==banned and not s.conflict
        C.validate_forest(s,q,o,h,prime)
        a=C.Forest(s,q,o,h).lower()[0]; b=second(rows,need,banned,q,o,h)
        lb=min(a,b);assert lb>B,('not strict',rows,need,floor10(lb))
        counts['forest']+=1;floors.append(floor10(lb))
    @cache
    def shared_done(key):
        row=shared[key];assert set(row)=={'rows','leaf'}
        rows=[tuple(r) for r in row['rows']];assert live(rows,(19,))
        assert all(prime(q) for q,_ in rows)
        check_forest(rows,(),(19,),row['leaf'])
        return rows
    def walk(rows,need,banned,t):
        assert live(rows,banned)
        mode=t['type']
        if mode=='open':assert set(t)=={'type'};return (tuple(rows),)
        if mode=='forest':check_forest(rows,need,banned,t);return ()
        if mode=='shared':
            assert set(t)=={'type','key'} and shared_done(t['key'])==rows
            reused.add(t['key']);counts['shared']+=1;return ()
        if mode=='abundance':
            assert set(t)=={'type','roots'};abundance(rows,need,banned,t['roots'],prime);counts[mode]+=1;return ()
        assert mode=='split' and set(t)=={'type','q','cases'}
        children,_=split(rows,t['q'],banned,prime);assert set(children)==set(t['cases'])
        counts['split']+=1
        return sum((walk(child,need,banned,t['cases'][f]) for f,child in children.items()),())
    for m in range(2,256,4):
        needed=tuple(q for i,q in enumerate(O) if i>=2 and m>>i&1)
        banned=tuple(q for i,q in enumerate(O) if not m>>i&1)
        children,tail=split([(P,E)],Q,banned,prime);assert tail==base_tail
        all_live+=len(children)
        open_set={}
        cell=d['cases'][str(m)];assert set(cell)=={'root','cases'}
        advertised=cell['cases']
        if cell['root'] is not None:
            assert not advertised and cell['root']['type']=='abundance'
            assert not walk([(P,E)],needed,banned,cell['root'])
            remaining[m]={};continue
        assert set(advertised)==set(children)
        for f,t in advertised.items():
            holes=walk(children[f],needed,banned,t)
            if holes:open_set[int(f)]=holes
        remaining[m]=open_set
    assert set(map(int,d['cases']))==set(remaining) and all_live==3488
    assert used==set(d['ecpp']) and reused==set(shared)
    fs=sorted(f for f in targets if all(f not in row for row in remaining.values()))
    closed=[m for m,t in remaining.items() if not t]
    from collections import Counter
    unresolved=Counter(f for row in remaining.values() for f in row)
    print('VERIFIED',(P,E),'new full fibers',fs,'masks closed across full domain',closed,'remaining mask counts',dict(sorted(unresolved.items())),'stats',counts,'forest min',min(floors,default=None),'SHA256',sha256(raw).hexdigest(),flush=True)
    return remaining


if __name__=='__main__':
    a=argparse.ArgumentParser(description=__doc__);a.add_argument('--packet',type=Path,default=H/'Seven882.json.gz');verify(a.parse_args().packet)
