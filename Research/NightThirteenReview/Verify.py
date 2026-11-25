"""Pure Python independent verifier for p=13. No other files or external modules.
All intervals include their endpoints; a surviving necessary condition means OPEN.
Use --scan for an explicitly provisional run on lower e. See README for lemmas.
"""
import argparse, math, time
from collections import Counter
from fractions import Fraction
from functools import cache
from random import Random

P=13; B=10**2400; BAN=(19,7,11,31)
TARGET={808:(6473,),810:(97808132238521,),820:(464671223,),828:(),838:(86418679,),852:(5119,)}

def require(x,msg):
    if not x:raise ValueError(msg)

@cache
def sg(z,f):return (z**(f+1)-1)//(z-1)

def val(n,z):
    assert n>0
    t=0
    while n%z==0:n//=z;t+=1
    return t

@cache
def nth(n,k):
    if n<=1 or k==1:return n
    if k==2:return math.isqrt(n)
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//x**(k-1))//k
        if y>=x:return x
        x=y

@cache
def cyc(h):
    return (P**h-1)//math.prod(cyc(d) for d in range(1,h) if h%d==0)

SMALL=[z for z in range(3,10001,2) if all(z%d for d in range(3,math.isqrt(z)+1,2))]

@cache
def prime(n):
    # No primality oracle or pseudoprime claim: fixed witnesses use trial division.
    if not (3<=n<2**64) or n%2==0: return False
    if n<10**15:return all(n%d for d in range(3,math.isqrt(n)+1,2))
    # Deterministic Miller-Rabin (seven bases, exclusively below 2^64)
    d=n-1;j=0
    while d%2==0:d//=2;j+=1
    for a in (2,325,9375,28178,450775,9780504,1795265022):
        if a%n==0:continue
        b=pow(a,d,n)
        if b in (1,n-1):continue
        for _ in range(j-1):
            b=b*b%n
            if b==n-1:break
        else:return False
    return True

