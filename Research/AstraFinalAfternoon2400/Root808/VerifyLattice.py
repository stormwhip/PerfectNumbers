"""Exact standard-library verifier of the two divisor-depth caps for Phi_809(7)."""
import gzip
from hashlib import sha256
from itertools import combinations
import json
from math import gcd, isqrt
from pathlib import Path

A=(7**809-1)//6
F=65537
L=1618
H=Path(__file__).resolve().parent


def coprime_mod(a,b):
    def norm(poly):
        poly=[v%F for v in poly]
        while poly and not poly[-1]:poly.pop()
        return poly
    a,b=norm(a),norm(b)
    if not a or not b or a[-1]==0 or b[-1]==0:return False
    while b:
        while len(a)>=len(b):
            q=a[-1]*pow(b[-1],-1,F)%F
            j=len(a)-len(b)
            for i,v in enumerate(b):a[i+j]=(a[i+j]-q*v)%F
            while a and not a[-1]:a.pop()
        a,b=b,a
    return len(a)==1


def run(depth,mult):
    raw=(H/f'Lattice{mult}-{depth}.json.gz').read_bytes()
    d=json.loads(gzip.decompress(raw));assert set(d)=={'bands','depth','multiplicity','w'}
    assert (d['depth'],d['multiplicity'])==(depth,mult)
    mod=7;rr=[2,4]
    for j in range(1,depth):
        nxt=mod*7
        rr=[r+k*mod for r in rr for k in range(7) if ((r+k*mod)**2+(r+k*mod)+1)%nxt==0]
        assert len(rr)==2
        mod=nxt
    w=L*mod; assert gcd(A,w)==1
    rr=[r+mod*((1-r)*pow(mod,-1,L)%L) for r in rr]
    if mult==1:
        rr += [A*pow(r,-1,w)%w for r in rr]
    assert min(rr)>1 and len(set(rr))==len(rr) and all(r<w and A%r for r in rr)
    bands=d['bands'];assert bands and bands[0][1]==isqrt(A) and bands[-1][0]==min(rr)
    assert all(x[0]==y[1]+1 for x,y in zip(bands,bands[1:]))
    assert all(1<=lo<=hi and 1<=k<n<=64 for lo,hi,k,n in bands)
    expected={(i,j) for i,r in enumerate(rr) for j,(_,hi,_,_) in enumerate(bands) if r+w<=hi}
    seen=set()
    for i,j,row,other in d['w']:
        assert (i,j) in expected and (i,j) not in seen
        seen.add((i,j)); r=rr[i]; lo,hi,k,n=bands[j]; high=(hi-r)//w
        c=r*pow(w,-1,A)%A;c-=A if 2*c>A else 0
        base=[]; power=[1]
        for t in range(n):
            e=min(t,mult*k)
            if e==len(power):power=[c*power[0],*[power[l-1]+c*power[l] for l in range(1,e)],1]
            assert len(power)==e+1
            base.append([0]*(t-e)+[x*A**(k-e//mult) for x in power]+[0]*(n-1-t))
        fs=[]
        for v in (row,other):
            assert len(v)==n and all(type(t)==int for t in v)
            f=[sum(x*y for x,y in zip(v,col)) for col in zip(*base)]
            assert sum(abs(x)*high**e for e,x in enumerate(f))<lo**(mult*k)
            # Any common integer root would reduce to a common root
            # mod F, regardless of any degree drop on reduction.
            fs.append(f)
        assert coprime_mod(*fs)
    assert seen==expected
    print('PASS divisor multiplicity',mult,'depth',depth,'complete intervals',len(bands),'pairs',len(seen),'SHA256',sha256(raw).hexdigest())

if __name__=='__main__':
    assert __debug__
    assert all(F%i for i in range(2,isqrt(F)+1)) and all(809%i for i in range(2,isqrt(809)+1))
    assert A%809 and gcd(A,42)==1 and pow(2,A-1,A)!=1
    run(227,1)
