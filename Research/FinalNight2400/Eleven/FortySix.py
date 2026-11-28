"""All odd bases. Price is 19/5 at each target; common order five by CRT."""
from fractions import Fraction
from math import gcd,isqrt,prod
from functools import lru_cache
P,T,E=11,879701,462
B=10**2400

def divs(n):return [d for d in range(1,n+1,2) if n%d==0]
@lru_cache(None)
def generator(p):
    fac={q for q in range(2,p) if (p-1)%q==0 and all(q%d for d in range(2,isqrt(q)+1))}
    return next(g for g in range(2,p) if all(pow(g,(p-1)//q,p)!=1 for q in fac))
def levels(p,o,c):
    g=pow(generator(p),(p-1)//o,p)
    a=[pow(g,j,p) for j in range(1,o) if gcd(o,j)==1];m=1
    for u in range(1,c+1):
        m*=p;yield m,a
        if u<c:a=[r+m*((-((pow(r,o,m*p)-1)//m)*pow(o*pow(r,o-1,p),-1,p))%p) for r in a]

def check(f):
    p,t=P,T
    assert all(t%i for i in range(2,isqrt(t)+1)) and t-1==4*25*19*463
    X=p**E*t**f;A=(p**(E+1)-1)//(p-1);C=(t**(f+1)-1)//(t-1)
    assert gcd(A*C,X)==t
    D=A*C//t; ct=f-1
    assert 3**8000>B and t>8000 and 3**(5*(p-1))>=p**19
    # Common order 5 joint and both single 5 options. High t orders
    # reserve four powers of the base for p at order five.
    a5=[(1,(0,)),*levels(p,5,E)];b5=[(1,(0,)),*levels(t,5,ct)]
    small={};large={}
    def charge(store,r,m,h):
        if r<3 or not r%2 or 5*h*(r.bit_length()-1)>=19*m.bit_length():return
        if any(r%k==0 and r not in (k,k*k) for k in (3,5,7,11,13,17,19,23,29,31,37,41,43)):return
        if r**(5*h)<m**19:store[r]=max(store.get(r,1),Fraction(m**19,r**(5*h)))
    for n,bb in b5:
        inv=1;pi=pow(p,-1,n)
        for m,aa in a5:
            for a in aa:
                for b in bb:charge(small,a+m*((b-a)*inv%n),m*n,4)
            inv=inv*pi%n
    for o in divs((t-1)//4):
        if o<=5:continue
        h=o-5
        if 3**(5*min(h,8000))>=t**(19*ct):continue
        if o>100:
            R=3
            while R**(5*h)<t**(19*ct):R*=2
            assert R<100000
            for r in range(3,R,2):
                if pow(r,o,t)!=1:continue
                m=gcd(r**o-1,t**ct);charge(large,r,m,h)
        else:
            for m,aa in levels(t,o,ct):
                for r in aa:charge(large,r,m,h)
    U=prod(small.values(),start=Fraction(1))*prod(large.values(),start=Fraction(1));M=p**E*t**ct
    return Fraction((U.numerator+U.denominator-1)//U.denominator)
R=186573765099366387558103
S=15829818018805614866849809679719065959794687
def sig(r,h):return (r**(h+1)-1)//(r-1)
CERT={S:[2,3,49188809,53636244844518783621595072162718509],53636244844518783621595072162718509:[2,2,3,7,197,2724329,1189743385550999224631899],1189743385550999224631899:[2,3,17,1531,35543,988643,216812521],216812521:[2,2,2,3,3,5,602257],R:[2,3,7,47,349,24971,10845312385487],10845312385487:[2,33149,163584307],163584307:[2,3,3,3,3029339]}
@lru_cache(None)
def prime(r):
    if r<10**8:return r>=2 and all(r%i for i in range(2,isqrt(r)+1))
    fs=CERT[r]; return prod(fs)==r-1 and all(prime(k) for k in fs) and any(pow(a,r-1,r)==1 and all(gcd(pow(a,(r-1)//k,r)-1,r)==1 for k in fs) for a in range(2,100))

def run():
    f=46;U=check(f);A=sig(P,E)//T;C=sig(T,f);X=P**E*T**f;M=X//T;D=A*C;H=max(A,C)
    assert gcd(A,C)==1 and prime(R) and prime(S) and R%4==S%4==3 and C%R==0 and sig(R,2)%S==0
    assert pow(R,5,P)!=1 and pow(R,(T-1)//4,T)==1 and pow(R,((T-1)//4)//5,T)!=1 and pow(R,(T-1)//4//463,T)!=1 # order >=25*463>8000
    assert pow(S,(T-1)//4,T)!=1 and (S**5-1)%P==0 and (S**5-1)%P**2!=0
    assert 3**(P**4-1)>B
    def branch(rows):
        if any(sig(r,h)%k==0 for r,h in rows for k in (7,19)):return 'banned'
        assigned=[(P,E),(T,f)]+rows
        X0=prod(r**h for r,h in assigned)
        blocks=[sig(r,h) for r,h in assigned];M0=1
        for r,h in assigned:
            incoming=0
            for k in range(len(blocks)):
                while blocks[k]%r==0:blocks[k]//=r;incoming+=1
            if incoming>h:return 'excess'
            if r in (P,T):M0*=r**(h-incoming)
        D0=prod(blocks);assert gcd(D0,X0)==1
        H=max(n*prod(gcd(n,z) for j,z in enumerate(blocks) if i!=j) for i,n in enumerate(blocks))
        if X0*D0>B:return 'mandatory'
        # Non-root blocks bound q by size. If a nonroot huge, use instead
        # its reciprocity when p=11 divides q+1 and row base also 11? no.
        cut=max(T**(f-1),*blocks[1:],(B//(X0*D0))+1)
        simple=X0**5*M0**19>B**5*U*cut**14
        if simple:return 'simple'
        left=X0**5*M0**19;right=B**5*U
        lo,hi=0,1
        while hi**14*right<left:hi*=2
        while hi-lo>1:
            mid=(lo+hi)//2
            if mid**14*right<left:lo=mid
            else:hi=mid
        if lo>=max(T**(f-1),*blocks[1:]) and (2*X0)**5*M0**19*(2*X0*D0)**14*(lo+1)**19>(3*B)**5*U*(3*B*H)**14:return 'supplier'
        return 'pending'
    V=13584009104671777218460029405269012416436766343;W=193882521011;Z=2150985008682894323231
    CERT.update({W:[2,5,14387,1347623],Z:[2,5,1051,125093,286541,5709721],V:[2,3,113,20035411658807931000678509447299428342827089],20035411658807931000678509447299428342827089:[2,2,2,2,3,3,3,3,23,3917,11801,19543,2650532721869,280716957685349],280716957685349:[2,2,641,42221,2593117],2650532721869:[2,2,53,1153,10843463]})
    assert all(prime(r) and r%4==3 for r in (R,S,W,Z,V)) and len({P,T,R,S,W,Z,V})==7
    assert all(sig(r,h)%n==0 for r,h,n in [(T,f,R),(R,2,S),(R,4,W),(W,4,Z),(S,2,V)])
    for start,node in [([],R),([(R,2)],S),([(R,4)],W),([(R,4),(W,4)],Z),([(R,2),(S,2)],V)]:
        counts={};pending=[];h=2
        while X*prod(r**e for r,e in start)*node**h<=B:
            result=branch(start+[(node,h)]);counts[result]=counts.get(result,0)+1
            if result=='pending':pending.append(h)
            h+=2
        expected={R:[2,4],S:[2],W:[4],Z:[],V:[]}[node]
        print('node',node,'size tail',h,'buckets',counts,'recursive',pending,flush=True)
        assert pending==expected
    print('PASS exact first valuation 46 at (11,462)')
if __name__=='__main__':run()
