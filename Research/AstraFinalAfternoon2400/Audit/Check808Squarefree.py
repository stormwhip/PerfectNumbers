"""Independent all-class lattice and conditional factor-count proof for 7^808."""
from fractions import Fraction
from hashlib import sha256
from math import comb,gcd,isqrt,prod
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from Check7x808 import A,B,X,isprime
# Separate field Euclid implementation, shared with independent root11 arithmetic.
from Check11x48Price import poly_gcd
L,F=1618,65537


def roots(o,depth):
    ds=[d for d in range(1,o) if o%d==0]
    g=next(z for z in range(2,7) if pow(z,o,7)==1 and all(pow(z,d,7)!=1 for d in ds))
    m=7
    for _ in range(depth):
        assert pow(g,o,m)==1
        rr={pow(g,i,m) for i in range(1,o) if gcd(i,o)==1}
        assert all(r>0 for r in rr)
        yield m,rr
        m*=7;g=pow(g,7,m)


def lattice():
    dpath=H.parent/'Root808/Lattice1-227.json.gz'
    raw=dpath.read_bytes(); d=json.loads(gzip.decompress(raw)); assert (d['depth'],d['multiplicity'])==(227,1)
    m,rr=list(roots(3,227))[-1]; period=L*m
    assert gcd(A,period)==1
    # Preserve the source packet's coordinate indexing by first matching the
    # mod-7 residues 2 and 4; rewrite the CRT using its opposite inverse.
    ordered=[next(a for a in rr if a%7==x) for x in (2,4)]
    direct=[1+L*((r-1)*pow(L,-1,m)%m) for r in ordered]
    classes=direct+[A*pow(r,-1,period)%period for r in direct]
    assert len(set(classes))==4 and all(1<r<period and A%r for r in classes)
    bands=d['bands']
    bound=isqrt(A)
    for lo,hi,k,n in bands:
        assert hi==bound and 1<lo<=hi and 1<=k<n<=64
        bound=lo-1
    assert bound==min(classes)-1
    # Determine required certificate keys by intersecting exact class windows
    # with the actual segment, separately from the source's broader high-only
    # obligation. Extra witnesses for segments with no class point are harmless.
    needed=set(); conservative=set(); actual=set(); empty=0
    for i,r in enumerate(classes):
        for j,(lo,hi,k,n) in enumerate(bands):
            upper=(hi-r)//period
            reach=max(1,(lo-r+period-1)//period)
            if reach<=upper:needed.add((i,j))
            if upper>=1:conservative.add((i,j))
            else:empty+=1
    for i,j,v,w in d['w']:
        assert (i,j) in conservative and (i,j) not in actual
        actual.add((i,j))
        r=classes[i]; lo,hi,k,n=bands[j]; horizon=(hi-r)//period
        shift=r*pow(period,-1,A)%A; shift-=A if 2*shift>A else 0
        ps=[]
        for coeff in (v,w):
            assert len(coeff)==n and all(type(x)==int for x in coeff)
            poly=[0]*n
            for ell,a in enumerate(coeff):
                e=min(ell,k); z=a*A**(k-e)
                for j0 in range(e+1):poly[ell-e+j0]+=z*comb(e,j0)*shift**(e-j0)
            assert sum(abs(x)*horizon**l for l,x in enumerate(poly))<lo**k
            ps.append(poly)
        assert poly_gcd(*ps)
    assert needed<=actual==conservative
    print('PASS independent all contiguous lattice bands',len(bands), 'witnesses',len(actual),'nonempty exact cells',len(needed),'SHA256',sha256(raw).hexdigest(),flush=True)


def mass():
    tab={}
    for m,rs in roots(3,808):
        for r in rs:
            if r>=3 and r%2 and r!=19 and all(pow(x,r-1,r)==1 for x in (2,3,5) if x<r):
                tab[r]=max(tab.get(r,1),Fraction(m*m,r*r))
    U=prod(tab.values()); assert U<579125
    for o in (2,3,6):
        for m,rs in roots(o,808):
            for r in rs:
                if r>=5 and r%4==1 and r!=19 and all(pow(x,r-1,r)==1 for x in (2,3,5) if x<r):
                    assert r**5>=m*m
        assert all(o*7**i-6>=6*i for i in range(1,5))
    assert 3**5030<=B<3**5031 and 3**6>=7**2 and 7**5>5031
    assert X*A*A*7**(2*(808-235))>B*U
    for s in range(809):
        assert X*A*A*max(5,2*7**s-1)*7**(2*max(0,808-235-s))>B*U
    assert X**2*A**2*7**(2*(808+808-230))>(B*U)**2
    print('PASS all 809 linear-external allocations, high Euler and linear-internal',flush=True)


if __name__=='__main__':
    assert __debug__ and isprime(809) and isprime(F)
    assert gcd(A,42*809)==1 and pow(2,A-1,A)!=1 and pow(A,3,49)!=1
    lattice();mass()
