"""Progression sieve + strengthened shared A capacity, for five exponents. Standard library only.
Usage: python -I -S -B joint-lab/Base.py [snapshot]. Outputs rigorous scaled natural logs.
"""
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Joint import *

def check_range(e,hi):
    d=6*(e+1);assert prime(e+1);end=(hi-1)//d+1;cnt=0
    for b in range(1,end,500000):
        n=min(end-b,500000);v=bytearray([1])*n
        for p in small:
            if p>1200:break
            if d%p==0:continue
            # All actual candidates 1+k*d > p here.
            i=(-b-pow(d,-1,p))%p
            if i<n:v[i:n:p]=bytes((n-1-i)//p+1)
        for i,x in enumerate(v):
            if x:
                r=1+(b+i)*d;assert pow(3,e+1,r)!=1 or not prime64(r),(e,r);cnt+=1
    return cnt

def envelope(e,RA):
    # Global E3 b=0. External U>=0. No s-window premise needed.
    P=3**(e+1);pe=P//3;A=(P-1)//2;best=[10**20]*2;worst=[None]*2
    for s in range(1,e+1):
        y=3**s;q=2*y-1;delta=P//y;srcE=lo(2*q)-hi(3);srcI=max(0,lo(y*q)-hi(P*(delta+4)));bare=lo(pe*A*q)
        for i in range(e-s+1):
            cost=bare+(e-s-i)*4*lo(3);d=2*i*lo(RA)-hi(A)
            for k,z in enumerate([srcE+max(0,d),max(srcI,max(srcI,srcE)+d)]):
                if cost+z<best[k]:best[k]=cost+z;worst[k]=(s,i)
    return best,worst
if __name__=='__main__':
    assert __debug__
    for ee in [1162,1108,990,970,856]:
        R=10**11;cnt=check_range(ee,R);z,arg=envelope(ee,R);print(json.dumps(dict(e=ee,R=R,surviving_progression_checks=cnt,base_nanonats=z,base_decimal_floors=[v//hi(10) for v in z],arg=arg)),flush=True)
