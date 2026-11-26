"""Optional arithmetic audit: remaining Euler-one sources on the hard 66 path.

This script reconstructs the pinned valuation-envelope constants independently.
It does not exclude the path; it restricts the sources of its exterior Euler prime.
"""
from fractions import Fraction
from functools import cache
from itertools import product
from math import gcd, prod
from pathlib import Path
import sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H.parents[1]/'FinalSprint'))
import JointValuation as J

Q=797161
R=42059143035592870990447
P=589657170962820100934139512775879733212083419
F=((3,12),(Q,66),(5897,6),(R,2),(P,12))
BAN={19,7,11,31,13}


def sigma(r,h):return (r**(h+1)-1)//(r-1)


def val(n,q):
    assert n>0
    s=0
    while n%q==0:n//=q;s+=1
    return s


def cap_two(prefix,targets):
    fixed=dict(prefix);X=prod(r**h for r,h in prefix);S=prod(sigma(r,h) for r,h in prefix)
    assert len(targets)==2 and all(h%2==0 for _,h in prefix)
    cap=[fixed[q]-val(S,q) for q in targets];M=prod(q**v for q,v in zip(targets,cap))
    fm=B//X;bad=set(fixed)|BAN;discount={}
    @cache
    def options(q,t,a):
        shift=val(t,q);d=gcd(q-1,t);out=[]
        if shift and shift<=a:out.append((q,1,q**shift))
        if d>1 and a>shift:
            for order in J.divisors(d):
                if order==1:continue
                for jj,r in enumerate(J.lifts(q,order,a-shift),1):
                    m=q**jj
                    out.extend((m,x,q**(jj+shift)) for x in r)
        return out
    def charge(r,h):
        if r<3 or r%2==0 or r in bad or h%2 and (h%4!=1 or r%4!=1):return
        if r**h>fm:return
        for p in (5,17,23,29,37,41,43,47,53,59,61,67,71,73,79,83,89,97):
            if r!=p and r%p==0:return
        if any(((h+1)%z==0 if r%z==1 else pow(r,h+1,z)==1) for z in BAN):return
        v=[]
        for q,a in zip(targets,cap):
            if r%q==1:j=val(h+1,q)
            else:
                d=q**(a+1);j=val((pow(r,h+1,d)-1)%d or d,q)
            if j>a:return
            v.append(j)
        x=prod(q**j for q,j in zip(targets,v))
        if x*x>r**h and pow(2,r-1,r)==1:
            discount[r]=max(discount.get(r,Fraction(1)),Fraction(x*x,r**h))
    for h in range(2,fm.bit_length()+1):
        if h%2 and h%4!=1:continue
        if 5**h>fm:break
        if h==2:
            a=[[(1,0,1),*options(q,h+1,c)] for q,c in zip(targets,cap)]
            for (m,x,n),(m2,x2,n2) in product(*a):
                z=x+m*((x2-x)*pow(m,-1,m2)%m2);step=m*m2
                while z*z<(n*n2)**2:charge(z,h);z+=step
        else:
            for q,c in zip(targets,cap):
                if 5**h>=q**(4*c):continue
                for m,x,n in options(q,h+1,c):
                    while J.less(x,h,n**4):charge(x,h);x+=m
    U=prod(discount.values(),start=Fraction(1));V=Fraction(X*M*M,U)
    return (X,S,cap,V,discount)


B=10**2400

def audit():
    assert __debug__
    X,S,cap,V,discount=cap_two(F,(Q,P))
    assert cap==[65,11] and V>B
    blocks=[sigma(r,h)//gcd(sigma(r,h),X) for r,h in F]
    D=S//gcd(S,X);assert gcd(D,X)==1 and D==prod(blocks)
    A=(P**13-1)//(P-1);T=(Q**67-1)//((Q-1)*5897)
    assert D==A*T and gcd(A,T)==1
    from math import isqrt
    for z,d,block in ((Q,67,T),(P,13,A)):
        assert all(d%u for u in range(2,isqrt(d)+1)) and gcd(block,2*d*z*(z-1))==1
        assert all(block%r for r in range(2*d+1,20_000_001,2*d))
    assert isqrt(A)**2!=A and isqrt(T)**2!=T
    rough=20_000_001
    left=[];t_impossible=0;balanced_counts=[0,0,0]
    sys.path.insert(0,str(H))
    from Balance import lower
    from SmallRest import excludes as close_small_rest
    small_closed=0;parity_closed=0
    for i,j in product(range(cap[0]+1),range(cap[1]+1)):
        m=Q**i*P**j;a=2*m-1;mod=4*m
        if V*a>B*m*m:continue
        for z in blocks:
            k=z*pow(a,-1,mod)%mod or mod;h=z//a
            assert k>h or ((h-k)//mod<=16 and all(z%x for x in range(k,h+1,mod)))
        if X*D*a>B:continue
        l=(2*a+2)//3
        assert X*a*l**3>B and a-1>=B.bit_length()  # neither nonprimitive emission nor r=1 mod e
        assert X*D*a*l>B
        if X*D*a*((l+T-1)//T)>B:t_impossible+=1
        absent=0
        for z,t,s,block in ((Q,67,i,T),(P,13,j,A)):
            alone=(l+block-1)//block
            assert gcd(block,z-1)==1
            # Charges only the size beyond the already compulsory support.
            if X*D*a*max(alone,lower(z,t,s,a,dict(F)[z]))>B:
                absent+=1
        balanced_counts[absent]+=1
        if absent<2:
            if X*D*a*rough**2>B:parity_closed+=1
            elif close_small_rest(F,S,D,B,a):small_closed+=1
        left.append((i,j))
    assert len(left)==184 and t_impossible==67
    assert balanced_counts==[74,94,16]
    print('PASS high Euler excluded; 184 exterior-Euler-one windows require an emitter on the two named blocks; 67 exclude emitters on the 386-digit block.',flush=True)
    print('BALANCED PASS 16 further windows eliminated; remaining 94 in one block, 74 in either block.',flush=True)
    assert parity_closed==14 and small_closed==0
    print(f'PARITY/REST PASS: {parity_closed} parity, {small_closed} exact small-rest; {168-parity_closed-small_closed} windows left.',flush=True)

if __name__=='__main__':audit()
