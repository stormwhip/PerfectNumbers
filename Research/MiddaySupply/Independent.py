"""Independent replay of unknown interior source boxes; known/exterior are reference baseline predicates.
Exact nonexistence only. Simpler integer tests used in place of discovery's candidate catalog.
"""
from pathlib import Path
from math import prod,gcd,lcm,isqrt
from functools import cache
from fractions import Fraction
import argparse,json,sys
D=Path(__file__).resolve().parent; R=D.parent;B=10**2400
sys.path.insert(0,str(R/'NightUniformReview'));import Replay as Prior
CASES={19:(676,(629611,16678454203)),11:(718,(8629,)),7:(1018,(85597,2539349)),31:(486,(380260554467939,))}

def sigma(x,f):return (x**(f+1)-1)//(x-1)
def vp(x,p):
    n=0
    while x%p==0:n+=1;x//=p
    return n
@cache
def root(n,f):
    if f==1:return n
    if f==2:return isqrt(n)
    a=0;b=1<<((n.bit_length()+f-1)//f)
    while a+1<b:
        m=(a+b)//2
        if m**f<=n:a=m
        else:b=m
    return b if b**f<=n else a

def lower_q(p,s,k):
    # Completely reconstruct rejection of every multiplier below stored k.
    y=p**s;ban=Prior.O.tb.forbidden(p)
    if k<1 or k%2!=1:raise ValueError('Euler multiplier not odd positive')
    for i in range(1,k,2):
        q=2*y*i-1
        if i%p and all(i%z and q%z for z in ban) and not any(q!=z and q%z==0 for z in range(3,1200,2)) and pow(2,q-1,q)==1:raise ValueError('uncertified Euler skip')
    return 2*y*k-1

@cache
def basis(p):
    e,rs=CASES[p];h=e+1
    assert all(h%z for z in range(2,isqrt(h)+1));pe=p**e;A=sigma(p,e)
    if any(A%r for r in rs):raise ValueError('bad divisors')
    Prior.primes(rs,A);known=set(rs)|{r for r in Prior.small if A%r==0};C=A;prof=Prior.O.profile(p);k=prof.kap
    M=pe*A;V=Fraction(pe**(k+1),prof.U(e));ban=Prior.O.tb.forbidden(p)
    for r in known:
        c=vp(C,r);C//=r**c;f=c+c%2
        while any(sigma(r,f)%b==0 for b in ban):f+=2
        M*=r**(f-c);V*=max(1,Prior.O.price(p,k,r,c))
    assert gcd(C,2*h)==1;step=2*h;limit=10001+(1-10001)%step+10000*step; first=next((r for r in range(10001+(1-10001)%step,limit,step) if C%r==0),limit)
    squareloss=first if isqrt(C)**2!=C else 1
    m=p-1
    while m%2==0:m//=2
    if pow(C,m,p)!=1:
        w=next((r for r in range(10001+(1-10001)%step,limit,step) if pow(r,m,p)!=1 and C%r==0),limit)**2
    else:w=1
    return pe,A,C,k,M*squareloss,V*w,squareloss,w

@cache
def teich(p,b,f):
    j=vp(f+1,p);n=b-j
    if n<=0:return [(0,1)]
    mod=p**n
    return [(pow(a,p**(n-1),mod),mod) for a in range(2,p) if pow(a,f+1,p)==1]

COVER=None

def progression(C,c,lo,hi,rs,mod,h,exact=False):
    step=2*h;d=gcd(step,mod)
    if (rs-1)%d:return False
    T=lcm(step,mod);x=1+step*((rs-1)//d)*pow(step//d,-1,mod//d);x%=T
    first=lo+(x-lo)%T
    if first>hi:return False
    if hi-first<=32*T:return any(C%r**c==0 for r in range(first,hi+1,T))
    w0=(C+hi**c-1)//hi**c;w1=C//lo**c;w0+=(C*pow(x,-c,T)-w0)%T
    if w1-w0<=32*T:return any(C%w==0 and (r:=root(C//w,c))**c*w==C and lo<=r<=hi and r%T==x for w in range(w0,w1+1,T))
    # Invoke already separately audited second-order rectangle test on disjoint bins.
    a=lo
    while a<=hi:
        b=min(hi,2*a-1)
        if Prior.rect(C,c,x,T,a,b,16) and not (COVER and COVER(C,c,x,T,a,b)):
            first=a+(x-a)%T
            if not exact or not COVER or b-first>250000*T or any(C%v**c==0 for v in range(first,b+1,T)):return True
        a=b+1
    return False

def check(p,s,kmult,cap,end=None,floor=None):
    end=s if end is None else end
    pe,A,C,k,M,V,extra,discount=basis(p);e,rs=CASES[p];h=e+1;P=pe*p;Y=p**s;Q=lower_q(p,s,kmult) if floor is None else floor; room=B*extra//(M*Q); maxc=Prior.logi(C,10001);maxg=Prior.logi(room,10001)
    # Enumerate all (g,c) over integer ranges. Prune intervals of exact b by a worst endpoint.
    initial_Q=Q
    def box(c,g,lb,ub,lo,hi):
        Q=initial_Q
        if globals().get('DIGIT') and end==s and p==11 and s>=519 and c+g==4:
            from OrderFloor import order_floor
            Q=max(Q,order_floor(p,s,5,16000))
            if c==2 and 526<=s<=529:
                from EulerPrefix import bound
                Q=max(Q,bound(p,e,s,2,5,C,600000 if s==527 else 120000))
        if g:hi=min(hi,root(B*(extra if g%2 else 1)//(M*Q),g))
        if ub<lb:return False
        f=c+g;t=p**lb;z=t*Y; allow=V/(discount if lb==0 else 1)
        hi=min(hi,root(B*p**(min(e,ub+end)*k)*allow.denominator//(Q*allow.numerator),f),root(B*p**ub//(pe*A),2*f-c))
        lo=max(lo,root(2*Q*t//3,f)+1)
        gap=z*Q//(max(P,Q)*(P//z+4))
        if g:lo=max(lo,root(gap,g)+1)
        elif gap>=1:return False
        if lo>hi:return False
        if not any(progression(C,c,lo,hi,x,m,h,lb==ub) for x,m in teich(p,lb,f)):return False
        if lb<ub:
            mid=(lb+ub)//2
            return box(c,g,lb,mid,lo,hi) or box(c,g,mid+1,ub,lo,hi)
        if globals().get('DIGIT') and not DIGIT(C,c,p,f,lb,s,h,lo,hi,Q):return False
        if cap and lb and (f+1)%p and (W:=sigma(hi,f)//(Q*t))<=cap:
            # Directly lift the geometric SUM polynomial, not (x-1) * sum.
            for w in range(1,W+1,2):
                if w%p==0:continue
                for a,m in teich(p,lb,f):
                    assert m==t; u=a
                    while m<z:
                        m=min(z,m*m); val=(pow(u,f+1,m)-1)*pow(u-1,-1,m)%m;der=((f+1)*pow(u,f,m)-val)*pow(u-1,-1,m)%m
                        u=(u-(val+t*w)*pow(der,-1,m))%m
                    if progression(C,c,lo,hi,u,m,h):return True
            return False
        return True
    for g in range(maxg+1):
        upper=root(B*(extra if g%2 else 1)//(M*Q),g) if g else C
        for c in range(1+(g+1)%2,maxc+1,2):
            if box(c,g,0,e-s,10001,min(upper,root(C,c))):return [c,g]
    return None

def main():
    ap=argparse.ArgumentParser();ap.add_argument('input');ap.add_argument('--cap',type=int,default=0);ap.add_argument('--out',required=True);ap.add_argument('--leaves');ap.add_argument('--band',type=int,nargs=2);args=ap.parse_args();
    if args.leaves:
        import gzip,hashlib
        sys.set_int_max_str_digits(0); bank=json.loads(gzip.decompress((D/args.leaves).read_bytes()));seen=set()
        def coverage(C,c,z,T,lo,hi):
            global COVER
            key=hashlib.sha256('|'.join(map(str,(C,c,z,T))).encode()).hexdigest();cut=lo
            for i,(a,b,w) in sorted(enumerate(bank.get(key,())),key=lambda item:item[1][0]):
                if b<cut:continue
                if a>cut:break
                if (key,i) not in seen:
                    if not Prior.LatticeLeaf.verify(C,c,z,T,a,b,w):raise ValueError('bad polynomial')
                    seen.add((key,i))
                cut=b+1
                if cut>hi:return True
            return False
        global COVER
        COVER=coverage
    rows=json.loads((D/args.input).read_bytes());out=[]
    if args.band:
        lo,hi=args.band;sub=[r for r in rows if lo<=r['s']<=hi];assert [r['s'] for r in sub]==list(range(lo,hi+1));p,e=sub[0]['p'],sub[0]['e'];q=min(lower_q(p,r['s'],r['euler_floor_multiplier']) for r in sub);w=check(p,lo,1,args.cap,end=hi,floor=q);out=dict(p=p,e=e,lo=lo,hi=hi,rough=w,verified_leaves=len(seen) if args.leaves else 0);print(out,flush=True);(D/args.out).write_text(json.dumps(out)+'\n');return
    for row in rows:
        if row['open'] or row['guard'] is not None:continue
        p,e,s=row['p'],row['e'],row['s'];w=check(p,s,row['euler_floor_multiplier'],args.cap);out.append([p,e,s,w]);print(p,e,s,w,flush=True);(D/args.out).write_text(json.dumps(out)+'\n')
if __name__=='__main__':main()
