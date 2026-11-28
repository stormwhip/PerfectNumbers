#!/usr/bin/env python3
"""Exact Euler-at-1109 exclusion for even first pivots 2,8,16,18,28."""
import argparse
from fractions import Fraction
from math import gcd, prod
from pathlib import Path
import runpy

v=runpy.run_path(str(Path(__file__).with_name('Verify276.py')))
P,T,S,B=(v[k] for k in ('P','T','S','B'))
state,sigma,vp,prime,require=(v[k] for k in ('state','sigma','vp','prime','require'))


def classify(f):
    require(f in (2,8,16,18,28),'supported first-pivot exponent')
    require(all(prime(p) for p in (P,T,S,277)), 'fixed primality')
    require(S%4==1 and P-1==2*9 and S-1==4*277 and gcd(9*P,S*277)==1,'parity or odd effective length supports')
    require(3**5030<=B<3**5031 and 277*S>5031,'full ordinary length')
    require(3**18>=P**2 and all(3**(o*(P**k-1))>=P**(2*k) for o in (3,9) for k in (1,2)) and 3*P**3>5031,'19 LTE')
    require((2*S+1)**(S-1)>B,'Euler-locked order-one supply to 1109 impossible')
    prefix=[(P,276),(T,f)]
    X,_,Y,_=state(prefix)
    D=Y//gcd(X,Y)
    require(vp(D,S)==1 and vp(Y,S)==1,'1109 forced and single fixed valuation')
    U,_=v['loss19'](276,{P,T,S})
    require(U<=10**6,'19 loss cap')
    # Fixed Euler at 1109 implies all remaining bases are odd primes with
    # even exponents. The order-277 uniform price is independent of h.
    C=50_000_000
    require(X*C**276>B,'strict base cap')
    rr=[r for r in range(2,S) if pow(r,277,S)==1]
    require(len(rr)==276,'complete prime-order primitive roots')
    m=S
    for z in range(1,5):
        low=min(r if r%2 else r+m for r in rr)
        if z==4:
            require(low>=C,'strict all-class depth-four tail')
            break
        require(low**276>=S**(100*z),('1109 deficit',z))
        m1=m*S
        rr=[r+m*((-((pow(r,277,m1)-1)//m)*pow(277*pow(r,276,S),-1,S))%S) for r in rr]
        require(all(0<r<m1 and pow(r,277,m1)==1 for r in rr),'Hensel derivative lifts')
        m=m1
    # 1109 exact Euler h must be 1 modulo 4; all h>=5 may be checked at
    # one lower endpoint, since 19 supply from this actual Euler atom is
    # bounded through its order-three base and LTE window.
    require(pow(S,3,P)==1 and S%P!=1,'1109 at prime 19 order 3')
    z=vp(S**3-1,P)
    require(z==1 and P**3>5031,'fixed bound on 1109 to 19 output')
    # For an exponent h on q=1109, h+1 <=5031 and any contribution
    # to 19 is <=z+2=3. Initial outputs to 19 are recomputed.
    c19=276-vp(Y,P)-(z+2)
    require(c19>=0,'nonnegative conservative target demand')
    # N >= (X*1109^h)*19^(2*c19)*1109^(100*(h-1))/U.
    # The monotone check at h=9 handles all larger Euler exponents.
    require(X*S**9*P**(2*c19)*S**800 > B*10**6,'strict monotone h=9 terminal')
    tail=next(h for h in range(1,5031) if X*(D//S)*S**h>B)
    hwin=[h for h in range(1,tail,4) if not v['raw_closed'](prefix+[(S,h)])]
    require(1 in hwin and 5 in hwin,'initial low Euler window')
    if not X*S**5*P**(2*c19)*S**400 > B*10**6:
        # Exact four incoming units at 1109, total joint product cap less
        # than the least order-277 depth-two prime; four distinct depth-one
        # suppliers already exceed that cap.
        candidates=prefix+[(S,5)]
        X5,_,Y5,_=state(candidates)
        require(5-vp(Y5,S)==4,'Euler h=5 exact residual demand')
        K=63_700
        require(X5*P**(2*(276-vp(Y5,P)))*K**276>B*10**6,'Euler h=5 product cap')
        pool=[q for q in range(3,K,2) if q not in dict(candidates) and pow(q,277,S)==1 and prime(q)]
        require(pool[:4]==[13,29,53,67] and all(pow(q,277,S**2)!=1 for q in pool),'Euler h=5 full supplier coverage')
        require(prod(pool[:4])>=K,'Euler h=5 four distinct supplier terminal')
    # At the remaining exact Euler exponent one, its odd output forces
    # 3,5,37. All three are ordinary; use their minimal abundance first.
    eulerone=prefix+[(S,1)]
    Xe,He,Ye,_=state(eulerone)
    F=(3,5,37)
    require(all(prime(q) and q not in dict(eulerone) and Ye%q==0 for q in F),'Euler-one outgoing forced primes')
    abund=lambda p,e: Fraction(sigma(p,e),p**e)
    A=Fraction(He,Xe)*prod(abund(q,2) for q in F)
    forbidden={7,11,13,17,23,29,31}
    require(all(prime(q) and q not in (set(dict(eulerone))|set(F)) and A*abund(q,2)>2 for q in forbidden),'strict abundance absences')
    require(all(any(sigma(q,a)%u==0 for u in forbidden) for q in F for a in (2,4)),'2/4 all violate absent prime')
    require(Fraction(He,Xe)*prod(abund(q,6) for q in F)>2,'strict amplified abundance terminal')
    return hwin,tail


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--pivot',type=int,default=28)
    f=ap.parse_args().pivot
    live,tail=classify(f)
    print('EXCLUDED all',len(live),'Euler-at-1109 rows at pivot exponent',f,'strict raw tail',tail,'; only even 1109 exponents remain')


if __name__=='__main__':
    main()
