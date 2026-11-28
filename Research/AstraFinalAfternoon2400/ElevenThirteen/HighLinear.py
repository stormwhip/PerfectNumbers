"""High linear-Euler windows for the two anonymous root-13 keys. Standard library."""
from functools import cache
from math import gcd, isqrt

P=13
B=10**2400
BAN=(19,7,11,31)
ES=(612,618)
ROUGH=10**7


def require(test, what):
    if not test:
        raise ValueError(what)


@cache
def floor_root(n,k):
    if k==1:return n
    if k==2:return isqrt(n)
    if n<2:return n
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//x**(k-1))//k
        if y>=x:
            require(x**k<=n<(x+1)**k, ('integer root', k))
            return x
        x=y


def ceil_root(n,k):
    return 1+floor_root(n-1,k)


def prime_tiny(n):
    return n>=2 and all(n%d for d in range(2,1+isqrt(n)))


def inputs(e):
    X=P**e; W=P*X; A=(W-1)//(P-1); n=e+1; M=2*n
    require(e in ES and prime_tiny(n) and A%n and gcd(A,P-1)==1, 'prime-index order class')
    require(A%M==1 and gcd(M,P)==1, 'cyclotomic progression')
    require(all(A%q for q in BAN), 'distinct support bans')
    count=0
    for r in range(1+M,ROUGH+1,M):
        require(A%r!=0, ('roughness failure',e,r))
        count+=1
    # Exact square-root and a Fermat compositeness witness imply at least two distinct prime factors:
    # test all possible prime-power exponents, without assuming squarefreeness.
    require(pow(2,A-1,A)!=1, 'Fermat witness')
    for k in range(2, A.bit_length()):
        if prime_tiny(k): require(floor_root(A,k)**k!=A,('perfect power',e,k))
    return X,W,A,M,count


@cache
def minimum_q(s,h):
    Y=P**s
    # Nonlinear order or the case P | h+1 has already been ruled out.
    u=pow(Y,-1,h+1);u+=(h+1)*((1-u)%2)
    for _ in range(64):
        q=2*u*Y-1
        if gcd(u,P*19*7*11*31)==1 and all(q%r!=0 or q==r for r in (3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)):
            break
        u+=2*(h+1)
    return 2*u*Y-1


def cell(e,s,dat):
    X,W,A,M,_=dat
    Y=P**s;Q0=2*Y-1
    require(2*s>e and Q0>5100 and 3**5100>B, 'external Euler and primitive exponent domain')
    # Provided by separate inequalities in the proof; no internal q or external emitter here.
    require(X*A*Q0*Q0*2>3*B, 'external emitter cannot be excluded')
    require(X*A*Q0**5>B, 'nonlinear Euler cannot be excluded')
    require(X*Q0*(2*Q0)**3>27*B,'imprimitive emitter cannot be excluded')
    T0=B//(X*A*Q0); out=set();c=1
    while ROUGH**(c+1)<=A:
        h=c+c%2
        while X*Q0*ROUGH**h<=B and ROUGH**(h-c)<=T0:
            hh=h;h+=2
            if (hh+1)%P==0:continue
            Q=minimum_q(s,hh);T=B//(X*A*Q)
            if not T:continue
            lo=max(ROUGH+1,ceil_root((2*Q+2)//3,hh));hi=floor_root(A//ROUGH,c)
            if hh>c:hi=min(hi,floor_root(T,hh-c))
            if hi<lo:continue
            if hh==c==2 and 2*(3*(P-1)*A)**2+3*(P-1)*A*Q <2*Y*Q*Q:continue
            if 3*W*T<Y*Q and 3*T<2*Y:
                hi=min(hi,2*(W//Y)+1)
            if hi<lo:continue
            d=hh+1-c; Dhi=(P-1)*(A//lo**c)
            pos=(W-1)*hi**d//(Q*Y);neg=(Q*hi**d+(Q+1)*Dhi)//(Q*Y)
            J=(-1-(P-1)*A)*pow(Y,-1,M)%M
            if (J or M)>pos and ((-J)%M or M)>neg:continue
            out.add((hh,c))
        c+=1
    return out


def main():
    expected={612:{(8,3),(10,5)},618:{(10,5)}}
    for e in ES:
        dat=inputs(e)
        require(dat[-1]=={612:8156,618:8077}[e],('progression count',e))
        for s in range(537,e+1):require(not cell(e,s,dat),('high cell not excluded',e,s))
        require(cell(e,536,dat)==expected[e],('control boundary',e))
        print('PASS', P,e,'s<=536:',e-536,'high cells excluded; s=536 relaxed shapes',sorted(expected[e]),flush=True)


if __name__=='__main__':main()
