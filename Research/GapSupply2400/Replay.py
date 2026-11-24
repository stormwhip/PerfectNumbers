"""Self-contained integer certificate for joint emitter gap and valuation costs."""
from functools import cache
from math import gcd, isqrt, prod
import argparse
import json
from pathlib import Path

B=10**2400
ORDER=(19,7,11,31,13,3,5,17)
T=100000
HERE=Path(__file__).resolve().parent

def primes(n):
    flags=bytearray(b'\1')*(n+1); flags[:2]=b'\0\0'
    for d in range(2,isqrt(n)+1):
        if flags[d]: flags[d*d::d]=bytes((n-d*d)//d+1)
    return [i for i in range(2,n+1) if flags[i]]
PRIMES=primes(T)

def ilog(n,b):
    i=0
    while n>=b: n//=b;i+=1
    return i

@cache
def decomp(p,e):
    A=(p**(e+1)-1)//(p-1); residual=A; small={}
    for r in PRIMES:
        if residual%r==0:
            c=0
            while residual%r==0: residual//=r;c+=1
            small[r]=c
    return A,residual,small

@cache
def price(p,e):
    A,U,small=decomp(p,e); banned=ORDER[:ORDER.index(p)]
    G=ilog(U,(T+1)**(p-1)); items=[]
    for r in PRIMES:
        if r%p!=1 or r in banned:continue
        f=small.get(r,0)
        j=1
        while True:
            m=p**j-1
            if any(pow(r,m+1,z*(r-1))==1 for z in banned): break
            d=r**max(0,m-f)
            if d>T:break
            items.append(d); f=max(f,m); j+=1
    costs=[1]
    for d in sorted(items+[T+1]*e)[:e]:costs.append(costs[-1]*d)
    return G,costs

def check(p,e,s):
    if p not in (3,5) or e<2 or e%2 or not 0<s<=e or (p==5 and 2*s<=e):return False
    pe=p**e; P=p*pe; Y=p**s; Q=2*Y-1; A=decomp(p,e)[0]
    if pe*2**p*Q**(p+1)<3**p*B:return False
    G,costs=price(p,e)
    return pe*A*Q**2*Y*costs[max(0,e-s-G)]>=B*max(P,Q)*(P//Y+4)

def main():
    ap=argparse.ArgumentParser();ap.add_argument('--output',type=Path);args=ap.parse_args()
    import sys
    sys.path.insert(0,str(HERE.parent/'EulerSourceIntervals'))
    import VerifyEulerSourceIntervals2400 as prev
    frontier=prev.open_exponents();rows=[]
    for p,es in frontier.items():
        base=prev.marginal_costs(p,max(es),PRIMES)
        for e in es:
            old=prev.analyze_exponent(p,e,base); intervals=old['extended_euler_one']; sset={i for a,b in intervals for i in range(a,b+1)}
            add=[s for s in range(e+1) if s not in sset and check(p,e,s)]
            missing=prev.intervals(sorted(set(range(e+1))-sset-set(add)))
            rows.append(dict(p=p,e=e,added=prev.intervals(add),open_one=missing,high=old['higher_euler_exponents'],closed=not missing and old['higher_euler_exponents']==[[0,e]]))
    if args.output:args.output.write_text(json.dumps(rows,separators=(',',':'))+'\n',encoding='utf-8')
    print('proved',[(r['p'],r['e']) for r in rows if r['closed']]);print('target',next(r for r in rows if r['p']==3 and r['e']==1330))

if __name__=='__main__':main()
