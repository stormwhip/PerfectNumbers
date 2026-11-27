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
def sig(r,h):return (r**(h+1)-1)//(r-1)
CERT={180723414399727954622158411013081: [2, 2, 2, 5, 11, 191, 146213, 8177455843, 1798556907053], 1798556907053: [2, 2, 181, 683, 727, 5003], 8177455843: [2, 3, 157, 8680951], 110325624297040487192218899595891: [2, 3, 5, 7, 7, 113, 664172080531217188563114199], 664172080531217188563114199: [2, 3, 3, 3, 17, 433, 97571, 17124948803196827], 17124948803196827: [2, 1297, 62761, 105188789], 105188789: [2, 2, 19, 241, 5743], 14465337262023883272971: [2, 5, 1446533726202388327297], 1446533726202388327297: [2, 2, 2, 2, 2, 2, 2, 3, 13, 29, 229, 43633545828193], 43633545828193: [2, 2, 2, 2, 2, 3, 3, 3, 83, 608455291], 608455291: [2, 3, 5, 31, 229, 2857], 104921390983312892647: [2, 3, 3, 7, 2549, 11633, 28082251913], 28082251913: [2, 2, 2, 11, 13, 24547423], 16112683243887984931: [2, 3, 5, 11, 29, 15991, 105288347239], 105288347239: [2, 3, 31, 2389, 236947], 4817379708398989591: [2, 3, 5, 37, 607, 7149887511167], 7149887511167: [2, 3574943755583], 3574943755583: [2, 43, 12541, 3314657], 51436505067473263: [2, 3, 11, 61, 1627, 7852539481], 7852539481: [2, 2, 2, 3, 5, 23, 23, 123701], 3993661447611491: [2, 5, 199, 2006865049051], 2006865049051: [2, 3, 3, 3, 5, 5, 503, 883, 3347], 25303424196319: [2, 3, 122861, 34325273], 1190236451: [2, 5, 5, 13, 1831133], 34214860794011: [2, 5, 13, 43, 14029, 436291]}
@lru_cache(None)
def prime(r):
    if r<10**8:return r>=2 and all(r%i for i in range(2,isqrt(r)+1))
    fs=CERT[r]; return prod(fs)==r-1 and all(prime(k) for k in fs) and any(pow(a,r-1,r)==1 and all(gcd(pow(a,(r-1)//k,r)-1,r)==1 for k in fs) for a in range(2,100))

def run():
    f=42;U=check(f);A=sig(P,E)//T;C=sig(T,f);X=P**E*T**f;M=X//T;D=A*C;H=max(A,C)
    def branch(rows):
        if X*prod(r**h for r,h in rows)*A*C > B*prod(gcd(A*C,r**h) for r,h in rows):return 'raw'

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
        left=X0**5*M0**19;right=B**5*int(U)
        simple=left>right*cut**14
        if simple:return 'simple'
        bound=(left-1)//right
        if not bound:return 'pending'
        hi=1<<((bound.bit_length()+13)//14)
        while True:
            nxt=(13*hi+bound//hi**13)//14
            if nxt>=hi:break
            hi=nxt
        lo=hi;assert lo**14<=bound<(lo+1)**14
        if lo>=max(T**(f-1),*blocks[1:]) and (2*X0)**5*M0**19*(2*X0*D0)**14*(lo+1)**19>(3*B)**5*U*(3*B*H)**14:return 'supplier'
        return 'pending'
    r=34214860794011;v=14465337262023883272971;w=4817379708398989591
    n=110325624297040487192218899595891;z=16112683243887984931
    known=[34214860794011,173,1171,4441,7127,16699,30103,95531,161641,12402811,1190236451,25303424196319,3993661447611491,51436505067473263,4817379708398989591,16112683243887984931,104921390983312892647,14465337262023883272971,110325624297040487192218899595891,180723414399727954622158411013081]
    assert all(prime(n) for n in known) and r%4==3 and sig(T,f)%r==0
    labels=set();stats={}
    def tree(rows,depth):
        result=branch(rows)
        stats[result]=stats.get(result,0)+1
        if result!='pending':return []
        if depth==0:return [rows]
        used={b for b,h in rows}; edges=[]
        for b in known:
            if b in used:continue
            if b%4==1:
                # If b=q, all a=1 mod4 are already excluded by root-only pricing:
                # all currently added rows are temporarily restored as atoms.
                m=gcd(M,b+1)
                if X**5*b**5*(M//m)**19<=B**5*U:continue
            if any(sig(a,g)%b==0 for a,g in [(T,f)]+rows):edges.append(b)
        if not edges:return [rows]
        target=max(edges);labels.add(target);left=[]
        h=0
        while True:
            h+=2
            if X*prod(b**g for b,g in rows)*target**h>B:break
            left.extend(tree(rows+[(target,h)],depth-1))
        return left
    assert r%4==3
    live=[];h=2
    while X*r**h<=B:
        if branch([(r,h)])=='pending':live.append(h)
        h+=2
    assert live==[4,6,10,12]
    print('forced R, raw size tail',h,'direct live',live)
    for h in [4,10,12]:
        rem=tree([(r,h)],5);assert not rem
    print('PASS f42 requires v_R(N)=6; labels',len(labels),'tree counts',stats)
if __name__=='__main__':run()
