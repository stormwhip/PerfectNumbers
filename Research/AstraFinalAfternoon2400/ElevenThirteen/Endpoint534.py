"""Exact integer exploration/check for (13,618) s=534 via a sparse emitter polynomial."""
from pathlib import Path
from math import gcd,isqrt
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from HighLinear import B,P,ROUGH,inputs,cell,minimum_q,floor_root,ceil_root,require

E=618; S=534; CAP=52360
SURV={8:(1081,2935,11863,13393,25615),10:(2935,7005,8655,22471,47991)}


def endrow(u,h,c,A,X,W,Y):
    q=2*u*Y-1;T=B//(X*A*q);lo=ceil_root((2*q+2)//3,h);hi=min(floor_root(A//ROUGH,c),floor_root(T,h-c));d=h+1-c
    Dhi=(P-1)*(A//lo**c)
    pos=(W-1)*hi**d//(q*Y);neg=(q*hi**d+(q+1)*Dhi)//(q*Y)
    return q,lo,hi,pos,neg


def candidates(e=E,s=S):
    X,W,A,M,_=inputs(e);Y=P**s
    require(cell(e,s,(X,W,A,M,0))=={(8,3),(10,5)},'shape roster')
    J=(-1-(P-1)*A)*pow(Y,-1,M)%M
    for h,c in ((8,3),(10,5)):
        row=endrow(CAP,h,c,A,X,W,Y)
        require(row[-2]<(J or M) and row[-1]<((-J)%M or M),'signed monotone tail')
        start=(minimum_q(s,h)+1)//(2*Y)
        for u in range(start,CAP,2*(h+1)):
            if gcd(u,P*19*7*11*31)!=1:continue
            yield e,s,h,c,u,J,M,X,W,A,Y


def F(z,q,W,Y,a,h,c):
    # (W-1-q)*z^(h+1) - Y*a*q*z^c - (q+1)*(W-1).
    return (W-1-q)*z**(h+1)-Y*a*q*z**c-(q+1)*(W-1)


def possible_roots(q,lo,hi,alpha,W,Y,h,c,M,A):
    # F(x)/x^c is strictly increasing on x>0: first term scales x^(h+1-c),
    # negative constant term scales -x^(-c), middle term is constant.
    if lo>hi or W-1<=q:return None
    lo+= (1-lo)%M;hi-= (hi-1)%M
    if lo>hi or F(lo,q,W,Y,alpha,h,c)>0 or F(hi,q,W,Y,alpha,h,c)<0:return None
    # Very tight power bracketing reduces bisection, but every discarded r
    # is certified by the sign of the exact sparse polynomial.
    C=W-1-q
    low0=floor_root(Y*alpha*q//C,h+1-c)
    lo_new=max(lo,low0-(low0-1)%M)
    if lo_new<=hi and F(lo_new,q,W,Y,alpha,h,c)<=0:lo=lo_new
    while hi-lo>M:
        mid=lo+M*((hi-lo)//(2*M));v=F(mid,q,W,Y,alpha,h,c)
        if not v:return None if A%mid**c else mid
        if v<0:lo=mid
        else:hi=mid
    for z in {lo,hi}:
        if F(z,q,W,Y,alpha,h,c)==0 and A%z**c==0:return z
    return None


def main(full=False):
    stats={8:[0,0,0],10:[0,0,0]};seen={8:[],10:[]}
    for e,s,h,c,u,J,M,X,W,A,Y in candidates():
        q=2*u*Y-1
        if not full and u not in SURV[h]:continue
        stats[h][0]+=1
        if full and (pow(2,q-1,q)!=1 or pow(3,q-1,q)!=1 or pow(5,q-1,q)!=1):continue
        q,lo,hi,pos,neg=endrow(u,h,c,A,X,W,Y)
        seen[h].append(u);stats[h][1]+=1
        require(neg<((-J)%M or M) and W-1>q,'positive A0 regime')
        for a in range(J or M,pos+1,M):
            require(possible_roots(q,lo,hi,a,W,Y,h,c,M,A) is None,('valid emitter root',e,s,h,c,u,a))
            stats[h][2]+=1
        print('closed q multiplier',h,u,'signed cells',max(0,(pos-J)//M+1),flush=True)
    print('CAP',CAP,'witness counts',stats,'full',full,'left for emitter test',seen,flush=True)
    if full:
        require(stats=={8:[1917,5,2525],10:[1727,5,314]} and all(tuple(seen[h])==SURV[h] for h in (8,10)),'finite proof diagnostics')
        print('PASS (13,618) s=534: exhaustive Euler and signed-polynomial check',flush=True)

if __name__=='__main__':main(sys.argv[1:]==['--full'])
