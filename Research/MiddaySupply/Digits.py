"""Batch all unknown w through the second p-adic digit of sigma_f(r).
Exact necessary test. No dependence on lattice packages."""
from pathlib import Path
from math import gcd,lcm
import sys,json,argparse
from functools import lru_cache
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import Joint as J
U=J.U

def floors(n,m,a,b):
    v=0
    while n:
        q,a=divmod(a,m);w,b=divmod(b,m);v+=q*n*(n-1)//2+w*n
        top=a*n+b
        if top<m:return v
        n,b=divmod(top,m);m,a=a,m
    return v

def digit(C,c,p,f,b,s,h,lo,hi,Q,cap=65):
    if hi>2*lo and b and s and (f+1)%p:
        a=lo
        while a<=hi:
            v=min(hi,2*a-1)
            if digit(C,c,p,f,b,s,h,a,v,Q,cap):return True
            a=v+1
        return False
    if not s or not b or (f+1)%p==0:return True
    H=p**b; M=p**min(s,b); modulus=H*M
    W=U.sig(hi,f)//(Q*H)
    if W==0:return False
    if W>=M:return True
    # gcd(p,2h) can be nontrivial; don't silently discard that case.
    if gcd(p,2*h)!=1:return True
    for z,T in U.lifts(p,h,b,f) or []:
        first=lo+(z-lo)%T
        if first>hi:continue
        n=(hi-first)//T+1
        # p cannot divide first-1 for the nontrivial simple Teich roots.
        inv=pow(first-1,-1,modulus);v=(pow(first,f+1,modulus)-1)*inv%modulus
        assert v%H==0 and T%H==0
        deriv=((f+1)*pow(first,f,M)-(v%M))*inv%M
        alpha=-deriv*(T//H)%M;beta=-(v//H)%M
        # w positive and odd; restrict to 1..W. The interval includes even w,
        # safely allowing some impossible residues.
        def count(i,n):
            c0=alpha*i+beta
            return floors(n,M,alpha,c0-1)-floors(n,M,alpha,c0-1-W)
        def find(i,n,hits):
            if hits==0:return False
            if hits>cap:return True
            if n==1:return C%(first+i*T)**c==0
            n0=n//2;left=count(i,n0)
            return find(i,n0,left) or find(i+n0,n-n0,hits-left)
        hits=count(0,n)
        if hits>cap:
            if hits>250000:return True
            from Strip import roots
            if roots(C,c,first,T,n,M,alpha,beta,W,250000,expected=hits):return True
        elif find(0,n,hits):return True
    return False

def go(p,ss,out,cap):
    p,e,rs=next(t for t in J.CASES if t[0]==p);orig=J.short
    def strengthened(*a):return digit(*a[:-1],cap) and orig(*a)
    J.short=strengthened;rows=[]
    for s in ss:
        row=J.run(p,e,tuple(rs),s,128,cap=65);rows.append(row);print(p,e,s,row['open'],[(x[2:6],len(x[6]),len(x[7])) for x in row['first']],flush=True);(D/out).write_text(json.dumps(rows)+'\n')
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('p',type=int);a.add_argument('s',nargs='+',type=int);a.add_argument('--out',required=True);a.add_argument('--cap',type=int,default=128);o=a.parse_args();go(o.p,o.s,o.out,o.cap)
