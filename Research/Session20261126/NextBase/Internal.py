"""E3b ISO integer envelope; no LP, no floating point. Optional all three generic parameters.
External source E3a handled separately. E3b assumes b=0; validates b>0 via separate inequality.
Outputs > 10^t lower-bound certificates whenever check() succeeds, otherwise a low-prefix cap.
"""
from math import isqrt,gcd
from functools import cache
E=1108;P=3**1109;A=(P-1)//2;PE=P//3;R=10175119360001;B=10**2400
@cache
def coeff(s):
    y=3**s; delta=P//y
    return y,delta

def test(s,m,target):
    y,delta=coeff(s);q=2*m*y-1;limit=10**target//(PE*q);u=E-s
    # In the D1 branch r-1<2delta pay denominator 2delta+4.
    # In the D2 branch r-1>=2delta, P/(r-1)<=Y/2, giving t>Y/(3H).
    # If R>2delta+1 only the second case applies. Otherwise existing y/(H(delta+4)).
    # H=max(1,P/q) retained (no over-credit when q>P).
    I=y*q//(max(q,P)*(3 if R>=2*delta+1 else delta+4));Q=2*q//3
    z=max(I,1);H=max(A*R,A*z);M=max(Q,z)
    # max(H, R^(2i)M)/81^i has a single minimum at a crossover neighbor.
    a,b=0,min(u,60)+1;assert R**120>A*A
    while a+1<b:
        k=(a+b)//2
        if R**(2*k)*M<=H:a=k
        else:b=k
    return all(81**(u-i)*max(H,R**(2*i)*M)>limit for i in {a,min(b,u)})

def caps(target):
    low=[]
    for s in range(1,E+1):
        if test(s,1,target):continue
        m=2
        while not test(s,m,target):m*=2
        a,b=m//2,m
        while b>a+1:
            k=(b+a)//2
            if test(s,k,target):b=k
            else:a=k
        low.append((s,a))
    return low
if __name__=='__main__':
    import sys
    low=caps(int(sys.argv[1]));print('sum',sum(x for _,x in low),'max',max(low,key=lambda z:z[1],default=None),'s',len(low));print(low)
