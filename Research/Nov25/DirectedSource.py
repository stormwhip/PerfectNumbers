"""Pilot for directed Euler-one source accounting in ordinary non-Fermat roots.

The exact known-source check is independent of the unknown-source lattice proof.
Discovery and advanced branches may return unknown; no claim is entered by this file.
"""
from fractions import Fraction
from functools import cache
from math import gcd, prod
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
R=H.parent
sys.path.insert(0,str(R/'NightUniformReview'))
import Replay as U


@cache
def certified_anchor_floor(p, q, c):
    ban=U.O.tb.forbidden(p)
    f=c+c%2
    while any(U.sig(q,f)%a==0 for a in ban):
        f+=2
    return f


def interval_factor(z,Y,p,l,h,ban,exact_cap,possible=lambda q: True):
    """Conservative existence of an Euler divisor of z in a closed interval.

    q=1 mod 4, q=-1 mod Y, q+1 avoids all absent roots, and s is exact.
    For wide boxes retain uncertainty unless a necessary congruence test fails.
    """
    if l>h:
        return False
    modulus=4*Y
    a=l+(2*Y-1-l)%modulus
    if a>h:
        return False
    if (h-a)//modulus<exact_cap:
        return any(z % q == 0 and (q+1)%(Y*p) and all((q+1)%b for b in ban) and possible(q)
                   for q in range(a,h+1,modulus))
    # q == 2Y-1 modulo 4Y even for Y=1. Cofactor is then in one
    # CRT class modulo 4Y, not just modulo Y.
    low=(z+h-1)//h
    top=z//l
    residue=z*pow(2*Y-1,-1,modulus)%modulus
    first=low+(residue-low)%modulus
    if first>top:
        return False
    if (top-first)//modulus<exact_cap:
        for v in range(first,top+1,modulus):
            if z%v==0:
                q=z//v
                if (q+1)%(Y*p) and all((q+1)%b for b in ban) and possible(q):
                    return True
        return False
    return True


