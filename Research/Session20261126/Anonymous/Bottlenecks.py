"""Exhaustive survey of scalar-envelope *countermodels*, never odd perfect numbers.
A=unfactored root sigma ordinary, p^s Euler supply, source of q ordinary external b=0, internal supply i=e-s;
we strengthen by insisting A_i perfectly efficient ordinary supply at unit k=2, full square kernel >=10^13,
external normalized source minimal >2q/3, and accurate exact s small m proving conditional Euler q probable prime.
The missing non-scalar condition is realization of the shared A capacity by genuine primes; not asserted here.
"""
from math import isqrt,gcd
import sys,json
from pathlib import Path
here=Path(__file__).resolve().parent

def sig(p,e):return (p**(e+1)-1)//(p-1)
def run(p,e):
    A=sig(p,e);R=10**13
    # choose s and i so there is slack in A and r^f* q is affordable. For Feasible m, q PRP (not primality claimed).
    s=e//2;i=e-s;P=p**e;q0=2*p**s-1
    for m in range(1,30000,2):
        if m%p==0 or any(m%t==0 for t in ((19,) if p==7 else (19,7,11,31))):continue
        q=2*m*p**s-1
        if all(pow(a,q-1,q)==1 for a in (2,3)):break
    else:raise ValueError((p,e))
    assert q%4==1 and gcd(A,q)==1
    # Certify q prime, not just probable prime: 7^s or 13^s divides q-1? q=2m p^s-1 has smooth q+1 instead.
    # Lucas p-adic order via quadratic norm-one element. If prime ell|q with (D/ell) arbitrary,
    # a witnessed p^s in ord(g mod ell) forces ell >= p^s-1>sqrt(q). No factoring q+1 needed.
    assert (p**s-1)**2>q
    def mul(x,y,D):return ((x[0]*y[0]+D*x[1]*y[1])%q,(x[0]*y[1]+x[1]*y[0])%q)
    def exp(x,h,D):
        z=(1,0)
        while h:
            if h&1:z=mul(z,x,D)
            x=mul(x,x,D);h//=2
        return z
    found=False
    for D in range(2,80):
        # (1+sqrt D)/(1-sqrt D): well-defined norm 1 whenever gcd(1-D,q)=1.
        if gcd(D*(1-D),q)!=1:continue
        inv=pow(1-D,-1,q);g=((1+D)*inv%q,2*inv%q);z=exp(g,(q+1)//p,D)
        if exp(z,p,D)==(1,0) and gcd(q,gcd((z[0]-1)%q,z[1]))==1:found=True;break
    assert found,(p,e,m)
    # Normalize M1=P q r^f H with H=max(A R,p^(2i)), r^f near 2q/3 by proxy.
    # Include even square shape for abstract source and hull, without claiming sigma relation q|sigma(r^f).
    r=1+isqrt(2*q//3);src=r*r;H0=max(A*R,p**(2*i));H=(isqrt(H0)+1)**2
    assert H%2 or (H:=(isqrt(H)+1)**2)%2
    if r%2==0:r+=1;src=r*r
    # More faithful divisibility A|H: H as independent paid lower bound, condition NOT included.
    mass=P*q*H*src;generic=P*q*p**(2*(e-s))*src
    print(json.dumps(dict(p=p,e=e,s=s,i=i,m=m,q_prime_norm1_D=D,abstract_mass_floor=len(str(mass))-1,abstract_generic_floor=len(str(generic))-1,shortfall=2400-(len(str(max(mass,generic)))-1),source_b=0,scope='numeric envelope only'))) # not full primes or N
    assert mass<10**2400 and generic<10**2400
if __name__=='__main__':
    for p,e in ((7,906),(7,738),(7,456),(13,612),(13,618)):run(p,e)
