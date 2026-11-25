"""Independent second-digit band counter using archived transposed floor sum and direct geometric derivative."""
import sys,json,argparse
from math import lcm,gcd
from pathlib import Path
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import Independent as I

def verifier(C,c,p,f,b,s,h,lo,hi,Q):
 if hi>2*lo and b and s and (f+1)%p:
    x=lo
    while x<=hi:
        z=min(2*x-1,hi)
        if verifier(C,c,p,f,b,s,h,x,z,Q):return True
        x=z+1
    return False
 if not b or not s or (f+1)%p==0 or gcd(h*2,p)!=1:return True
 y=p**b;m=p**min(b,s);upper=I.sigma(hi,f)//(y*Q)
 if upper>=m:return True
 if not upper:return False
 T=2*h*y
 for z,mod in I.teich(p,b,f):
    assert mod==y
    a=1+2*h*((z-1)*pow(2*h,-1,y)%y);r=lo+(a-lo)%T
    if r>hi:continue
    # Horner simultaneously computes sum and derivative; no division by r-1.
    d=0;v=1
    for _ in range(f):d=(d*r+v)%m;v=(v*r+1)%(m*y)
    assert v%y==0;u=(d*(2*h))%m;w=v//y
    # v/y+u*x modulo m must be in [m-upper,m-1]; thresholds via floor jumps.
    def count(j,n):return I.Prior.fs(n,m,u,w+u*j+upper)-I.Prior.fs(n,m,u,w+u*j)
    def rec(j,n):
        q=count(j,n)
        if q==0:return False
        if q>128:return True
        if n<8:return any(C%(r+(j+i)*T)**c==0 for i in range(n) if ((w+u*(j+i))%m)>=m-upper)
        half=n//2;return rec(j,half) or rec(j+half,n-half)
    n=(hi-r)//T+1;total=count(0,n)
    if total>128:
        if total>250000:return True
        from Strip import roots
        if roots(C,c,r,T,n,m,(-u)%m,(-w)%m,upper,250000,expected=total):return True
    elif rec(0,n):return True
 return False
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('lo',type=int);ap.add_argument('hi',type=int);args=ap.parse_args();rows=json.loads((D/'Batch11.json').read_bytes());I.DIGIT=verifier;out=[]
 for r in rows:
    s=r['s'];
    if not args.lo<=s<=args.hi:continue
    w=I.check(11,s,r['euler_floor_multiplier'],65);out.append([11,718,s,w]);(D/f'IndependentDigits{args.lo}_{args.hi}.json').write_text(json.dumps(out)+'\n');print(s,w,flush=True)