def exterior_possible(p,e,s,b,M,V,k,pe,A,ban,*,max_trials=32):
    """Enumerate every legal even f; wide base progressions yield UNKNOWN.

    The hypothetical ordinary emitter r is outside sigma(p^e), and the Euler
    prime has exponent exactly one. Charge disjoint components A, p^e, r^f, q.
    """
    B=U.B;Y=p**s;Q=max(5,2*Y-1);budget=B*Y**k
    cap=B//(M*Q);need=2*Q*p**b//3
    if cap<=need:return False
    for f in range(2,U.logi(cap,3)+1,2):
        lo=max(3,U.root(need,f)+1);hi=U.root(cap,f)
        if hi<lo:continue
        j=U.val(f+1,p);t=b-j
        if hi-lo<max_trials:
            candidates=range(lo|1,hi+1,2)
        elif t<=0:
            return True
        else:
            modulus=p**t;rs=[]
            for a in range(2,p):
                if pow(a,f+1,p)!=1:continue
                z=pow(a,p**(t-1),modulus)
                r=lo+(z-lo)%modulus
                if r%2==0:r+=modulus
                n=(hi-r)//(2*modulus)+1
                if n>max_trials:return True
                rs.extend(range(r,hi+1,2*modulus))
            candidates=rs
        for r in candidates:
            if r==p or r in ban or A%r==0:continue
            if r<2**64 and not U.O.G.is_prime_det64(r):continue
            a=U.sig(r,f)
            if any(a%q==0 for q in ban):continue
            b1=U.val(a,p)
            if b1<b or b1>e-s:continue
            z=V*r**f
            hiq=min(a//p**b1,B//(M*r**f),budget*p**(k*b1)*z.denominator//z.numerator)
            def possible(q):
                if q==r or q==p or q in ban or A%q==0 or (q<2**64 and not U.O.G.is_prime_det64(q)):
                    return False
                X=pe*r**f*q;S=A*a*(q+1);D=S//gcd(2*X,S)
                return gcd(D,X)==1 and X*D<=B and S<=2*X
            if interval_factor(a//p**b1,Y,p,Q,hiq,ban,64,possible):return True
    return False


def run(p,e,anchors,*,new=True,max_s=0,min_s=0):
    """Return conditional diagnostics; all internal Euler/high-Euler obligations explicit."""
    if p not in (7,11,19,31) or e%2 or e<2:
        raise ValueError('ordinary non-Fermat p=3 mod 4 only')
    P=p**(e+1);pe=p**e;A=U.sig(p,e);B=U.B;ban=U.O.tb.forbidden(p)
    prof=U.O.profile(p);k=prof.kap;L=prof.U(e)
    if pe**(k+1)<=B*L:
        return dict(guard='internal Euler not excluded')
    if p==11:
        hi=max([Fraction(1),*(v for t,v in U.hl(p,prof.top,k) if t<=e)])
        if pe**(k+1)<=B*L*hi:return dict(guard='high Euler not excluded')
    elif pe**3<=B*L*prof.D(e):
        return dict(guard='high Euler not excluded')
    U.primes(anchors,A)
    ss=set(anchors)|{r for r in U.small if A%r==0};C=U.chunks(p,e,ss);bs=U.blocks(p,C)
    cs={r:U.val(A,r) for r in ss}
    jp={r:r**(certified_anchor_floor(p,r,c)-c) for r,c in cs.items()}
    vp={r:U.price(p,k,r,c) for r,c in cs.items()}
    costs={h:(l,v*v) for h,l,v in bs}
    M=pe*A*prod(jp.values())*prod(l for l,v in costs.values())
    V=Fraction(pe**(k+1)*prod(vp.values())*prod(v for l,v in costs.values()),L)
    Z=max([1,*vp.values(),*(v for l,v in costs.values())])
    spare=max([1,*jp.values(),*(l for l,v in costs.values())])
    crows=[]
    for s in range(min_s,min(e,max_s or e)+1):
        Y=p**s;Q=max(5,2*Y-1);budget=B*Y**k;d0=max(P,Q)*(P//Y+4)
        if V*Q>budget or M*Q>B or (M*Q*Q*Y>=B*spare*d0 and 2*M*Q*Q>=3*B):
            continue
        def min_b(refund):
            z=V/refund;n=2*z.numerator*Q*Q;d=3*budget*z.denominator
            return 0 if n<=d else 1+U.logi((n-1)//d,p)//(k-1)
        b=min_b(1 if new else Z)
        ext=b<=e-s and 2*M*Q*Q*p**b<=3*B
        if new and ext:
            ext=exterior_possible(p,e,s,b,M,V,k,pe,A,ban)
        hit=None
        for r,c in sorted(cs.items(),reverse=True):
            b=min_b(vp[r] if new else Z)
            if b>e-s:continue
            z=Y*p**b
            need=2*Q*p**b//3;th=z*Q//(max(P,Q)*(P//z+4))
            room=B*(jp[r] if new else spare)//(M*Q)
            for f in range(c+c%2,c+U.logi(room,r)+1,2):
                rpow=r**f
                if rpow<=need or r**(f-c)<=th:continue
                a=U.sig(r,f);b1=U.val(a,p)
                if b1<b or (new and (b1>e-s or any(a%q==0 for q in ban))):continue
                cap=B//(pe*A)
                if new:
                    # Retain directed bounds for the exact source. Omitting its
                    # static charge then inserting r^f/p^(k*b1) prices it once.
                    rest=V/vp[r]*rpow
                    cap=min(cap, B*p**(k*(s+b1))*rest.denominator//rest.numerator,
                            B*jp[r]//(M*r**(f-c)))
                    # Recompute the balanced necessary lower bound with actual b1.
                    zb=Y*p**b1
                    if r**(f-c)<=zb*Q//(max(P,Q)*(P//zb+4)):continue
                    def possible(q):
                        if q in (p,r,*ban) or A%q==0 or (q<2**64 and not U.O.G.is_prime_det64(q)):
                            return False
                        X=pe*rpow*q;S=A*a*(q+1);D=S//gcd(2*X,S)
                        if gcd(D,X)>1 or X*D>B or S>2*X:
                            return False
                        # Only exact q^1 spends the unique Euler slot. Every
                        # other known residual factor has an even exponent.
                        for w in cs:
                            if w==r or w==q:continue
                            c0=U.val(D,w)
                            if c0:
                                D*=w**(certified_anchor_floor(p,w,c0)-c0)
                        return X*D<=B
                    if not interval_factor(a,Y,p,Q,min(a,cap),ban,64,possible):continue
                elif not U.qfactor(a,Y,Q,min(a,cap)):
                    continue
                hit=['known',r,c,f,b1];break
            if hit:break
        if hit is None:
            for h,n in C.items():
                l,v=costs.get(h,(1,1));b=min_b(v if new else Z)
                if new and b>0:
                    # The only potential valuation refund is a zero-source
                    # witnessed prime. Positive supply cannot use that coupon.
                    b=min_b(1)
                if b>e-s:continue
                z=Y*p**b
                th=z*Q//(max(P,Q)*(P//z+4));need=2*Q*p**b//3
                for g in range(U.logi(B*(l if new else spare)//(M*Q),10001)+1):
                    if not g and th>=1:continue
                    room=B*((l if g%2 else 1) if new else spare)//(M*Q)
                    lo=max(10001,U.root(th,g)+1) if g else 10001
                    hi=U.root(room,g) if g else n
                    if lo>hi:continue
                    for c in range(2-g%2,U.logi(n,lo)+1,2):
                        f=c+g
                        L0=max(lo,U.root(need,f)+1);H0=min(hi,U.root(n,c))
                        if U.cand(n,c,p,f,L0,H0,b,h,0):
                            hit=['rough',h,c,f,b,len(str(L0)),len(str(H0))];break
                    if hit:break
                if hit:break
        if hit or ext:
            crows.append([s,ext,hit])
    return dict(guard=None,open=crows,anchors=len(anchors),blocks=len(C))
