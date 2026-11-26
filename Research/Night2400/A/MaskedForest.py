"""Independent integer forest at exact components and stipulated absent primes."""
from functools import cache
from math import gcd, prod


def exact_absence_bound(parts, roots, owners, head, bad, B):
    X=prod(p**e for p,e in parts)
    S=prod(((p**(e+1)-1)//(p-1))//(1+e%2) for p,e in parts)
    D=S
    for p,e in parts:
        while D%p==0:
            D//=p
    U=X*D*prod(q for q,p in owners)
    ban=prod(bad)
    fixed_euler=any(e%2 for p,e in parts)
    children={q:[] for q in [*roots,*(q for q,p in owners)]}
    for q,p in owners:
        children[p].append(q)
    def val(n,p):
        v=0
        while n%p==0:
            n//=p
            v+=1
        return v
    @cache
    def solve(p,h):
        plain=special=B+1
        for odd in (False,True):
            if odd and (fixed_euler or p%4!=1 or gcd(p+1,ban)>1):
                continue
            best=special if odd else plain
            e=h+((1-h)%4 if odd else h%2)
            step=4 if odd else 2
            n=0
            while n<head and p**e<best:
                T=(p**(e+1)-1)//(p-1)
                if gcd(T,ban)==1:
                    n+=1
                    T//=1+odd
                    u=T
                    while (g:=gcd(u,U))>1:
                        u//=g
                    f=[solve(q,val(T,q)) for q in children[p] if T%q==0]
                    a=p**e*u*prod(v for v,w in f)
                    if not odd:
                        plain=min(plain,a)
                    special=min([special,a]+([a//v*w for v,w in f] if not odd and not fixed_euler else []))
                    best=special if odd else plain
                e+=step
            if not odd:
                plain=min(plain,p**e)
            special=min(special,p**e)
        return plain,special if not fixed_euler else plain
    hs=[val(D,p) for p in roots]
    assert all(hs)
    S=X*(D//prod(p**h for p,h in zip(roots,hs)))
    f=[solve(p,h) for p,h in zip(roots,hs)]
    a=S*prod(v for v,w in f)
    return min([a]+[a//v*w for v,w in f]) if not fixed_euler else a
