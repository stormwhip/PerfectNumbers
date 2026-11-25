"""Search-only support-bound calculation; exact Python alpha. Optional group child tests. Takes e mask id, fixed 3 exponent.
"""
from Verify import *
from math import prod,gcd
from sympy import primerange, n_order
from functools import cache
B=10**2400
@cache
def order(r,p):
    if r==p:return 0
    if r%p==1:return p
    return int(n_order(r%p,p))

def run(e,idx,h3):
    H,eu=RULES[idx];s=set(H);fx={19:e,3:h3,eu:1};a0=prod(ab(r,f) for r,f in fx.items());D={};M=prod(p**f for p,f in fx.items());T=1
    for r,h in fx.items():
        n=sigma(r,h);n//=n&-n;T*=n
        for p,v in factors(n).items():D[p]=D.get(p,0)+v
    pool=sorted((set(D)|s)-set(fx));lo={p:2*((max(D.get(p,0),1)+1)//2) for p in pool};cap={p:(B.bit_length()//(p.bit_length()-1)) for p in pool};ban=set(P8)-s
    for p in fx:
        if D.get(p,0)>fx[p]:return 'incoming'
        if D.get(p,0)==fx[p]:ban.add(p)
    known=prod(pool)*prod(fx)
    def clean(n):
        while (g:=gcd(n,known))>1:n//=g
        return n
    M*=clean(T);B0=B//M
    for _ in range(10):
        K=a0*prod(ab(r,l) for r,l in lo.items())
        if K>=2:return 'abundance'
        oth=2/(2-K);lim=min(20000,int(oth)-2) # K*(1+1/p)>2 when p<K/(2-K)=oth-1
        obvious={p for p in primerange(3,lim+1) if p not in pool and p not in fx};ban|=obvious
        mins={};opts={};newlo={}
        for r in pool:
            orders={order(r,p) for p in ban}-{0};gs=[f for f in range(lo[r],cap[r]+1,2) if all((f+1)%o for o in orders)]
            if not gs:return 'no exponent'
            newlo[r]=gs[0];off=min(gs[0]+150,cap[r]);mm=[]
            for h in gs:
                if h>off:
                    mm.append(r**h);break
                z=clean(sigma(r,h));mm.append(r**h*z)
            mins[r]=min(mm);opts[r]=gs[:5]
        print('e',e,'mask',idx,'h3',h3,'alpha',float(K),'ban limit',lim,'lo',newlo,'floor mass',len(str(M*prod(mins.values())))-1,flush=True)
        if M*prod(mins.values())>B:return 'size'
        if newlo==lo:break
        lo=newlo
    return opts
if __name__=='__main__':print(run(*map(int,sys.argv[1:])))
