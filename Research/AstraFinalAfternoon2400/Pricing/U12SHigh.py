#!/usr/bin/env python3
"""Exact high ordinary 1109 child exclusions beneath t^28,U^12."""
from fractions import Fraction
from math import gcd,isqrt,prod
from itertools import product
from pathlib import Path
import runpy

H=Path(__file__).resolve().parent
V=runpy.run_path(str(H/'OrdinaryU28.py'))
P,T,U,S,B,BASE=(V[k] for k in ('P','T','U','S','B','BASE'))
state,sigma,vp,need=(V[k] for k in ('state','sigma','vp','need'))
rows=BASE+((U,12),)


def grouped(blocks):
    groups=[]
    for x in blocks:
        new=[]
        for y in groups:
            if gcd(x,y)>1:x*=y
            else:new.append(y)
        groups=new+[x]
    return groups


def inside(block,s,e,i):
    """Necessary CRT cofactor condition for q in this single block."""
    m=s**i; q0=max(5,2*m-1)
    if q0>block:return False
    k=4*m; r=block*(2*m-1)%k or k
    upper=block//q0
    if upper<r:return False
    if (upper-r)//k<10 and all(block%x for x in range(r,upper+1,k)):
        return False
    return True


def no_shared_277(X):
    # This full CRT excludes bases simultaneously of order 277 at T and S.
    # Order 831 at T is then also impossible for an S supplier: even the
    # least 3 has exponent >=830, but explicitly exhaust that family too.
    r=V['v']['roots']; sr=r(S,277)
    m=S*T; inv=pow(T,-1,S)
    for o in (277,831):
        hits=[]
        # Minimum cap for all actual odd bases and no least-root assumption.
        need(X*m**(o-1)>B,'CRT modulus covers physical base range')
        for a,b in product(sr,r(T,o)):
            z=b+T*((a-b)*inv%S)
            if z%2==0:z+=m
            if X*z**(o-1)<=B:
                # A prime multiple of 19 is exactly fixed 19. A square
                # of a prime multiple of 19 could only be 19^2, which
                # cannot represent Euler at the already fixed 19.
                need(z%P==0,'overlap base not eliminated')
                hits.append(z)
        need(sorted(hits)==([19,361,6859,130321] if o==277 else []),'shared odd order root set')
    for L in range(3,5032,2):
        opts=[(0,1,3,9),(0,3,23,69,277,831),(0,3,29,87),(0,277)]
        for a,b,c,d in product(*[[o for o in seq if o<=1 or L%o==0] for seq in opts]):
            if d and b in (277,831):continue
            used=2*int(3 in (a,b,c))+2*int(a==9)+4*int(b>3)+4*int(c>3)+276*int(bool(d))+(6*vp(L,P) if a else 0)
            need(used<=L-1,('four-price length coverage',L,a,b,c,d))


def main():
    V['v']['verify_primes']();V['v']['check_domain']()
    X,_,Y,M=state(rows)
    need(vp(Y,S)==1,'compulsory ordinary 1109')
    no_shared_277(X*S**2)
    H0=runpy.run_path(str(H/'VerifyT28Ordinary.py'))
    H0['source_price'](X)
    a,d=19,10
    caps=[e-vp(Y,q) for q,e in rows]
    loss,n=V['losses'](X,M//X,caps,a,d)
    need(n==4,'expected complete three-target loss support')
    D=M//X
    tail=next(h for h in range(1,5031) if X*(D//S)*S**h>B)
    live=[];close=[]; leftover={}
    for h in range(2,tail,2):
        prefix=rows+((S,h),)
        if V['v']['m']['v']['raw_closed'](prefix):continue
        live.append(h)
        Xh,_,Yh,Mh=state(prefix)
        C=[e-vp(Yh,q) for q,e in prefix]
        need(all(0<=u<=v for u,v in zip(C,caps)) and C[-1]==h-1,'adjusted exact supplies')
        blocks=[sigma(q,e)//gcd(sigma(q,e),Xh) for q,e in prefix]
        comb=grouped(blocks)
        # If exact cancellation of fixed support differs (not every raw
        # block was individually stripped by all possible fixed powers),
        # keep the weaker unconditional raw outside cap for this branch.
        stronger=prod(comb)==Mh//Xh and all(gcd(b,c)==1 for i,b in enumerate(comb) for c in comb[i+1:])
        capext=B//Mh
        if stronger:capext=min(capext,isqrt((3*B*max(comb))//(2*Mh)))
        nominal=Fraction(Xh**d*prod(p**(a*c) for (p,_),c in zip(rows,C)),loss)
        # Re-price 1109 at the common 19/10 weight (its 100-weight
        # uniform price is stronger). This enables full same-source
        # cancellation for the other terminal, even if the distinguished
        # emitter also supplies 1109. Do not combine the two prices.
        uniform=nominal*S**(a*(h-1))
        lim=B**d*uniform.denominator
        uniform_inside=uniform.numerator>lim*max(blocks)**(a-d)
        uniform_outside=False
        if stronger and uniform_inside:
            # Intersect two monotone exact bounds through an integer
            # decimal breakpoint; a failed breakpoint only weakens this test.
            cuts=[capext]+[10**k for k in range(200,451,25)]
            for Q0 in cuts:
                if uniform.numerator<=lim*Q0**(a-d):continue
                if Q0>=capext or uniform.numerator*Mh**(a-d)*2**a*(Q0+1)**a>B**a*uniform.denominator*max(comb)**(a-d)*3**a:
                    uniform_outside=True
                    break
        if uniform_inside and uniform_outside:
            close.append(h)
            continue
        left=[]
        outer_scale=B**d*nominal.denominator
        for i in range(h):
            m=S**i; q0=max(5,2*m-1)
            cut=[]
            if q0<=capext:cut.append(capext)
            cut.extend(b for b in blocks if inside(b,S,h,i))
            if not cut:continue
            # q >= m * p^j t^k U^l. Price only loses to the linear
            # cubic targets by q^(a-d), and disjoint 1109 adds exact nominal
            # weight100 less its i linear units. q can be capped per i.
            Q=max(cut)
            # Simple bit-length bounds avoid most giant exponentiations.
            exp=a*i+100*d*(h-1-i)
            rhs=outer_scale*Q**(a-d)
            shift=(S.bit_length()-1)*exp
            if nominal.numerator.bit_length()+shift-1>=rhs.bit_length():continue
            if nominal.numerator*S**exp>rhs:continue
            left.append(i)
        if not left:close.append(h)
        else:leftover[h]=left
    need(tail==217 and live==list(range(2,110,2)) and close==list(range(24,110,2)) and list(leftover)==list(range(2,24,2)),'complete exact local receipt')
    print('U12 ordinary 1109 raw tail',tail,'live',len(live),'closed',close,'remaining',list(leftover),flush=True)
    return close,leftover


if __name__=='__main__':main()
