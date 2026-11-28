"""Integer forest with a separately charged exterior-to-labels Euler prime q.

Inputs: actual odd perfect prefix P and exact Euler congruence q=2m-1 mod 4m.
All forest vertices must be incompatible with that class. The quantity returned
is a lower bound; see Proof.md. Does not require exponent one at q.
"""
from functools import cache
from math import gcd, prod

BOUND=10**2400

def reserve(P,roots,owners,head,bad,m,with_trace=False,exact_one=False):
    X=prod(p**h for p,h in P)
    S=prod((p**(h+1)-1)//(p-1)//(1+h%2) for p,h in P)
    Q=2*m-1; W=4*m; assert Q>1 and all(h%2==0 for p,h in P)
    K=set(roots); V=K|{p for p,_ in owners}; assert all(p%W!=Q for p in V|{p for p,_ in P})
    F=prod(bad)
    def strip(n,pool):
        while (g:=gcd(n,pool))>1:n//=g
        return n
    def val(n,p):
        h=0
        while n%p==0:n//=p;h+=1
        return h
    @cache
    def rebate(Z):
        best=Z; low=Q; u=Z%W
        while low<=Z:
            u=u*Q%W  # Q^2=1 mod W
            a=u or W
            top=Z//low
            if a<=top and (a+W<=top or Z%a==0):best=min(best,a)
            if exact_one:break
            low*=Q
        return best
    D=strip(S,X); left=strip(D,prod(roots)); pool=X*D*prod(p for p,_ in owners)
    kids={p:[] for p in V}
    for p,g in owners:kids[g].append(p)
    kp={p:prod(v) for p,v in kids.items()}
    trace={}
    @cache
    def solve(p,v):
        h=v+v%2; cost=BOUND+1; done=0; node=None
        while (a:=p**h)<cost and done<head:
            Z=(p*a-1)//(p-1)
            if gcd(Z,F)==1:
                done+=1
                rem=strip(Z,pool); b=a*rebate(rem)
                child=[(q,val(Z,q)) for q in kids[p] if Z%q==0] if gcd(kp[p],Z)>1 else []
                for q,e in child:b*=solve(q,e)
                if b<cost:cost=b; node=(h,rem,child)
            h+=2
        a=p**h
        if a<cost:cost=a;node=(h,0,[])
        if with_trace:trace[p,v]=node or (h,0,[])
        return cost
    root=[(p,val(D,p)) for p in roots]
    value=X*Q*rebate(left)*prod(solve(p,v) for p,v in root)
    if not with_trace:return value
    def walk(p,v):
        h,rem,cs=trace[p,v]
        yield p,h,rem
        for a,b in cs:yield from walk(a,b)
    return value,[x for p,v in root for x in walk(p,v)]
