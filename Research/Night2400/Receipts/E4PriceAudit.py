"""Independently reprice E4's two exact joint incoming leaves."""
from fractions import Fraction
from functools import cache
from itertools import product
from math import gcd, isqrt, prod
import sys

B=10**2400
Q=1169407471026387018305554817094515359
R=120298224779693


def valuation(a,p):
    n=0
    while a%p==0:
        a//=p
        n+=1
    return n


@cache
def divs(x):
    a=set()
    for k in range(1,isqrt(x)+1):
        if x%k==0:
            a.update((k,x//k))
    return sorted(a)


@cache
def root_classes(p,k,depth):
    ps=[x for x in divs(k) if x>1 and len(divs(x))==2]
    base=2
    while True:
        u=pow(base,(p-1)//k,p)
        if u>0 and all(pow(u,k//x,p)>1 for x in ps): break
        base+=1
    # Lift only the generator, with Newton doubling, then take primitive powers.
    mod=p
    level=1
    while level<depth:
        level=min(2*level,depth)
        mod=p**level
        u=(u-(pow(u,k,mod)-1)*pow(k*pow(u,k-1,mod),-1,mod))%mod
    assert pow(u,k,mod)==1
    return [pow(u,i,mod) for i in range(1,k) if gcd(k,i)==1]


def checked(p,f):
    return (p**(f+1)-1)//(p-1)


def audit(P,select):
    X=prod(p**f for p,f in P)
    assert all(not f%2 for _,f in P)
    seq=[checked(p,f) for p,f in P]
    assert all(z%2 and z%19 for z in seq)
    S=prod(seq)
    peaks=[P[i][0] for i in select]
    caps=[dict(P)[p]-valuation(S,p) for p in peaks]
    assert min(caps)>=0
    M=prod(p**c for p,c in zip(peaks,caps))
    Cut=B//X
    moduli=[p**(c+1) for p,c in zip(peaks,caps)]
    n=len(peaks)
    w={}

    @cache
    def find(r,f):
        if r<3 or r%2==0 or r in dict(P) or r==19:
            return
        if f%2 and (f%4!=1 or r%4!=1):
            return
        if r%19==1:
            if (f+1)%19==0: return
        elif pow(r,f+1,19)==1:
            return
        if any(r!=p and r%p==0 for p in (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)):
            return
        if (r.bit_length()-1)*f>=Cut.bit_length():
            return
        cost=r**f
        if cost>Cut:
            return
        a=1
        for p,c,m in zip(peaks,caps,moduli):
            if r%p==1:
                j=valuation(f+1,p)
            else:
                x=(pow(r,f+1,m)-1)%m
                j=c+1 if x==0 else valuation(x,p)
            if j>c: return
            a*=p**j
        if a*a>cost and pow(2,r-1,r)==1:
            w[r]=max(w.get(r,Fraction(1)),Fraction(a*a,cost))

    def options(p,c,f):
        shift=valuation(f+1,p)
        if 0<shift<=c:
            yield (p,1,p**shift)
        if shift>=c:
            return
        for k in divs(gcd(p-1,f+1))[1:]:
            depth=c-shift
            for a in root_classes(p,k,depth):
                for j in range(1,depth+1):
                    m=p**j
                    yield (m,a%m,m*p**shift)

    @cache
    def inv(a,m): return pow(a,-1,m)

    def scan(m,a,c,f):
        # Only positive odd residues need enumeration (all moduli are odd).
        r=a if a%2 else a+m
        if r<3: r+=2*m
        if m==1 and r==1: r=3
        lim=min(c,Cut+1)
        while (r.bit_length()-1)*f<lim.bit_length() and r**f<lim:
            find(r,f)
            r+=2*m

    for f in range(2,2*n):
        if f%2 and f%4!=1: continue
        for coords in product(*[[(1,0,1),*options(p,c,f)] for p,c in zip(peaks,caps)]):
            modulus=prod(k for k,a,b in coords)
            supply=prod(b for k,a,b in coords)
            if supply==1: continue
            # Direct CRT of all constrained coordinates.
            residue=sum(a*(modulus//k)*inv((modulus//k)%k,k) for k,a,b in coords if k>1)%modulus
            scan(modulus,residue,supply**2,f)
    for p,c in zip(peaks,caps):
        f=2*n
        while 3**f<=Cut and 3**f<p**(2*n*c):
            if f%2==0 or f%4==1:
                for m,a,z in options(p,c,f):
                    if 3**f<z**(2*n): scan(m,a,z**(2*n),f)
            f+=1
    U=prod(w.values(),start=Fraction(1))
    V=X*M*M/U
    assert V>B
    D=S//gcd(X,S)
    parts=[z//gcd(X,z) for z in seq]
    assert D==prod(parts) and gcd(D,X)==1
    counts=[0,0,0]
    for ss in product(*(range(c+1) for c in caps)):
        m=prod(p**s for p,s in zip(peaks,ss))
        least=2*m-1
        if V.numerator*least>B*m*m*V.denominator:
            counts[0]+=1
            continue
        assert X*D*least>B
        if least>max(parts):
            counts[1]+=1
            continue
        for (p,f),z in zip(P,parts):
            if z<least:
                continue
            if p%4==3 and m%p==0:
                # p has odd order modulo any Euler divisor of sigma(p^even),
                # contrary to reciprocity for q=1 mod 4 and q=-1 mod p.
                continue
            gap=4*m
            # (2m-1)^2=1 mod 4m.
            a=(z*least)%gap
            assert a%2==1
            assert (z//least-a)//gap<=128 and all(z%k for k in range(a,z//least+1,gap))
        counts[2]+=1
    print('PRICE',P,'targets',peaks,'caps',caps,'exceptions',len(w),'Euler',counts,flush=True)
    return len(w),counts


if __name__=='__main__':
    assert __debug__
    if sys.argv[1:]==['22']:
        exceptions,counts=audit(((7,420),(Q,22)),[1])
        assert counts==[8,0,14]
    else:
        assert sys.argv[1:]==['6','30']
        assert audit(((7,420),(Q,6),(R,30)),[0,1,2])==(18,[36827,38953,0])
