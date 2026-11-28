"""Independent coverage for high Euler linear supply to root 13."""
from math import gcd, isqrt
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from Check7x808 import floorroot, isprime
B=10**2400
R=10**7
P=13
BANS=(19,7,11,31)


def qmin(y,h):
    o=h+1
    m,=[a for a in range(1,2*o,2) if a*y%o==1]
    for j in range(65):
        a=m+2*j*o
        q=2*a*y-1
        if j==64 or (all(a%p for p in (P,*BANS)) and all(q%p for p in SMALL)):
            return q
    raise AssertionError


def analyze(e):
    X=P**e; W=P*X; A=sum(P**i for i in range(e+1))
    M=2*(e+1)
    assert A*(P-1)+1==W and isprime(e+1) and A%(e+1) and gcd(A,P*(P-1)*M//2)==1
    assert A%M==1 and all(A%p for p in BANS)
    count=0
    for a in range(1+M,R+1,M):
        # A can only have order e+1 factors. Exclude every tested candidate in its class.
        assert pow(P,e+1,a)!=1
        count+=1
    assert pow(2,A-1,A)!=1
    for degree in range(2,A.bit_length()):
        if isprime(degree):
            assert floorroot(A,degree)**degree != A
    resident={}
    for s in range(536,e+1):
        y=P**s; q0=2*y-1
        assert 2*s>e and q0>5031
        assert X*A*q0**5>B and 2*X*A*q0*q0>3*B and 8*X*q0**4>27*B
        res=(-1-(P-1)*A)%M
        a,=[k for k in range(1,M+1) if y*k%M==res]
        b,=[k for k in range(1,M+1) if (-y*k)%M==res]
        pos,neg=a*y,b*y
        live=[]
        h=2
        while X*q0*(R+1)**h<=B:
            if (h+1)%P:
                Q=qmin(y,h)
                t=B//(X*A*Q)
                lo=max(R+1,floorroot(2*Q//3,h)+1)
                for c in range(1,h+1):
                    if not t:
                        continue
                    hi=floorroot(A//(R+1),c)
                    if h>c:
                        hi=min(hi,floorroot(t,h-c))
                    if c==h==2 and 2*(3*(P-1)*A)**2+3*(P-1)*A*Q<=2*y*Q*Q:
                        continue
                    if 3*W*t<y*Q and 3*t<2*y:
                        hi=min(hi,2*W//y+1)
                    if hi<lo:
                        continue
                    v=hi**(h+1-c)
                    d=(P-1)*(A//lo**c)
                    if (W-1)*v<=Q*pos and Q*v+(Q+1)*d<Q*neg:
                        continue
                    live.append((h,c))
            h+=2
        resident[s]=sorted(live)
    assert all(not items for s,items in resident.items() if s>536)
    print('PASS',e,'roughness classes',count,'closed high windows',len(resident)-1, 'boundary 536',resident[536],flush=True)
    return resident[536]


if __name__=='__main__':
    assert __debug__ and 3**5030<=B<3**5031
    SMALL=tuple(q for q in range(3,98,2) if isprime(q))
    assert analyze(612)==[(8,3),(10,5)]
    assert analyze(618)==[(10,5)]
