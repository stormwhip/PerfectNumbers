"""Independently regenerate the rare-source h=2 domain and its two refinements."""
from fractions import Fraction
from itertools import product
from math import gcd, lcm, prod
from pathlib import Path
import sys

sys.path.insert(0,str(Path(__file__).resolve().parent))
from Check7x808 import floorroot
import Check19x276x1109x4 as witness

B,P,T,S = witness.B,witness.P,witness.Q,witness.S
vp,sigma,prime,cmp = witness.vp,witness.geom,witness.plainprime,witness.composite_witness
parent=((P,276),(T,1),(S,2))


def state(rows):
    x=prod(p**f for p,f in rows)
    g=prod(sigma(p,f) for p,f in rows)
    y=g>>vp(g,2)
    return x,y,g<=2*x and lcm(x,y)<=B and all(vp(y,p)<=f for p,f in rows)


def exact_orders(s):
    return [o for o in range(3,min(s,5032),2) if (s-1)%o==0]


def roots(s,o,cap):
    divs=[k for k in range(2,o+1) if o%k==0 and prime(k)]
    group=[r for r in range(2,s) if pow(r,o,s)==1 and all(pow(r,o//ell,s)!=1 for ell in divs)]
    assert len(group)==sum(gcd(o,j)==1 for j in range(o))
    m=s
    for z in range(1,cap+1):
        yield m,group
        if z<cap:
            mm=m*s
            # Fermat inversion instead of the source's inverse routine; exact root certification.
            new=[]
            for a in group:
                rho=(pow(a,o,mm)-1)//m
                x=a+m*(-rho*pow(o*pow(a,o-1,s),s-2,s)%s)
                assert 0<x<mm and pow(x,o,mm)==1
                new.append(x)
            assert len(set(new))==len(group)
            group=new
            m=mm


def keep(a,fixed):
    # The six one-way Fermat tests here keep exactly the conservative legacy pool;
    # independent prime verification is not needed for losing bases retained by them.
    return a>=3 and a%2 and a not in fixed and all(pow(k,a-1,a)==1 for k in (2,3,5,7,11,13) if k<a)


def table(s,c,x,fixed,a,d=1,split=False):
    assert 3**(d*(s-1))>=s**a
    out={}
    for o in exact_orders(s):
        w=2 if split else o-1
        assert d*w>=a
        # Preserve real order exponent for the cap even when charging only two units.
        cap=floorroot(B//x,o-1)
        if cap<3:
            continue
        for m,g in roots(s,o,c):
            if min(r if r&1 else r+m for r in g)>cap:
                break
            pt=m**a
            for r in g:
                if r<=cap and keep(r,fixed) and r**(d*w)<pt:
                    out[r]=max(out.get(r,1),Fraction(pt,r**(d*w)))
    return out


def crt_deficit(b,c1,c2,x,fixed):
    # Only axis-free cubic/cubic here; the single-target loss tables carry the axes.
    cap=floorroot(B//x,2)
    A=[(m,g) for m,g in roots(P,3,c1) if min(g)<=cap]
    C=[(n,g) for n,g in roots(b,3,c2) if min(g)<=cap]
    out={}
    for (m,rs),(n,ss) in product(A,C):
        unit=n*pow(n,-1,m)
        N=m*n
        p=N**19
        for r,s in product(rs,ss):
            y=(s+unit*(r-s))%N
            if y<=cap and y%2 and 20*(y.bit_length()-1)<19*N.bit_length() and y**20<p and keep(y,fixed):
                out[y]=max(out.get(y,1),Fraction(p,y**20))
    return out


def main():
    assert __debug__ and all(prime(p) for p in (P,T,S,277))
    assert all(f%2==0 or p==T and f==1 and p%4==1 for p,f in parent)
    x,y,ok=state(parent)
    assert ok and (276-vp(y,P),2-vp(y,S))==(275,1)
    assert S-1==4*277 and S*277>5031 and x*(2*S+1)**(S-1)>B and gcd(P*3,S*277)==1
    assert 3**5030<=B<3**5031 and 3**18>P**2
    _,U=witness.u19(276)
    assert U<10**6
    K=68465
    assert x*P**550*K**276>B*10**6
    bases=[b for b in range(3,K,2) if b not in dict(parent) and prime(b) and pow(b,277,S)==1]
    assert all(pow(b,277,S*S)!=1 for b in bases)
    # Independently search m first. b^m cap and 277m≤5031 cover tails.
    candidate=[(b,277*m-1) for m in range(1,5031//277+1,2) for b in bases if b**m<K]
    live=[(b,f) for b,f in candidate if state((*parent,(b,f)))[-1]]
    assert len(candidate)==1723 and len(live)==45 and all(f==276 for _,f in live)
    print('PASS independent exact source domain: 1723 candidates, 45 live, all exponent 276',flush=True)
    left=[]
    for b,f in live:
        row=(*parent,(b,f))
        X,Y,_=state(row)
        c=f-vp(Y,b)
        w=min([12]+[o-1 for o in exact_orders(b)])
        if X*b**(w*c)<=B:
            left.append(b)
            continue
        loss=prod(table(b,c,X,dict(row),w).values())
        if X*b**(w*c)<=B*loss:
            left.append(b)
    assert left==[13,67,103,139,199,271,277]
    print('PASS inbound single-target prices leave',left,flush=True)
    still=[]
    for b in left:
        row=(*parent,(b,276))
        X,Y,_=state(row)
        c1,c2=276-vp(Y,P),276-vp(Y,b)
        nominal=X**10*(P**c1*b**c2)**19
        if nominal<=B**10:
            still.append(b)
            continue
        assert gcd(P,b*(b-1))==1 and gcd(b,P-1)==1
        for o1,o2 in product(exact_orders(P),exact_orders(b)):
            assert (o1,o2)==(3,3) or lcm(o1,o2)-1>=4
        lp=table(P,c1,X,dict(row),19,10,split=True)
        lb=table(b,c2,X,dict(row),19,10,split=True)
        lc=crt_deficit(b,c1,c2,X,dict(row))
        U=prod(max(lc.get(z,1),lp.get(z,1)*lb.get(z,1)) for z in lp.keys()|lb.keys()|lc.keys())
        assert nominal>B**10*U,b
    assert still==[13]
    print('PASS joint rational prices leave precisely',still,flush=True)


if __name__=='__main__':
    main()
