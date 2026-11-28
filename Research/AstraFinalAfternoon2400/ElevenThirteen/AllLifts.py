"""Complete finite Hensel-progression helper; no closure uses a capped search."""
from math import gcd, isqrt


def require(test, why):
    if not test:raise ValueError(why)


def isprime(p):return p>=2 and all(p%d for d in range(2,1+isqrt(p)))


def left_root(n, k):
    if k==1:return n
    if n<2:return n
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//x**(k-1))//k
        if y>=x:
            require(x**k<=n<(x+1)**k, 'integer root bracketing')
            return x
        x=y


def reduced_order(x,p,o):
    return pow(x,o,p)==1 and all(pow(x,d,p)!=1 for d in range(1,o) if o%d==0)


def lift(p,o,z):
    require(isprime(p) and o>1 and (p-1)%o==0 and z>0,'invalid order or level')
    m=p;xs=[x for x in range(1,p) if reduced_order(x,p,o)]
    for _ in range(1,z):
        k=m*p;xs=[x+m*(-((pow(x,o,k)-1)//m)*pow(o*pow(x,o-1,p),-1,p)%p) for x in xs];m=k
    return xs,m


def universe(p,o,z,num,den,ceiling,lower=3,residues=(),candidate_cap=None):
    """All integer r with exact depth z, order o mod p, and r**(den*(o-1)) < p**(num*z).

    `ceiling` is an independently justified inclusive size bound. `residues`
    is a conjunction of (modulus,remainder), using moduli prime to the current
    CRT stride (e.g. (2,1) for odd bases). A positive optional cap is a fail-closed
    resource limit: generator raises without yielding any partial result.
    """
    require(num>0 and den>0 and lower>=1 and ceiling>=0 and (candidate_cap is None or candidate_cap>0),'bad interval')
    roots,mod=lift(p,o,z)
    hi=min(ceiling,left_root(p**(num*z)-1,den*(o-1)));runs=[]
    for x in roots:
        M=mod
        for d,b in residues:
            require(d>1 and gcd(d,M)==1,'non-coprime CRT')
            x+=M*((b-x)*pow(M,-1,d)%d);M*=d
        lo=lower+(x-lower)%M
        if lo<=hi:runs.append((lo,hi,M))
    volume=sum((b-a)//m+1 for a,b,m in runs)
    if candidate_cap is not None and volume>candidate_cap:
        raise OverflowError((p,o,z,volume,'no coverage credit'))
    return sorted(r for a,b,m in runs for r in range(a,b+1,m) if pow(r,o,mod*p)!=1)


def check():
    done=0
    for p,o in ((7,3),(11,5),(13,3),(19,3),(19,9)):
        for z in (1,2,3):
            for num,den in ((2,1),(6,1),(7,2),(19,5)):
                for residues in ((),((2,1),),((2,1),(5,1))):
                    C=2500; G=universe(p,o,z,num,den,C,residues=residues)
                    A=[r for r in range(3,C+1) if all(r%d==b for d,b in residues) and reduced_order(r,p,o) and pow(r,o,p**z)==1 and pow(r,o,p**(z+1))!=1 and r**(den*(o-1))<p**(num*z)]
                    require(G==A,('brute progression mismatch',p,o,z,num,den,residues));done+=1
    for p,b in ((13,29),(19,83)):
        require(isprime(b) and b>p and b in universe(p,3,1,6,1,p**3-1,residues=((2,1),)),('nonleast witness',p,b))
    try:universe(19,3,2,6,1,19**6-1,candidate_cap=5)
    except OverflowError:pass
    else:raise ValueError('cap must not silently truncate')
    print('PASS',done,'independent brute-force profiles; two nonleast legal-depth prime examples; fail-closed volume cap')

if __name__=='__main__':check()
