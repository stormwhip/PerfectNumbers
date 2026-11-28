#!/usr/bin/env python3
"""Exact joint price for (19,276), t^18, Q^2, R^1."""
from fractions import Fraction
from math import gcd, prod, log10
from pathlib import Path
import json
import runpy

v=runpy.run_path(str(Path(__file__).with_name('Verify276.py')))
P,T,B=(v[k] for k in ('P','T','B'))
sigma,vp,state,require=(v[k] for k in ('sigma','vp','state','require'))
Q=2395723558714191605903463333646981101789939140815259939
R=720115882406222085965068726893873898633343366787816797352202677324108536240208081709751502952901480917
F=[1109,55871819,706729028162919660606947,146424547557021552241171230299053,1349913932010395163418526213595518782940656913,151,52783,89,37189,3967517759,49106578036867897502915386199,558353619464169741454381939801951595147630844964578823919]
rows=((P,276),(T,18),(Q,2),(R,1))


def orders(s):return [a for a in range(3,5032,2) if (s-1)%a==0]


def roots(s,o):
    ds=[d for d in range(1,o) if o%d==0]
    a=next(a for a in range(2,100) if pow(x:=pow(a,(s-1)//o,s),o,s)==1 and all(pow(x,d,s)!=1 for d in ds))
    g=pow(a,(s-1)//o,s)
    return [pow(g,j,s) for j in range(1,o) if gcd(j,o)==1]


def layers(s,o,c):
    rr=roots(s,o); m=s
    for z in range(1,c+1):
        require(len(rr)==len(set(rr)) and all(0<b<m and pow(b,o,m)==1 for b in rr),'complete unique lift')
        yield m,rr,m**19
        m*=s;rr=[pow(b,s,m) for b in rr]


def logarithm(r):return (log10(r.numerator)-log10(r.denominator))/10


def main():
    here=Path(__file__).resolve().parent
    book=json.loads((here/'T18R1Primes.json').read_bytes())
    kernel=runpy.run_path(str(here.parents[1]/'RootFiveNext'/'PrimeCheck.py'))
    def prime(n):
        if n<2**64:return kernel['prime64'](n)
        current=n
        for row in book[str(n)]:
            require(current==row[0],'ECPP chain binding')
            current=kernel['level'](*row)
        return kernel['prime64'](current)
    require(all(prime(q) for q in (P,T,Q,R,*F)) and len(set(F))==len(F),'proof-grade targets and compulsory bases')
    require(R%4==1 and 3**5030<=B<3**5031 and min(T,Q)>5031 and 3**60>=P**19, 'Euler, length and LTE')
    require(orders(P)==[3,9] and orders(T)==[3,23,69,277,831],'complete first two odd orders')
    require(sigma(T,18)%Q==0 and sigma(Q,2)%R==0,'exact forced path')
    X,_,Y,_=state(rows); c,d,e=(dict(rows)[p]-vp(Y,p) for p in (P,T,Q))
    require((c,d,e)==(276,17,1),'demands')
    p0=list(layers(P,3,c)); t0=list(layers(T,3,d))
    C={}; A={}; D={}
    def keep(tab,b,n,k):
        if b<3 or b%2==0 or b in dict(rows) or k*(b.bit_length()-1)>=n.bit_length() or b**k>=n:
            return
        if any(pow(h,b-1,b)!=1 for h in (2,3,5,7,11,13) if h<b):return
        tab[b]=max(tab.get(b,1),Fraction(n,b**k))
    for m,ls,pow19 in p0+list(layers(P,9,c)):
        for b in ls:keep(A,b,pow19,20)
    # Higher order T may spend at least 4 exponents; the smaller two still
    # allow conservative coverage and simpler bound composition.
    for o in orders(T):
        for m,ls,pow19 in layers(T,o,d):
            for b in ls:keep(D,b,pow19,20 if o==3 else 40)
    for m,rs,pw in p0:
        for n,ss,tw in t0:
            inv=pow(m,-1,n)
            for r in rs:
                for s in ss:keep(C,r+m*((s-r)*inv%n),pw*tw,20)
    loss={b:max(C.get(b,1),A.get(b,1)*D.get(b,1)) for b in C.keys()|A.keys()|D.keys()}

    # Q order 11: allocate ten units. Q order 19: allocate twelve, and
    # ignore t-powers / other proved composites in the full minimal-root group.
    qord=orders(Q); require(qord==[11,19,209],'Q orders')
    for o in qord:
        budget=10 if o==11 else 12
        for b0 in roots(Q,o):
            b=b0 if b0%2 else b0+Q
            while b**(10*budget)<Q**90:
                require(b==T or b%T==0 or any(pow(h,b-1,b)!=1 for h in (2,3,5,7,11,13) if h<b),('Q losing prime candidate',b,o))
                b+=2*Q
    # Verify shared 19/LTE budget against every length and allowed order subset.
    for L in range(3,5032,2):
        k=vp(L,P)
        for a in [0,1]+[a for a in orders(P) if L%a==0]:
            for b in [0]+[b for b in orders(T) if L%b==0]:
                for q in [0]+[q for q in qord if L%q==0]:
                    pprice=(6*k if a else 0)
                    gprice=2*int(a==3 or b==3)+2*int(a==9)+4*int(b>3)
                    qprice=0 if q==0 else 10 if q==11 else 12
                    require(pprice+gprice+qprice<=L-1, ('joint length',L,a,b,q))
    def net(b,a):
        W=sigma(b,a); cp,ct,cq=(vp(W,p) for p in (P,T,Q))
        if cp>c or ct>d or cq>e:return None
        return Fraction(b**(10*a),(P**cp*T**ct)**19*Q**(90*cq))*loss.get(b,1)
    G=Fraction(X**10*(P**c*T**d)**19*Q**(90*e),prod(loss.values()))
    print('nominal minus loss',logarithm(G),'loss entries',len(loss),flush=True)
    for b in F:
        w=vp(Y,b); best=None
        require(w>0 and b not in dict(rows),'authentic mandatory credit prior to minimization')
        for a in range(w+w%2,5031,2):
            if X*b**a>B:break
            n=net(b,a)
            if n is not None and (best is None or n<best):best=n
        require(best is not None,'missing modeled gain')
        G*=best
    print('joint with mandatory gain',logarithm(G),flush=True)
    require(G>B**10,'insufficient price')


if __name__=='__main__':main()
