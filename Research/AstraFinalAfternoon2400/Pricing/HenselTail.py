#!/usr/bin/env python3
"""Coverage fixture for rational high-weight losses without enumerating lifts.

The output is a conservative cap, not itself a frontier exclusion. For a
strict size cap R, pass R-1 as max_base. Caller proves a cap on the basic
valuation of each source, and supplies the true primitive-order root family.
"""
from fractions import Fraction
from itertools import combinations
from math import prod


def require(ok, reason):
    if not ok:
        raise ValueError(reason)


def family(s, o, roots, J):
    """Generate exact primitive roots from the caller-certified first layer."""
    require(J >= 1 and o > 1 and (s-1)%o == 0, 'invalid order or depth')
    require(all(0 < r < s and pow(r,o,s)==1 for r in roots), 'invalid starting root')
    require(len(roots) == len(set(roots)), 'duplicate roots')
    M = s
    for j in range(1, J+1):
        yield j, M, tuple(roots)
        M1 = M*s
        nxt = []
        for r in roots:
            v = pow(r,o,M1)-1
            require(v%M==0,'invalid known root')
            x = r+M*((-(v//M)*pow(o*pow(r,o-1,s),-1,s))%s)
            require(0<x<M1 and pow(x,o,M1)==1,'lift calculation')
            nxt.append(x)
        roots, M = nxt, M1


def monotone_class(s, M, r, j_min, j_max, a, d, e, units, max_base):
    """Bounds d-th-power losses for one exact depth or terminal window.

    This assumes every used base in the window consumes >= j_min units,
    has valuation <= j_max, and occurs at most once. Composite integers
    are deliberately admitted; exact valuations need not be checked.
    """
    require(1 <= j_min <= j_max <= units and a>=1 and d>=1 and e>=1 and 0<r<M and M%2==1, 'bad input')
    r0 = r if r%2==1 else r+M
    if r0 < 3:
        r0 += 2*M
    step = 2*M
    t = min(units//j_min, 1 + (max_base-r0)//step)
    if t <= 0:
        return (Fraction(1),)
    P, h = s**(a*j_max), d*e
    # No omitted uplift can improve the first t losses, because b_k increases.
    out = [Fraction(1)]
    for k in range(t):
        q = (r0+step*k)**h
        if q>=P:
            break  # Monotone nonpositive-loss tail.
        out.append(out[-1]*Fraction(P,q))
    return tuple(out)


def upper_loss(s, o, roots, J, c, a, d, e, max_base):
    """DP relaxation respecting sum of basic valuations, with no lift scan.

    Classes at j<J use exact valuation j; all j>=J are consolidated at J.
    DP sums minimum units for the selected counts; for the terminal group
    the losses deliberately use maximum valuation c, so the DP is an upper
    bound. Separate source orders should receive independent caps or be put
    into a shared resource DP; do not multiply in a smaller total cap unless
    a joint theorem establishes how many units each order receives.
    """
    require(1<=J<=c,'invalid terminal depth')
    best = [Fraction(1)]*(c+1)
    for j,M,rr in family(s,o,roots,J):
        for r in rr:
            costs = monotone_class(s,M,r,j,c if j==J else j,a,d,e,c,max_base)
            best = [max(best[t-j*k]*v for k,v in enumerate(costs) if j*k<=t) for t in range(c+1)]
    return best[-1]


def test_small():
    # PR11's true nonleast positive high-weight loss.
    require(pow(83,3,19)==1 and pow(83,3,19**2)!=1 and 83%19==7 and 83**2<19**6,'missing old witness')
    # Toy exact coverage: include every odd base, even composites. Exhaustive
    # valuation-weighted knapsack is independent of the lift implementation.
    for s,o,J,c,a,d,e,R in [(7,3,1,5,6,1,2,50),(7,3,2,6,6,1,2,100),(19,3,2,6,11,2,2,140)]:
        roots=[r for r in range(2,s) if pow(r,o,s)==1]
        full = []
        for b in range(3,R+1,2):
            if b%s in roots:
                z=1
                while z<c and pow(b,o,s**(z+1))==1:
                    z+=1
                loss=max(Fraction(1),Fraction(s**(a*z),b**(d*e)))
                if loss>1:
                    full.append((z,loss))
        brute=[Fraction(1)]*(c+1)
        for j,v in full:
            for t in range(c,j-1,-1):
                brute[t]=max(brute[t],brute[t-j]*v)
        require(upper_loss(s,o,roots,J,c,a,d,e,R)>=brute[-1], 'unsafe upper cap')
    print('PASS old nonleast witness; three independent brute-force high-weight caps')


if __name__ == '__main__':
    test_small()
