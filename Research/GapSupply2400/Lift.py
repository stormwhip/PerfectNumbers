"""Order-restricted square-divisor audit for the joint valuation bound."""
import argparse
import json
from functools import cache
from math import gcd,lcm,prod
from pathlib import Path
import Replay as v

@cache
def phi(p,h):
    n=p**h-1
    for d in range(1,h):
        if h%d==0:n//=phi(p,d)
    return n

@cache
def free_block(p,h,steps):
    U=phi(p,h)
    for r in v.PRIMES:
        while U%r==0:U//=r
        if U==1:return 0
    step=lcm(2*h,p); start=1+((v.T-1)//step+1)*step
    floor=start+step*steps
    for r in range(start,floor,step):
        if U%(r*r)==0:
            floor=r;break
    return v.ilog(U,floor**(p-1))

@cache
def data(p,e,steps):
    if e+1>v.T:raise ValueError('order exception not sieved')
    A,U,small=v.decomp(p,e); G=sum(free_block(p,h,steps) for h in range(2,e+2) if (e+1)%h==0)
    # Known and unknown blocks are coprime after sieving since h <= T.
    prem={r:r**(c%2) for r,c in small.items() if r%p!=1}
    return G,prod(prem.values())//max(prem.values(),default=1)

def run(p,e,steps):
    from VerifyEulerSourceIntervals2400 import analyze_exponent,marginal_costs
    base=analyze_exponent(p,e,marginal_costs(p,e,v.PRIMES));pe=p**e;P=p*pe;A=v.decomp(p,e)[0];G,premium=data(p,e,steps);costs=v.price(p,e)[1]
    missing=[]
    for s in range(e+1):
        if any(lo<=s<=hi for lo,hi in base['extended_euler_one']):continue
        Y=p**s;Q=2*Y-1
        if (not s or (p==5 and 2*s<=e) or pe*2**p*Q**(p+1)<3**p*v.B or
            pe*A*Q**2*Y*costs[max(0,e-s-G)]*premium<v.B*max(P,Q)*(P//Y+4)):
            missing.append(s)
    from VerifyEulerSourceIntervals2400 import intervals
    return dict(p=p,e=e,G=G,premium=premium,open_one=intervals(missing),high=base['higher_euler_exponents'],closed=not missing and base['higher_euler_exponents']==[[0,e]])

if __name__=='__main__':
    import sys
    sys.path.insert(0,str(v.HERE.parent/'EulerSourceIntervals'))
    from VerifyEulerSourceIntervals2400 import open_exponents
    ap=argparse.ArgumentParser();ap.add_argument('--steps',type=int,default=10000);ap.add_argument('--output',type=Path);args=ap.parse_args()
    if args.steps<0:ap.error('negative steps')
    rows=[run(p,e,args.steps) for p,es in open_exponents().items() for e in es if (p==3 and e>=1180) or (p==5 and e>=640)]
    if args.output:args.output.write_text(json.dumps(rows,separators=(',',':'))+'\n')
    print('proved',[(r['p'],r['e']) for r in rows if r['closed']]);print('1302', next(r for r in rows if r['p']==3 and r['e']==1302))
