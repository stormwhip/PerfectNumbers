#!/usr/bin/env python3
"""Exact fixed-prefix terminal for high ORDINARY 1109 exponents at t^28."""
import argparse
from fractions import Fraction
from math import gcd, isqrt, prod
from pathlib import Path
import runpy

v=runpy.run_path(str(Path(__file__).with_name('Verify276.py')))
P,T,S,B=(v[k] for k in ('P','T','S','B'))
state,sigma,vp,prime,require=(v[k] for k in ('state','sigma','vp','prime','require'))


def source_price(X):
    require(S-1==4*277 and prime(277) and 277*S>5031 and (2*S+1)**(S-1)>B,'only unshifted order277')
    C=50_000_000
    require(X*C**276>B, 'strict ordinary or Euler-square base cap')
    roots=[r for r in range(2,S) if pow(r,277,S)==1];m=S
    require(len(roots)==276,'complete root family')
    for z in range(1,5):
        r0=min(r if r%2 else r+m for r in roots)
        if z==4:
            require(r0>=C,'depth-four size exclusion for all lifted classes')
            return
        require(r0**276>=S**(100*z),'zero deficit price')
        m1=m*S
        roots=[r+m*(-((pow(r,277,m1)-1)//m)*pow(277*pow(r,276,S),-1,S)%S) for r in roots]
        require(len(set(roots))==276 and all(0<r<m1 and pow(r,277,m1)==1 for r in roots),'derivative lifting')
        m=m1


def price19():
    # The Euler-square atom q^2 may itself be composite. Retain EXACT all
    # geometric squared odd candidates in addition to possible prime bases.
    require(3**18>=P**2 and all(3**(o*(P**k-1))>=P**(2*k) for o in (3,9) for k in (1,2)) and 3*P**3>5031,'19 LTE price')
    tab={}
    for o in (3,9):
        rr=[r for r in range(2,P) if pow(r,o,P)==1 and (o==3 or pow(r,3,P)!=1)]
        m=P
        for z in range(1,277):
            num=m*m
            for b in rr:
                if b<3 or b%2==0 or b in (P,T,S) or b**(o-1)>=num:
                    continue
                q=isqrt(b)
                if q*q!=b and any(pow(a,b-1,b)!=1 for a in (2,3,5,7,11,13) if a<b):
                    continue
                loss=Fraction(num,b**(o-1))
                tab[b]=max(tab.get(b,1),loss)
            m1=m*P
            rr=[r+m*(-((pow(r,o,m1)-1)//m)*pow(o*pow(r,o-1,P),-1,P)%P) for r in rr]
            require(len(set(rr))==(2 if o==3 else 6) and all(0<r<m1 and pow(r,o,m1)==1 for r in rr),'order 19 roots')
            m=m1
    return prod(tab.values())


def potential_internal(A,m,b0):
    """Returns False only after excluding all Euler q>=b0 with q|A."""
    if A<b0:
        return False
    modulus=4*m
    least=2*m-1
    u=A*pow(least,-1,modulus)%modulus or modulus
    upper=A//b0
    if u>upper:
        return False
    # If too many checks would be required, leave the window unresolved.
    if (upper-u)//modulus>=20:
        return True
    return any(A%z==0 for z in range(u,upper+1,modulus))


def classify(f):
    require(f in (2,8,16,18,28), 'supported even pivot exponent')
    require(all(prime(p) for p in (P,T,S)) and 3**5030<=B<3**5031,'prime prefix / length')
    base=[(P,276),(T,f)]
    X,_,Y,_=state(base)
    D=Y//gcd(X,Y)
    require(vp(D,S)==1 and vp(Y,S)==1,'1109 compulsory unit')
    source_price(X)
    require(gcd(P*9,S*277)==1 and S>5031//277,'separate order supports')
    U19=price19()
    tail=next(h for h in range(1,5031) if X*(D//S)*S**h>B)
    live=[];closed=[];remaining=[];counters=[0,0,0]
    for h in range(2,tail,2):
        rows=base+[(S,h)]
        if v['raw_closed'](rows):
            continue
        live.append(h)
        Xh,_,Yh,Mh=state(rows)
        c=h-vp(Yh,S)
        require(c==h-1,'s incoming exact from fixed part')
        arcs=[]
        e19=276-vp(Yh,P)
        require(e19>=0,'19 overfilled')
        blocks=[sigma(q,f) for q,f in rows]
        powersP=[P**j for j in range(e19+1)]
        qoptimistic=(B//Xh+1)//2
        for i in range(c+1):
            si=S**i
            bare=Xh*S**(100*(c-i))
            if bare*max(5,2*si-1)>B:
                # Pure 1109 bound also works independent of how 19 is supplied.
                counters[0]+=e19+1
                continue
            for j,pj in enumerate(powersP):
                m=si*pj
                # q special => q + 1 has 2-adic valuation 1. q=2m-1 mod 4m.
                q0=max(5,2*m-1)
                # The q^2 ordinary atom is distinct from ordinary prime atoms.
                # 19 and 1109 effective order/surcharge supports are coprime.
                if m>qoptimistic or bare*q0*powersP[e19-j]**2*U19.denominator>B*U19.numerator:
                    counters[0]+=1
                    continue
                # Outside D, q is an extra forced prime and Mh*q divides N.
                if Mh*q0<=B:
                    arcs.append((i,j))
                    continue
                counters[1]+=1
                # Inside D, q divides at least one raw sigma block.
                for k,A in enumerate(blocks):
                    if j>0 and k==0:
                        # q≡−1 mod 19 contradicts q|sigma(19^276):
                        # odd order would imply (19/q)=1, whereas Euler
                        # q≡1 mod4 gives (19/q)=(q/19)=(-1/19)=-1.
                        continue
                    if potential_internal(A,m,q0):
                        arcs.append((i,j))
                        break
                else:
                    counters[2]+=1
        if arcs:
            remaining.append((h,arcs))
        else:
            closed.append(h)
    summary={2:(137,184,274,549),8:(128,172,256,514),16:(116,156,232,466),18:(113,152,226,454),28:(98,132,196,394)}
    k,a,b,d=summary[f]
    require(len(live)==k and closed==list(range(a,b+1,2)) and tail==d,'proved ordinary row summary')
    return live,closed,remaining,tail,counters


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pivot',type=int,default=28)
    f=ap.parse_args().pivot
    live,closed,remaining,tail,counters=classify(f)
    print('Pivot exponent:',f, 'live ordinary 1109 rows:',len(live),'raw tail:',tail)
    print('Closed h:',closed,'count:',len(closed),'Euler-window counters:',counters)
    print('Remaining ordinary h:',[h for h,arcs in remaining])


if __name__=='__main__':
    main()
