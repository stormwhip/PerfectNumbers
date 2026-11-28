"""Independent exact arithmetic and allocation coverage for root-three E3 windows."""
from functools import cache
from hashlib import sha256
from math import gcd, isqrt
B=10**2400
E=856
X=3**E
W=3*X
A=sum(3**j for j in range(E+1))
BANS=(7,11,13,19,31)
R=100097600002


def prime(p):
    return p>1 and all(p%q for q in range(2,isqrt(p)+1))


def cost_lists():
    # Two independent tariffs. No need to stop on a banned factor: retaining
    # a later cheap item would only lower a tariff. Actual supplier tiers
    # must nevertheless include every earlier tier and have no banned factor.
    cap=15000
    mass_cap=cap**2
    factor_cap=(mass_cap+cap+1)//3
    mass=[mass_cap]*E
    factors=[factor_cap]*E
    for p in range(4,cap+1,3):
        if p in BANS or not prime(p):
            continue
        k=1
        bad_mass=False
        while True:
            power=3**(k-1)
            m=p**(2*power)
            piece=(m+p**power+1)//3
            if m>=mass_cap and piece>=factor_cap:
                break
            y=p**(3*power)
            bad_mass=bad_mass or any((y-1)%(b*(p-1))==0 for b in BANS)
            if not bad_mass and m<mass_cap:
                mass.append(m)
            if piece<factor_cap and not any(piece%b==0 for b in BANS):
                factors.append(piece)
            k+=1
    def prefixes(l):
        t=[1]
        for v in sorted(l)[:E]:
            t.append(t[-1]*v)
        return t
    return prefixes(mass),prefixes(factors)


@cache
def best_q(s,tag):
    y=3**s
    m=next(k for k in range(1,6,2) if k%3==tag)
    for j in range(29):
        k=m+6*j
        q=2*y*k-1
        if j==28 or (all(k%p and q%p for p in BANS) and not any(q%p==0 and p!=q and q>1000 for p in SMALL)):
            return q
    raise AssertionError


def main():
    assert __debug__ and isqrt(A)**2<A and 2*A==W-1 and prime(857)
    assert gcd(A,6*857)==1
    M,T=cost_lists()
    for s in range(1,9):
        assert X*M[E-s]>B
    assert 2*3**9-1> B.bit_length()+1
    assert all(p%3!=1 or p in BANS or (p*p+p+1)%7==0 for p in SMALL if p<43)
    assert 43**(3**7-1)>B
    floor=[]
    for s in range(9,E+1):
        q=2*3**s-1
        for b in range(min(6,E-s)+1):
            ord_mass=(43 if b else 5)**2*(2*q)**3//27
            f=max(43**(3**b-1),ord_mass)
            a=X*q*f*M[E-s-b]
            z=3**(E-b)*f*f
            assert a>B or z>B
            floor.append(max(a,z))
    print('PASS historical primitive condition regenerated:',len(floor),len(str(min(floor)))-1,flush=True)
    rr=[R**(2*i) for i in range(E+1)]
    ext=[]; inter=[]
    for s in range(9,E+1):
        y=3**s
        k=E-s
        for tag in (1,2):
            q=best_q(s,tag)
            if X*M[k]>B or X*A*q*T[k]>B or 2*X*q*q*M[k]>3*B:
                continue
            den=max(W,q)*(W//y+4)
            num=y*q
            # Independent roles evaluated with the full Cartesian domain,
            # regardless of whether the other role is already eliminated.
            for i in range(k+1):
                joint=X*q*M[k-i]*max(A*R,rr[i])
                if joint*2*q<=3*B:
                    ext.append((s,tag))
                    break
            for i in range(k+1):
                side=X*q*M[k-i]
                if side*max(A*R,rr[i])>B:
                    continue
                if side*num*max(A,rr[i])>B*den:
                    continue
                if side*2*q*rr[i]>3*B:
                    continue
                inter.append((s,tag))
                break
    assert ext==[(s,d) for s in range(696,E+1) for d in (1,2)]
    assert inter==[(s,d) for s in range(678,E+1) for d in (1,2)]
    print('PASS both source roles:', [(len(r),r[0][0],r[-1][0],sha256(repr(r).encode()).hexdigest()) for r in (ext,inter)],flush=True)


if __name__=='__main__':
    SMALL=[p for p in range(2,601) if prime(p)]
    main()
