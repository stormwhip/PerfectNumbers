"""Short sealed scalar cubic-dominance price for a single target at weight 2."""
from Prices import *

@cache
def lower_mass(p,c,Bx):
    # Maximum shift over ALL h>=2 for r>=5 and r^h<=Bx.
    hmax=0
    while qpow(5,hmax+1)<=Bx:hmax+=1
    s=0
    while qpow(p,s+1)<=hmax+1:s+=1
    # Ordinary or admissible high Euler h: L=h+1 either odd or 2 mod4.
    # Primitive nontrivial order o therefore odd or twice an odd number.
    assert all(5**(p**k-1)>=p**(2*k) for k in range(1,s+1))
    oset=[o for o in divisors(p-1) if o>2 and o%4 and o<=hmax+1 and 5**(o-1)<p**(2*c)]
    for o in (2,*oset):
        assert all(5**(o*(p**k-1)-(4 if o==2 else 0))>=p**(2*k) for k in range(1,s+1))
    return oset,hmax

def price2(rows,p,exclude=lambda r,h:False):
    """Bounds unassigned exponent f>=2, for fixed Euler or all admissible f.
    For o=2, legal Euler always f>=5, not f=1. For all orders, allocated
    min compatible exponent d and the p-index shift cost are disjoint.
    A root candidate (r,d) accounts for ALL actual powers of this r in the class.
    """
    fixed,odd,X,S,D,blocks=get_context(rows)
    c=fixed[p]-vp(S,p);orders,hm=lower_mass(p,c,B//X);E={}
    for o in (2,*orders):
        if odd and not o%2:continue
        # When o=2, actual h>=5 already (Euler exponent one excluded).
        # Odd o, ordinary h>=o-1; if Euler h odd then L multiple 2o.
        f=5 if o==2 else o-1
        if 5**f>=p**(2*c):continue
        # Any actual base in this order costs r^f<=B/X. Once all roots modulo
        # p^depth are above this bound, every deeper class is impossible.
        depth=min(c,2+(B//X).bit_length()//(f*(p.bit_length()-1)))
        while depth<c:
            if all(not less(r,f,B//X+1) for r in root_levels(p,o,depth)[-1][-1]):break
            depth=min(c,depth+2)
        for j,m,roots in root_levels(p,o,depth):
            lim=m*m
            if 5**f>=lim:continue
            for r in roots:
                # f>=2 and r^f<lim force r<m. This is the w<=o−1
                # direct case for odd orders; order 2 uses f>=5 instead.
                if r in fixed or r in BAN or r<5 or r%2==0 or not less(r,f,lim):continue
                if any(r!=q and r%q==0 for q in SMALL):continue
                if not o%2 and r%4!=1:continue
                if exclude(r,f):continue
                # Check only always-active bans; for even o the odd-power
                # emission from the minimal odd-length block is not sigma(f).
                # If gcd(L_min,q) assumption is not universal, omit the cut.
                if o%2 and any(exact_supply(r,f,q,0)>0 for q in BAN):continue
                if X*D*r**f//gcd(D,r**f)>B:continue
                if pow(2,r-1,r)!=1:continue
                E[r]=max(E.get(r,F(1)),F(lim,r**f))
    return F(X*p**(2*c))/prod(E.values(),start=F(1)),E

if __name__=='__main__':
    from Explore import CASES
    from sys import argv
    for k in argv[1:] or CASES:
        rows=CASES[k];p=rows[-1][0];V,E=price2(rows,p);print(k, 'Vfloor',floor10(V), 'losses',len(E), 'loss-floor',floor10(prod(E.values(),start=F(1))),flush=True)
