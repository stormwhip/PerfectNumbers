"""Exact Euler/ordinary-source bounds for anonymous root-three atoms."""
from Explore import CASES
from Prices import *
from CleanPrice import price2
from hashlib import sha256
from sys import argv
from time import monotonic

@cache
def certificate(rows):
    fixed,odd,X,S,D,blocks=get_context(rows)
    spec=[(p,h+1,b) for (p,h),a in zip(rows,[sig(p,h)//(1+h%2) for p,h in rows]) if (b:=a//prod(t**vp(a,t) for t in fixed))>1]
    assert [b for p,o,b in spec]==blocks and prod(blocks)==D
    assert all(gcd(a,b)==1 for j,a in enumerate(blocks) for b in blocks[j+1:])
    R=20_000_001
    for p,o,b in spec:
        assert prime(o) and gcd(b,2*o*p*(p-1))==1 and sig(p,o-1)%b==0
        assert all(b%d for d in range(2*o+1,R,2*o))
        assert isqrt(b)**2!=b
    return R,fixed,odd,X,S,D,spec

def cd(n,d):return (n+d-1)//d

def first_not_rejected(q,mod,spec):
    # Only skip demonstrably impossible positives: q=1 mod4, u=(q+1)/2
    # has no forbidden prime, and q is prime. Do not count this as primality.
    for _ in range(50):
        if q>=5 and all(((q+1)//2)%b for b in BAN) and all(q==p or q%p for p in SMALL):
            # A large pow is unnecessary once the preliminary filter accepts.
            return q
        q+=mod
    return q

def inside_euler(a,m,b):
    c=b*pow(a,-1,4*m)%(4*m) or 4*m; hi=b//max(a,5)
    if c>hi:return False
    if (hi-c)//(4*m)>64:return True
    return any(b%x==0 for x in range(c,hi+1,4*m))

def min_additional_abundance_lower(X,S,D,R,q):
    assert S%2==1
    l=0;n=1
    while n*R<=D:n*=R;l+=1
    ratio=F(S,X)*F(R,R-1)**l*F(q,q-1)
    # Free Euler case: all fixed exponents even, S is sigma(X).
    mass=1
    for p in (5,17,23,29,37,41,43,47,53,59,61,67,71,73):
        ratio*=F(p,p-1)
        if ratio>=2:return mass
        mass*=p**2
    return mass

def run(k,weights):
    rows=CASES[k];R,fixed,odd,X,S,D,spec=certificate(rows)
    assert not odd and set(weights)<= {2}
    targets=tuple((p,w) for (p,h),w in zip(rows[1:],weights));Q=[p for p,w in targets]
    V,E=price2(rows,Q[0]) if len(Q)==1 else price(rows,targets)
    V=F(V);cs=[fixed[p]-vp(S,p) for p in Q];L=len(spec)
    stats={}; remain=[];outcomes=[]
    for ls in product(*(range(c+1) for c in cs)):
        m=prod(p**i for p,i in zip(Q,ls));a=2*m-1;q=first_not_rejected(a,4*m,spec);W=m*m
        tag=None
        if V*q>B*W:tag='price'
        elif X*D*q>B:tag='mandatory'
        elif not any(inside_euler(a,m,b) for p,o,b in spec):
            # Every block needs a parity copy >=R. With q outside D,
            # if the emitter is in one block, price the other parities only.
            # If the emitter is exterior, can price all block parities.
            F0=min_additional_abundance_lower(X,S,D,R,q)
            if X*D*q*R**L*F0>B:tag='parity'
            else:
                cut_all=True;budget=None;details=[]
                for p,o,b in [*spec,(0,0,1)]:
                    # Ignore support extras here to avoid possibly overlapping the emitter.
                    # G is the maximal possible paid mass of its own block, others contribute parity R.
                    G=b;O=R**(L-(p!=0)); Y=2*q
                    i0=next((i for i,z in enumerate(Q) if z==p),None)
                    # Separate first price and the cofactor-bound mass; independent bound on the same N.
                    if 4*V*X*D*O*q**4>9*W*G*B**2:
                        details.append((p,'product'));continue
                    if p and i0 is not None and ls[i0]>0:
                        # Balance with W=p^o, Y=p^i; increase q in e/max(W,e).
                        Zi=p**ls[i0];K=p**o
                        if X*D*O*q*q*Zi>B*max(K,q)*(K//Zi+4):
                            details.append((p,'balance'));continue
                    cut_all=False;details.append((p,'open'))
                if cut_all:tag='emitter'
        if tag is None:remain.append(ls)
        else:stats[tag]=stats.get(tag,0)+1
        outcomes.append((ls,tag or 'open'))
    print(k,'high-Euler-excluded',V>B,'V floor',floor10(V),'losses',len(E),'counts',stats,'left',len(remain),'range',remain[:4],remain[-4:], 'sha256',sha256(repr(outcomes).encode()).hexdigest(),flush=True)
    return V,stats,remain
if __name__=='__main__':run(argv[1],tuple(map(int,argv[2].split(','))))
