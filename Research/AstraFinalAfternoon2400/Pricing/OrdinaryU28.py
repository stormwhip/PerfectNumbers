#!/usr/bin/env python3
"""Anonymous Euler-window scan for remaining ordinary U exponents at t^28."""
import argparse
from fractions import Fraction
from itertools import combinations, product
from math import gcd, isqrt, prod
from functools import lru_cache
from pathlib import Path
import runpy

HERE=Path(__file__).resolve().parent
v=runpy.run_path(str(HERE/'VerifyT28U.py'))
P,T,U,S,B,BASE=(v[k] for k in ('P','T','U','S','B','BASE'))
state,sigma,vp,need,orders,layers=(v[k] for k in ('state','sigma','vp','require','orders','layer_cache'))
PS=(P,T,U)


def losses(X,D,caps,wn,wd):
    """Ordinary primes and conservative Euler squares, price powered to wd."""
    tab=[{} for _ in range(4)]
    Xcap=B//X
    relative=B//(X*D)
    small=(3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71)
    @lru_cache(maxsize=None)
    def plausible(b):
        q=isqrt(b)
        if q*q==b:
            if q<5 or q%4!=1 or q in (*PS,S):return False
            candidate=q
        else:
            candidate=b
        if any(candidate!=p and candidate%p==0 for p in small):return False
        # At weight exactly two many very large bases are positive. A
        # composite witness there is optional; defer it to keep replay cheap.
        if wn<2*wd or candidate.bit_length()<=128:
            if any(pow(a,candidate-1,candidate)!=1 for a in (2,3,5,7,11,13) if a<candidate):return False
        return True
    def keep(z,b,M,e):
        if b<3 or not b%2 or b in (*PS,S) or e*(b.bit_length()-1)>=wn*M.bit_length() or b*b>Xcap:
            return
        N=M**wn; dd=b**e
        if dd>=N:return
        power=b**(e//wd)
        if power//gcd(power,D)>relative:return
        if plausible(b):
            z[b]=max(z.get(b,1),Fraction(N,dd))
    def crop(p,o,c):
        for m,rr,_ in layers(p,o,c):
            if min((b if b%2 else b+m) for b in rr)**(o-1)>Xcap:break
            yield m,rr
    def merge(A,C):
        m,rr=A;n,ss=C;r=pow(m,-1,n)
        return m*n,[b+m*((c-b)*r%n) for b in rr for c in ss]
    G=[tuple(crop(p,3,c)) for p,c in zip(PS,caps)]
    for ar in G:
        for M,rr in ar:
            for b in rr:keep(tab[0],b,M,2*wd)
    pairs=[]
    for i,j in combinations(range(3),2):
        for a,b in product(G[i],G[j]):
            M,rr=merge(a,b)
            for p in rr:keep(tab[0],p,M,2*wd)
            if (i,j)==(0,1):pairs.append((M,rr))
    for m,rr in pairs:
        v=pow(m,-1,U); inv=v
        for n,tt in G[2]:
            mod=m*n
            for x,y in product(rr,tt):
                a=x+m*((y-x)*inv%n)
                keep(tab[0],a,mod,2*wd)
            inv+=n*((-((m*inv-1)//n))*v%U)
    for j,p in enumerate(PS,1):
        for o in orders(p):
            if o==3:continue
            for M,rr in crop(p,o,caps[j-1]):
                for b in rr:keep(tab[j],b,M,2*wd if j==1 else 4*wd)
    out={b:prod(t.get(b,1) for t in tab) for b in set().union(*tab)}
    # Keep denominator growth bounded without rounding down. For sparse
    # rational instances the exact loss product is inexpensive.
    if len(out)<100:
        return prod(out.values()),len(out)
    scale=10**10
    Ubound=scale
    for f in out.values():
        Ubound=-(-(Ubound*f.numerator)//f.denominator)
    return Fraction(Ubound,scale),len(out)


def divisibility_windows(a):
    rows=BASE+((U,a),)
    X,_,Y,M=state(rows)
    c=[e-vp(Y,p) for p,e in rows]
    need(min(c)>=0, 'incoming caps')
    wn,wd=(39,20) if a==14 else (19,10)
    need(wn<=2*wd and 3**(6*wd)>=P**wn,'valid weight and LTE')
    L,n=losses(X,M//X,c,wn,wd);N=prod(p**(wn*d) for p,d in zip(PS,c))
    print(a,'loss support done:',n,flush=True)
    goal=Fraction(X**wd*N,L)
    # In all such states 1109 is compulsory and is known ordinary; its
    # min extra exponent beyond D's incoming can be charged to raw M.
    need(vp(Y,S)>=1, 'missing compelled 1109')
    # Known 3 mod 4 primes are ordinary regardless of the free Euler slot.
    extras=[S]
    for q in (3,7,11,23,43,127,211,443,1531):
        need(q%4==3 and all(q%d for d in range(3,isqrt(q)+1,2)),'proved ordinary reserve labels')
        if vp(Y,q)%2:extras.append(q)
    extras=[q for q in extras if vp(Y,q)%2]
    M*=prod(extras)
    blocks=[sigma(p,e) for p,e in rows]
    raw=[A//gcd(A,X) for A in blocks]
    # Any unknown q dividing a raw output also divides that output after
    # removing factors present in X (their prime bases are fixed).
    blocks=raw
    left=[]; counts=[0,0,0]; powH=[[p**h for h in range(d+1)] for p,d in zip(PS,c)]
    maxblock=max(blocks)
    cap_ext=B//M;cap_any=B//X
    overlap=None
    # If external q has no existing incoming unit, some distinct ordinary
    # b^f must supply it. Then b^f>2q/3. Each block's support is pairwise
    # disjoint after fixed rows stripped; charge the extra forced 1109 to
    # its own block. The overlap with a prime power is at most the largest.
    db=list(blocks)
    if prod(db)==Y//gcd(X,Y) and all(gcd(a,b)==1 for a,b in combinations(db,2)):
        for r in extras:
            k,=tuple(k for k,d in enumerate(db) if d%r==0)
            db[k]*=r
        overlap=max(db)
        cap_ext=min(cap_ext,isqrt((3*B*overlap)//(2*M)))
    bound=B**wd*goal.denominator
    print(a,'powered price bounds ready',flush=True)
    # A window-free cap q<=Q: q>=2m-1>=m, hence after crediting
    # every linear Euler unit to all 3 targets, N^wd >= goal / Q^(wn-wd).
    # q can be external (q<=cap_ext) or divide a raw sigma block.
    Q=max(cap_ext,*blocks)
    if goal.numerator>bound*Q**(wn-wd):
        print(a,'cap',c,'loss',n,'EXCLUDED uniform Euler cap',flush=True)
        return []
    ext_pre=None
    if overlap is not None:
        ext_pre=(goal.numerator*M**(wn-wd)*2**wn, B**wn*goal.denominator*overlap**(wn-wd)*3**wn)
    low,high=0,cap_any+1
    while low+1<high:
        mid=(low+high)//2
        if goal.numerator>bound*mid**(wn-wd):low=mid
        else:high=mid
    # For m<=low, q>=m already discharges the price inequality. For
    # external q>low, same-source cancellation can likewise prune the
    # entire external range if even q=low+1 is large enough.
    no_external=(cap_ext<=low or ext_pre is not None and ext_pre[0]*(low+1)**wn>ext_pre[1])
    for j,k,l in product(*(range(d+1) for d in c)):
        m=powH[0][j]*powH[1][k]*powH[2][l]
        q=minq=max(5,2*m-1)
        if q>cap_any:
            counts[0]+=1;continue
        if m<=low:
            counts[1]+=1;continue
        if no_external and q>maxblock:
            counts[2]+=1;continue
        ext=not no_external and q<=cap_ext
        if ext and ext_pre is not None:
            # External q requires some other ordinary b^f with outgoing
            # q*W, W=product of target supplies it provides. Remove its
            # regular price and use b^f>2qW/3 instead. Combine that with
            # N > (M/overlap)*q*(2qW/3) to cancel W, with no overlap.
            if ext_pre[0]*q**(2*wn)>ext_pre[1]*m**wn:
                ext=False
        if ext:
            left.append((j,k,l,'external'));continue
        for z,A in enumerate(blocks):
            if A<minq or (z==0 and j):continue # reciprocity for the 19 block
            K=4*m; base=A*(2*m-1)%K or K  # involution mod 4m
            hi=A//minq
            if hi<base:continue
            if (hi-base)//K<20 and all(A%i for i in range(base,hi+1,K)):continue
            left.append((j,k,l,f'internal{z}'));break
        else:
            counts[2]+=1
    print(a,'cap',c,'loss',n,'closed quantities',counts,'survives',len(left),'sample',left[:12],flush=True)
    return left


def main():
    ap=argparse.ArgumentParser();ap.add_argument('valuations',nargs='*',type=int,default=[14,16,18,20,22,24]);A=ap.parse_args()
    v['verify_primes']();v['check_domain']()
    for a in A.valuations:
        need(2<=a<=24 and not a%2,'ordinary U exponent')
        left=divisibility_windows(a)
        if a in (14,16,18,20,22,24):
            need(not left,'expected high-U terminal did not cover all Euler classes')


if __name__=='__main__':main()
