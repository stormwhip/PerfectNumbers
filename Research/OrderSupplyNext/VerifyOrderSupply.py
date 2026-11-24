"""Offline exact-integer replay of the five-root certificate packet. Python >=3.10, no nonstandard imports.
Sources: inspect individual functions below. The two archived Teichmuller/Gemini modules supply the baseline lemmas.
"""
from pathlib import Path
import sys,json,gzip,math,os,argparse,hashlib,subprocess,shutil
from math import gcd,prod,lcm,isqrt
from functools import cache
from fractions import Fraction
from collections import Counter
H=Path(__file__).resolve().parent
T=H.parent/'TeichmullerValuation'
sys.path.insert(0,str(T))
import VerifyTeichmullerValuation2400 as tb
import VerifyGeminiExponents2400 as G
B=10**2400
roots=(7,11,13,19,31)
@cache
def profile(p):
    tb.check_lemmas(p)
    return tb.Profile(p)
@cache
def prepared(p):
    prof=profile(p)
    return G.discounts(p,prof),G.euler_deficits(p,prof.top)
@cache
def eulerD(p):return max([Fraction(1),*(v for _,v in prepared(p)[1])])

# ---- fetch.py ----
@cache
def audits():
    a=json.loads((T/'Audit2400.json').read_text()); b=json.loads((T/'GeminiBatchAudit2400.json').read_text()); closed={s['id'] for s in b['additions']}; prior={tuple(pair) for pair in b['verified_exponents']}; prior.update((s['root'],r['exponent']) for s in a['additions'] for r in s['proof']); return [s for s in a['open_manifest'] if s['root'] in roots and s['id'] not in closed], prior

@cache
def active(p):
    shards,prior=audits(); es={e for s in shards if s['root']==p for e in tb.covered_exponents(p,s['exponent'],s['exact']) if (p,e) not in prior and p**e*tb.odd_part(tb.sigma(p,e))<=B}; return sorted(es,reverse=True)


# ---- screen.py ----
@cache
def baseline(p,e):
    if (p,e) in audits()[1]: return True
    if e%2 and any(tb.odd_part(tb.sigma(p,e))%z==0 for z in tb.forbidden(p)):return True
    if e%2:return tb.verify_odd_root_exponent(p,e,profile(p))[0]
    return tb.verify_even_exponent(p,e,profile(p))[0]


# ---- curve.py ----
def require(ok,msg):
    if not ok:raise ValueError(msg)

def mul(n,a,P,k):
    # Jacobian affine model (X/Z^2,Y/Z^3); None is the identity at all prime divisors.
    def twice(P):
        if P is None:return None
        x,y,z=P
        if y==0:return None
        S=4*x*y*y%n; M=(3*x*x+a*pow(z,4,n))%n
        X=(M*M-2*S)%n; return X,(M*(S-X)-8*pow(y,4,n))%n,2*y*z%n
    def add(P,Q):
        if P is None:return Q
        if Q is None:return P
        x,y,z=P;u,v,w=Q; zz=z*z%n;ww=w*w%n
        U=x*ww%n;V=u*zz%n;Y=y*ww*w%n;T=v*zz*z%n;h=(V-U)%n;s=(T-Y)%n
        if h==0:
            if s==0:return twice(P)
            require((T+Y)%n==0 and gcd(s,n)==1,'mixed point reduction')
            return None
        hh=h*h%n;hhh=h*hh%n;l=U*hh%n
        X=(s*s-hhh-2*l)%n
        return X,(s*(l-X)-Y*hhh)%n,h*z*w%n
    # Nonzero projective coordinates may become nonunits if n is composite. We must not identify
    # a mixed exceptional point as a global identity. Accumulate all nonzero branch-denominators.
    # Product check below after every intermediate point, deferred through a single gcd.
    Q=None;prod=1
    for bit in bin(k)[2:]:
        old=Q; Q=twice(Q)
        if Q is not None:prod=prod*Q[2]%n
        if bit=='1':
            Q=add(Q,P)
            if Q is not None:prod=prod*Q[2]%n
    require(gcd(n,prod)==1,'noninvertible EC operation');return Q

