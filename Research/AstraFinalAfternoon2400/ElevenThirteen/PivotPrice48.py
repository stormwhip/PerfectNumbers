"""Complete weight-two pricing for the 87-bit pivot of canonical (11,48)."""
from pathlib import Path
import sys
from functools import cache
from fractions import Fraction
from math import gcd,isqrt,prod
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'FinalNight2400/Ten')]
from Coverage import prime,domain,B,sigma,val,require,legal_prefix
from Weighted import lifts
P=11;E=48;T=100641220283951395639601683
BAN=(19,7)
ORDERS=(3,7,21,49,147)
SMALL=(3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97)


def trim(n,V):
    while (g:=gcd(n,V))>1:n//=g
    return n


@cache
def loss(c):
    """Safe for any subset of ordinary prime bases or one even-index Euler square atom."""
    U={}
    for o in ORDERS:
        for j,zs in enumerate(lifts(T,o,c),1):
            m=T**j;num=m*m;bound=T**(2*j//(o-1)+1)
            for r in zs:
                if not 3<=r<=bound or not r%2 or r in (*BAN,P,T):continue
                if any(r%s==0 and r not in (s,s*s) for s in SMALL):continue
                d=r**(o-1)
                if d>=num or pow(r,o,m*T)==1:continue
                y=isqrt(r)
                if y*y!=r and pow(2,r-1,r)!=1:continue
                U[r]=max(U.get(r,Fraction(1)),Fraction(num,d))
    return prod(U.values(),start=Fraction(1)),len(U)


def legacy_overlap(blocks):
    return max(b*prod(gcd(b,u) for j,u in enumerate(blocks) if i!=j) for i,b in enumerate(blocks))


def bound(parts,verbose=False,depth_check=None):
    X=prod(p**h for p,h in parts);V=prod(p for p,h in parts)
    A=[trim(sigma(p,h)//(1+h%2),V) for p,h in parts];D=prod(A)
    demand=dict(parts)[T]-sum(val(sigma(p,h),T) for p,h in parts)
    if demand<0:return True
    F,num=loss(demand)
    if any(h%2 for p,h in parts):return X*T**(2*demand)*F.denominator>B*F.numerator
    Dcap=legacy_overlap(A)
    # In high-i exterior windows the selected emitter of q may own any one major divisibility block.
    dead=[];open_=[]
    for i in range(demand+1):
        Q=max(5,2*T**i-1);M=T**(demand-i);P0=X*Q*M*M*F.denominator;P1=B*F.numerator
        if P0>P1:dead.append(i);continue
        # Test prime from an exact sigma block by size and congruence, without assuming least whole lift.
        def may_own(Z):
            Y=T**i
            if Q>Z:return False
            mod=4*Y
            k=(pow(2*Y-1,-1,mod)*Z)%mod or mod
            if Z//Q<k:return False
            if Z//Q<k+mod and Z%k:return False
            return True
        # q=1 mod 4 and T=3 mod 4. For i>0, q=-1 mod T, so quadratic
        # reciprocity gives (T/q)=(q/T)=-1, contradicting odd order if q|sigma(T^f).
        if any(may_own(Z) for (p,_),Z in zip(parts,A) if p!=T or i==0):open_.append((i,'internal possible'));continue
        # For each emitter allocation: overlap with the T-block may be huge,
        # but an r in it cannot supply T unless the target congruence also fits.
        Hmax=Dcap
        # q external to the fixed support -> there is a distinct emitter r^h.
        # Exterior q may have exponent a>=5; keeping only q is a valid weaker size bound.
        if X*D*Q>B:dead.append(i);continue
        survived=[]
        for j in range(demand-i+1):
            y=T**j
            if 2*X*D*Q*Q*y>3*B*Dcap:continue
            if 2*X*Q*Q*M*M*F.denominator>3*B*F.numerator*y:continue
            survived.append(j)
        if depth_check and survived:
            survived=[j for j in survived if not depth_check(i,j)]
        if survived:open_.append((i,(min(survived),max(survived))))
        else:dead.append(i)
    if verbose:print('dead',dead,'open',open_,flush=True)
    return not open_


def setup():
    c=(T-1)//294
    require(prime(T) and prime(c) and 294*c==T-1 and c>5100 and 3**5100>B,'orders and all length bounds')
    require(ORDERS==tuple(o for o in range(3,5101,2) if (T-1)%o==0),'order domain')


if __name__=='__main__':
    setup()
    for f in (36,30,28,26,24,22,18,16,14,12,10,8,4,2):
        u,n=loss(f-1)
        print(f,n,len(str(u.numerator))-len(str(u.denominator)),bound([(P,E),(T,f)]),flush=True)
