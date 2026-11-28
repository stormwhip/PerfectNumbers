"""General signed-tail/congruence bound for enumerated anonymous high Euler windows."""
from pathlib import Path
import argparse,sys,time
from math import gcd,isqrt
from functools import cache
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H))
from HighLinear import B,P,ROUGH,inputs,cell,minimum_q,floor_root,ceil_root,require
from EmitterCRT import possible_q_prime


def primes(n):
    sw=bytearray(b'\1')*(n+1);sw[:2]=b'\0\0'
    for q in range(2,isqrt(n)+1):
        if sw[q]:sw[q*q::q]=b'\0'*(1+(n-q*q)//q)
    return [q for q in range(3,n+1,2) if sw[q]]


def bounds(dat,s,h,c,u):
    X,W,A,M,_=dat;Y=P**s;q=2*u*Y-1;T=B//(X*A*q);d=h+1-c
    lo=ceil_root((2*q+2)//3,h);hi=min(floor_root(A//ROUGH,c),floor_root(T,h-c))
    Dmax=(P-1)*(A//lo**c)
    pos=(W-1)*hi**d//(q*Y);neg=(q*hi**d+(q+1)*Dmax)//(q*Y)
    return q,lo,hi,pos,neg


def signed_end(dat,s,h,c,u):
    X,W,A,M,_=dat;Y=P**s;J=(-1-(P-1)*A)*pow(Y,-1,M)%M
    def dead(j):
        q,lo,hi,a,b=bounds(dat,s,h,c,j)
        return hi<lo or (a<(J or M) and b<((-J)%M or M))
    if dead(u):return u
    lower=u;upper=2*u
    while not dead(upper):upper*=2
    while lower+1<upper:
        z=(lower+upper)//2
        if dead(z):upper=z
        else:lower=z
    require(dead(upper),'tail sign')
    return upper


@cache
def fast_compare(q):
    from flint import fmpz
    qf=fmpz(q)
    return int(pow(fmpz(2),q-1,qf))==1 and int(pow(fmpz(3),q-1,qf))==1


def verify(e,s,cap_limit=3000000,out=None,use_flint=False):
    dat=inputs(e);X,W,A,M,_=dat;Y=P**s
    require(500<=s<=536 and 2*Y-1>20000,'strict scope and sieve bound')
    shapes=cell(e,s,dat);totals=[]
    small=primes(20000)
    # For q=2Yu−1, a small prime factor is equivalent to one excluded u residue.
    residue=[(l,pow((2*Y)%l,-1,l)) for l in small if Y%l]
    for h,c in sorted(shapes):
        d=h+1;u=(minimum_q(s,h)+1)//(2*Y);step=2*d;v=signed_end(dat,s,h,c,u)
        count=max(0,(v-u+step-1)//step)
        if count>cap_limit:
            print('OPEN CAP',e,s,h,c,u,v,count,flush=True);return False
        P0=bytearray(b'\1')*count
        for l,k in residue:
            if step%l==0:
                if u%l==k:P0[:]=b'\0'*len(P0)
                continue
            j=((k-u)*pow(step,-1,l))%l
            if j<count:P0[j::l]=b'\0'*(1+(count-1-j)//l)
        n_test=passed=0;unresolved=[]
        for j,val0 in enumerate(P0):
            v0=u+j*step
            if not val0 or gcd(v0,P*19*7*11*31)>1:continue
            q=2*v0*Y-1;n_test+=1
            if use_flint:
                if not fast_compare(q):continue
            elif pow(2,q-1,q)!=1 or pow(3,q-1,q)!=1:continue
            passed+=1
            q,lo,hi,_,_=bounds(dat,s,h,c,v0)
            if possible_q_prime(q,d,lo,hi,M,1):unresolved.append(v0)
        print(e,s,h,c,'q multiplier',u,v,'raw',count,'Fermat',n_test,'surviving Fermat',passed,'unresolved',unresolved,flush=True)
        totals.append((h,c,u,v,count,n_test,passed))
        if unresolved:return False
    if out is not None:out.extend(totals)
    return True

if __name__=='__main__':
    a=argparse.ArgumentParser();a.add_argument('e',type=int);a.add_argument('ss',type=int,nargs='+');a.add_argument('--cap',type=int,default=3000000);a.add_argument('--fast-search',action='store_true');args=a.parse_args()
    require(13**min(args.ss)>20000 and 500<=min(args.ss)<=max(args.ss)<=536,'supported enumeration domain')
    for s in args.ss:
        t=time.monotonic();v=verify(args.e,s,args.cap,use_flint=args.fast_search)
        print('result',args.e,s,v,round(time.monotonic()-t,2),flush=True)
        if not v:raise SystemExit(1)
