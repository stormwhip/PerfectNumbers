"""Offline exact (7,438), t^12, 27431^22 verifier, with frozen Euler-position replay."""
import json
from pathlib import Path
import sys
from fractions import Fraction
from functools import cache
from math import gcd, prod

H=Path(__file__).resolve().parent
R=H.parents[1]
sys.path[:0]=[str(H),str(R/'RootFiveNext')]
from PrimeCheck import prime64
from Propagation import sigma, val, part, partition, outside_progression, odd_price, screened_prime

p=7; r=27431; t=572749682520506652634407616247; B=10**2400
anchor=8725765874640560753391040471813942392607
initial=(2393,12825715037166394925286953,163494849020985537265457406871,anchor)
T=t**11
factors={2:[3,31,37,8311,170557,1119871,73282003,27172915549024433107236966627477201806224806984767161],
         4:[11,881,123031,1210411,46431209371,1730612894951,1379886810430227255901],
         6:[30493,1403962600226621],10:[89]}

@cache
def pock(n):
    if n<2**64:
        return prime64(n)
    rows=PC[str(n)]
    assert rows and len({p for p,e,a in rows})==len(rows)
    F=prod(p**e for p,e,a in rows)
    assert (n-1)%F==0 and F*F>n
    return all(2<=p<n and e>=1 and pock(p) and pow(a,n-1,n)==1 and gcd(pow(a,(n-1)//p,n)-1,n)==1 for p,e,a in rows)


def prove_t():
    data=json.loads((R/'FinalNight2400/Seven/Lucas.json').read_bytes())
    @cache
    def lucas(x):
        if x<100000:
            return prime64(x)
        g,row=data[str(x)]; row={int(y):h for y,h in row.items()}
        return (prod(y**h for y,h in row.items())==x-1 and pow(g,x-1,x)==1
                and all(2<=y<x and h>0 and lucas(y) and gcd(pow(g,(x-1)//y,x)-1,x)==1 for y,h in row.items()))
    assert lucas(t)


def replay_euler():
    """Replay the order/cost prerequisite; no dynamic historical imports."""
    prove_t()
    X=p**438*t**12
    S=sigma(p,438)*sigma(t,12)
    A=sigma(p,438)//t
    C=sigma(t,12)
    D=A*C
    assert prime64(p) and prime64(r) and p%4==r%4==t%4==3 and r-1==2*5*13*211
    assert t>5100 and 3**5099>B
    assert [o for o in range(3,5101,2) if (t-1)%o==0]==[439]
    assert gcd(D,X)==gcd(A,C)==1 and val(S,t)==1
    a=3
    while X*a**438<=B:
        if a not in (p,t,19) and prime64(a) and pow(a,439,t)==1 and a%t!=1:
            assert X*(D//a**val(D,a))*a**438>B
        a+=2
    a=5
    while X*a**877<=B:
        if a not in (p,t,19) and prime64(a):
            assert pow(a,878,t)!=1 or pow(a,2,t)==1
        a+=4
    assert a<2**64
    # Euler q is the sole source and ord_t(q)=2. LTE supplies v_t(q+1)=11.
    # q cannot lie in C by reciprocity (t == 3 mod 4, q == 1 mod 4).
    assert outside_progression(A,2*T-1,4*T,2*T-1,B//X)
    assert X*D*(2*T-1)**5>B


def exact(rows):
    X=prod(q**h for q,h in rows)
    S=[sigma(q,h) for q,h in rows]
    D=prod(s//part(s,X) for s in S)
    c={q:h-sum(val(s,q) for s in S) for q,h in rows}
    conflict=(D%19==0 or prod(S)>2*X or min(c.values())<0 or X*D>B or c[t]!=11)
    return X,S,D,c,conflict


@cache
def credits(y):
    """Independent per-base floor and exact maximum supplies, including size tail."""
    best=None; a=b=0; h=2; W=y*y
    while W<=B:
        s=(W*y-1)//(y-1); u=val(s,p); v=val(s,r)
        Z=Fraction(W,p**(2*u)*r**(4*v)); best=Z if best is None else min(best,Z)
        a=max(a,u);b=max(b,v);h+=2;W*=y*y
    assert best is not None
    return best,(a,b)


def threshold(low,high,f):
    x,y=low-1,high+1
    while y-x>1:
        m=(x+y)//2
        if f(m): y=m
        else: x=m
    return x


def price_cut(rows, labels, U):
    X,S,D,c,conflict=exact(rows)
    assert not conflict
    labels=set(labels)-{q for q,h in rows}
    assert all(pock(y) and D%y==0 and y!=19 for y in labels)
    blocks=partition(S,X,tuple(sorted(labels)))
    assert prod(x for x,vec in blocks)==D
    M=max(x for x,vec in blocks)
    # Euler cannot lie in the first two blocks (precondition). For r^22, j>0
    # also implies reciprocity exclusion, but the cofactor test alone suffices.
    pending=[s//part(s,X) for s in S[2:]]
    F=prod(y for y in labels if val(D,y)%2)
    G=prod((credits(y)[0] for y in labels),start=Fraction(1)); GN,GD=G.as_integer_ratio()
    mp=max([0]+[credits(y)[1][0] for y in labels]);mr=max([0]+[credits(y)[1][1] for y in labels]);un,ud=U.as_integer_ratio()
    pp=[p**i for i in range(2*c[p]+1)]; rr=[r**i for i in range(4*c[r]+1)]
    stats=[0]*4
    for i in range(c[p]+1):
      up=c[p]-i
      for j in range(c[r]+1):
        vr=c[r]-j; m=T*pp[i]*rr[j]; Q=2*m-1
        # Every chosen label is smaller than the least possible q for this prefix.
        assert not labels or max(labels)<Q
        if X*Q*pp[2*up]*rr[4*vr]*GN*ud>B*GD*un:
            stats[0]+=1;continue
        # q is linear and so q<=B/(XD) if exterior, but while checking exteriority
        # we use the weaker always valid B/X since D might already contain q.
        assert all(outside_progression(Z,Q,4*m,Q,B//X) for Z in pending),(rows,i,j,'internal Euler')
        if X*D*Q*F>B:
            stats[1]+=1;continue
        for v in range(vr+1):
          for lo,hi,distinct in [(0,min(mp,up),v>mr),(mp+1,up,True)]:
            if lo>hi:continue
            K=2*X*Q*Q*rr[v]
            V=K*D*(F if distinct else 1)
            end=threshold(lo,hi,lambda u:V*pp[u]>3*B*M)
            if end>=lo:
                a,b=(GN,GD) if distinct else (1,1)
                assert K*pp[end]*pp[2*(up-end)]*rr[4*(vr-v)]*ud*a>3*B*un*b,(rows,i,j,end,v)
                stats[3]+=1
            else: stats[2]+=1
    return stats


def main():
    assert __debug__
    replay_euler()
    # Completeness: the possible odd order divides target-1, and even
    # disjoint effective indices at p,r are bought from one LCM length.
    assert gcd(3*p,r*((r-1)//2))==1
    def allow(x):return x not in (p,r,t,19) and screened_prime(x)
    Up,np,op,P=odd_price(p,438,2,1,B,5100,allow)
    Ur,nr,orr,Q=odd_price(r,22,4,1,B,5100,allow)
    assert op==orr==0
    U=Up*Ur;print('ordinary loss bases/lift tests',len(P),len(Q),np,nr,flush=True)
    base=[(p,438),(t,12),(r,22)]
    X,S,D,c,conflict=exact(base)
    assert not conflict and prod(initial)==S[-1] and all(pock(z) for z in initial)
    assert val(D,anchor)==1 and anchor<2*T-1
    live=[]; h=2
    while X*(D//anchor)*anchor**h<=B:
        rows=base+[(anchor,h)]
        X1,S1,D1,c1,conflict=exact(rows)
        if not conflict:
            live.append(h)
            labels=factors[h]
            assert all(z in (p,r,t) or D1%z==0 for z in labels)
            assert all(pock(z) and S1[-1]%z==0 for z in labels)
            print('anchor',h,'closed; windows and crossover slices',price_cut(rows,set(initial)|set(labels),U),flush=True)
        h+=2
    assert live==[2,4,6,10] and h==22
    print('PASS entire exact (7,438), t^12, 27431^22; ordinary anchor',anchor,'live',live,'first even tail',h,flush=True)

if __name__=='__main__':
    PC=json.loads((H/'Pock22.json').read_bytes())
    main()
