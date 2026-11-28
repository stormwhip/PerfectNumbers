"""Independent rare third-target coverage and strict endpoints at the (19,276) source 13."""
from fractions import Fraction
from math import gcd, isqrt, prod
from pathlib import Path
import runpy

H=Path(__file__).resolve().parents[1]
S=44119464395283956806299428681
P,Q=19,13
PREFIX=((19,276),(1176672733,1),(1109,2),(13,276))
B=10**2400
X=prod(p**h for p,h in PREFIX)
Y=prod(sum(p**i for i in range(h+1)) for p,h in PREFIX)//2


def trial(p):
    return p>1 and all(p%d for d in range(2,isqrt(p)+1))


def vp(n,p):
    k=0
    while n%p==0:n//=p;k+=1
    return k


def additive_roots(p,o,limit):
    # Independent all-modulus initial scan for small primes and Hensel digits.
    roots=[r for r in range(2,p) if pow(r,o,p)==1 and all(pow(r,d,p)!=1 for d in range(1,o) if o%d==0)]
    m=p
    for z in range(1,limit+1):
        yield m,roots
        M=m*p
        roots=[r+j*m for r in roots for j in range(p) if pow(r+j*m,o,M)==1]
        m=M


def old_table():
    cg={}; pside={}; qside={}
    a=list(additive_roots(P,3,275)); b=list(additive_roots(Q,3,276)); c=list(additive_roots(P,9,275))
    def add(d,r,num):
        if r<3 or not r%2 or r in dict(PREFIX) or X*r*r>B:return
        den=r**20
        if num>den and all(pow(w,r-1,r)==1 for w in (2,3,5,7,11,13,17) if w<r):
            d[r]=max(d.get(r,1),Fraction(num,den))
    for M,rs in a+c:
        for r in rs:add(pside,r,M**19)
    for N,rs in b:
        for r in rs:add(qside,r,N**19)
    for M,rs in a:
        for N,ts in b:
            J=pow(N,-1,M)
            for r in rs:
                for t in ts:
                    z=t+N*((r-t)*J%M)
                    if z%2 and 20*(z.bit_length()-1)<19*(M*N).bit_length():add(cg,z,(M*N)**19)
    return {z:max(cg.get(z,1),pside.get(z,1)*qside.get(z,1)) for z in set(cg)|set(pside)|set(qside)}


def order_roots(o):
    # Find all roots via a cyclic subgroup; use consecutive powers and filter
    # by prime divisors of o, not the applicant's primitive index list.
    factors=[d for d in range(2,o+1) if o%d==0 and trial(d)]
    for a in range(2,100):
        g=pow(a,(S-1)//o,S)
        if pow(g,o,S)==1 and all(pow(g,o//d,S)!=1 for d in factors):break
    else:raise AssertionError('generator')
    r=1; out=[]
    for _ in range(o):
        if all(pow(r,o//d,S)!=1 for d in factors):out.append(r)
        r=r*g%S
    assert len(out)==sum(gcd(i,o)==1 for i in range(o))
    return out


def rare_table():
    primes=(15539196401,1578110473)
    assert all(map(trial,primes)) and (S-1)%prod(primes)==0 and prod(primes)**2>S
    assert pow(2,S-1,S)==1 and all(gcd(pow(2,(S-1)//p,S)-1,S)==1 for p in primes)
    assert 3**5030<=B<3**5031<S**5031 and gcd(19*13*9,S*(S-1))==1
    assert S>5031 and [o for o in range(3,5032,2) if (S-1)%o==0]==[5,71,277,355,1385,2287]
    X2=X*S*S
    for o in (71,277,355,1385,2287):
        residues=[r if r%2 else r+S for r in order_roots(o)]
        ok=[r for r in residues if X2*r**(o-1)<=B]
        assert ok==[] or o==277 and set(ok)=={13**j for j in range(1,6)} and X2*S**276>B
    roots=order_roots(5);m=S
    for z in range(1,20):
        u=min(r if r%2 else r+m for r in roots)
        if X2*u**4>B:return z
        assert u**80>=S**(77*z)
        # For Teichmueller units of order dividing S−1, raising a
        # representative root to S advances it by one lift level.
        roots=[pow(r,S,m*S) for r in roots];m*=S
        assert all(pow(r,5,m)==1 for r in roots)
    raise AssertionError('rare tail')


def main():
    assert __debug__
    depth=rare_table(); print('Independent rare high orders and 5-lift size cutoff depth',depth,flush=True)
    table=old_table()
    ref=runpy.run_path(str(H/'Nineteen/Net13.py'))
    assert table==ref['loss'](), 'independent compact 19/13 loss table'
    F=(67,967,8311,11621,50627,392233)
    assert all(trial(z) and Y%z==0 and pow(z,5,S)!=1 for z in F) and vp(Y,S)==1
    p,Q=19,13
    C,D=276-vp(Y,p),276-vp(Y,Q)
    C0=C*0+1
    def ratio(q,h):
        g=(q**(h+1)-1)//(q-1)
        i,j=vp(g,p),vp(g,Q)
        if i>C or j>D:return None
        return Fraction(q**(10*h),(p**i*Q**j)**19)*table.get(q,1)
    for q in F:
        ex=2*((vp(Y,q)+1)//2); mass=q**ex
        costs=[]
        while X*mass<=B:
            r=ratio(q,ex)
            if r is not None:costs.append(r)
            ex+=2;mass*=q*q
        assert costs
        C0*=min(costs)
    A=Fraction(X**10*(p**C*Q**D)**19,prod(table.values()))*C0
    h=4; count=0
    while X*S**h<=B:
        z=A*ratio(S,h)
        assert z.numerator**2*S**(77*(h-1)) > B**20*z.denominator**2
        h+=2;count+=1
    assert (count,h)==(29,62)
    print('PASS independent joint loss/explicit credits/rare order coverage;',count,'strict exponent rows; raw tail',h)

if __name__=='__main__':main()
