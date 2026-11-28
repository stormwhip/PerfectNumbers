#!/usr/bin/env python3
"""Euler-placement and exact U children at t^28, using a triple cubic price."""
from fractions import Fraction
from itertools import combinations, product
from math import gcd, prod
from pathlib import Path
import runpy
import argparse
from functools import cache

m=runpy.run_path(str(Path(__file__).with_name('ProbeT18R1.py')))
P,T,B,state,sigma,vp,require,orders,roots,layers=[m[k] for k in ('P','T','B','state','sigma','vp','require','orders','roots','layers')]
S=1109
U=244980869729503357305949
BASE=((P,276),(T,28))


def pock(n, qs):
    F=prod(qs)
    require((n-1)%F==0 and F*F>n and pow(2,n-1,n)==1 and all(gcd(pow(2,(n-1)//q,n)-1,n)==1 for q in qs),'Pocklington witnesses')


def verify_primes():
    prime64=runpy.run_path(str(Path(__file__).resolve().parents[2]/'RootFiveNext'/'PrimeCheck.py'))['prime64']
    require(all(prime64(q) for q in (P,T,S,19299719,22797223643,3,5,7,11,73,113,1721,1326017491966837)), 'deterministic small primes')
    m=703968016464090107201
    pock(m,(19299719,22797223643));pock(U,(m,))


@cache
def layer_cache(s,o,c):
    return tuple(layers(s,o,c))


def complete_loss(rows, caps, ps=(P,T,U)):
    tab=[{} for _ in range(4)]
    def keep(pool,b,n,k):
        if b>=3 and b%2 and b not in dict(rows) and k*(b.bit_length()-1)<n.bit_length() and b**k<n and all(pow(a,b-1,b)==1 for a in (2,3,5,7,11,13) if a<b):
            pool[b]=max(pool.get(b,1),Fraction(n,b**k))
    def merge(A,B):
        m,rr,p=A;n,ss,q=B;v=pow(m,-1,n)
        return m*n,[r+m*((s-r)*v%n) for r in rr for s in ss],p*q
    X=state(rows)[0]
    cubic=[]
    for s,c in zip(ps,caps):
        active=[]
        for M,rs,N in layer_cache(s,3,c):
            if X*min(r if r%2 else r+M for r in rs)**2>B:
                break
            active.append((M,rs,N))
        cubic.append(active)
    # Every nonempty subset of active cubic targets shares two exponents;
    # CRT modulo its full product covers every positive-loss ordinary base.
    # Merge the P,T pair once before all U levels.
    for arrays in cubic:
        for M,rs,N in arrays:
            for b in rs:keep(tab[0],b,N,20)
    pq=[]
    xcap=B//X
    for i,j in combinations(range(3),2):
        for a,b in product(cubic[i],cubic[j]):
            z=merge(a,b)
            for b in z[1]:keep(tab[0],b,z[2],20)
            if i==0 and j==1 and gcd(z[0],U)==1:pq.append(z)
    # At positivity b^20 < M^19 and b >= the minimal representative of
    # each projecting CRT block. Exact base-size cap cheaply prunes many.
    # A fixed CRT combination of the first two levels has one inverse
    # per third level; update it by a single q-adic digit, instead of
    # calling a big-integer Euclidean inverse for each cell.
    if cubic[2]:
        p3=ps[2]
        for m,rr,pm in pq:
            baseinv=pow(m,-1,p3)
            inv=baseinv
            for n,ss,pn in cubic[2]:
                threshold=19*(m.bit_length()+n.bit_length())
                full=None
                for r,s in product(rr,ss):
                    k=r+m*((s-r)*inv%n)
                    if k>=3 and k%2 and 20*(k.bit_length()-1)<threshold and k*k<=xcap:
                        if full is None: full=pm*pn
                        keep(tab[0],k,full,20)
                # Unique lift of m*inv=1 modulo n to modulo n*p3.
                inv += n*((-((m*inv-1)//n)*baseinv)%p3)
    for j,s in enumerate(ps,1):
        for o in orders(s):
            if o==3:continue
            for M,rr,N in layers(s,o,caps[j-1]):
                if (X*min(r if r%2 else r+M for r in rr)**(o-1)>B):break
                for b in rr:keep(tab[j],b,N,20 if j==1 else 40)
    return {b:prod(t.get(b,1) for t in tab) for b in set().union(*tab)}


def check_domain():
    require(3**5030<=B<3**5031 and P-1==18 and min(T,U)>5031 and 3**60>=P**19,'length and LTE bounds')
    ops=[orders(p) for p in (P,T,U)]
    require(ops==[[3,9],[3,23,69,277,831],[3,29,87]],'complete odd order lists')
    for L in range(3,5032,2):
        for a,b,c in product(*[[0]+([1] if i==0 else [])+[d for d in o if L%d==0] for i,o in enumerate(ops)]):
            cost=2*int(3 in (a,b,c))+2*int(a==9)+4*int(b>3)+4*int(c>3)+(6*vp(L,P) if a else 0)
            require(cost<=L-1,('internal length allocation',L,a,b,c))
    X,_,Y,_=state(BASE)
    D=Y//gcd(X,Y)
    require(U%4==1 and vp(D,U)==vp(Y,U)==1 and sigma(T,28)%U==0,'forced U, exactly one incoming unit')
    h=next(h for h in range(1,5031) if X*(D//U)*U**h>B)
    raw=[a for a in range(1,h,4) if not m['v']['raw_closed'](BASE+((U,a),))]
    require(raw==[1,5,9,13,17,21,25], 'exact raw Euler domain')
    ordinary=[a for a in range(2,h,2) if not m['v']['raw_closed'](BASE+((U,a),))]
    require(ordinary==list(range(2,28,2)),'complete ordinary raw U domain')
    # Euler placement at 1109 has been excluded independently, hence 1109^2
    # divides N. At U^26 even the minimum additional 1109 power is fatal.
    euler_s=runpy.run_path(str(Path(__file__).with_name('VerifyT28Euler.py')))
    require(euler_s['classify'](28)==(list(range(1,198,4)),394),'Euler-at-1109 prerequisite')
    _,_,Y26,M26=state(BASE+((U,26),))
    require(vp(Y26,S)==1 and M26*S>B,'strict U^26 terminal with ordinary 1109')
    return raw,h


def terminal(a):
    rows=BASE+((U,a),)
    X,H,Y,_=state(rows)
    if a in (5,17):
        F=(3,5,7)
        require(all(Y%q==0 for q in F),'authentic compulsory outgoing labels')
        require(Fraction(H,X)*prod(Fraction(sigma(q,2),q*q) for q in F)>2,'strict abundance')
        return True, 'abundance'
    caps=[f-vp(Y,q) for q,f in rows]
    require(min(caps)>=0,'nonnegative demands')
    loss=complete_loss(rows,caps)
    V=Fraction(X**10*prod(q**(19*c) for (q,_),c in zip(rows,caps)),prod(loss.values()))
    compulsory=[q for q in (S,3,5,7,11,73,113,1721,1326017491966837) if Y%q==0]
    for q in compulsory:
        best=None; d=vp(Y,q)
        for f in range(d+d%2,5031,2):
            mass=q**f
            if X*mass>B:break
            A=sigma(q,f); u=[vp(A,p) for p,_ in rows]
            if any(z>c for z,c in zip(u,caps)):continue
            r=Fraction(mass**10,prod(p**(19*z) for (p,_),z in zip(rows,u)))*loss.get(q,1)
            if best is None or r<best:best=r
        require(best is not None,'compulsory base net minimum')
        V*=best
    from math import log10
    return V>B**10, (len(loss),(log10(V.numerator)-log10(V.denominator))/10)


def u_low_supply_partition(a, terminal_table=None):
    """Inherited U Euler parity, 19 effective length, full rare supplier cap."""
    require(a in (1,9),'designated Euler exponent')
    uniform=runpy.run_path(str(Path(__file__).with_name('VerifyT28Ordinary.py')))
    prefix=BASE+((U,a),)
    uniform['source_price'](state(prefix)[0])
    loss19,_=m['v']['loss19'](276,{P,T,U,S})
    require(loss19<=10**6 and gcd(P*9,S*277)==1,'19 / 1109 disjoint source allocation')
    require(3**18>=P**2 and all(3**(o*(P**k-1))>=P**(2*k) for o in (3,9) for k in (1,2)) and 3*P**3>5031,'ordinary 19 LTE units')
    X,_,Y,_=state(prefix)
    require(vp(Y,S)==1 and vp(Y,P)==1 and pow(S,3,P)==1 and vp(S**3-1,P)==1,'fixed outgoing and 1109 order-three')
    # Uniform price closes all h≥6: at worst lose 3 additional 19 units.
    require(X*S**6*P**(2*(276-1-3))*S**500>B*10**6,'strict monotone h >= 6 terminal')
    prime=m['v']['prime']
    r=[]
    for h,K in ([(2,7460),(4,6941)] if a==1 else [(2,1567),(4,1458)]):
        rows=prefix+((S,h),)
        X,_,Y,_=state(rows)
        require(X*P**(2*(276-vp(Y,P)))*K**276>B*10**6,'strict rare product caps')
        pool=[b for b in range(3,K,2) if b not in dict(rows) and pow(b,277,S)==1 and prime(b)]
        require(pool[:3]==[13,29,53] and all(pow(b,277,S**2)!=1 for b in pool),'entire feasible rare classes')
        if h==4:
            require(vp(Y,S)==1 and prod(pool[:3])>=K,'three distinct exact supplier terminal')
        else:
            require(vp(Y,S)==1,'one missing supplier unit')
            for b in pool:
                for m0 in range(1,5031//277+1,2):
                    if b**m0>=K:break
                    f=277*m0-1
                    if not m['v']['raw_closed'](rows+((b,f),)):
                        r.append((b,f))
    require(r==[(b,276) for b in ((13,29,53,67,83,103) if a==1 else (13,))], 'complete residual rare source list')
    inbound=runpy.run_path(str(Path(__file__).with_name('Explore276H2.py')))
    left=[]
    for b,f in r:
        rows=prefix+((S,2),(b,f))
        X,_,Y,_=state(rows)
        c=f-vp(Y,b)
        w=min([12]+[o-1 for o in orders(b)])
        if X*b**(w*c)>B:
            loss=prod(inbound['single'](b,c,rows,w).values())
            if X*b**(w*c)>B*loss:
                continue
        c19=276-vp(Y,P)
        nominal=X**10*(P**c19*b**c)**19
        if nominal>B**10:
            loss=inbound['joint'](b,c19,c,rows)
            if nominal>B**10*loss:
                continue
        left.append((b,f))
    require(left==[(13,276)],'remaining U^1 rare source after valuations')
    # Last b=13 has simultaneous cubic 19, t and b. Its own order-one
    # supply is paid with six powers per LTE unit (as at 19).
    b,f=left[0]
    rows=prefix+((S,2),(b,f))
    X,_,Y,_=state(rows)
    targets=(P,T,b)
    C=[dict(rows)[q]-vp(Y,q) for q in targets]
    require(C==[274,27,276] and prime(b) and orders(b)==[3],'third cubic target demands')
    require(3**60>=b**19,'third target LTE payment')
    for L in range(3,5032,2):
        for a,d,e in product(*[[0]+([1] if q in (P,b) else [])+[o for o in orders(q) if L%o==0] for q in targets]):
            cost=2*int(3 in (a,d,e))+2*int(a==9)+4*int(d>3)+6*(int(a>0)*vp(L,P)+int(e>0)*vp(L,b))
            require(cost<=L-1,'compatible triple-cubic and LTE length')
    if terminal_table is not None and 'loss' in terminal_table:
        # Identical valuation caps and excluded/fixed bases, and X at a=9
        # is larger, so earlier a=1 size filters only retain a superset.
        X0, oldcaps, oldfixed, U13=terminal_table['loss']
        require(X>=X0 and C==oldcaps and set(dict(rows))==oldfixed,'covered cached final atom domain')
    else:
        U13=complete_loss(rows,C,targets)
        if terminal_table is not None:
            terminal_table['loss']=(X,C,set(dict(rows)),U13)
    exact=Fraction(X**10*prod(q**(19*c) for q,c in zip(targets,C)),prod(U13.values()))
    require(exact>B**10,'last U1 high-demand terminal')
    print('final rare source U^'+str(a)+', 1109^2, 13^276; losses:',len(U13),flush=True)
    return []


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--except-one',action='store_true')
    args=ap.parse_args()
    verify_primes(); vals,tail=check_domain(); out=[]
    shared={}
    # Run the inexpensive, distinct terminals before the two deep rare cases.
    for a in (5,17,13,21,25,1,9):
        require(a in vals,'covered exact Euler index')
        if a==1 and args.except_one:
            continue
        if a in (1,9):
            require(u_low_supply_partition(a,shared)==[],'all remaining U ordinary-source windows')
            out.append(a)
            print(a,'EXCLUDED by strict rare-source joint terminals',flush=True)
            continue
        ok,info=terminal(a); print(a,'EXCLUDED' if ok else 'OPEN',info,flush=True)
        if ok:out.append(a)
    require(sorted(out)==[a for a in vals if a!=1 or not args.except_one],'claimed complete Euler-U window')
    print('raw Euler tail',tail,'live',vals,'excluded',out,flush=True)
    print('U^26 excluded by ordinary 1109; U even 2..24 outside packet',flush=True)


if __name__=='__main__':main()
