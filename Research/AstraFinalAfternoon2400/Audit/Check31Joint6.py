"""Independent complete arithmetic on the exact first 72 / second 16 node."""
from fractions import Fraction
from functools import cache
from itertools import product
from math import gcd, isqrt, lcm, prod
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Check31Domains import B, BANS, state, vp, geometric
from Check7x808 import floorroot
T,Q=917087137,20668766888345125939752429067
ROW=((31,6),(T,72),(Q,16))


def orders(t):
    return [o for o in range(3,5032,2) if (t-1)%o==0]


@cache
def roots(t,o,c):
    divisors=[d for d in range(1,o) if o%d==0]
    start=2
    while True:
        g=pow(start,(t-1)//o,t)
        if pow(g,o,t)==1 and all(pow(g,d,t)!=1 for d in divisors):
            break
        start+=1
    ans=[]
    m=t
    selected={i for i in range(1,o) if gcd(i,o)==1}
    for _ in range(c):
        assert pow(g,o,m)==1
        r=1
        a=[]
        for j in range(1,o):
            r=(r*g)%m
            if j in selected:
                a.append(r)
        assert len(set(a))==len(selected) and all(0<r<m for r in a)
        ans.append((m,a))
        mm=m*t
        g+=m*(-((pow(g,o,mm)-1)//m)*pow(o*pow(g,o-1,t),-1,t)%t)
        m=mm
    return tuple(ans)


def allowed(y):
    def probable(z):
        return z>=3 and z%2 and z not in (*dict(ROW),*BANS) and all(pow(a,z-1,z)==1 for a in (2,3,5,7,11,13,17,19,23,29,31,37) if a<z)
    z=isqrt(y)
    return y%2 and (probable(y) or z*z==y and z%4==1 and probable(z))


def strip(block,x):
    while (g:=gcd(block,x))>1:
        block//=g
    return block


def external(block,m):
    q0=2*m-1; step=4*m
    qlo=max(5,q0); qhi=block
    if qhi<qlo:
        return True
    lo=1; hi=block//qlo
    k=lo+(block*q0-lo)%step  # (2m−1)^2≡1 (mod 4m)
    return k>hi or k+step>hi and block%k!=0


@cache
def check(row):
    assert row==ROW
    X,S,ok=state(row)
    assert ok and 3**5030<=B<3**5031 and min(T,Q)>5031
    d=lcm(X,S)//X
    assert gcd(X,d)==1
    cT,cQ=(dict(row)[p]-vp(S,p) for p in (T,Q))
    levels=[orders(p) for p in (T,Q)]
    for o,k in product([1,*levels[0]],[1,*levels[1]]):
        supply=sum((r-1)//2 for r in (o,k) if r>3)+2*(3 in (o,k))
        assert supply<=lcm(o,k)-1
    # Weight 3/2. Least representatives cover every noncubic class and every
    # cubic CRT class; size uses only the reserved (not artificially larger) exponent.
    def table(items,reserve):
        lost={}
        for M,y in items:
            if y<3 or y%2==0 or (y.bit_length()-1)*2*reserve>=3*M.bit_length():
                continue
            if y**(2*reserve)<M**3 and X*lcm(d,y**reserve)<=B and allowed(y):
                lost[y]=max(lost.get(y,1),Fraction(M**3,y**(2*reserve)))
        return lost
    ps=[]
    for p,c,os in zip((T,Q),(cT,cQ),levels):
        flat={}
        for o in os:
            if o==3:
                continue
            r=(o-1)//2
            assert 2*r>=3
            if 3**(2*r)>=p**(3*c):
                continue
            for y,v in table(((m,b) for m,ls in roots(p,o,c) for b in ls),r).items():
                flat[y]=max(flat.get(y,1),v)
        ps.append(flat)
    left=[(1,[0]),*roots(T,3,cT)]
    right=[(1,[0]),*roots(Q,3,cQ)]
    cube=table(((m*n,(r+n*((l-r)*pow(n,-1,m)%m))%(m*n))
                for (m,a),(n,b) in product(left,right) for l,r in product(a,b)),2)
    assert not cube and not any(ps)
    # For arbitrary possibly overlapping stripped emissions, a safe upper
    # bound on an emitter's overlap is the largest complete overlap class.
    blocks=[geometric(p,e) for p,e in row]
    pending=[strip(a,X) for a in blocks if strip(a,X)>1]
    classes=[]
    while pending:
        a=pending.pop()
        b=next((z for z in pending if gcd(a,z)>1),None)
        if b is None:
            classes.append(a)
        else:
            pending.remove(b)
            pending.append(a*b)
    assert prod(classes)==d and all(gcd(a,b)==1 for i,a in enumerate(classes) for b in classes[:i])
    overlap=max(classes)
    counts=[0,0,0]
    for i,j in product(range(cT+1),range(cQ+1)):
        m=T**i*Q**j
        q=max(5,2*m-1)
        R=(T**(cT-i)*Q**(cQ-j))**3
        if (X*q)**2*R>B**2:
            counts[0]+=1
            continue
        assert all((p==Q and Q%4==3 and j>0) or external(z,m) for (p,_),z in zip(row,blocks)),(i,j)
        if X*d*q>B:
            counts[1]+=1
        else:
            assert (2*X*q*q)**3*d*R>27*B**3*overlap,(i,j)
            counts[2]+=1
    assert sum(counts)==(cT+1)*(cQ+1)
    print('PASS exact root31 joint terminal zero losses, demands',cT,cQ,'allocation windows',counts,flush=True)
    return True


if __name__=='__main__':
    assert __debug__;check(ROW)
