"""Independent all-representative 2035349 exponent-46 ordinary/square price.
Here w=6 <= order−1 for every admissible odd order, and no LTE length shift
exists at this target. The least representative is consequently sufficient.
"""
from math import gcd,isqrt,prod
from fractions import Fraction
from hashlib import sha256

def first_not_rejected(q,mod):
    for i in range(50):
        if q>=5 and all(((q+1)//2)%p for p in (7,11,13,19,31)) and all(q==p or q%p for p in range(3,98,2) if prime(p)):
            return q
        q+=mod
    return q

B=10**2400;q=2035349;p=1093;bans=(7,11,13,19,31)
R=[(3,6),(p,156),(q,46)]; X=prod(r**h for r,h in R)

def sigma(r,h):return sum(r**i for i in range(h+1))
def prime(n):return n>=2 and all(n%i for i in range(2,isqrt(n)+1))
def vp(n,p):
    h=0
    while n%p==0:n//=p;h+=1
    return h

def ds(n):return {d for i in range(1,isqrt(n)+1) if n%i==0 for d in (i,n//i)}

def proof():
    assert __debug__ and all(prime(n) for n in (p,q,7,157,463))
    assert q-1==4*7*157*463 and q>B.bit_length()+1
    S=prod(sigma(r,h) for r,h in R);cap=46-vp(S,q);cp=156-vp(S,p)
    assert (cp,cap)==(155,45)
    U=[[] for j in range(cap+1)]
    hmax=0
    while 5**(hmax+1)<=B//X:hmax+=1
    orders=sorted(d for d in ds(q-1) if d>1 and d%2 and d<=hmax+1)
    for d in orders:
        factors=[k for k in ds(d) if prime(k)]
        h=next(k for k in range(2,q) if all(pow(k,(q-1)//t,q)!=1 for t in factors))
        gen=pow(h,(q-1)//d,q)
        # For potential losing rows, use h=d−1. This lower exponent is enough:
        # every allowed h>=d−1 and the ban of a d-block persists in all of them.
        f=d-1
        if 5**f>=q**(6*cap):continue
        z=[pow(gen,j,q) for j in range(1,d) if gcd(j,d)==1]
        inverses=[pow(d*pow(a,d-1,q),-1,q) for a in z]
        mod=q
        for j in range(1,cap+1):
            Q=mod**6
            for a in z:
                if a<5 or a%2==0 or a in (3,p,q,*bans):continue
                if (a.bit_length()-1)*f>=Q.bit_length() or a**f>=Q:continue
                if any(a not in (t,t*t) and a%t==0 for t in range(3,98,2) if prime(t)):continue
                if any((f+1)%t==0 if a%t==1 else pow(a,f+1,t)==1 for t in bans):continue
                U[j].append(Fraction(Q,a**f))
            new=mod*q
            z=[a+mod*((-((pow(a,d,new)-1)//mod)*v)%q) for a,v in zip(z,inverses)];mod=new
    # A row of exact level j can be represented at that depth. Treat lower
    # actual levels independently and allow duplicates across levels. This is
    # conservative and doesn't trust either model's retained representative IDs.
    lut=[Fraction(1)]*(cap+1)
    for j,values in enumerate(U):
        if j:
            for v in sorted(values,reverse=True)[:cap//j]:
                for k in range(cap,j-1,-1):lut[k]=max(lut[k],lut[k-j]*v)
    V=X*q**(6*cap)/lut[cap];assert V>B
    reject=[]
    for i in range(cp+1):
        for j in range(cap+1):
            m=p**i*q**j;q0=first_not_rejected(2*m-1,4*m)
            if X*q0*q**(6*(cap-j))>B*lut[cap-j]:reject.append((i,j))
    digest=sha256(repr(reject).encode()).hexdigest()
    assert len(reject)==1510 and digest=='667992a751f962deea97e7010a1ca7d7485d7628d51c8cac61fbdea7295e5fdc'
    print('independent 156/46 excluded',len(reject),'digest',digest,flush=True)
    return reject
if __name__=='__main__':proof()
