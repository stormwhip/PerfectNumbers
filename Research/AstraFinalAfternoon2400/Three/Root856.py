"""Integer-only (3,856), conditional E3 exterior/interior emitter window.
Proof uses primitive emitter result of frozen Source/SourceSquare.md, or independently
checks it in full below. No factor data, arbitrary precision floats or external imports.
"""
from math import isqrt
from fractions import Fraction as F
from functools import cache
from hashlib import sha256
from itertools import accumulate
from sys import argv
from subprocess import run as subrun
from pathlib import Path

B=10**2400; E=856; X=3**E; W=3*X; A=(W-1)//2; BAN=(7,11,13,19,31)
R=1+1714*58_400_000+1

def range_receipt(exe):
    p=subrun([str(Path(exe).resolve()),'3','857','58400000'],text=True,capture_output=True,check=True)
    assert p.stdout.strip()=='PASS 3 857 58400000 100097600001 2673408',p.stdout

def primes(n):
    s=bytearray([1])*(n+1);s[:2]=b'\x00\x00'
    for p in range(2,isqrt(n)+1):
        if s[p]:s[p*p::p]=b'\0'*((n-p*p)//p+1)
    return [p for p in range(2,n+1) if s[p]]

def geom(r,h):return (r**(h+1)-1)//(r-1)
def floor_pow(n,p):
    lo,hi=0,n.bit_length()
    while lo+1<hi:
        m=(lo+hi)//2
        if p**m<=n:lo=m
        else:hi=m
    return lo

@cache
def tariff():
    # Exact mass lower on all chosen ordinary supplier prime powers.
    lim=15000;K=lim**2;items=[]
    for p in primes(lim):
        if p in BAN or p%3!=1:continue
        k=1;last=0
        while True:
            now=3**k-1;marginal=p**(now-last)
            if marginal>=K or any(geom(p,now)%b==0 for b in BAN):break
            items.append(marginal);k+=1;last=now
    vals=sorted(items+[K]*E)[:E]
    return [1,*accumulate(vals,int.__mul__)]

@cache
def primitive():
    assert all(p in BAN or geom(p,2)%7==0 for p in primes(42) if p%3==1)
    assert 43**(3**7-1)>B
    M=tariff()
    assert all(X*M[E-s]>B for s in range(1,9)) and 2*3**9-1>B.bit_length()+1
    checked=[]
    for s in range(9,E+1):
        q=2*3**s-1
        for b in range(min(6,E-s)+1):
            f=max(43**(3**b-1),(43 if b else 5)**2*(2*q)**3//27)
            low=max(X*q*f*M[E-s-b],(X//3**b)*f*f)
            assert low>B,(s,b)
            checked.append(low)
    return len(checked),len(str(min(checked)))-1

@cache
def block():
    assert 857 in primes(857)
    assert A%857!=0 and A%3 and A%2 and isqrt(A)**2!=A
    assert all(A%p for p in range(2*857+1,20_000_001,2*857))
    return floor_pow(A,R)

SMALL=tuple(primes(600))

@cache
def lower_euler(y,tag):
    # Odd m with m mod 3=tag; true q=2*y*m-1. All skipped candidates
    # violate bans in m or q or small-factor primality.
    j=1 if tag==1 else 5
    for m in range(j,j+6*28,6):
        q=2*y*m-1
        if any(m%b==0 or q%b==0 for b in BAN):continue
        if q>1000 and any(q%p==0 for p in SMALL):continue
        return q
    return 2*y*(j+6*28)-1

@cache
def three_factor_price():
    lim=15000;K=(lim*lim+lim+1)//3;items=[]
    for r in primes(lim):
        if r in BAN or r%3!=1:continue
        z=r
        while True:
            g=z*z+z+1
            if any(g%b==0 for b in BAN) or g//3>=K:break
            items.append(g//3);z=z**3
    return [1,*accumulate(sorted(items+[K]*E)[:E],int.__mul__)]

def run():
    assert __debug__
    print('primitive',primitive(),'rough max prime count',block(),flush=True)
    M=tariff();T=three_factor_price();remain={0:set(),1:set()}
    RR=[R**(2*i) for i in range(E+1)]; VA=[max(A*R,v) for v in RR]
    for s in range(9,E+1):
        y=3**s;k=E-s
        # Uniform bound excluding already before the source's support split.
        if X*M[k]>B:continue
        for tag in (1,2):
            q=lower_euler(y,tag)
            # Multiply odd divisor sums, not merely their supports. All selected
            # Phi_(3^j)(r)/3 factors are coprime to 3 and q, because q=2 mod3.
            if X*A*q*T[k]>B or 2*X*q*q*M[k]>3*B:continue
            # Interior balancing: r^(f-v_r(A)) > y*q/(max(W,q)*(W/y+4)).
            den=max(W,q)*(W//y+4);Q=y*q; S=X*q
            ext=False;inside=False
            for i in range(k+1):
                room=S*M[k-i]; V=VA[i]
                if 2*q*room*V<=3*B:ext=True
                if (room*V<=B and room*A*Q<=B*den and
                    2*q*room*RR[i]<=3*B and room*RR[i]*Q<=B*den):inside=True
                if ext and inside:break
            if ext:remain[0].add((s,tag))
            if inside:remain[1].add((s,tag))
    for role in (0,1):
        ss=sorted(remain[role]);print('source','external' if role==0 else 'internal','left',len(ss),'s-range',min(s for s,t in ss),max(s for s,t in ss),'tag counts',[(t,sum(z==t for s,z in ss)) for t in (1,2)],'sha256',sha256(repr(ss).encode()).hexdigest(),flush=True)
    return remain
if __name__=='__main__':
    if len(argv)!=2:raise SystemExit('Usage: Root856.py VERIFIED_RANGE_BINARY (compile Range.cpp first)')
    range_receipt(argv[1]);run()
