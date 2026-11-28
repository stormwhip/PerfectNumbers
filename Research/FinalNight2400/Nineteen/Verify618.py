"""Exact self-contained, no discovery files or third-party arithmetic required."""
from math import gcd, isqrt, prod

p, e, t, B = 19, 618, 2477, 10**2400
n, d = 99, 50

def sig(x,h): return (x**(h+1)-1)//(x-1)
def val(x,r):
    k=0
    while x%r==0: x//=r;k+=1
    return k
def prime_small(x): return x>=2 and all(x%j for j in range(2,isqrt(x)+1))
def strip(x,r): return x//r**val(x,r)

def deficit():
    assert 39**(18*d)>19**n and 3**(54*d)>19**n
    best={}
    for o in (3,9):
        roots=[r for r in range(1,19) if pow(r,o,19)==1 and pow(r,o//3,19)!=1]; M=19
        for u in range(1,e+1):
            for r in roots:
                if r<3 or r%2==0 or r in (19,t) or any(r%j==0 and r!=j for j in (3,5,7,11,13,17,19,23,29,31,37)): continue
                a,b=p**(n*u),r**(d*(o-1))
                if a>b:
                    A,C=best.get(r,(1,1))
                    if a*C>b*A: best[r]=(a,b)
            if u==e:break
            K=M*19
            roots=[r+M*((-((pow(r,o,K)-1)//M)*pow(o*pow(r,o-1,19),-1,19))%19) for r in roots];M=K
            assert all(pow(r,o,M)==1 for r in roots)
    a=prod(x for x,y in best.values()); b=prod(y for x,y in best.values());g=gcd(a,b)
    assert len(best)==8
    return a//g,b//g

def zero_t():
    assert all(prime_small(j) for j in (19,619,t)) and t-1==4*619
    X=p**e; S=sig(p,e); assert val(S,t)==1
    assert (2*t+1)**(t-1)>B and 5**(2*t-1)>B
    for r in range(3,405,2):
        if X*r**618>B: break
        if r!=19 and prime_small(r) and pow(r,619,t)==1:
            assert X*strip(S,r)*r**618>B
    else: raise AssertionError('even tail')
    for q in range(5,26,4):
        if X*q**1237>B:break
        if prime_small(q): assert pow(q,1238,t)!=1 or pow(q,2,t)==1
    else: raise AssertionError('Euler tail')


def verify():
    assert __debug__;zero_t(); U,V=deficit(); threshold=B**d*U
    def price(K,c):return K**d*p**(n*c)*V>threshold
    A=sig(p,e)//t; result=[]; by_split={}
    for f in range(48,69,2):
        X=p**e*t**f; c=e-val(sig(t,f),p);C=strip(sig(t,f),p); D=A*C
        assert gcd(A,C)==1 and gcd(X,D)==1
        T=t**(f-1);Q=2*T-1
        # q=Q mod 4T. q|C would imply C/q in a single class mod 4T.
        j=(C*pow(Q,-1,4*T))%(4*T);assert C//Q<4*T and (not j or j>C//Q or C%j)
        # a>=5: external q by size, internal q by absorbing the odd m.
        assert X*D*Q**5>B and price(X*Q**3,c)
        # a=1, no Euler supply; q may already divide D but not X.
        assert price(X*Q,c)
        used=0
        for s in range(1,c+1):
            Qs=2*T*p**s-1
            if X*D*Qs>B:break   # monotonically increasing
            if price(X*Qs,c-s):continue
            # critical junction: strict first bound increases with u,
            # price bound decreases. Evaluate each at its weakest side.
            u=0;lhs=2*X*D*Qs**2;rhs=3*max(A,C)*B
            while u<=c-s and lhs<=rhs: lhs*=p; u+=1
            if u:
                v=u-1
                assert (2*X*Qs**2*p**v)**d * p**(n*(c-s-v))*V > (3*B)**d*U,(f,s,v)
            used+=1
        result.append(f);by_split[f]=used
    print('19^618, 2477 exponent exclusions:',result,'supplier-split s counts:',by_split,flush=True)
if __name__=='__main__':verify()
