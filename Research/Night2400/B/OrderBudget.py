"""Cold finite supply-cap test when a small target forces high supplier exponents."""
from math import gcd,isqrt,prod
from functools import cache

B=10**2400
BAN=(19,7,11,31,13)


def vp(n,q):
    assert n>0
    a=0
    while n%q==0:
        n//=q;a+=1
    return a


def sigma(q,h):return (q**(h+1)-1)//(q-1)


@cache
def trial(p):return p>=2 and all(p%d for d in range(2,isqrt(p)+1))


def excludes(prefix,q,r_bound=20000):
    """Exact primes and prefix viability must have already been proved by caller."""
    assert __debug__ and type(q) is int and 3<=q<=10000 and trial(q)
    assert type(r_bound) is int and 3<=r_bound<=20000
    fixed=dict(prefix);assert len(fixed)==len(prefix) and q in fixed
    assert sum(h%2 for _,h in prefix)==1, 'budget requires a fixed Euler prime'
    X=prod(r**h for r,h in prefix);S=prod(sigma(r,h)//(1+h%2) for r,h in prefix)
    a=fixed[q]-vp(S,q);assert a>=1
    D=S
    for p,_ in prefix:D//=p**vp(D,p)
    assert X*D<=B
    # For each allowed number of supplied units, integer minimum net cost.
    # A unit from a source already dividing D is charged only its unspent power.
    L=B//(X*D);dynamic=[1]+[L+1]*a
    minordinary=min([q]+[d for d in range(3,q,2) if (q-1)%d==0])-1
    assert minordinary>=2
    for r in range(3,r_bound+1,2):
        if r in fixed or r in BAN or not trial(r):continue
        c=vp(D,r);largest=c
        while r**(largest+1-c)<=L:largest+=1
        opts={}
        for h in range(max(minordinary,c+c%2),largest+1,2):
            t=h+1
            if r%q==1:
                v=vp(t,q)
            elif pow(r,t,q)==1:
                modulus=q**(a+1)
                v=vp((pow(r,t,modulus)-1)%modulus or modulus,q)
            else:continue
            if v==0 or v>a:continue
            if any((h+1)%p==0 if r%p==1 else pow(r,h+1,p)==1 for p in BAN):continue
            opts.setdefault(v,r**(h-c))
        if opts:
            nxt=dynamic.copy()
            for v,m in opts.items():
                for j in range(a-v+1):nxt[j+v]=min(nxt[j+v],dynamic[j]*m)
            dynamic=nxt
    # A large supplier must exceed even the bare component budget B/X;
    # do not use B/(XD) here because its prime can divide D.
    assert (r_bound+1)**minordinary>B//X
    assert dynamic[a]>L,('residual target supply fits',prefix,q)
    return a


def supplier_options(prefix,q,r_bound):
    """Complete list of potential suppliers in a one-unit fixed-Euler deficit."""
    assert __debug__
    fixed=dict(prefix);assert len(fixed)==len(prefix) and sum(h%2 for _,h in prefix)==1
    assert type(q) is int and 3<=q<=10000 and trial(q) and q in fixed
    assert type(r_bound) is int and 3<=r_bound<=20000
    S=prod(sigma(r,h)//(1+h%2) for r,h in prefix);X=prod(r**h for r,h in prefix)
    D=S
    for p in fixed:D//=p**vp(D,p)
    assert fixed[q]-vp(S,q)==1 and X*D<=B
    L=B//(X*D)
    minordinary=min([q]+[d for d in range(3,q,2) if (q-1)%d==0])-1
    assert (r_bound+1)**minordinary>B//X
    for r in range(3,r_bound+1,2):
        if r in fixed or r in BAN or not trial(r):continue
        c=vp(D,r);h=max(minordinary,c+(c%2))
        while r**(h-c)<=L:
            t=h+1
            if (t%q==0 if r%q==1 else pow(r,t,q)==1):
                T=sigma(r,h);U=S*T;Y=X*r**h
                if (vp(T,q)==1 and gcd(U,prod(BAN))==1 and 2*S*T<=2*Y
                        and all(vp(U,z)<=e for z,e in (*prefix,(r,h)))):
                    for z in (*fixed,r):U//=z**vp(U,z)
                    if Y*U<=B:
                        yield r,h
            h+=2
