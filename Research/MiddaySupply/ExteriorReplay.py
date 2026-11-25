"""Independent, conservative exterior q-emitter witness search."""
from pathlib import Path
import sys
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import Independent as I

def possible(p,s,k0):
    pe,A,C,k,M,V,extra,disc=I.basis(p);e=I.CASES[p][0];Q=I.lower_q(p,s,k0);y=p**s;bound=I.B//(M*Q)
    # Sufficiently large f is impossible as r>=3 and r^f<=bound.
    for f in range(2,I.Prior.logi(bound,3)+1,2):
        def band(i,j):
            lower=max(3,I.root(2*Q*p**i//3,f)+1);upper=min(I.root(bound,f),I.root(I.B*p**j//(pe*A),2*f),I.root((I.B*p**((s+j)*k)*V.denominator)//(Q*V.numerator),f))
            if lower>upper:return False
            classes=[]
            for z,m in I.teich(p,i,f):
                T=2*m;r=lower+(z-lower)%m
                if r%2==0:r+=m
                if r<=upper:classes.append((r,T))
            if not classes:return False
            if i<j:
                t=(i+j)//2;return band(i,t) or band(t+1,j)
            for r,T in classes:
                n=(upper-r)//T+1
                if n<=128:
                    for a in range(r,upper+1,T):
                        if a==p or A%a==0 or a in I.Prior.O.tb.forbidden(p):continue
                        if a<2**64 and not I.Prior.O.G.is_prime_det64(a):continue
                        v=I.sigma(a,f)
                        if I.vp(v,p)!=i or any(v%u==0 for u in I.Prior.O.tb.forbidden(p)):continue
                        top=min(v//p**i,I.B//(M*a**f),I.B*(y*p**i)**k*V.denominator//(V.numerator*a**f));v//=p**i
                        if top<Q:continue
                        mod=4*y;first=Q+(2*y-1-Q)%mod
                        if first>top:continue
                        if top-first<=128*mod:
                            if any(v%q==0 for q in range(first,top+1,mod)):return True
                            continue
                        bot=(v+top-1)//top;last=v//Q;bot+=(v*pow(2*y-1,-1,mod)-bot)%mod
                        if last-bot<=128*mod:
                            if any(v%j==0 for j in range(bot,last+1,mod)):return True
                            continue
                        return True
                    continue
                if not i or (f+1)%p==0:return True
                m=p**min(i,s);t=p**i;W=I.sigma(upper,f)//(Q*t)
                if W>=m:return True
                if W==0:continue
                d=0;v=1
                for _ in range(f):d=(d*r+v)%m;v=(v*r+1)%(m*t)
                assert v%t==0;u=d*(T//t)%m;w=v//t
                if I.Prior.fs(n,m,u,w+W)>I.Prior.fs(n,m,u,w):return True
            return False
        if band(0,e-s):return True
    return False
