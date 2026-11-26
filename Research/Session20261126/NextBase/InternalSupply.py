"""Eliminate positive 3-supply internal E3b source throughout e=1108 (not full E3b)."""
from math import isqrt

def verify(e,R):
    pe=3**e;A=(3*pe-1)//2;B=10**2400
    assert R>=10**12 and isqrt(A)**2!=A
    # A source with positive b has r>R and f>=3^b-1. Already b>=6 impossible.
    assert R**(3**6-1)>B
    triples=0
    for s in range(1,e):
        q=2*3**s-1
        for b in range(1,min(5,e-s)+1):
            # floor(2q/3) use only. For q<5 use q>=5 (all genuine s have q bound).
            source=max((2*q//3)**(3**b),R**(3**b-1));u=e-s-b
            H=A*R;M=source
            # minimize 81^(u-i)*max(H,R^(2i)*M) at the two crossover neighbors
            a,k=0,min(u,60)+1;assert R**120>H
            while a+1<k:
                j=(a+k)//2
                if R**(2*j)*M<=H:a=j
                else:k=j
            for i in {a,min(k,u)}:
                assert pe*q*81**(u-i)*max(H,M*R**(2*i))>B,(e,s,b,i)
            triples+=1
    return triples
if __name__=='__main__':print(verify(1108,10175119360001))
