"""Independent arithmetic replay of (3,856) windows; imports no candidate code.
Run a trusted locally compiled Range.cpp separately to establish R.
"""
from math import isqrt,prod
from fractions import Fraction

E=856;B=10**2400;P=3**E;A=(3*P-1)//2; BAN=(7,11,13,19,31); R=100097600002

def prime(n):return n>=2 and all(n%k for k in range(2,isqrt(n)+1))
def sig(n,f):return (n**(f+1)-1)//(n-1)

# Independent exact domain rebuild: generate fixed q0 solely by trial and
# recompute the two tariff curves from multisets, with an independent tail.
pr=[p for p in range(2,15001) if prime(p)]; sb=[p for p in pr if p>=3 and p<=600]

def sequence(kind):
    cap=(15000**2+15001)//3 if kind else 15000**2
    pool=[cap]*E
    for p in pr:
        if p in BAN or p%3!=1:continue
        h=0
        for d in (3,9,27,81):
            if any(sig(p,d-1)%b==0 for b in BAN):break
            k=(p**(2*d//3)+p**(d//3)+1)//3 if kind else p**(d-1-h)
            if k>=cap:break
            pool.append(k);h=d-1
        else:raise AssertionError('unbounded supplier tail')
    pool.sort();return [prod(pool[:i]) for i in range(E+1)]


def euler(s,t):
    y=3**s;L=[m for m in range(1,170,2) if m%3==t]
    assert len(L)>=28
    for m in L[:28]:
        q=2*y*m-1
        if all(m%b for b in BAN) and all(q%b for b in (*BAN,*sb)):return q
    return 2*y*(L[27]+6)-1


def run():
    assert __debug__
    M,C=sequence(0),sequence(1)
    # Do not inherit the source zero theorem as an untested bound. For small
    # s no E3 survives; for all others independently test the imprimitive bound.
    assert all(P*M[E-s]>B for s in range(1,9))
    W=3*P;eps=[Fraction(1),Fraction(1)]; keep=[[],[]]
    for s in range(9,E+1):
        Y=3**s;k=E-s
        for b in range(min(6,k)+1):
            f=Fraction((43 if b else 5)**2*(2*(2*Y-1))**3,27)
            f=max(f,Fraction(43**(3**b-1))); assert max(P*(2*Y-1)*f*M[k-b],P*f*f/3**b)>B
        if s<640: # checked by completely uniform source comparison
            q=2*Y-1
            assert 2*P*q*q*M[k]>3*B
            continue
        for tag in (1,2):
            q=euler(s,tag);bal=Fraction(Y*q,max(W,q)*(W//Y+4));lo=[None,None]
            tail=0
            for i in range(k+1):
                outside=P*q*M[k-i];r=R**(2*i)
                for mode,v in ((0,Fraction(2*q,3)*max(A*R,r)),(1,max(A*R,r,A*bal,Fraction(2*q,3)*r,r*bal))):
                    n=outside*v
                    if lo[mode] is None or n<lo[mode]:lo[mode]=n
            baseline=max(P*A*q*C[k],Fraction(2*P*q*q*M[k],3))
            for mode,v in enumerate(lo):
                if max(v,baseline)<=B:keep[mode].append((s,tag))
    assert keep[0]==[(s,t) for s in range(696,857) for t in (1,2)]
    assert keep[1]==[(s,t) for s in range(678,857) for t in (1,2)]
    print('PASS independent tariff and windows:', [len(x) for x in keep], flush=True)
if __name__=='__main__':run()
