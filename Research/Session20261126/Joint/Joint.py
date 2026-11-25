"""Reproducible integer-rounded joint certificates. Read-only snapshot, stdout only.
python -I -S -B joint-lab/Joint.py [snapshot] [leaf indices...]"""
import sys, json, hashlib
from math import gcd, isqrt
from decimal import Decimal as D,localcontext
from functools import cache
from pathlib import Path
ROOT=Path(sys.argv[1]) if len(sys.argv)>1 else next(p for p in Path(__file__).resolve().parents if (p/'Research/P3I00193Review/Candidate/P3E1162Complete.json').is_file())
raw=(ROOT/'Research/P3I00193Review/Candidate/P3E1162Complete.json').read_bytes();assert hashlib.sha256(raw).hexdigest()=='54652cb67d6f807170248c00eb0c9004a200cd7b9027a73e923b7ea1a46cb30b'
cert=json.loads(raw); B=10**2400; e=1162; T=10**9; pe=3**e; A=(3*pe-1)//2; BAN={7,11,13,19,31}; Y=3**1020;Q=2*Y-1
@cache
def lo(n):
    # Decimal ln is correctly rounded; adjacent value bounds the transcendental.
    with localcontext() as ctx:
        ctx.prec=60;return int((D(n).ln().next_minus()*T).to_integral_value(rounding='ROUND_FLOOR'))
def hi(n):return lo(n)+2
@cache
def sig(p,f):return (p**(f+1)-1)//(p-1)
def val(n,p):
    v=0
    while n%p==0:v+=1;n//=p
    return v
def prime64(n):
    if not 2<=n<2**64:return False
    for a in (2,3,5,7,11,13,17,19,23,29,31,37):
        if n%a==0:return n==a
    h=val(n-1,2);d=(n-1)>>h
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        z=pow(a,d,n)
        if z in (0,1,n-1):continue
        for _ in range(h-1):
            z=z*z%n
            if z==n-1:break
        else:return False
    return True
