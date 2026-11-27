"""Independent audit of the small-prime residual budget leaves of B's f=66 packet."""
import gzip,json
from math import gcd,isqrt
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from BDomainAudit import B,BAN,Z,state,v,sigma

Q=983


def small_options(P,limit):
    assert sum(e%2 for p,e in P)==1
    X,S,D,why=state(P)
    assert why is None
    need=dict(P)[Q]-v(S,Q)
    cap=B//(X*D)
    # Nonfixed powers have even exponent, so f+1 is odd. Positive supply requires
    # f+1 divisible by Q or a nontrivial odd multiplicative order dividing Q-1.
    odd_orders=[k for k in range(3,Q,2) if (Q-1)%k==0]
    assert odd_orders==[491] and need>0 and (limit+1)**490>B//X
    for r in range(3,limit+1,2):
        if r in (*dict(P),*BAN) or any(r%d==0 for d in range(2,isqrt(r)+1)):
            continue
        c=v(D,r)
        # Here the only possible odd order >1 is 491. Iterate only corresponding
        # exponent progressions instead of scanning and testing every even exponent.
        if r%Q==1: order=Q
        elif pow(r,491,Q)==1: order=491
        else: continue
        k=max(1,(c+order)//order)
        if k%2==0:k+=1
        opts=[]
        while True:
            e=k*order-1
            cost=r**(e-c)
            if cost>cap:break
            T=sigma(r,e)
            u=v(T,Q)
            if u<=need and gcd(T,Z)==1:
                opts.append((e,u,cost))
            k+=2
        if opts:yield r,opts


def audit(P,t):
    X,S,D,why=state(P)
    a=dict(P)[Q]-v(S,Q)
    cap=B//(X*D)
    opts=list(small_options(P,t['bound']))
    if t['type']=='supplier-split':
        assert a==1
        keys={f'{p}:{e}' for p,lst in opts for e,u,c in lst if u==1 and state(P+((p,e),))[3] is None}
        assert keys==t['cases'].keys()
        print('SUPPLIERS',P,sorted(keys),flush=True)
        return
    # Work in the multiplicative monoid of positive costs, discarding all sums
    # requiring more than the global residual cap. A source is usable at most once.
    attainable={0:1}
    for _,lst in opts:
        full=dict(attainable)
        for e,u,c in lst:
            for j,cost in attainable.items():
                if j+u<=a and cost*c<=cap:
                    full[j+u]=min(full.get(j+u,cap+1),cost*c)
        attainable=full
    assert a not in attainable
    print('BUDGET',P,'need',a,'available_supplier_bases',len(opts),'joint_supply_max',max(attainable),flush=True)


if __name__=='__main__':
    assert __debug__
    with gzip.open('Research/Night2400/B/Fiber66.json.gz','rt') as f:d=json.load(f)
    total=0
    def visit(P,t):
        global total
        if t['type']=='split':
            for e,child in t['cases'].items():visit(P+((t['q'],int(e)),),child)
        elif t['type'] in ('supplier-split','order-budget'):
            assert t['q']==Q
            audit(P,t);total+=1
    visit(((3,12),(797161,66)),d['tree']);assert total==9
