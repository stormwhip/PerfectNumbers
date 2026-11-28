"""Discovery of lattice certificates for high-depth pivot-source divisors. Verification stdlib."""
from pathlib import Path
from functools import cache
from math import gcd,comb
from hashlib import sha256
import sys,json,gzip
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'FinalNight2400/Nineteen')]
from VerifyLattice import coprime
from PivotPrice48 import P,E,T,B,ORDERS,lifts,require,setup
from Coverage import sigma,prime,domain
from HighLinear import floor_root


@cache
def core():
    # Exact prefix X=(11^48)(T^36); Δ is the only possible large-overlap block.
    f=36;X=P**E*T**f;A=sigma(P,E)//T;D=sigma(T,f)
    require(T%4==3 and prime(37) and D%37!=0 and gcd(A,D)==1 and gcd(D,11*T)==1,'prime-index block')
    require((T-1)%37!=0 and D%74==1,'emitter residue')
    require(36 in domain(P,E)[0] and prime(65537),'original live scope / quotient field')
    return X,A,D


@cache
def rough_trial(D,L):
    return all(D%q for q in range(75,L+1,74))


@cache
def s_cut(i,j):
    X,A,D=core();Q=2*T**i-1;y=T**j
    if 2*X*D*Q**2*y<=3*B:return False
    # A and D are coprime. If r|A, its overlap is <=A, and the above
    # strict inequality already discards it. Thus v_r(D)=c>=1.
    power_lo=(2*X*A*D*Q**2*y+3*B-1)//(3*B)
    maxsz=B//(X*A*Q)
    L=10**7
    if not rough_trial(D,L):return False
    c=0
    while L**(c+1)<=D:
        c+=1
        for o in ORDERS:
            if j<1:continue
            m=T**j;zs=lifts(T,o,j)[-1]
            S=(2*Q*y+2)//3
            for h in range(o-1,5100,2*o):
                if h<c:continue
                if (10**7)**h>maxsz:break
                lo=max(10**7+1,1+floor_root(power_lo-1,c),1+floor_root(S-1,h));hi=min(floor_root(D,c),floor_root(maxsz,h))
                if h>c:hi=min(hi,floor_root(B//(X*A*D*Q),h-c))
                if hi<lo:continue
                hits=[]
                for r in zs:
                    z=1+74*((r-1)*pow(74,-1,m)%m);M=74*m;R=lo+(z-lo)%M
                    if R<=hi:
                        if hi<R+M:
                            if D%R**c:continue
                        elif c>=2 and lattice(D,c,R,M,hi):continue
                        hits.append((R,(hi-R)//M))
                if hits:print('depth residual',i,j,h,c,lo.bit_length(),hi.bit_length(),[(r.bit_length(),v.bit_length()) for r,v in hits],flush=True);return False
    return True


PROOF=H/'Price48Depth.json.gz'
BOOK={};USED=set();DISCOVER=False


def lattice(D,c,R,M,hi):
    K=(hi-R)//M
    require(c>=2 and K>0 and gcd(M,D)==1,'lattice domain')
    key=sha256(repr((c,R,M,hi)).encode()).hexdigest()
    def vector(k,n):
        mats=[]
        x=R*pow(M,-1,D)%D;x=x-D if x*2>D else x
        for l in range(n):
            j=min(l,c*k);i=l-j;v=[0]*n;F=D**(k-j//c)
            for t in range(j+1):v[i+t]=F*comb(j,t)*x**(j-t)*K**(i+t)
            mats.append(v)
        return mats
    if key not in BOOK and DISCOVER:
        from flint import fmpz_mat
        for k,n in ((1,4),(1,5),(1,6),(2,6),(2,7),(2,8),(3,8),(3,10),(4,12),(5,14),(6,18),(8,21)):
            b=fmpz_mat(vector(k,n));z,t=b.lll(transform=True)
            xs=[];target=R**(c*k)
            for v,a in zip(z.tolist(),t.tolist()):
                v=[int(w) for w in v]
                if sum(abs(w) for w in v)>=target:continue
                f=[w//K**j for j,w in enumerate(v)]
                while f and not f[-1]:f.pop()
                if not f:continue
                prior=next((u for u,g in xs if (g[-1]%65537 or f[-1]%65537) and coprime(g,f)),None)
                if prior is not None:
                    BOOK[key]=[k,n,prior,list(map(int,a))];break
                xs.append((list(map(int,a)),f))
            if key in BOOK:break
        if key not in BOOK:return False
    if key not in BOOK:return False
    k,n,*W=BOOK[key];require(1<=k<=10 and k+1<=n<=30 and len(W)==2,'lattice shape');M0=vector(k,n);fs=[]
    for a in W:
        require(len(a)==n and all(type(t)==int for t in a),'lattice weights')
        v=[sum(x*y for x,y in zip(a,col)) for col in zip(*M0)]
        require(sum(abs(w) for w in v)<R**(c*k) and all(w%K**j==0 for j,w in enumerate(v)),'lattice coefficient bounds')
        fs.append([w//K**j for j,w in enumerate(v)])
    for f in fs:
        while f and not f[-1]:f.pop()
    require(all(fs) and (fs[0][-1]%65537 or fs[1][-1]%65537) and coprime(*fs),'lattice coprimality');USED.add(key);return True


def main():
    global DISCOVER
    if sys.argv[1:]==['--discover']:DISCOVER=True
    elif not sys.argv[1:]:BOOK.update(json.loads(gzip.decompress(PROOF.read_bytes())))
    else:raise SystemExit('usage: PivotPrice48Depth.py [--discover]')
    from PivotPrice48 import bound,loss
    core();require(loss(35)==(1,0),'cubic price has nonzero deficits')
    require(bound([(P,E),(T,36)],verbose=True,depth_check=s_cut),'open 36 fiber')
    require(len(USED)==6 and USED==set(BOOK),'lattice cell count / unreferenced rows')
    if DISCOVER:PROOF.write_bytes(gzip.compress(json.dumps(BOOK,separators=(',',':')).encode(),mtime=0))
    print('PASS conditional t^36',len(USED),'lattice cells',flush=True)

if __name__=='__main__':
    if not __debug__:raise SystemExit('frozen Hensel verifier requires assertions')
    setup();main()
