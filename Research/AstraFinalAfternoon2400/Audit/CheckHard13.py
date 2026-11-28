"""Independent exact branch reconstruction and price terminal for the final source-13 case."""
from fractions import Fraction
from functools import cache
from itertools import combinations,product
from math import gcd,lcm,prod
from pathlib import Path
import json,runpy,sys

H=Path(__file__).resolve().parent
sys.path.insert(0,str(H))
from CheckRare13 import PREFIX, B, S as R, old_table, rare_table, trial
from CheckSevenForestDomains import sig
E=24104457298489411978880226626239089834405670981
W=193674953884899827032111908407518984632293817664100530035167667243179946003138491029077057781
L4=2578012157088772906227552121660556427718057794243245064037125765899184360233830141
BASES=(67,967,8311,11621,50627,392233)
EBASES=(31,15413977)
TARGETS=(19,13,E)
SCALE=(19,19,15)
A=H.parent


def vp(n,p):
    i=0
    while n%p==0:n//=p;i+=1
    return i


@cache
def state(rows):
    x=prod(p**h for p,h in rows)
    s=prod(sig(p,h) for p,h in rows)
    y=s//(s&-s)
    d=lcm(y,x)//x
    return x,y,d,


def raw(rows,q):
    x,y,d=state(rows); assert q not in dict(rows)
    j=vp(y,q); assert j>=1
    out=[];m=lcm(x,y)//q**j
    while m*q**j<=B:
        if j%2==0:
            rp=rows+((q,j),);xx,yy,dd=state(rp)
            if xx*dd<=B and yy<=xx and all(vp(yy,p)<=h for p,h in rp):out.append(j)
        j+=1
    return out,j


def prices_bound(rows,targets,weights,norm,charges,lowers):
    x,y,d=state(rows)
    needs=[dict(rows)[p]-vp(y,p) for p in targets]
    assert min(needs)>=0
    paid=Fraction(x**norm*prod(p**(u*w) for p,u,w in zip(targets,needs,weights)),prod(charges.values()))
    paid*=prod(charges.get(p,1) for p,h in rows)
    for z in lowers:
        v=vp(y,z);assert v and z not in dict(rows)
        k=v+v%2; f=z**k; best=None
        while x*f<=B:
            s=(f*z-1)//(z-1)
            incoming=[vp(s,p) for p in targets]
            if all(i<=u for i,u in zip(incoming,needs)):
                n=Fraction(f**norm,prod(p**(i*w) for p,i,w in zip(targets,incoming,weights)))*charges.get(z,1)
                best=n if best is None else min(best,n)
            k+=2;f*=z*z
        assert best is not None
        paid*=best
    return paid


@cache
def odddiv(p):return [d for d in range(3,5032,2) if (p-1)%d==0]


def group_cap(p,o,cap):
    pp=[j for j in range(2,o+1) if o%j==0 and trial(j)]
    a=2
    while True:
        g=pow(a,(p-1)//o,p)
        if pow(g,o,p)==1 and all(pow(g,o//j,p)!=1 for j in pp):break
        a+=1
    rs=tuple(pow(g,j,p) for j in range(1,o) if gcd(j,o)==1)
    m=p
    for _ in range(cap):
        assert len(set(rs))==sum(gcd(i,o)==1 for i in range(o))
        yield m,rs
        nxt=p*m
        if p<100:
            rs=tuple(r+i*m for r in rs for i in range(p) if pow(r+i*m,o,nxt)==1)
        else:
            di=pow(o,-1,p)
            rs=tuple(r+((1-pow(r,o,nxt))//m * di * pow(r,p-2,p)**(o-1) % p)*m for r in rs)
        assert all(0<r<nxt and pow(r,o,nxt)==1 for r in rs)
        m=nxt


def e4_table(rows):
    x,y,d=state(rows)
    caps=[dict(rows)[p]-vp(y,p) for p in TARGETS]
    assert caps==[275,274,3]
    assert E>5031 and 3**60>19**19 and 3**60>13**19
    # Enumerate length from effective order lcm, not the author's direct scan
    # over possible actual lengths. Charge exact 19/13 LTE independently.
    total=0
    for aa in product(*[[0,1,*odddiv(19)],[0,1,*odddiv(13)],[0,*odddiv(E)]]):
        L0=lcm(*(max(a,1) for a in aa))
        for L in range(L0,5032,2*L0):
            basic=2*bool(3 in aa)+2*(aa[0]==9)+4*(aa[2]>3)
            units=6*sum(vp(L,p) for p,a in zip(TARGETS[:2],aa[:2]) if a)
            assert basic+units<=L-1, (aa,L,basic,units)
            total+=1
    print('PASS independent effective-length coverage combinations',total,flush=True)
    all_cubics=[list(group_cap(p,3,c)) for p,c in zip(TARGETS,caps)]
    cube={}; nine={}; rare={}
    def combine(groups,ws,e,target):
        # Reversed/confluent CRT. Filter with the exact combined size.
        M=1; n=1; rr=[0]
        for (mod,ss),w in zip(groups,ws):
            inv=pow(mod,-1,M) if M>1 else 0
            rr=[b+mod*((a-b)*inv%M) for a in rr for b in ss]
            M*=mod;n*=mod**w
        if not any(b>=3 and b%2 and e*(b.bit_length()-1)<n.bit_length() for b in rr):return
        for b in rr:
            if b>=3 and b%2 and b not in dict(rows) and x*b*b<=B and e*(b.bit_length()-1)<n.bit_length():
                d=b**e
                if d<n and all(pow(a,b-1,b)==1 for a in (2,3,5,7,11,13,17) if a<b):
                    target[b]=max(target.get(b,1),Fraction(n,d))
    for j in (1,2,3):
        for indices in combinations(range(3),j):
            for groups in product(*(all_cubics[i] for i in indices)):
                combine(groups,[SCALE[i] for i in indices],20,cube)
    for g in group_cap(19,9,caps[0]):combine([g],[19],20,nine)
    for o in odddiv(E):
        if o!=3:
            for g in group_cap(E,o,caps[2]):combine([g],[15],40,rare)
    return {z:cube.get(z,1)*nine.get(z,1)*rare.get(z,1) for z in cube.keys()|nine.keys()|rare.keys()}


def main():
    assert __debug__
    # Primality of the large fixed labels is used only after the issued
    # certificate authenticates them, run by the separate author command.
    assert rare_table()==15
    table=old_table(); t20={z:f*f for z,f in table.items()}
    values,tail=raw(PREFIX,R)
    assert (values,tail)==(list(range(2,19,2)),39)
    test=[tuple(PREFIX)+((R,h),) for h in values if h!=2]
    p=PREFIX+((R,2),)
    values,tail=raw(p,E); assert (values,tail)==([2,4,6,8,10],23)
    for rows in test:
        z=prices_bound(rows,(19,13,R),(38,38,77),20,t20,(L4,) if rows[-1][1]==4 else ())
        assert z>B**20
    for h in values:
        rows=p+((E,h),)
        if h==4:
            four=e4_table(rows)
            z=prices_bound(rows,TARGETS,SCALE,10,four,BASES+EBASES+(5,11))
            assert z>B**10
            print('PASS independent E^4 per-base table count',len(four),flush=True)
        else:
            forced=BASES+EBASES+((3,W) if h==2 else ())
            z=prices_bound(rows,(19,13,R),(38,38,77),20,t20,forced)
            assert z>B**20
    print('PASS independently regenerated 8 L high rows, 5 E rows, exact tails 39 and 23')

if __name__=='__main__':main()