@cache
def verify_node(n,t,s,a,x,y,q):
    require(n>2**64 and n%2 and s>0 and q>1 and q<n and 0<=x<n and 0<=y<n,'malformed ECPP node')
    m=n+1-t;require(m==s*q and t*t<=4*n,'invalid Hasse interval/cofactor')
    # q > (n^(1/4)+1)^2. For q>1 write u=q-1, then u-sqrt(n)>2 n^(1/4);
    # equivalently u^2+n > (2u+4)*sqrt(n), requiring u>sqrt(n) independently.
    u=q-1; require(u*u>n and (u*u+n)**2>(2*u+4)**2*n,'insufficient factor')
    a%=n;b=(y*y-x*x*x-a*x)%n
    require(gcd(4*a**3+27*b*b,n)==1,'singular curve')
    P=(x,y,1); S=mul(n,a,P,s);require(S is not None and gcd(S[2],n)==1,'infinite witness')
    require(mul(n,a,S,q) is None,'wrong point order')

def verify_cert(r,c):
    if r<2**64:require(G.is_prime_det64(r),'small composite');return
    require(type(c)==list and bool(c) and c[0][0]==r,'wrong ECPP root');
    q=None
    for row in reversed(c):
        n,t,s,a,(x,y)=row
        require(all(type(v)==int for v in (n,t,s,a,x,y)) and s>0,'bad scalar'); child,rem=divmod(n+1-t,s);require(not rem,'bad cofactor')
        if q is None:require(child<2**64 and G.is_prime_det64(child),'unproven leaf')
        else:require(q==child,'broken chain')
        verify_node(n,t,s,a,x,y,child);q=n
    require(q==r,'root mismatch')


# ---- verify.py ----
def independent_chain(p,e,rs):
    if e%2:raise ValueError('even root required')
    A=tb.sigma(p,e);pe=p**e;kap=tb.kappa(p);U=profile(p).U(e)
    cs={r:G.val(A,r) for r in rs}
    # Branch explicitly on the Euler slot in each parity-completion LCM.
    opts=[None]+[r for r in rs if r%4==1]; rounded={q:A*prod(t for t,c in cs.items() if c%2 and t!=q) for q in opts}
    if all(pe*m>B for m in rounded.values()):return 'Parity'
    for r in sorted(rs,reverse=True):
        if r.bit_length()<60:break
        c=cs[r]; f=c; rf=r**f
        while pe*rf<=B:
            if f%2==0 or f%4==r%4==1:
                total=tb.sigma(r,f); odd=tb.odd_part(total); b=G.val(odd,p)
                if b<=e and not any(odd%t==0 for t in tb.forbidden(p)):
                    allowed=[r] if f%2 else [q for q in opts if q!=r]
                    if not f%2 or pe*rf*p**(kap*(e-b))<=B*U:
                        if any(lcm(pe*rf,odd,rounded[q])<=B for q in allowed):break
            f+=1;rf*=r
        else:return 'Chain'
    return None


# ---- hybrid_replay.py ----
@cache
def block_list(a,e):
    return tuple(tb.odd_part(G.phi(a,d)) for d in range(2,e+2) if not (e+1)%d)

def progression(lo,hi,res,step,max_visits=4):
    v=lo+(res-lo)%step
    if v>hi:return ()
    if (hi-v)//step>=max_visits:return None
    return range(v,hi+1,step)

