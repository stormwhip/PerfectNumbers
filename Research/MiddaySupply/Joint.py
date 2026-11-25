"""Refine a single retained rough source by exact-supply branch and bound. Diagnostic."""
from pathlib import Path
import sys,json,argparse,math
from functools import cache
from collections import Counter
from fractions import Fraction
D=Path(__file__).resolve().parent;R=D.parent
sys.path[:0]=[str(D),str(R/'Nov25')]
import DirectedSource as old
from DirectedExperiment import CASES
U=old.U; B=U.B

def euler_floor(p,s,ban,n):
    y=p**s
    for k in range(1,2*n+1,2):
        q=2*y*k-1
        if q<5 or k%p==0 or any(k%z==0 or q%z==0 for z in ban) or any(q%z==0 and q!=z for z in U.small[:180]):continue
        if pow(2,q-1,q)==1:return q
    return 2*y*(2*n+1)-1

@cache
def context(p,e,rs):
    a=U.sig(p,e);pe=p**e;prof=U.O.profile(p);k=prof.kap
    ss=set(rs)|{r for r in U.small if a%r==0};U.primes(rs,a)
    chunks=U.chunks(p,e,ss);cost={h:(l,v*v) for h,l,v in U.blocks(p,chunks)}
    M=pe*a;V=Fraction(pe**(k+1),prof.U(e));
    for r in ss:
        c=U.val(a,r);M*=r**(old.certified_anchor_floor(p,r,c)-c);V*=U.price(p,k,r,c)
    for l,v in cost.values():M*=l;V*=v
    return a,pe,k,chunks,cost,M,V

def short(C,c,p,f,b,s,h,lo,hi,Q,cap):
    # sigma(r^f)=q p^b w; q=-1 modulo p^s, hence
    # r^(f+1)-1 + (r-1)*p^b*w = 0 modulo p^(b+s).
    # Only use simple roots when b>0 and p does not divide f+1.
    if not b or (f+1)%p==0 or not cap:return True
    y=p**s; t=p**b; mod=t*y; W=U.sig(hi,f)//(Q*t)
    if W>cap:return True
    dh=2*h; d=math.gcd(dh,mod); stride=math.lcm(dh,mod)
    for w in range(1,W+1,2):
        if w%p==0:continue
        for a in range(2,p):
            if pow(a,f+1,p)!=1:continue
            z=a;m=p
            while m<mod:
                m=min(m*m,mod)
                fun=pow(z,f+1,m)-1+(z-1)*t*w
                der=(f+1)*pow(z,f,m)+t*w
                z=(z-fun*pow(der,-1,m))%m
            if (z-1)%d:continue
            res=(z+mod*((1-z)//d)*pow(mod//d,-1,dh//d))%stride
            first=lo+(res-lo)%stride
            if first>hi:continue
            if hi-first>=8*stride:return True
            if any(C%r**c==0 for r in range(first,hi+1,stride)):return True
    return False

@cache
def limited_discount(p,e,rem):
    prof=U.O.profile(p)
    # Multiplicative 0/1 knapsack: each exceptional ordinary prime can occur once;
    # when activated its order term t consumes at least t remaining valuation units.
    bag={0:Fraction(1)}
    for t,r,o in prof.non_euler:
        if t>rem:continue
        ratio=Fraction(p**(prof.kap*t),r**(o-1))
        for used,d in tuple(bag.items()):
            if used+t<=rem:bag[used+t]=max(bag.get(used+t,1),d*ratio)
    return max(bag.values())

@cache
def kernelfloor(C,h,bits):
    from SquareWitness import floor
    return floor(C,h,bits)[0]

def run(p,e,rs,s,n,split=True,cap=0,leafcheck=None,reserve=False,kernel=0):
    a,pe,k,chunks,cost,M,V=context(p,e,rs);y=p**s;P=pe*p;Q=euler_floor(p,s,U.O.tb.forbidden(p),n); stats=Counter();surv=[]
    def check(C,c,pp,f,L,H,b,h,mode):
        g=f-c; l,v=cost.get(h,(1,1));u=0
        Q0=Q
        if p==11 and e==718 and s>=519 and f==4:
            from OrderFloor import order_floor
            Q0=max(Q,order_floor(p,s,5,16000))
            if c==2 and 526<=s<=529:
                from EulerPrefix import bound
                Q0=max(Q0,bound(p,e,s,2,5,C,600000 if s==527 else 120000))
        def descend(i,j):
            # Upper endpoint on b pays back more valuation; lower endpoint on b forces stronger congruence/gap.
            nonlocal u
            Q=Q0
            u+=1;stats['intervals']+=1
            z=y*p**i;v0=V/(v if i==0 else 1)
            if reserve:v0*=Fraction(U.O.profile(p).U(e),limited_discount(p,e,e-s-i))
            lo=max(L,U.root(2*Q*p**i//3,f)+1)
            th=z*Q//(max(P,Q)*(P//z+4));
            if g:lo=max(lo,U.root(th,g)+1)
            elif th>=1:return False
            hi=min(H,U.root((B*(y*p**j)**k*v0.denominator)//(Q*v0.numerator),f),U.root((B*p**j)//(pe*a),2*f-c))
            # actual incoming product: p^e A r^{f-c} sigma(r^f)/p^j divides N (r coprime sigma).
            if g:
                hi=min(hi,U.root(B*(l if g%2 else 1)//(M*Q),g))
                if kernel and g%2==0 and U.root(C,2)**2!=C:
                    sf=kernelfloor(C,h,kernel);hi=min(hi,U.root(B*l//(M*Q*sf),g))
            if lo>hi:return False
            # For small spans, include exact b even at the lower endpoint; no filtering of primality.
            if i==j or not split:
                if genuine(C,c,pp,f,lo,hi,i,h,16) and (i!=j or short(C,c,p,f,i,s,h,lo,hi,Q,cap)) and (leafcheck is None or leafcheck(genuine,C,c,pp,f,lo,hi,i,h,16)):
                    surv.append([s,h,c,f,i,j,str(lo),str(hi)]);return True
                return False
            # Large groups can often be pruned via the interval's weakest CRT; binary split only plausible ones.
            if not genuine(C,c,pp,f,lo,hi,i,h,16):return False
            m=(i+j)//2
            return descend(i,m) or descend(m+1,j)
        return descend(b,e-s) if b<=e-s else False
    genuine=U.cand
    U.cand=check
    try:row=old.run(p,e,rs,min_s=s,max_s=s)
    finally:U.cand=genuine
    return dict(p=p,e=e,s=s,guard=row['guard'],open=row.get('open'),first=surv[:1],stats=dict(stats),euler_floor_multiplier=(Q+1)//(2*y))

if __name__=='__main__':
    ap=argparse.ArgumentParser();ap.add_argument('p',type=int);ap.add_argument('s',nargs='+',type=int);ap.add_argument('--sieve',default=128,type=int);ap.add_argument('--save');ap.add_argument('--cap',default=0,type=int);ap.add_argument('--reserve',action='store_true');ap.add_argument('--kernel',type=int,default=0);op=ap.parse_args();p,e,rs=next(x for x in CASES if x[0]==op.p);out=[]
    for s in op.s:
        row=run(p,e,tuple(rs),s,op.sieve,cap=op.cap,reserve=op.reserve,kernel=op.kernel);out.append(row);print(p,e,s,row['open'],row['stats'],row['euler_floor_multiplier'],flush=True)
        if op.save:(D/op.save).write_text(json.dumps(out,indent=1)+'\n')
