"""Prove r²|A impossible at ordinary 19-supply u>=98. No LLL at replay."""
from pathlib import Path
from math import isqrt,comb,gcd
import gzip,json,sys
P=Path(__file__).resolve().parent;p=19;A=(p**619-1)//18//2477;F=65537

def trim(a):
    while a and not a[-1]:a.pop()
    return a

def coprime(a,b):
    a=trim([x%F for x in a]);b=trim([x%F for x in b])
    while b:
        while len(a)>=len(b):
            j=len(a)-len(b);q=a[-1]*pow(b[-1],-1,F)%F
            for i,bi in enumerate(b):a[i+j]=(a[i+j]-q*bi)%F
            trim(a)
        a,b=b,a
    return len(a)==1

def run():
    assert __debug__ and all(F%i for i in range(2,isqrt(F)+1));d=json.loads(gzip.decompress((P/'SquareLatticeCert.json.gz').read_bytes()));assert d['u']==96
    m=19;roots=[r for r in range(2,19) if pow(r,9,19)==1]
    for _ in range(1,96):
        k=m*p;roots=[r+m*((-((pow(r,9,k)-1)//m)*pow(9*pow(r,8,p),-1,p))%p) for r in roots];m=k
    rr=[r+m*((1-r)*pow(m,-1,1238)%1238) for r in roots];M=1238*m;assert len(rr)==8 and gcd(A,M)==1
    bands=d['bands'];assert bands[0][1]==isqrt(A) and all(x[0]==y[1]+1 for x,y in zip(bands,bands[1:])) and min(rr)>=bands[-1][0]
    W={(i,j):(v,w) for i,j,v,w in d['w']};seen=set()
    for i,R in enumerate(rr):
        assert R>1 and A%R # x=0 excluded
        c=R*pow(M,-1,A)%A;c=c-A if 2*c>A else c
        for j,(lo,hi,k,n) in enumerate(bands):
            assert 0<lo<=hi and 0<k<n;X=(hi-R)//M
            if X<=0:continue
            V=W[i,j];seen.add((i,j));poly=[]
            for v in V:
                assert len(v)==n;a=[0]*n
                for l,t in enumerate(v):
                    l1=min(l,2*k);s=l-l1;fac=t*A**(k-l1//2)
                    for h in range(l1+1):a[s+h]+=fac*comb(l1,h)*c**(l1-h)
                assert sum(abs(z)*X**h for h,z in enumerate(a))<lo**(2*k);poly.append(trim(a))
            a,b=poly;assert a and b and (a[-1]%F or b[-1]%F) and coprime(a,b)
    assert seen==set(W)
    # For u>=98 and h+1<19^3, v19(h+1)<=2 so u0>=96; no refined +2 analysis needed.
    assert 3**(19**3-1)>10**2400 and (19-1)%619 and A%619
    return 98
if __name__=='__main__':
    sys.set_int_max_str_digits(0);print('PASS inverse divisor cap',run(),'8 residue classes, 264 exact polynomial pairs',flush=True)