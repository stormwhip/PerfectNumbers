"""Exact CRT emitter/paid-overlap supplement for (7,48). Standard library only."""
from functools import cache
from fractions import Fraction
from math import gcd,lcm,prod
from pathlib import Path
import sys
sys.path.insert(0,str(Path(__file__).resolve().parent))
from Propagation import divisors,hensel,introot,partition,outside_progression,part,val,sigma
import Verify48Price as V

P,T,B=V.P,V.T,V.B
EXTRA={2:{74:()},10:{92:(97,109,127,30109),98:(11,23,37,73,97,109,127,30109,143229911757857),100:(),102:()}}

@cache
def cyclo(x,k):
    a=x**k-1; b=prod(cyclo(x,j) for j in divisors(k)[:-1]); assert a%b==0
    return a//b

@cache
def single(s,u):
    if not u:return ((0,1,1),)
    out=[]
    if s**u<=5100:out.append((1,s,s**u))
    for o in range(3,5101,2):
        if (s-1)%o:continue
        z=0;m=1
        while o*m<=5100 and z<u:
            M, rr=next(x for j,x in enumerate(hensel(s,o,u-z),1) if j==u-z)
            out.extend((r,M,o*m) for r in rr if max(3,r)**(o*m-1)<=B)
            z+=1;m*=s
    return tuple(out)

@cache
def merged(s,r,u,v):
    out=[]
    for x,m,I in single(s,u):
      for y,n,J in single(r,v):
        K=lcm(I,J); e=max(2,K-1)
        if K>5100: continue
        a=(x+m*((y-x)*pow(m,-1,n)%n))%(m*n) if n>1 else x
        M=m*n; first=3+(a-3)%M
        if first**e<=B:out.append((a,M,first,e))
    return tuple(out)

@cache
def paid_cap(D,cells,max_power):
    """Upper bound the share z^v_z(D), not the full emitter power."""
    if D<=1:return 1
    out=1
    for a,m,z0,e in cells:
        if z0>D or z0**e>max_power:continue
        top=min(D,introot(max_power,e))
        if top<z0:continue
        if (top-z0)//m<1800:
            # Scan ALL positive representatives of a coprime odd source.
            for z in range(z0,top+1,m):
                if z%2 and D%z==0:out=max(out,z**val(D,z))
            continue
        assert gcd(a,m)==1
        inv=pow(a,-1,m) if m>1 else 0
        R=D; low=z0
        # Do not assume that the exponent of paid overlap is the emitter's
        # minimal legal exponent, or that D is squarefree.
        while low<=D:
            R=R*inv % m if m>1 else 1
            k=R or m
            if k<=D//low:out=max(out,D//k)
            low*=z0
    return out


def check(f,h,extras):
    r=V.PIVOT[f]; w=V.WEIGHT[f]; rows=[(P,48),(T,f),(r,h)]
    X,SS,DS,D,c,bad=V.state(rows); assert not bad
    cert=sorted((set(V.SMALL)|set(V.ROOTS[f])|set(extras))-{r})
    assert all(V.prime64(z) and D%z==0 and z not in (P,T,r,19) for z in cert)
    assert all(sigma(r,h)%z==0 for z in extras)
    ss=[SS[0],SS[1]]+[cyclo(r,k) for k in divisors(h+1)[1:]]
    assert prod(ss)==prod(SS)
    small=[x//part(x,X) for x in ss]
    blocks=partition(small,1,cert)
    assert prod(x for x,row in blocks)==D
    named={z**val(D,z):z for z in cert}
    assert c[T]<=f-1 and c[r]<=h and gcd(T*((T-1)//16),r*((r-1)//2))==1
    U=V.cost(T,f-1,6,(P,T,r,19))*V.cost(r,h,w,(P,T,r,19));un,ud=U.as_integer_ratio()
    tp=[T**i for i in range(6*c[T]+1)];rp=[r**i for i in range(w*c[r]+1)]
    facts=[(z,val(D,z),V.credit(z,r,w)) for z in cert]
    stat=[0,0,0,0,0,0]
    for i in range(c[T]+1):
      for j in range(c[r]+1):
        m=tp[i]*rp[j]; q0=2*m-1; Q=max(5,q0); modulus=4*m
        u=c[T]-i;v=c[r]-j
        safe=[(z,e,k) for z,e,k in facts if z<Q or z%modulus!=q0]
        G=prod((k[0] for z,e,k in safe),start=Fraction(1));gn,gd=G.as_integer_ratio()
        F=prod(z for z,e,k in safe if e%2);base=X*D*Q
        if X*Q*tp[6*u]*rp[w*v]*gn*ud>B*un*gd:stat[0]+=1;continue
        assert r%4==3
        assert all(outside_progression(z,q0,modulus,Q,B//X) for z in (small if not j else small[:2])),(f,h,i,j,'inside')
        if base*F>B:stat[1]+=1;continue
        ut=max([0]+[k[1] for z,e,k in safe]);vr=max([0]+[k[2] for z,e,k in safe])
        gross=B//(X*Q)
        for a in range(u+1):
          for b in range(v+1):
            str_rem=(a>ut or b>vr); f1=F if str_rem else 1; gn1,gd1=(gn,gd) if str_rem else (1,1)
            price=X*Q*tp[6*(u-a)]*rp[w*(v-b)]*ud*gn1; rhs=3*B*un*gd1
            fee=2*Q*tp[a]*rp[b]
            if fee*price>rhs:stat[2]+=1;continue
            cells=merged(T,r,a,b)
            if not cells:stat[3]+=1;continue
            fee=max(fee,3*min(z**g for x,m,z,g in cells)-1)
            # "fee < 3 z^g": subtract one from the nonstrict size cap.
            if fee*price>rhs or fee>3*gross:stat[3]+=1;continue
            for C in [1]+[z for z,row in blocks]:
                if str_rem and C in named:continue
                local=tuple(k for k in cells if C not in named or named[C]>=k[2] and named[C]%k[1]==k[0])
                if not local:continue
                M=paid_cap(C,local,gross)
                if base*f1*fee>3*B*M:stat[4]+=1;continue
                # We multiply two bounds only as a bound for N².
                assert base*f1*fee*fee*price>3*B*M*rhs,(f,h,i,j,a,b,C)
                stat[5]+=1
    return stat


def main():
    assert __debug__
    assert all(V.prime64(q) for q in (P,T,572161,1944734959,*V.SMALL,*V.ROOTS[2],*V.ROOTS[10]))
    assert T-1==16*7**3*572161*1944734959 and 572161>5100 and 1944734959>5100
    assert prod(V.SMALL)*T==sigma(P,48) and prod(V.ROOTS[2])==sigma(T,2)
    assert sigma(T,10)%prod(V.ROOTS[10])==0
    args=[tuple(map(int,s.split(':'))) for s in sys.argv[1:]] or [(f,h) for f in EXTRA for h in EXTRA[f]]
    for f,h in args:
        assert h not in V.PUBLISH[f]
        assert h in V.domain([(P,48),(T,f)],V.PIVOT[f])[0]
        print('PASS 48 overlap',f,h,check(f,h,EXTRA[f][h]),flush=True)

if __name__=='__main__':main()
