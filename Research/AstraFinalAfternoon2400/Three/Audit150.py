"""Independent stdlib replay of 398581^150 exact local Euler cuts."""
from math import gcd, isqrt, prod
from hashlib import sha256

P=398581;Q=1093;B=10**2400;BAN={7,11,13,19,31};R=20_000_001

def prime(n):return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
def val(n,p):
    c=0
    while n%p==0:c+=1;n//=p
    return c

def sig(p,f):return sum(p**j for j in range(f+1))

def ceil2(n):return n+(n%2)

from functools import cache
@cache
def factors(n):return tuple(d for d in range(2,n+1) if n%d==0 and prime(d))
SMALL=[p for p in range(3,98,2) if prime(p)]

def Hensel(q,o,l):
    # Direct group enumeration modulo q rather than trusting a searched
    # generator; use this independently calculated table only for needed o.
    G=next(x for x in range(2,q) if all(pow(x,(q-1)//p,q)!=1 for p in factors(q-1)))
    g=pow(G,(q-1)//o,q);roots=[pow(g,k,q) for k in range(1,o) if gcd(o,k)==1]
    inverses=[pow(o*pow(a,o-1,q),-1,q) for a in roots]
    m=q
    for i in range(l):
        yield m,roots
        M=m*q;roots=[a+m*((-((pow(a,o,M)-1)//m)*v)%q) for a,v in zip(roots,inverses)];m=M

def loss():
    assert (P-1)==4*3*5*7*13*73 and all(prime(x) for x in (P,Q,151))
    assert sig(3,6)==Q and sig(Q,2)==3*P
    X=3**6*Q**2*P**150;D=sig(P,150);S=Q*3*P*D
    assert gcd(D,2*151*P*(P-1)*3*Q*prod(BAN))==1 and isqrt(D)**2!=D
    assert (val(S,Q),val(S,3),val(S,P))==(1,1,1)
    assert all(D%x for x in range(303,R,302))
    Bx=B//X;fmax=Bx.bit_length()
    assert P>fmax+1 # no length LTE shift or order 1 at this target
    oset=sorted({2**t*3**a*5**b*7**c*13**d*73**e for t in range(2) for a in range(2) for b in range(2) for c in range(2) for d in range(2) for e in range(2)}-{1})
    Amax=P**298; checks=0
    for o in oset:
        f=max(5,o-1) if o==2 else o-1
        if 5**f>=Amax:continue
        for m,roots in Hensel(P,o,149):
            lim=m*m
            seen=False
            for r in roots:
                if (r.bit_length()-1)*f<Bx.bit_length() and r**f<=Bx:seen=True
                if r<5 or r%2==0 or r in (3,Q,P,*BAN) or (o%2==0 and r%4!=1):continue
                if (r.bit_length()-1)*f>=lim.bit_length() or r**f>=lim:continue
                if any(r!=p and r%p==0 for p in SMALL):continue
                if o%2 and any((f+1)%p==0 if r%p==1 else pow(r,f+1,p)==1 for p in BAN):continue
                if X*D*r**f//gcd(D,r**f)>B:continue
                checks+=1
                assert pow(2,r-1,r)!=1,(o,m,r)
            if not seen:break
    V=X*Amax;assert V>B
    return X,D,V

def fresh_q(m,a):
    m*=3**a
    for k in range(1,1001,2):
        q=2*m*k-1
        if k%3 and all(k%b for b in BAN) and all(p==q or q%p for p in SMALL):return q
    return 2002*m-1

def int_disproved(D,m,q0):
    x=2*m-1;K=4*m;u=D*pow(x,-1,K)%K or K
    L=D//q0
    if L>=u+65*K:return False
    return all(D%v for v in range(u,L+1,K))

def verify():
    assert __debug__
    X,D,V=loss();W=P**151; tests=[]; counts={}
    for i in (0,1):
        for j in range(150):
            y=P**j
            for a in range(6):
                m=Q**i*y;q=fresh_q(m,a);mm=m*3**a
                if V*q>B*y*y or X*D*q>B:s='basic'
                elif not int_disproved(D,mm,q):s='internal Euler possible'
                elif X*D*R*q>B:s='parity'
                else:
                    h=2*X*D*R*q*q>3*B
                    z=4*V*X*q**4>9*B**2*y*y
                    if j:z=z or X*D*q*q*y>B*max(W,q)*(W//y+4)
                    s='source' if h and z else 'exterior Euler open'
                tests.append((i,j,a,s));counts[s]=counts.get(s,0)+1
    digest=sha256(repr(tests).encode()).hexdigest()
    assert digest=='7918cc639dfd359b96d3f604e08b42d4a630492b2b78068b07f08318f6ac30ae'
    print('PASS independent 150 Hensel and source partition',counts,digest,flush=True)
if __name__=='__main__':verify()
