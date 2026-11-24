"""Self-contained all-Euler source/anchor replay. Requires only the tracked OrderSupplyNext+Teichmuller verification archive, Python stdlib. Strict JSON format [[p,e,primeWitnesses,maxDepth,maxNodes],...]. Every record must pass. Outputs accepted pairs only AFTER the entire packet completes. No sibling discovery directories, environment flags, floating arithmetic or middle-stage manifests.
"""
from pathlib import Path
from functools import lru_cache as cache0
from fractions import Fraction
from collections import Counter
import argparse,json,math,sys,time,gzip
H=Path(__file__).resolve().parent;R=H.parent;sys.path.insert(0,str(R/'OrderSupplyNext'));import VerifyOrderSupply as O
B=10**2400
cache=cache0(maxsize=32768)

def req(cond,why):
    if not cond:raise ValueError(why)
@cache
def sig(r,f):return (r**(f+1)-1)//(r-1)
@cache
def phi(r,h):
    n=r**h-1
    for d in range(1,h):
        if h%d==0:n//=phi(r,d)
    return n
@cache
def floorroot(n,k):
    if n<2 or k==1:return n
    if k==2:return math.isqrt(n)
    x=1<<((n.bit_length()+k-1)//k)
    while True:
        y=((k-1)*x+n//x**(k-1))//k
        if y>=x:return x
        x=y

def val(n,p):
    a=0
    while n%p==0:a+=1;n//=p
    return a

def floors(n,m,a,b):
    res=0
    while True:
        q,a=divmod(a,m);res+=q*n*(n-1)//2;q,b=divmod(b,m);res+=q*n;y=a*n+b
        if y<m:return res
        n,b=divmod(y,m);m,a=a,m

def box(C,c,z,T,l,h):
    k0=(l-z+T-1)//T;k1=(h-z)//T
    if k0>k1:return False
    if math.gcd(z,T)!=1:return True
    w=C*pow(z,-c,T)%T;ul=(C+h**c-1)//h**c;uh=C//l**c;l0=(ul-w+T-1)//T;l1=(uh-w)//T
    if l0>l1:return False
    width=l1-l0+1
    if width>=T:return True
    zc=pow(z,c,T*T);d=((C-zc*w)%(T*T))//T;i=pow(zc,-1,T);a=-c*pow(z,c-1,T)*w*i%T;b=d*i+a*k0-l0;n=k1-k0+1
    return floors(n,T,a,b)>floors(n,T,a,b-width)
@cache
def lift(p,a,j):return pow(a,p**(j-1),p**j)
@cache
def source(C,c,p,f,lo,hi,b,h):
    if hi<lo:return False
    j=b-val(f+1,p)
    if j<=0:return True
    m=p**j
    for a in range(2,p):
        if pow(a,f+1,p)!=1:continue
        z=lift(p,a,j);t=2*h;g=math.gcd(m,t)
        if (1-z)%g:continue
        z+=m*(((1-z)//g*pow(m//g,-1,t//g))%(t//g));t=math.lcm(t,m);z%=t;r=lo+(z-lo)%t
        if r>hi:continue
        if math.gcd(z,t)==1:
            ul=(C+hi**c-1)//hi**c;uh=C//lo**c;u=ul+(C*pow(z,-c,t)-ul)%t
            if (uh-u)//t<8:
                for w in range(u,uh+1,t):
                    if C%w:continue
                    v=floorroot(C//w,c)
                    if v**c*w==C and lo<=v<=hi and v%t==z:return True
                continue
        if (hi-r)//t<=8:
            if any(C%(v**c)==0 for v in range(r,hi+1,t)):return True
        else:
            low=lo
            while low<=hi:
                end=min(2*low-1,hi)
                if box(C,c,z,t,low,end):return True
                low=end+1
    return False
PRIMES=tuple(r for r in range(3,10001,2) if all(r%j for j in range(3,math.isqrt(r)+1,2)))
@cache
def price(p,r,c):return max(Fraction(1),O.price(p,O.tb.kappa(p),r,c))
@cache
def ecp():return json.load(gzip.open(R/'OrderSupplyNext/OrderPrimeProofs.json.gz','rt'))
@cache
def prime(r):
    if r<2**64:return O.G.is_prime_det64(r)
    pr=ecp().get(str(r));req(pr,'missing ECPP');O.verify_cert(r,pr);return True

def replay(p,e,rs,depth,cap):
    req(type(p)==type(e)==int and p in (7,11,19,31) and 2<=e<=5000 and not e%2,'bad root/exponent');req(type(rs)==list and all(type(r)==int and r>2 for r in rs) and len(set(rs))==len(rs) and type(depth)==type(cap)==int and 0<=depth<=12 and 1<=cap<=50000,'bad parameters')
    A=sig(p,e);pe=p**e;P=p*pe;ban=O.tb.forbidden(p);K=O.tb.kappa(p);pr=O.profile(p);U=pr.U(e)
    for r in rs:req(A%r==0 and prime(r),'bad witness')
    # Internal Euler q|A has (q/p)=1 by odd order + reciprocity; hence v_p(q+1)=0.
    req(pe**(K+1)>B*U,'internal Euler remains')
    # Archived stronger a>=5 pricing in Gemini, or elementary 2-units formula. Gemini discounts upper-bound all ordinary loss without sponsor pricing here; U remains paid in full. For special p=11 all eligible Euler components cost at least p^(4v)/E5 since E5 bounds p^(5t) deficits. The cases order 1,2 and LTE growth are exact elementary size bounds.
    if pe**3<=B*U*pr.D(e):
        req(p==11 and K==4 and 2*p-1>=2*K and all(3**(o*p-1-O.tb.fmin_euler(o))>=p**K for o in (5,10)),'higher Euler remains');E=max([Fraction(1),*(z for j,z in O.G.euler_deficits(p,pr.top) if j<=e)]);req(pe**(K+1)>B*U*E,'higher Euler price failed')
    nodes=0;leaves=Counter()
    def walk(X,S,F,free):
        nonlocal nodes
        nodes+=1
        if nodes>cap:return False
        D=S//math.gcd(2*X,S);L=X*D
        if L>B or S>2*X or math.gcd(D,X*math.prod(ban))>1:leaves['simple']+=1;return True
        supply=val(S,p);req(supply<=e,'root overvaluation inconsistency');V=Fraction(X*p**(K*(e-supply)),U);C=D;mx=1;sale=Fraction(1);ks=[]
        for r in set(PRIMES)|set(rs):
            if C%r:continue
            c=val(C,r);C//=r**c;f=c+c%2
            while any(sig(r,f)%q==0 for q in ban):f+=2
            j=r**(f-c);v=price(p,r,c);ks.append((r,c));L*=j;mx=max(mx,j);V*=v;sale=max(sale,v)
        chunks=[]
        for r,f in ((p,e),*F):
            for h in range(3,f+2,2):
                if (f+1)%h==0:
                    m=math.gcd(C,phi(r,h))
                    if m>1:chunks.append((r,h,m))
        split=math.prod(z for r,h,z in chunks)==C and all(math.gcd(z,h)==1 for r,h,z in chunks);pass_leaf=split
        if split:
            origins=[sig(r,f) for r,f in F];VV=V/sale
            for s in range(e-supply+1):
                Y=p**s;Q=max(5,2*Y-1);T=B*Y**K
                # Separate q|some fixed ordinary sigma *before* charging all known components at ordinary cost.
                if L<=B*mx and VV*Q<=T and any(O.possible_factor(z,s,Y,Q,min(z,B//X)) for z in origins):pass_leaf=False;break
                if L*Q>B or V*Q>T:continue
                b=0
                while 2*VV*Q*Q>3*T*p**((K-1)*b):b+=1
                if b>e-supply-s:continue
                if 2*L*Q**2*p**b<=3*B:pass_leaf=False;break
                room=B*mx//(L*Q);need=2*Q*p**b//3;Z=Y*p**b;th=Z*Q//(max(P,Q)*(P//Z+4));hit=False
                for r,c in ks:
                    f=c+c%2;croot=val(A,r)
                    while r**(f-c)<=room:
                        z=sig(r,f)
                        if (not croot or r**(f-croot)>th) and r**f>need and val(z,p)>=b and O.possible_factor(z,s,Y,Q,min(z,B//X)):hit=True;break
                        f+=2
                    if hit:break
                if not hit:
                    for orig,h,n in chunks:
                        lb=th if orig==p else 0
                        for g in range(max(0,O.G.ilog(room,10001))+1):
                            if not g and lb>=1:continue
                            bot=max(10001,floorroot(lb,g)+1 if g else 10001);top=floorroot(room,g) if g else n
                            for c in range(2-g%2,O.G.ilog(n,bot)+1,2):
                                f=c+g;lo=max(bot,floorroot(need,f)+1);hi=min(top,floorroot(n,c))
                                if source(n,c,p,f,lo,hi,b,h):hit=True;break
                            if hit:break
                        if hit:break
                if hit:pass_leaf=False;break
        if pass_leaf:leaves['source']+=1;return True
        if len(F)>=depth or not free:return False
        r=max(free);c=val(D,r);req(c>0,'anchor not forced');f=c+c%2;M=X*(D//r**c);a=r**f
        while M*a<=B:
            z=sig(r,f)
            if all(z%q for q in ban) and not walk(X*a,S*z,F+((r,f),),free-{r}):return False
            f+=2;a*=r*r
        return True
    req(walk(pe,A,(),set(rs)),f'open {p}/{e}');return [p,e],nodes,dict(leaves)

def main():
    if not __debug__:raise SystemExit('run normally, not -O')
    a=argparse.ArgumentParser();a.add_argument('packet',type=Path);args=a.parse_args();D=json.loads(args.packet.read_text(encoding='utf8'));req(type(D)==list and D and all(type(x)==list and len(x)==5 for x in D),'bad packet');req(len({(r[0],r[1]) for r in D})==len(D),'duplicate claims');t=time.perf_counter();out=[replay(*row) for row in D];print(json.dumps(dict(accepted=[r[0] for r in out],replay=out,seconds=round(time.perf_counter()-t,3)),separators=(',',':')))
if __name__=='__main__':main()