@cache
def prime(n):
    if n<2**64:return prime64(n)
    h=1;seen=set()
    for t,k,a in cert['primes'].get(str(n),[]):
        assert 2<=t<n and t not in seen and prime(t) and k>0
        h*=t**k;seen.add(t);assert (n-1)%h==0 and pow(a,n-1,n)==1 and gcd(n,pow(a,(n-1)//t,n)-1)==1
    return h*h>n
small=[p for p in range(5,50000,2) if prime(p)]
@cache
def nosource(p):
    if A%p==0 or p>=Q:return False
    # Only needed under external-source hypothesis; S(p^f)*A divides N by multiplicativity.
    f=2
    while pe*A*p**f*sig(p,f)<=B:
        z=sig(p,f)
        if z>=Q and z%3 and not any(z%a==0 for a in BAN) and ((-z)%Y or Y)*Q<=z:return False
        f+=2
    return True

def bases():
    RA=5000000000
    assert prime(e+1)
    for x in range(6*(e+1)+1,RA+1,6*(e+1)):
        assert pow(3,e+1,x)!=1 or not prime64(x)
    best=[10**20]*2;worst=[None]*2
    for s in range(1020,e+1):
        y=3**s;q=2*y-1;P=3*pe;delta=P//y
        # Every internal source has r>=3 and r< or > delta+2. Use D1,D2 separately (documentation 3.3).
        # Baseline universal balanced lemma; exact q=2Y-1 is allowed as a relaxation.
        srcE=lo(2*q)-hi(3);srcI=max(0,lo(y*q)-hi(P*(delta+4)))
        for i in range(e-s+1):
            cost=lo(pe*A*q)+(e-s-i)*4*lo(3)
            # source internal has separate A-share c; optimize jointly rather than granting entire A twice.
            d=2*i*lo(RA)-hi(A)
            for k,z in enumerate([srcE+max(0,d),max(srcI,max(srcI,srcE)+d)]):
                if cost+z<best[k]:best[k]=cost+z;worst[k]=(s,i)
    return best,worst

def basis(ns):
    # Partition into coprime supports; multiplicities in the originals are recovered by gcd stripping.
    acc=[]
    for x in set(ns):
        j=0
        while x>1 and j<len(acc):
            z=acc[j];g=gcd(x,z)
            if g==1:j+=1;continue
            a=z;b=1
            while (h:=gcd(a,x))>1:a//=h;b*=h
            if a!=1:acc[j]=a;acc.append(b);z=b
            while (h:=gcd(x,z))>1:x//=h
            j+=1
        if x>1:acc.append(x)
    assert all(gcd(x,y)==1 for i,x in enumerate(acc) for y in acc[:i]);return acc

@cache
def small_parts(n):
    b=[]
    for p in small:
        if p*p>n:break
        if n%p==0:
            k=val(n,p);n//=p**k;b.append((p,k))
    if n>1 and n<50000:b.append((n,1));n=1
    return b,n

@cache
def extra_info():
    fp=Path(__file__).with_name('Hints.json')
    if not fp.is_file():return [],set()
    sys.path.insert(0,str(fp.parent));from EC import ecprime
    h=json.loads(fp.read_bytes());ec={int(t) for t,chain in h['certs'].items() if ecprime(int(t),chain,prime64)}
    assert len(ec)==len(h['certs']) and all(t>=2 for t in h['factors']);return h['factors'],ec

def leaf(i, detail=False):
    l=(cert['cell10']+cert['cell11'])[i];F=l['forest'];L=l['lp'];absent=BAN|set(l['absent_extra']);u=set(map(int,F['cut_even'])) if F else set();p=set(L['P']) if L else set();pool=u|p;assert all(prime(t) and A%t and t<Q and nosource(t) for t in pool)
    assert set(l['present'])==set(F['roots'] if F else []) and not(u&p) and not(absent&pool)
    child={int(k):v for k,v in F['edges'].items()} if F else {};seen=set();roots=l['present'];stack=roots[:]
    while stack:
        r=stack.pop();assert r not in seen;seen.add(r);stack.extend(child.get(r,[]))
    assert seen==u
    data={};rema=[];w={};PEN=2*hi(3)
    for r in pool:
        stop= F['cut_even'][str(r)] if r in u else (42 if r<100 else 22 if r<400 else 12)
        opts=[]
        for f in range(2,stop,2):
            z=sig(r,f)
            if any(z%t==0 for t in absent):continue
            b=val(z,3);n=z//3**b
            for t in pool:
                while n%t==0:n//=t
            assert gcd(n,A)==1 and n<Q
            parts,left=small_parts(n);v=sum(k*(lo(t)-(PEN if t%3==1 else 0)) for t,k in parts)
            assert all(nosource(t) for t,k in parts)
            if left>1:rema.append(left)
            opts.append((f,z,f*lo(r)-4*hi(3)*b,v,left));
        data[r]=(stop,opts)
    bs=basis(rema);unsafe=[]
    extra=extra_info();divs,ec=extra
    if divs:bs=basis(list(bs)+divs)
    for t in sorted(bs):
        if not((prime(t) or t in ec) and nosource(t)):unsafe.append(t)
    for n in set(rema)|{1}:
        x=n;units={}
        for t in bs:
            z=1
            while (h:=gcd(x,t))>1:x//=h;z*=h
            if z>1:units[t]=lo(z)*(lo(50000)-PEN)//lo(50000)
        assert x==1;w[n]=(sum(units.values()),units)
    def solve(bad):
        @cache
        def dp(r,m):
            stop,opts=data[r];fe=max(stop,m+m%2)
            # For f>=fe, v3(f+1)<=log_3(f+1); cost bound f ln r-4 ln(f+1) monotone.
            best=fe*lo(r)-(4*hi(fe+1) if r%3==1 else 0)
            for f,z,cost,v,n in opts:
                if f<m:continue
                ww,loss=w[n];a=cost+v+ww-loss.get(bad,0)
                for t in child.get(r,[]):
                    if z%t==0:a+=dp(t,val(z,t))
                best=min(best,a)
            return best
        return sum(dp(r,2) for r in roots)
    # E3a worst-case removal; E3b safe to charge every cleaned block.
    internal=solve(None);ext=internal;worst=None;by={}
    for t in unsafe:
        v=solve(t);by[t]=v
        if v<ext:ext=v;worst=t
    if detail:return internal,by
    return dict(i=i,forest_internal=internal,forest_external=ext,unsafe=len(unsafe),worst_basis=worst)

if __name__=='__main__':
    assert __debug__;base,arg=bases();print('base',base,arg,flush=True)
    for i in (list(map(int,sys.argv[2:])) or list(range(42))):
        row=leaf(i);print(json.dumps(row|dict(total_floors=[(row['forest_external']+base[0])//hi(10),(row['forest_internal']+base[1])//hi(10)])),flush=True)