def possible_factor(x,s,y,lo,hi):
    # q prime congruent to 1 mod 4 and q=-1 mod p^s implies q=2y-1 (mod 4y) for s>0.
    # Unknown cofactors of a component need not be prime. Never assumes they are.
    if not s:return lo<=min(x,hi)
    hi=min(x,hi)
    if lo>hi:return False
    aa=progression(lo,hi,2*y-1,4*y)
    if aa is not None:return any(x%q==0 for q in aa)
    bb=progression((x+hi-1)//hi,x//lo,-x,y)
    return bb is None or any(x%v==0 for v in bb)

def close(p,e,rs,R):
    if e%2 or R not in rs:return False
    pe=p**e;A=tb.sigma(p,e);k=tb.kappa(p); U=profile(p).U(e);D=eulerD(p)
    for f in range(G.val(A,R),G.ilog(B//pe,R)+1):
        euler=f%2==1
        if euler and (f%4!=1 or R%4!=1):continue
        qpow=R**f;z=tb.odd_part(tb.sigma(R,f));b=G.val(z,p)
        if b>e or any(z%t==0 for t in tb.forbidden(p)):continue
        L=lcm(pe*qpow,z,A); nonR=set(rs)-{R};cs={t:G.val(L,t) for t in nonR}; ratios={t:max(Fraction(1),G.surplus(p,k,t,c)) for t,c in cs.items()}; S=prod(ratios.values(),start=Fraction(1)); V=pe*qpow*p**(k*(e-b)); parity=L*prod(t for t,c in cs.items() if c%2)
        if euler:
            if parity<=B and V*S<=B*U:return False
            continue
        possible=[t for t in nonR if t%4==1]; bestp=parity//max([1,*[t for t in possible if cs[t]%2]]);bestS=S/max([1,*[ratios[t] for t in possible]])
        if bestp>B:continue
        if V*bestS<=B*U*D:return False
        # q known: exact checking by each prime's actual valuation s.
        for t in possible:
            if cs[t]!=1:continue
            s=G.val(t+1,p)
            if s<=e-b and parity//t<=B and V*t*S<=B*U*ratios[t]*p**(k*s):return False
        if parity>B:continue
        blocks=[]
        for x in (*block_list(p,e),*block_list(R,f)):
            for t in {*nonR,p,R}:
                if x%t==0:x//=t**G.val(x,t)
            if x>1:blocks.append(x)
        bound=B*U*S.denominator; denom=V*S.numerator;y=1; sk=p**k
        for s in range(e-b+1):
            lo=max(5,2*y-1)
            if lo*denom<=bound:
                hi=bound//denom
                if parity*lo<=B:return False # q may be outside A and sigma(R^f)
                if any(possible_factor(x,s,y,lo,hi) for x in blocks):return False
            bound*=sk;y*=p
    return True


# ---- parallel_gem.py ----
def prove_fast(p,e,rs):
    A=tb.odd_part(tb.sigma(p,e)); pe=p**e; k=tb.kappa(p); U=profile(p).U(e); cap=p**(k*e); T=p**k
    if any(A%r for r in rs):raise ValueError('invalid candidate factor')
    fs={r:G.val(A,r) for r in rs}; sale={r:max(1,G.surplus(p,k,r,c)) for r,c in fs.items()}; S=prod(sale.values(),start=Fraction(1)); E=pe*A*prod(r for r,c in fs.items() if c%2)
    if e%2:return E>B or pe*cap*S>B*U
    Q=[r for r,c in fs.items() if r%4==1]; D=max([Fraction(1),*(v for _,v in prepared(p)[1])]); SH=S/max([1,*[sale[r] for r in Q]]);
    if E//max((r for r in Q if fs[r]%2),default=1)<=B and pe*cap*SH<=B*U*D:return False
    # Euler q^1 || N. If q is known inside A then v_q(A)=1. Otherwise q coprime to every known factor, hence no discount in S and E.
    for r in Q:
        if fs[r]!=1:continue
        s=G.val(r+1,p)
        if s<=e and E//r<=B and pe*r*p**(k*(e-s))*S<=B*U*sale[r]: return False
    residual=A//prod(r**c for r,c in fs.items()); V=Fraction(pe*cap*S); y=1
    # monotonic valuation lower at q=2y-1, reverse monotonic size. For q not among known factors and q outside A, E*q divides N; inside, E divides N and q|residual.
    for s in range(e+1):
        q=max(5,2*y-1)
        if V*q<=B*U:
            if E*q<=B:return False
            if residual>=q and E<=B:
                hi=min(residual,B*U//V); lo=q
                if hi>=lo and (s==0 or G.divides_a(p,e,y,lo,hi)):
                    c0=(-residual)%y or y
                    if lo<=min(hi,residual//c0):return False
        V/=T
        y*=p
    return True


# ---- emit.py ----
def prove_emit(p,e,rs,small=False):
    if e%2:return False
    pwr=p**e; A=tb.sigma(p,e);kap=tb.kappa(p); D0,E0=prepared(p);ds=[d for d in D0 if d[0]<=e];used={w for *_,ws in ds for w in ws};fs=[(r,G.val(A,r),max(Fraction(1),G.surplus(p,kap,r,G.val(A,r)))) for r in rs if r not in used];S=prod((v for _,_,v in fs),start=Fraction(1));eD=max([Fraction(1),*(v for t,v in E0 if t<=e)]);Q=[r for r in rs if r%4==1];L=pwr*A*prod(r for r in rs if G.val(A,r)%2);SH=S/max([1,*[v for r,c,v in fs if r%4==1]]);cap=p**(kap*e)
    if L//max([1,*[r for r in Q if G.val(A,r)%2]])<=B and pwr*cap*SH<=B*eD*G.loss(p,ds,False,0,5,None):return False
    # Single constant global loss bound is inexpensive and conservative at all s.
    U=profile(p).U(e); lower0=pwr*cap*SH;legal=[r for r in Q if G.val(A,r)==1]; C=A//prod(r**G.val(A,r) for r in rs);bad=[]; y=1
    for s in range(e+1):
        q=max(5,2*y-1)
        if lower0*q<=B*U:
            if L*q<=B or (L<=B and C>=q and ((not s) or G.divides_a(p,e,y,q,C))) or any(r>=q and G.val(r+1,p)==s and L//r<=B for r in legal):bad.append(s)
        lower0/=p**kap;y*=p
    if not bad:return True
    # Probe middle / thirds before endpoints, generally rejects failures in a single step.
    reord=sorted(range(len(bad)),key=lambda j:abs(len(bad)-1-2*j));
    if small:reord=reord[:1]
    for j in reord:
        s=bad[j]
        if not G.branch(p,e,s,pwr,A,[d for d in ds if d[0]<=e-s],fs):return False
    return not small


# ---- orderlift.py ----
@cache
def price(p,k,r,c):
    # Bound remaining f with the archimedean estimate of v_p(sigma) from LTE.
    # If o>1, v_p <= t+log_p(f+1); if o=1, v_p<=log_p(f+1). So r^f/(p^(kt)(f+1)^k) is an increasing lower bound for all large f.
    if r==p:raise ValueError('pricing root')
    o=tb.multiplicative_order(r,p);t=0 if o==1 or o%2==0 else G.val(r**o-1,p); k=tb.kappa(p);f=c+c%2; X=r**f; known=G.surplus(p,k,r,c);best=None; ban=tb.forbidden(p)
    while True:
        if best is not None and X*best.denominator>=best.numerator*p**(k*t)*(f+1)**k and r*r*(f+1)**k>=(f+3)**k:return max(known,best)
        n=tb.sigma(r,f)
        if not any(n%z==0 for z in ban):
            v=G.val(n,p); v0=Fraction(X,p**(k*v));best=v0 if best is None else min(best,v0)
        f+=2; X*=r*r
        if f>80:return known

def order_rule(p,e,rs):
    if e%2:return False
    A=tb.sigma(p,e);pe=p**e;k=tb.kappa(p);U=profile(p).U(e);D=max([Fraction(1),*(v for _,v in prepared(p)[1])]);fs={r:G.val(A,r) for r in rs};prem={r:1 for r in rs}
    # Enforce true minimal non-Euler exponent, not just next parity: small f forbidden by individual sigma divisibility.
    ban=tb.forbidden(p)
    for r,c in fs.items():
        f=c+c%2
        while f<60 and any(tb.sigma(r,f)%z==0 for z in ban):f+=2
        prem[r]=r**(f-c)
    sale={t:max(Fraction(1),price(p,k,t,c)) for t,c in fs.items()};S=prod(sale.values(),start=Fraction(1));V=pe*p**(k*e)*S;M=A*prod(prem.values()); Q=[r for r in rs if r%4==1]; Sh=S/max([1,*[sale[t] for t in Q]])
    if pe*M//max([1,*[prem[t] for t in Q]])<=B and pe*p**(k*e)*Sh<=B*U*D:return False
    for t in Q:
        if fs[t]!=1:continue
        s=G.val(t+1,p)
        if s<=e and pe*M//prem[t]<=B and V*t<=B*U*sale[t]*p**(k*s):return False
    moduli=[]
    for d in G.divisors(e+1)[1:]:
        x=G.phi(p,d)
        for t in rs:
            if not x%t:x//=t**G.val(x,t)
        if x>1:moduli.append(x)
    y=1;bound=B*U
    for s in range(e+1):
        q=max(5,2*y-1)
        if V*q<=bound:
            if pe*M*q<=B:return False
            if pe*M<=B and any(possible_factor(x,s,y,q,bound//V) for x in moduli):return False
        y*=p;bound*=p**k
    return True


# ---- pairprice.py ----
def leaf(p,e,rs,fixed):
    # fixed is a tuple (r,f) of exact prime powers, with r|A distinct from p and one another.
    pe=p**e;A=tb.sigma(p,e);k=tb.kappa(p);U=profile(p).U(e);D=eulerD(p); L=pe*A; b=0;Eul=None;power=pe; Z=[]
    for r,f in fixed:
        if f%2:
            if Eul or r%4!=1 or f%4!=1:return True
            Eul=r
        rf=r**f;power*=rf;z=tb.odd_part(tb.sigma(r,f));Z.append(z);b+=G.val(z,p);L=lcm(L,rf,z)
        if L>B or any(z%w==0 for w in tb.forbidden(p)):return True
    if b>e or any(G.val(L,r)>f for r,f in fixed):return True
    anch={r for r,f in fixed}; other=set(rs)-anch; cs={r:G.val(L,r) for r in other}; premium=prod(r for r,c in cs.items() if c%2);M=L*premium
    if Eul is not None and M>B:return True
    Q=[r for r in other if r%4==1]; Mmin=M//max([1,*[r for r in Q if cs[r]%2]])
    if Mmin>B:return True
    sale={r:max(Fraction(1),G.surplus(p,k,r,c)) for r,c in cs.items()}; S=prod(sale.values(),start=Fraction(1)); V=power*p**(k*(e-b))*S
    if Eul is not None:return V>B*U
    if V<=B*U*D*max([1,*[sale[r] for r in Q]]):return False
    for r in Q:
        if cs[r]!=1:continue
        s=G.val(r+1,p)
        if s<=e-b and M//r<=B and V*r<=B*U*sale[r]*p**(k*s):return False
    if M>B:return True
    # For unknown q, p^s progression starts at 2*p^s-1. Restrict to gaps where price by itself fails.
    W=V.numerator; C=B*U*V.denominator;y=1;d=k-1
    m=G.ilog(W//C,p);lo=max(0,m//d);y=p**lo;C*=y**k
    # Justification: for s<lo, q>=p^s and p^((k-1)s) < p^m <= W/C0.
    comps=None
    for s in range(lo,e-b+1):
        q=max(5,2*y-1)
        if W*q<=C:
            if M*q<=B:return False
            if comps is None:
                comps=[]
                for r,f in [(p,e),*fixed]:
                    for x in block_list(r,f):
                        for t in [*rs,p]:
                            if x%t==0:x//=t**G.val(x,t)
                        if x>1:comps.append(x)
            if any(possible_factor(x,s,y,q,C//W) for x in comps):return False
        y*=p;C*=p**k
    return True

def pair_rule(p,e,rs,anchors):
    if e%2 or len(set(anchors))!=len(anchors) or not set(anchors)<=set(rs):return False
    A=tb.sigma(p,e); pe=p**e
    def rec(i,fixed,L):
        if leaf(p,e,rs,fixed):return True
        if i>=len(anchors):return False
        r=anchors[i]; c=G.val(L,r); rf=r**c;other=L//rf; f=c
        while rf*other<=B:
            if f%2==0 or (f%4==r%4==1 and all(g%2==0 for _,g in fixed)):
                z=tb.odd_part(tb.sigma(r,f));H=lcm(other*rf,z)
                if H<=B and all(G.val(H,w)<=g for w,g in [*fixed,(r,f)]) and not any(z%v==0 for v in tb.forbidden(p)) and not rec(i+1,(*fixed,(r,f)),H):return False
            f+=1;rf*=r
        return True
    return rec(0,(),pe*A)


# ---- companion.py ----
@cache
def block_premium(p,e,rs):
    # Returns primitive blocks stripped of all known primes and of h; if coprime to other blocks (including known support), one nonsquare block guarantees a parity lift ≥least prime factor.
    A=tb.sigma(p,e); result=[]
    for h in G.divisors(e+1)[1:]:
        x=G.phi(p,h);n=x
        for r in rs:
            if n%r==0:n//=r**G.val(n,r)
        for r in range(2,h+1):
            if h%r==0:
                while n%r==0:n//=r
        if n==1 or gcd(n,A//n)!=1 or isqrt(n)**2==n:continue
        # Coprime to h, every prime divisor of Phi_h(p) has multiplicative order h. Primes are odd, so each is congruent to 1 mod lcm(h,2).
        step=math.lcm(2,h); a=1+step
        while a<2_000_000 and (not G.is_prime_det64(a) or n%a):a+=step
        # No assumption n is prime. If the first untested integer exceeds sqrt(n), n itself is prime, though that fact is not needed.
        result.append((n,min(a,n)))
    return result

def companion_rule(p,e,rs):
    if e%2:return False
    k=tb.kappa(p);A=tb.sigma(p,e);pe=p**e;fs={r:G.val(A,r) for r in rs};S=prod((max(Fraction(1),G.surplus(p,k,r,c)) for r,c in fs.items()),start=Fraction(1));M=A*prod(r for r,c in fs.items() if c%2);U=profile(p).U(e);D=max([Fraction(1),*(v for _,v in prepared(p)[1])]);Q=[r for r in rs if r%4==1];rat={t:max(Fraction(1),G.surplus(p,k,t,fs[t])) for t in Q};blocks0=block_premium(p,e,tuple(rs)); prem=prod(v for n,v in blocks0);outside=pe*M*prem
    # One Euler exception can be in known primes or in unknown support, not both. If a non-square block contains q, omit its whole guaranteed multiplier.
    maxdiscount=max([1,*[r for r in Q if fs[r]%2],*[v for n,v in blocks0]]);V=pe*p**(k*e)*S
    if outside//maxdiscount<=B and V<=B*U*D*max([1,*rat.values()]):return False
    for r in Q:
        if fs[r]!=1:continue
        s=G.val(r+1,p)
        if s<=e and outside//r<=B and V*r<=B*U*rat[r]*p**(k*s):return False
    comps=[]
    for h in G.divisors(e+1)[1:]:
        n=G.phi(p,h)
        for r in rs:
            if n%r==0:n//=r**G.val(n,r)
        if n>1:comps.append((n,max([1,*[v for x,v in blocks0 if gcd(x,n)>1]])))
    y=1;den=B*U
    for s in range(e+1):
        q=max(5,2*y-1)
        if V*q<=den:
            if outside*q<=B:return False
            if any(outside//v<=B and possible_factor(n,s,y,q,den//V) for n,v in comps):return False
        y*=p;den*=p**k
    return True


# ---- verify.py ----
def coverage(rows):
    shards,old=audits(); old=set(old)
    for v in ['SupplierBatch/BatchAudit2400.json','IndicatorCapacity/Audit2400.json']:
        old.update((r['root'],r['exponent']) for r in json.loads((H.parent/v).read_text())['exact_exponents'])
    old.update((r['root'],r['exponent']) for r in json.loads((H.parent/'EulerOneSieve/ActualExponentRecords.json').read_text()))
    new={(p,e) for p,e,_ in rows if (p,e) not in old and not baseline(p,e)}; add=[]
    for s in shards:
        p=s['root']; left=[]
        for e in tb.covered_exponents(p,s['exponent'],s['exact']):
            if p**e*tb.odd_part(tb.sigma(p,e))<=B and (p,e) not in old and not baseline(p,e):left.append(e)
        if left and all((p,e) in new for e in left):add.append([s['id'],p,left])
    return sorted(new),sorted(add)

def cert_root(r,c):
    if type(c)!=list or not c or c[0][0]!=r:raise ValueError('wrong ECPP witness')
    def pure(x):return type(x)==int or type(x)==list and all(pure(y) for y in x)
    if not pure(c):raise ValueError('invalid certificate syntax')

def _verify_one(item):
    r,c=item;verify_cert(r,c);return r

def verify_primes(rs,gp,workers):
    rs=set(rs); nums=sorted(r for r in rs if r>=2**64)
    for r in rs:
        if type(r)!=int or r<3 or r%2==0 or (r<2**64 and not G.is_prime_det64(r)):raise ValueError('invalid factor')
    with gzip.open(H/'OrderPrimeProofs.json.gz','rt',encoding='utf-8') as s: proofs=json.load(s)
    if set(proofs)!=set(map(str,nums)):raise ValueError('incorrect prime certificate set')
    for r in nums:cert_root(r,proofs[str(r)])
    if gp:
        cmd=['default(parisizemax,250000000);']+['c='+json.dumps(proofs[str(r)],separators=(',',':'))+';if(primecertisvalid(c),print("ok '+str(i)+'"));' for i,r in enumerate(nums)]
        ret=subprocess.run([gp,'-fq'],input='\n'.join(cmd)+'\n',text=True,capture_output=True,check=True)
        if ret.stdout.splitlines()!=['ok '+str(i) for i in range(len(nums))]:raise ValueError('PARI rejected witness')
    else:
        pairs=[(r,proofs[str(r)]) for r in reversed(nums)]
        if workers==1:
            for i,x in enumerate(pairs):
                _verify_one(x)
                if (i+1)%50==0:print('ECPP',i+1,'/',len(nums),flush=True)
        else:
            from concurrent.futures import ProcessPoolExecutor,as_completed
            with ProcessPoolExecutor(max_workers=workers) as pool:
                jobs=[pool.submit(_verify_one,x) for x in pairs]
                for i,job in enumerate(as_completed(jobs),1):
                    job.result()
                    if i%50==0:print('ECPP',i,'/',len(nums),flush=True)
    return len(nums)

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--gp',help='optional PARI/GP executable for accelerated ECPP verification');parser.add_argument('--output',type=Path);parser.add_argument('--workers',type=int,default=min(6,os.cpu_count() or 1));args=parser.parse_args()
    rows=json.loads((H/'Accepted.json').read_text(encoding='utf-8'));ec=verify_primes((r for row in rows for r in row['r']),args.gp,args.workers);proved=[];seen=set()
    for row in rows:
        p,e,rs=row['p'],row['e'],row['r'];rule=row['rule']
        if p not in roots or e%2 or e not in active(p) or len(rs)!=len(set(rs)) or any(tb.sigma(p,e)%r for r in rs) or (p,e) in seen:raise ValueError(('invalid pair',p,e))
        seen.add((p,e));tb.check_lemmas(p)
        if rule in ('Chain','Parity'):rule=independent_chain(p,e,rs);ok=bool(rule)
        elif rule=='Hybrid':ok=close(p,e,rs,row['R'])
        elif rule=='Fast':ok=prove_fast(p,e,rs)
        elif rule=='Emit':ok=prove_emit(p,e,rs)
        elif rule=='Order':ok=order_rule(p,e,rs)
        elif rule=='Pair':ok=pair_rule(p,e,rs,row['anchors'])
        elif rule=='Companion':ok=companion_rule(p,e,rs)
        else:raise ValueError('unknown rule '+rule)
        if not ok:raise ValueError(('unclosed',p,e))
        proved.append([p,e,rule])
    new,closed=coverage(proved);res={'ecpp':ec,'proved':proved,'new':new,'closed':closed}
    if args.output:args.output.write_text(json.dumps(res,indent=1)+'\n',encoding='utf-8')
    print('ECPP',ec,'complete actual exponents',len(proved),'new actual exponents',len(new),'new shards',len(closed),flush=True)
    print('by root',dict(sorted(Counter(p for p,e in new).items())),'shards',dict(sorted(Counter(p for i,p,es in closed).items())))
if __name__=='__main__':main()