@cache
def lifts(j):
    '''The two primitive cubic roots mod 13^j are the two simple roots of x^2+x+1.'''
    if j==1:return (3,9)
    prev=lifts(j-1);m=13**(j-1)
    return tuple(x+m*((-((x*x+x+1)//m)*pow(2*x+1,-1,13))%13) for x in prev)

@cache
def profile(e):
    # Only possible odd nontrivial order is 3; other nontrivial eligible
    # Euler order is 6. Its residues are negatives of the order-3 residues.
    loss=Fraction(1);high=Fraction(1);m=1
    for t in range(1,e+1):
        m*=13
        for x,nx in zip(lifts(t),lifts(t+1)):
            for r,nn,o in ((x,nx,3),(m-x,13*m-nx,6)):
                if r==nn or r%2==0 or r in BAN:continue
                # Composites discarded only on exhibiting a divisor or failed
                # Fermat test. Deficits from any retained composite are harmless.
                if r<3 or any(r!=z and r%z==0 for z in SMALL) or pow(2,r-1,r)!=1:continue
                d=Fraction(m*m,r*r)
                if o==3 and d>1:loss*=d
                if r%4==1: high=max(high,Fraction(m*m,r**5))
    return loss,high

@cache
def price(r,m):
    '''Even unassigned power r^f >= sale * 13^(2 cost) if sale>1.
    Otherwise its possible deficit is charged to the global loss once.'''
    o=1
    while pow(r,o,P)!=1:o+=1
    if o%2==0:return r**m
    t=0 if o==1 else val(r**o-1,P)
    f=m;best=Fraction(r**m)
    while True:
        b=(t+val(f+1,P)) if (f+1)%o==0 else 0
        best=min(best,Fraction(r**f,P**(2*b)))
        # LTE gives denominator <=13^(2t)*(f+1)^2; envelope increases.
        if r**f>=best*P**(2*t)*(f+1)**2:return max(Fraction(1),best)
        f+=2

def floor_sum(n,m,a,b):
    '''sum_{i=0}^{n-1} floor((ai+b)/m); transpose under the line.'''
    acc=0;sign=1
    while n:
        q,a=divmod(a,m);r,b=divmod(b,m);acc+=sign*(q*n*(n-1)//2+r*n)
        top=(a*(n-1)+b)//m
        if not top:break
        # Every height y=1,...,top has n-ceil((ym-b)/a) columns.
        acc+=sign*n*top
        n,m,a,b,sign=top,a,m,m-b+a-1,-sign
    return acc

def actual_factor(n,c,z,T,l,h):
    '''No false negatives for n=r^c*u, r=z mod T, l<=r<=h.'''
    if l>h:return False
    first=l+(z-l)%T
    if first>h:return False
    if h-first<16*T:return any(n%r**c==0 for r in range(first,h+1,T))
    w=n*pow(z,-c,T)%T; low_u=(n+h**c-1)//h**c; last_u=n//l**c
    first_u=low_u+(w-low_u)%T
    if first_u>last_u:return False
    if last_u-first_u<16*T:
        for u in range(first_u,last_u+1,T):
            if n%u:continue
            r=nth(n//u,c)
            if r**c*u==n and l<=r<=h and r%T==z:return True
        return False
    # Expand first and first_u directly (shifted box). n-r^c*u must vanish
    # mod T^2; i,j from zero at lower-left corner. z^c, unlike c, is a unit.
    count_i=(h-first)//T+1;count_j=(last_u-first_u)//T+1
    if count_j>=T:return True
    zc=pow(first,c,T*T);v=pow(zc,-1,T);rhs=((n-zc*first_u)%(T*T))//T
    a=(-c*pow(first,c-1,T)*first_u*v)%T;b=rhs*v%T
    return floor_sum(count_i,T,a,b)>floor_sum(count_i,T,a,b-count_j)

def boxes(n,c,z,T,lo,hi):
    while lo<=hi:
        h=min(hi,2*lo-1)
        if actual_factor(n,c,z,T,lo,h):return True
        lo=h+1
    return False

@cache
def crt(a,m,b,n):
    g=math.gcd(m,n)
    if (b-a)%g:return None
    t=n//g
    k=((b-a)//g)*pow(m//g,-1,t)%t
    return (a+k*m)%(m*t),m*t

@cache
def emitter_classes(h,f,b):
    j=b-val(f+1,P)
    if j<=0:return ((1,2*h),)
    # Ordinary f even; all principal residues other than 1 have order 3.
    # r=1 mod 13 cannot supply b>v13(f+1).
    if (f+1)%3:return ()
    return tuple(x for a in lifts(j) if (x:=crt(a,P**j,1,2*h)) is not None)

def test(e,extra,outer=False):
    assert 0<e<1000 and e%2==0
    require(len(set(extra))==len(extra) and all(prime(r) for r in extra),'invalid witness')
    pe=P**e;A=sg(P,e); C=A;known=[];M=pe*A;U,D=profile(e); V=Fraction(pe**3,U);maxj=maxv=1
    # Account for ALL small forced primes, not only listed extras.
    for r in sorted(set(SMALL)|set(extra)):
        if C%r:
            require(r not in extra,'not a divisor of sigma');continue
        c=val(C,r);C//=r**c;f=c+c%2
        while any(sg(r,f)%z==0 for z in BAN):f+=2
        j=r**(f-c);v=price(r,f);known.append((r,c,j,v));M*=j;V*=v;maxj=max(j,maxj);maxv=max(v,maxv)
    cs=[(h,math.gcd(C,cyc(h))) for h in range(3,e+2,2) if (e+1)%h==0]
    require(math.prod(n for h,n in cs)==C and math.gcd(C,e+1)==1,'uncertain primitive blocks')
    cs=[(h,n) for h,n in cs if n>1]
    # High Euler: generic cost; alternatively restore at most one forced sale
    # and parity premium when Euler prime is among them.
    elig=[(r,c,j,v) for r,c,j,v in known if r%4==1]
    high=pe**3>B*U*D or M>B*max([1]+[j for _,_,j,_ in elig]) or V>B*D*max([1]+[v for _,_,_,v in elig]);stats=Counter()
    if not high:return False,{'first':'high'}
    for s in range(e+1):
        Y=P**s;Q=max(5,2*Y-1);T=B*Y*Y
        for r,c,j,v in elig:
            if c==1 and val(r+1,P)==s and M<=B*j and V*r<=T*v:return False,{'first':['q-known',s,r]}
        if V*Q>T or M>B:stats['size-price']+=1;continue
        hi=T//V
        for h,n in cs:
            # Internal q: requires q=1 mod 4, q=1 mod 2h, q=-1 mod Y.
            # If Y=1, the last congruence is vacuous, not q=12 mod 13.
            cmod=crt(1,math.lcm(4,2*h),-1,Y)
            if cmod is not None and boxes(n,1,*cmod,Q,min(n,hi)):return False,{'first':['q-internal',s,h]}
        if M*Q>B:stats['external-size']+=1;continue
        b=0
        while 2*V*Q*Q>3*T*maxv*P**b:b+=1
        if b>e-s:stats['source-price']+=1;continue
        if 2*M*Q*Q*P**b<=3*B:
            if not outer:return False,{'first':['emitter-outside',s,b]}
            outside_b=b
            while 2*V*Q*Q>3*T*P**outside_b:outside_b+=1
            budget=B//(M*Q);f=2
            while outside_b<=e-s and 3**f<=budget:
                l=max(3,nth(2*Q*P**outside_b//3,f)+1);h=nth(budget,f)
                if l<=h:
                    for z,Z in emitter_classes(1,f,outside_b):
                        start=l+(z-l)%Z
                        for r in range(start,h+1,Z):
                            if r>=start+32*Z:return False,{'first':['outer-progression',s,outside_b,f]}
                            if r in BAN or r==P or A%r==0:continue
                            if any(r!=w and r%w==0 for w in SMALL) or pow(2,r-1,r)!=1:continue
                            u=sg(r,f);j=val(u,P)
                            if j<outside_b or j>e-s or any(u%w==0 for w in BAN):continue
                            u//=P**j; qz,qT=crt(1,4,-1,Y)
                            if boxes(u,1,qz,qT,Q,min(u,B//(M*r**f))):return False,{'first':['outer-prime',s,outside_b,f]}
                f+=2
        room=B*maxj//(M*Q);need=(2*Q*P**b)//3;gap=Y*Q//(max(pe*P,Q)*(pe*P//Y+4))
        for r,c,j,v in known:
            f=c+c%2
            while r**(f-c)<=room:
                if r**f>need and r**(f-c)>gap:
                    z=sg(r,f);qz,qT=crt(1,4,-1,Y)
                    if val(z,P)>=b and boxes(z,1,qz,qT,Q,min(z,B//(pe*A))):return False,{'first':['emitter-known',s,r,f,b]}
                f+=2
        # enumerate g=f-c first. For fixed g derive min r before enumerating c.
        g=0
        while 10001**g<=room:
            if g or gap==0:
                gl=max(10001,nth(gap,g)+1 if g else 10001);gh=nth(room,g) if g else C
                if gl<=gh:
                    for h,n in cs:
                        c=1 if g%2 else 2
                        while gl**c<=n:
                            f=c+g;lo=max(gl,nth(need,f)+1);hi=min(gh,nth(n,c))
                            if lo<=hi:
                                for z,Z in emitter_classes(h,f,b):
                                    if boxes(n,c,z,Z,lo,hi):return False,{'first':['emitter-rough',s,b,h,c,g]}
                            c+=2
            g+=1
        stats['source-empty']+=1
    return True,dict(stats)

def fixtures():
    rng=Random(386)
    for _ in range(2000):
        n=rng.randrange(100);m=rng.randrange(1,91);a=rng.randrange(-123,123);b=rng.randrange(-123,123)
        assert floor_sum(n,m,a,b)==sum((a*i+b)//m for i in range(n))
        z=rng.randrange(1,30);T=rng.randrange(2,70)
        if math.gcd(z,T)>1:continue
        c=rng.randrange(1,6);r=z+T*rng.randrange(30,500);u=rng.randrange(100,100000);C=r**c*u
        assert actual_factor(C,c,z%T,T,rng.randrange(1,r+1),rng.randrange(r,2*r+1))
    for j in range(1,20):assert all((z*z+z+1)%P**j==0 for z in lifts(j))
    print('fixtures pass',flush=True)

if __name__=='__main__':
    require(__debug__,'run without -O');ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--scan',nargs='+',type=int);ap.add_argument('--fixture',action='store_true');ap.add_argument('--outer',action='store_true',help='probe outside-source prime progression');ap.add_argument('--extra',nargs='*',type=int,default=[]);args=ap.parse_args()
    if args.fixture:fixtures()
    start=time.monotonic();rows=[]
    for e in (args.scan or sorted(TARGET,reverse=True)):
        ok,why=test(e,list(set(TARGET.get(e,()))|set(args.extra)),outer=args.outer);rows.append((e,ok));print(e,'CLOSED' if ok else 'OPEN',why,'seconds',round(time.monotonic()-start,2),flush=True)
    if not args.scan:require(all(ok for _,ok in rows),'target not proved')
