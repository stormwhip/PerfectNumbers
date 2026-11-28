#!/usr/bin/env python3
"""Research replay: target the newly fixed supplier's missing valuation at h=2."""
from fractions import Fraction
from math import gcd, prod
from pathlib import Path
import runpy

v = runpy.run_path(str(Path(__file__).with_name('Verify276.py')))
B, P, S, T = (v[k] for k in ('B', 'P', 'S', 'T'))
prime, raw_closed, require, state, vp = (v[k] for k in ('prime', 'raw_closed', 'require', 'state', 'vp'))


def root(x, k):
    r = 1 << ((x.bit_length() + k - 1)//k)
    while True:
        t = ((k-1)*r+x//r**(k-1))//k
        if t >= r:
            require(r**k <= x < (r+1)**k, 'integer root')
            return r
        r = t


def residues(s, o, cap):
    m=s
    rr=[r for r in range(2,s) if pow(r,o,s)==1 and not any(pow(r,d,s)==1 for d in range(1,o) if o%d==0)]
    for z in range(1,cap+1):
        yield m, rr
        m1=s*m
        rr=[r+m*((-((pow(r,o,m1)-1)//m)*pow(o*pow(r,o-1,s),-1,s))%s) for r in rr]
        require(len(set(rr))==len(rr) and all(0<r<m1 and pow(r,o,m1)==1 for r in rr),'Hensel lift')
        m=m1


def possible(b,fixed):
    return b >= 3 and b%2==1 and b not in fixed and all(pow(a,b-1,b)==1 for a in (2,3,5,7,11,13) if a<b)


def add(tab,b,num,den):
    if num>den:
        tab[b]=max(tab.get(b,1),Fraction(num,den))


def lte_check(s,w,d,o):
    # For ord 1, 3^(s^u-1) >= s^(wu/d) via s^u-1 >= (s-1)u.
    require(3**(d*(s-1)) >= s**w,'order one price')
    # For ord >1, o*(s^k-1) >= (s-1)k, so the same check pays LTE.
    require(o>=1,'invalid order')


def single(s,c,rows,w,d=1,force_two=False,omin=1):
    X=state(rows)[0]
    fixed=dict(rows)
    lte_check(s,w,d,1)
    tab={}
    for o in range(3,min(5031,s-1)+1,2):
        if (s-1)%o or o<omin:
            continue
        L=root(B//X,o-1)
        if L<3:
            continue
        e=2 if force_two else o-1
        require(d*e>=w,'weight beyond length')
        for z,(m,rr) in enumerate(residues(s,o,c),1):
            Q=s**(w*z)
            if all((r if r%2 else r+m)>L for r in rr):
                # All lifts at all greater depths remain in these residue classes.
                break
            for r in rr:
                if r>L or not possible(r,fixed):
                    continue
                if d*e*(r.bit_length()-1)>=Q.bit_length():
                    continue
                add(tab,r,Q,r**(d*e))
    return tab


def joint(b,c1,c2,rows):
    # Work at 19/10 for both targets. Neither target may divide the
    # other target's orders, so all LTE costs use separate factors.
    require((b-1)%19!=0 and 18%b!=0 and b!=P,'order support')
    p,s=P,b
    X=state(rows)[0]
    cap=root(B//X,2)
    fixed=dict(rows)
    cubic1=list(residues(p,3,c1));cubic2=list(residues(s,3,c2));C={}
    # Cubic/cubic is charged only once: CRT modulo M, positive loss entails b'<M.
    # LTE factors at the two distinct targets are paid with the extra length.
    for m,rr in cubic1:
        for n,tt in cubic2:
            if min(rr)>cap or min(tt)>cap:
                continue
            V=m*n
            inv=pow(m,-1,n)
            for x,y in ((x,y) for x in rr for y in tt):
                z=x+m*((y-x)*inv%n)
                if z>=V or z>cap or not z%2 or 20*(z.bit_length()-1)>=19*V.bit_length():
                    continue
                if z**20 < V**19 and possible(z,fixed):
                    add(C,z,V**19,z**20)
    a=single(p,c1,rows,19,10,force_two=True)
    d=single(s,c2,rows,19,10,force_two=True)
    # With >=1 order above cubic, their lcm minus 1 is >=8, hence
    # two exponent units per target fit separately. For pair of cubic orders
    # use C instead. Additional LTE factors increase the length by at least
    # (p−1)k_p+(s−1)k_s; both first-order cases obey the same lower bounds.
    one=Fraction(1)
    return prod(max(C.get(q,one),a.get(q,one)*d.get(q,one)) for q in set(C)|set(a)|set(d))


def run():
    parent=[(P,276),(T,1),(S,2)]
    X0,_,Y0,_=state(parent)
    K=68465
    U,_=v['loss19'](276,{P,S,T})
    require(U<=10**6 and X0*P**(2*(276-vp(Y0,P)))*K**276>B*10**6,'source cap')
    pool=[b for b in range(3,K,2) if b not in {P,S,T} and pow(b,277,S)==1 and prime(b)]
    require(all(pow(b,277,S**2)!=1 for b in pool),'source valuation')
    survivors=[]
    for b in pool:
        for m in range(1,5031//277+1,2):
            if b**m>=K:
                break
            f=277*m-1
            if not raw_closed(parent+[(b,f)]):
                survivors.append((b,f))
    require(len(survivors)==45,'exact source survivors')
    left=[]
    for b,f in survivors:
        rows=parent+[(b,f)]
        X,_,Y,_=state(rows)
        c=f-vp(Y,b)
        w=min([o-1 for o in range(3,b,2) if (b-1)%o==0],default=12)
        w=min(w,12)
        if X*b**(w*c)<=B:
            left.append(b)
            continue
        loss=prod(single(b,c,rows,w).values())
        if X*b**(w*c)*loss.denominator<=B*loss.numerator:
            left.append(b)
            print('single target failed:',b,flush=True)
        else:
            print('single target passed:',b,flush=True)
    require(left==[13,67,103,139,199,271,277], 'single-price remaining list')
    still=[]
    for b in left:
        rows=parent+[(b,276)]
        X,_,Y,_=state(rows)
        c1=276-vp(Y,P)
        c2=276-vp(Y,b)
        Q=(P**c1*b**c2)**19*X**10
        if Q<=B**10:
            still.append(b)
            print('joint target lacks nominal margin:',b,flush=True)
            continue
        U=joint(b,c1,c2,rows)
        if Q*U.denominator<=B**10*U.numerator:
            still.append(b)
            print('joint target failed:',b,flush=True)
        else:
            print('joint target passed:',b,flush=True)
    require(still==[13], 'joint-price remaining list')
    print('h=2 joint missing-target prices: remaining',still,flush=True)

if __name__=='__main__':
    run()
