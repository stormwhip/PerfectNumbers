"""Exact two-target Euler-square price cuts for canonical (7,48), no network."""
from functools import cache
from fractions import Fraction
from math import gcd, isqrt, prod
from pathlib import Path
import sys
H=Path(__file__).resolve().parent
sys.path[:0]=[str(H),str(H.parents[1]/'RootFiveNext')]
from Propagation import sigma, val, part, partition, outside_progression, odd_price, screened_prime
from PrimeCheck import prime64

P=7; T=6106505825833677713; B=10**2400
SMALL=(29,3529,4733,1074473,13473433)
ROOTS={2:(61,1965401149,518019223567,600424816906741), 10:(617,531983)}
PIVOT={2:518019223567, 10:531983}
WEIGHT={2:2, 10:10}
PUBLISH={2:tuple(range(76,97,2)),10:tuple(range(104,171,2))}


def state(rows):
    x=prod(p**e for p,e in rows)
    ss=[sigma(p,e) for p,e in rows]
    ds=[f//part(f,x) for f in ss]
    d=prod(ds)
    c={p:e-sum(val(s,p) for s in ss) for p,e in rows}
    bad=d%19==0 or x*d>B or min(c.values())<0 or prod(ss)>2*x
    return x,ss,ds,d,c,bad


def domain(fixed,q):
    x,ss,ds,d,c,bad=state(fixed)
    assert not bad and d%q==0 and q%4==3
    v=val(d,q); h=v
    out=[]
    while x*(d//q**v)*q**h<=B:
        if h%2==0 and not state(fixed+[(q,h)])[-1]:out.append(h)
        h+=1
    return out,h


@cache
def cost(s,c,w,fixed):
    def maybe(x):
        if x in fixed or x<3 or x%2==0:return False
        q=isqrt(x)
        # Ordinary prime or the Euler square. A square's underlying q is
        # prime, 1 mod 4, and cannot occur among the fixed ordinary rows.
        return screened_prime(x) or q*q==x and q%4==1 and q not in fixed and screened_prime(q)
    U,n,out,loss=odd_price(s,c,w,1,B,5100,maybe)
    assert out==0
    return U


@cache
def credit(z,r,w):
    out=None; umax=vmax=0; x=z*z
    while x<=B:
        s=(z*x-1)//(z-1); u=val(s,T); v=val(s,r)
        a=Fraction(x,T**(6*u)*r**(w*v))
        out=a if out is None else min(a,out)
        umax=max(umax,u); vmax=max(vmax,v); x*=z*z
    assert out is not None
    return out,umax,vmax


def certify(f,h,extra=()):
    r=PIVOT[f]; w=WEIGHT[f]; rows=[(P,48),(T,f),(r,h)]
    X,S,DS,D,c,bad=state(rows); assert not bad
    fixed=(P,T,r,19); assert c[T]<=f-1 and c[r]<=h
    # The full odd support of T-1 may be used, not just powers of 7.
    assert gcd(T*((T-1)//16),r*((r-1)//2))==1
    U=cost(T,f-1,6,fixed)*cost(r,h,w,fixed)
    un,ud=U.as_integer_ratio()
    labels=sorted((set(SMALL)|set(ROOTS[f])|set(extra))-{r})
    assert all(z not in fixed and D%z==0 and prime64(z) for z in labels)
    blocks=partition(S,X,labels)
    assert prod(a for a,row in blocks)==D
    M=max(a for a,row in blocks)
    credits=[(z,val(D,z),credit(z,r,w)) for z in labels]
    tp=[T**i for i in range(6*c[T]+1)]; rp=[r**i for i in range(w*c[r]+1)]
    stats=[0,0,0]
    for i in range(c[T]+1):
      for j in range(c[r]+1):
        m=tp[i]*rp[j]; a=2*m-1; Q=max(5,a); mod=4*m
        u=c[T]-i; v=c[r]-j
        safe=[(z,e,K) for z,e,K in credits if z%mod!=a or z<Q]
        G=prod((K[0] for z,e,K in safe),start=Fraction(1)); gn,gd=G.as_integer_ratio()
        F=prod(z for z,e,K in safe if e%2)
        if X*Q*tp[6*u]*rp[w*v]*gn*ud>B*un*gd:
            stats[0]+=1;continue
        # A positive j and r ≡ 3 mod 4 make r a nonresidue at q;
        # every prime divisor of the ordinary sigma(r^h) sees odd order at r.
        assert r%4==3
        assert all(outside_progression(z,a,mod,Q,B//X) for z in (DS if j==0 else DS[:2])),(f,h,i,j,'Euler interior')
        if X*D*F*Q>B:
            stats[1]+=1;continue
        # Do NOT require q^1. Any q^a has an ordinary emitter when q∤D;
        # leave the distinct q² price atom (if a>1) among the other atoms.
        um=max([0]+[K[1] for z,e,K in safe]); vm=max([0]+[K[2] for z,e,K in safe])
        for a1 in range(u+1):
          for b1 in range(v+1):
            distinct=a1>um or b1>vm
            J=2*Q*tp[a1]*rp[b1]
            if X*D*Q*J*(F if distinct else 1)>3*B*M:continue
            gn1,gd1=(gn,gd) if distinct else (1,1)
            assert X*Q*J*tp[6*(u-a1)]*rp[w*(v-b1)]*ud*gn1>3*B*un*gd1,(f,h,i,j,a1,b1)
        stats[2]+=1
    return stats


def main():
    assert __debug__
    F=572161; J=1944734959
    assert all(prime64(z) for z in (P,T,F,J,*SMALL,*ROOTS[2],*ROOTS[10]))
    assert T-1==16*7**3*F*J and F>5100 and J>5100
    assert P!=19 and all(T!=z for z in SMALL) and prod(SMALL)*T==sigma(P,48)
    assert prod(ROOTS[2])==sigma(T,2) and sigma(T,10)%prod(ROOTS[10])==0
    for f,expect in ((2,96),(10,170)):
        r=PIVOT[f]; live,tail=domain([(P,48),(T,f)],r)
        assert live==list(range(2,expect+1,2)) and tail=={2:195,10:344}[f]
        W=[0,0,0]
        for h in PUBLISH[f]:
            a=certify(f,h)
            W=[x+y for x,y in zip(W,a)]
        print('PASS (7,48), first',f,'ordinary anchor',r,'direct',len(live),'tail',tail,'cuts',PUBLISH[f],'Euler windows',W,flush=True)

if __name__=='__main__':main()
