"""Rebuild every Euler and lattice progression at canonical (11,48), t^36."""
from functools import cache
import gzip
from hashlib import sha256
import json
from math import comb, gcd, isqrt
from pathlib import Path
import sys

F=Path(__file__).resolve().parent
sys.path.insert(0,str(F))
from Check7x808 import floorroot
H=F.parent/'ElevenThirteen'
B=10**2400
P,T=11,100641220283951395639601683
X=P**48*T**36
A=sum(P**i for i in range(49))//T
D=sum(T**i for i in range(37))
ORD=(3,7,21,49,147)
MOD=65537
R0=10**7+1


def trial(n):
    return n>=2 and all(n%p for p in range(2,isqrt(n)+1))


@cache
def levels(o):
    def split(n):
        return [p for p in range(2,n+1) if n%p==0 and trial(p)]
    q=2
    while True:
        g=pow(q,(T-1)//o,T)
        if g and all(pow(g,o//p,T)!=1 for p in split(o)):
            break
        q+=1
    power=T
    roots=[pow(g,k,T) for k in range(1,o) if gcd(o,k)==1]
    S=[]
    for i in range(35):
        assert len(set(roots))==sum(gcd(o,k)==1 for k in range(o)) and all(0<r<power and pow(r,o,power)==1 for r in roots)
        S.append((power,roots))
        power*=T
        roots=[pow(r,T,power) for r in roots]
    return S


def possible(b):
    return b>=3 and b%2 and b not in (7,19,P,T) and ((lambda c:c*c==b)(isqrt(b))
                or (all(b==p or b%p for p in SMALL) and pow(2,b-1,b)==1))


def poly_gcd(A,B):
    def cut(v):
        while v and not v[-1]: v.pop()
        return v
    a,b=[cut([u%MOD for u in vec]) for vec in (A,B)]
    while b:
        inv=pow(b[-1],-1,MOD)
        while len(a)>=len(b):
            d=len(a)-len(b)
            c=a[-1]*inv%MOD
            for i,x in enumerate(b):
                a[d+i]=(a[d+i]-c*x)%MOD
            cut(a)
        a,b=b,a
    return len(a)==1


def cert(c,R,M,hi,data,used):
    key=sha256(repr((c,R,M,hi)).encode()).hexdigest()
    k,n,*ab=data[key]
    assert c>=2 and 1<=k<=10 and k+1<=n<=30 and gcd(M,D)==1
    Y=(hi-R)//M
    assert Y>=1 and len(ab)==2
    xc=R*pow(M,-1,D)%D
    if 2*xc>D:xc-=D
    out=[]
    for vec in ab:
        assert len(vec)==n and all(type(t)==int for t in vec)
        p=[0]*n
        for j,v in enumerate(vec):
            t=min(j,c*k)
            factor=v*D**(k-t//c)
            for z in range(t+1):
                p[j-t+z]+=factor*comb(t,z)*xc**(t-z)
        assert sum(abs(a)*Y**j for j,a in enumerate(p))<R**(c*k)
        out.append(p)
    assert poly_gcd(*out)
    used.add(key)


def main():
    assert __debug__ and trial(MOD) and trial(37)
    assert 3**5030<=B<3**5031 and (T-1)%37!=0 and gcd(D,37*P*T*A)==1
    assert sum(P**i for i in range(49))==A*T and A%T
    assert T%4==3 and (T-1)%294==0 and tuple(o for o in range(3,5032,2) if (T-1)%o==0)==ORD
    for o in ORD:
        for m,rs in levels(o):
            for r in rs:
                # Treat all candidate squares conservatively, including composite squares.
                # Primality of r need not be proved for upper-bounding deficit.
                if possible(r) and pow(r,o,m*T)!=1:
                    assert r**(o-1)>=m*m
    for b in range(75,R0,74):
        if pow(T,37,b)==1:
            assert D%b!=0
    pairs=[]
    for i in range(36):
        y=T**i; q=max(5,2*y-1); rest=T**(35-i)
        if X*q*rest**2>B:
            continue
        # This proof's remaining windows require positive i, hence q is
        # outside D by reciprocity; A exteriority follows by direct size.
        assert i>0 and q>A
        if X*A*D*q>B:
            continue
        for j in range(36-i):
            if 2*X*A*D*q*q*T**j>3*B*max(A,D) or 2*X*q*q*rest**2>3*B*T**j:
                continue
            pairs.append((i,j))
    assert pairs==[(16,j) for j in range(16,20)]+[(17,j) for j in range(16,19)]
    name=H/'Price48Depth.json.gz'
    packet=name.read_bytes(); data=json.loads(gzip.decompress(packet)); used=set()
    for i,j in pairs:
        q=2*T**i-1;y=T**j; M0=2*X*A*D*q*q*y
        assert 2*X*D*q*q*y>3*B and j>0
        maxf=B//(X*A*q)
        maxextra=B//(X*A*D*q)
        h=2
        while R0**h<=maxf:
            for c in range(1,h+1):
                if R0**c>D:
                    break
                low=max(R0,floorroot((M0-1)//(3*B),c)+1,floorroot((2*q*y-1)//3,h)+1)
                high=min(floorroot(D,c),floorroot(maxf,h))
                if c<h:high=min(high,floorroot(maxextra,h-c))
                if low>high:
                    continue
                for o in ORD:
                    if (h+1)%o:
                        continue
                    m,roots=levels(o)[j-1]
                    mod=74*m
                    for r in roots:
                        candidate=(r+m*((1-r)*pow(m,-1,74)%74))%mod
                        R=low+(candidate-low)%mod
                        if R>high:
                            continue
                        if R+mod>high:
                            assert D%R**c!=0
                        else:
                            cert(c,R,mod,high,data,used)
            h+=2
    assert used==data.keys() and len(used)==6
    print('PASS independently rebuilt full h/c/CRT cover (11,48), t^36;',len(pairs), 'relaxed Euler pairs and',len(used),'lattice cells',sha256(packet).hexdigest(),flush=True)


if __name__=='__main__':
    SMALL=[p for p in range(3,98,2) if trial(p)]
    main()
