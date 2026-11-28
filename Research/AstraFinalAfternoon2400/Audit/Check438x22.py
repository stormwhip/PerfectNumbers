"""Independent exponent/supplier coverage and crossovers for 7^438, t^12, 27431^22."""
from bisect import bisect_right
from fractions import Fraction
from functools import cache
from math import gcd, isqrt, lcm, prod
from pathlib import Path
import runpy
import sys
import json

H = Path(__file__).resolve().parent.parent/'Propagation'
P,R = 7,27431
T=572749682520506652634407616247
A0=8725765874640560753391040471813942392607
B=10**2400
S0=T**11


def val(x,p):
    z=0
    while x%p==0:
        x//=p
        z+=1
    return z


def sigma(y,e):
    return (y**(e+1)-1)//(y-1)


def prime(n):
    return n == 2 or n > 2 and n%2 and all(n%d for d in range(3,isqrt(n)+1,2))


def raw(row):
    X=prod(s**h for s,h in row)
    sums=[sigma(s,h) for s,h in row]
    W=prod(sums)
    dem={s:h-val(W,s) for s,h in row}
    D=lcm(X,W)//X
    return X,sums,D,dem,W%19!=0 and W<=2*X and min(dem.values())>=0 and X*D<=B


def exclude_internal(k,m,maxq):
    q0=2*m-1
    maxq=min(k,maxq)
    if maxq<q0:
        return True
    period=4*m
    low=(k+maxq-1)//maxq
    high=k//q0
    # q0^2 ≡ 1 mod 4m (q0=2m−1); enumerate directly the cofactor class.
    j0=low + (q0*k-low)%period
    return all(k%j for j in range(j0,high+1,period))


