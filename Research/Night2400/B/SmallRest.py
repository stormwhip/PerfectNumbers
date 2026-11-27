"""An exact small-cofactor terminal test for high Euler-one size windows."""
from math import gcd,isqrt,prod
from functools import cache

@cache
def sigma_small(n):
    assert n>=1
    s=1;r=2
    while r*r<=n:
        z=1
        while n%r==0:n//=r;z=z*r+1
        s*=z;r+=1 if r==2 else 2
    if n>1:s*=1+n
    return s


def excludes(F,S,D,B,minimum_euler,rough=20_000_001,cap=500000):
    """Test R in N = X D e R, with emitter-independent exact small cofactor."""
    X=prod(q**h for q,h in F);L=B//(X*D*minimum_euler)
    if L>=rough or L>cap:return False
    fixed=list(dict(F));ban=(19,7,11,31,13)
    assert D%2==X%2==1 and gcd(D,X)==1 and gcd(D,prod(ban))==1
    assert minimum_euler>L
    # rho(A) <= L0/(L0-1) to number of prime factors, with L0 the
    # smallest possible prime divisor of D. The integer cutoff uses all
    # multiplicities and is deliberately conservative.
    j=0;root=rough
    while root<=D:root*=rough;j+=1
    num=rough**j;den=(rough-1)**j
    # Since e does not divide D, R is coprime to DXe, and has no odd valuation.
    # Compare inclusive interval since D's exact sigma is not known.
    for r in range(1,1+isqrt(L),2):
        if gcd(r,prod(fixed)*prod(ban))!=1:continue
        t=r*r;st=sigma_small(t)
        if gcd(st,prod(ban))!=1:continue
        a=S*st;b=2*X*t
        if a>b:continue
        if a*num*(minimum_euler+1)<b*den*minimum_euler:continue
        return False
    return True
