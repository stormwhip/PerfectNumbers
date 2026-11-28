"""Exact joint price terminal for (31,6), first 72, pivot 16."""
from fractions import Fraction
from functools import cache
from itertools import product
from math import gcd,isqrt,lcm,prod
from pathlib import Path
import argparse,json,sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Replay import B, BANNED, SMALL, state, valuation, exclusive_components, external, max_positive_base, odd_lifts
from GenericPrice import T,Q,roots,domain,upperloss


def run(row,w):
    p,t=T,Q
    assert row[:2]==((31,6),(T,72)) and row[2:]==((Q,16),)
    assert p!=t and gcd(p,t)==1 and p>8000 and t>8000
    assert 1<=w<=2
    x,s,d,blocks,ok=state(row);assert ok
    a,b=w.numerator,w.denominator
    op,ot=domain(p),domain(t)
    cp,ct=(dict(row)[v]-valuation(s,v) for v in (p,t))
    assert (cp,ct)==(71,15)
    # Same noncubic order can occur at both targets (7,21,...). Divide
    # each o−1 budget by 2 rather than incorrectly using o−3 twice.
    hres=lambda o:0 if o in (1,3) else (o-1)//2
    for i,j in product((1,*op),(1,*ot)):
        assert (2 if 3 in (i,j) else 0)+hres(i)+hres(j)<=lcm(i,j)-1
    try:
        _,Up,Np=upperloss(row,p,{o:hres(o) for o in op if o>3},w,skip_order3=True)
        _,Ut,Nt=upperloss(row,t,{o:hres(o) for o in ot if o>3},w,skip_order3=True)
    except OverflowError:
        return dict(open='marginal progression too large')
    h=2*b
    ptab=((1,(0,)),*roots(p,3,cp));ttab=((1,(0,)),*roots(t,3,ct))
    u={};top=B//x
    def plausible(v):return v>=3 and v%2 and v not in dict(row) and v not in BANNED and all(v==q or v%q for q in SMALL) and pow(2,v-1,v)==1
    for (n,rr),(m,ss) in product(ptab,ttab):
        M=n*m; goal=M**a
        if m==1:inv=0
        else:inv=pow(n,-1,m)
        upper=min(max_positive_base(goal,h),isqrt(top))
        for r,z in product(rr,ss):
            y=r+n*((z-r)*inv%m)
            lifts=odd_lifts(y,M,upper)
            count=max(0,(lifts.stop-1-lifts.start)//lifts.step+1)
            if count>50000:return dict(open='joint progression too large',labels=count)
            for y in lifts:
                size=y*y
                if size//gcd(size,d)>B//(x*d):continue
                j=isqrt(y)
                if not (plausible(y) or j*j==y and j%4==1 and plausible(j)):continue
                cost=size**b
                assert cost<goal
                if y not in u or u[y][0]*cost<goal*u[y][1]:u[y]=goal,cost
    U=10**8
    for n,m in u.values():U=-(-(U*n)//m)
    U=(-(-U//10**8))*Up*Ut
    H=max(exclusive_components(blocks,x));price=B**b*U
    inside=[];outside=[]
    for i,j in product(range(cp+1),range(ct+1)):
        m=p**i*t**j;q=2*m-1;R=(p**(cp-i)*t**(ct-j))**a
        if (x*q)**b*R>price:continue
        if not all((v==t and v%4==3 and j>0) or external(z,m) for (v,_),z in zip(row,blocks)):
            inside.append((i,j));continue
        if x*d*q>B or (2*x*q*q)**a*d**(a-b)*R>3**a*B**a*U*H**(a-b):continue
        outside.append((i,j))
    return dict(weight=str(w),loss_counts=[len(u),Np,Nt],inside=inside,outside=outside)

if __name__=='__main__':
    assert __debug__
    a=argparse.ArgumentParser();a.add_argument('--weights',nargs='+',type=Fraction,default=[Fraction(3,2)]);args=a.parse_args()
    for w in args.weights:print(json.dumps(run(((31,6),(T,72),(Q,16)),w)),flush=True)