def euler():
    assert 3**5030 <= B < 3**5031 and T>5031
    assert [o for o in range(3,5032,2) if (T-1)%o==0]==[439]
    X=7**438*T**12
    a=sigma(7,438)//T
    c=sigma(T,12)
    assert sigma(7,438)%T==0 and val(a*c,T)==0
    D=a*c
    assert gcd(D,X)==gcd(a,c)==1 and T%4==3
    assert X*6592**438<=B<X*6593**438 and X*80**877<=B<X*81**877
    roots=[b for b in range(3,6593,2) if b not in (7,19) and prime(b) and pow(b,439,T)==1]
    assert all(lcm(X*D,b**438)>B for b in roots)
    assert all(pow(b,878,T)!=1 or pow(b,2,T)==1 for b in range(5,81,4) if prime(b))
    assert exclude_internal(a,S0,B//X) and X*D*(2*S0-1)**5>B
    print('PASS independent Euler-position bounds (ordinary max 6592, Euler max 80), order roots',roots,flush=True)


def positives(z,w,c):
    out={}
    for o in range(3,5032,2):
        if (z-1)%o or 3**(o-1)>=z**(w*c):
            continue
        assert w<=o-1
        fs=[p for p in range(2,o+1) if o%p==0 and prime(p)]
        seq=[r for r in range(1,z) if pow(r,o,z)==1 and all(pow(r,o//p,z)!=1 for p in fs)]
        assert len(seq)==sum(gcd(o,j)==1 for j in range(o))
        m=z
        for k in range(1,c+1):
            mk=m**w
            for a in seq:
                if a>=3 and a%2 and a not in (P,R,T,19) and a**(o-1)<mk:
                    # One-way compositeness filtering. Keep probable primes.
                    if all(a==s or a%s for s in (3,5,7,11,13,17,19,23,29,31,37)) and pow(2,a-1,a)==1:
                        out[a]=max(out.get(a,1),Fraction(mk,a**(o-1)))
            if k<c:
                n=m*z
                next_roots=[]
                for a in seq:
                    rho=(pow(a,o,n)-1)//m
                    deriv=o*pow(a,o-1,z)
                    digit=(-rho*pow(deriv,z-2,z))%z
                    b=a+digit*m
                    assert pow(b,o,n)==1
                    next_roots.append(b)
                seq=next_roots
                m=n
    return prod(out.values()), sorted(out)


@cache
def credit(y):
    best=None
    u_max=v_max=0
    pp=y*y
    while pp<=B:
        W=(y*pp-1)//(y-1)
        u,v=val(W,P),val(W,R)
        u_max=max(u_max,u)
        v_max=max(v_max,v)
        v0=Fraction(pp,P**(2*u)*R**(4*v))
        best=v0 if best is None else min(best,v0)
        pp*=y*y
    assert best is not None
    return best,u_max,v_max


def support_piece(block,n):
    # Iteratively strip gcd against the whole test support, not its shrinking gcd.
    rest=block
    while (g:=gcd(rest,n))>1:
        rest//=g
    return block//rest


def cutoff(y,head):
    """Return the maximal n≥-1 such that head*7^n ≤ y, using an exact monotone bisect."""
    return bisect_right(POW7,y//head)-1


def check(row,labels,U):
    x,ss,d,dem,live=raw(row)
    assert live and dem[T]==11
    remaining=[d]
    for block in (*ss,*labels):
        remaining=[q for u in remaining for a in [support_piece(u,block)] for q in (a,u//a) if q>1]
    assert prod(remaining)==d and all(gcd(u,v)==1 for i,u in enumerate(remaining) for v in remaining[:i])
    max_overlap=max(remaining)
    F=prod(y for y in labels if val(d,y)%2)
    assert all(d%y==0 and y<2*S0-1 for y in labels)
    cr=[credit(y) for y in labels]
    G=prod(a for a,_,_ in cr)
    u_max=max(u for _,u,_ in cr)
    v_max=max(v for _,_,v in cr)
    pows=[R**e for e in range(4*dem[R]+1)]
    alpha,beta=U.as_integer_ratio()
    mm,nn=G.as_integer_ratio()
    ordinary=0
    external=0
    crossover=0
    for i in range(dem[P]+1):
        pleft=dem[P]-i
        for j in range(dem[R]+1):
            rleft=dem[R]-j
            m=S0*POW7[i]*pows[j]
            q=2*m-1
            if x*q*POW7[2*pleft]*pows[4*rleft]*mm*beta > B*nn*alpha:
                ordinary+=1
                continue
            for block in ss[2:]:
                block//=support_piece(block,x)
                assert exclude_internal(block,m,B//x)
            if x*d*q*F>B:
                external+=1
                continue
            for v in range(rleft+1):
                K=2*x*q*q*pows[v]
                # The worst point of each slice is the greatest u still permitted by its
                # independent necessary size inequality. Use binary search on pure powers.
                for lo,hi,distinct in ((0,min(u_max,pleft),v>v_max),(u_max+1,pleft,True)):
                    if lo>hi:
                        continue
                    cap=cutoff(3*B*max_overlap,K*d*(F if distinct else 1))
                    e=min(hi,cap)
                    if e<lo:
                        continue
                    a,b=(mm,nn) if distinct else (1,1)
                    assert K*POW7[2*pleft-e]*pows[4*(rleft-v)]*beta*a>3*B*alpha*b
                    crossover+=1
    return ordinary,external,crossover


def main():
    assert __debug__
    global POW7
    POW7=[7**i for i in range(877)]
    data=runpy.run_path(str(H/'Verify438x22.py'))
    # Borrow only the original factor witnesses, not its prices, domains or terminal code.
    data['pock'].__wrapped__.__globals__['PC']=json.loads((H/'Pock22.json').read_bytes())
    test=data['pock']
    facts=data['factors']
    initial=tuple(data['initial'])
    assert initial[-1]==A0 and all(test(y) for y in initial)
    X,ss,D,ds,is_live=raw(((P,438),(T,12),(R,22)))
    assert is_live and prod(initial)==ss[-1] and val(D,A0)==1 and A0<2*S0-1
    live=[]
    for h in range(2,24,2):
        n=X*(D//A0)*A0**h
        if n>B:
            assert h==22
            break
        row=((P,438),(T,12),(R,22),(A0,h))
        if raw(row)[-1]:
            live.append((h,row))
    assert [h for h,_ in live]==[2,4,6,10]
    print('PASS four independently reconstructed branches (2,4,6,10), raw even tail 22',flush=True)
    euler()
    u,L7=positives(P,2,438)
    v,LR=positives(R,4,22)
    print('Complete losing base labels:',L7,LR,flush=True)
    for h,row in live:
        assert all(test(y) and sigma(A0,h)%y==0 for y in facts[h])
        labels=set((*initial,*facts[h]))-dict(row).keys()
        print('PASS independent credit and crossover',h,check(row,labels,u*v),flush=True)


if __name__=='__main__':
    main()
