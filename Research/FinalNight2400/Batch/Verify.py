"""Batched monotone budget certificate for a disjoint-order two-component prefix."""
import math,sys
from fractions import Fraction
from functools import lru_cache
B=10**2400
def prime(n):return n>=2 and all(n%d for d in range(2,math.isqrt(n)+1))
def geom(x,h):return (x**(h+1)-1)//(x-1)
@lru_cache(None)
def price(p,c,w,divs):
    # Target charge is p^(w*u); no rounding penalty. Keep primes and possible Euler squares.
    exc={};g=1
    while any(pow(g,(p-1)//l,p)==1 for l in {2,*[l for l in divs if prime(l)]}):g+=1
    assert pow(g,p-1,p)==1
    for o in divs:
        if o==1 or 3**min(8000,o-1)>=p**(w*c):continue
        assert o-1>=w
        def cost(r,u):
            if r<3 or r%2==0 or any(r%k==0 and r not in (k,k*k) for k in (3,5,7,11,13,17,19,23,29,31,37)):return
            num=p**(w*u)
            if (r.bit_length()-1)*(o-1)<num.bit_length() and r**(o-1)<num:
                root=math.isqrt(r)
                if pow(2,r-1,r)!=1 and not (root*root==r and root%4==1 and pow(2,root-1,root)==1):return
                exc[r]=max(exc.get(r,1),Fraction(num,r**(o-1)))
        if o>100:
            R=3
            while R**(o-1)<p**(w*c):R*=2
            if R<200000:
                for r in range(3,R,2):
                    if pow(r,o,p)==1:
                        z=math.gcd(r**o-1,p**c);u=0
                        while z>1:z//=p;u+=1
                        cost(r,u)
                continue
        a=pow(g,(p-1)//o,p);rs=[pow(a,j,p) for j in range(1,o) if math.gcd(o,j)==1];m=1
        for u in range(1,c+1):
            m*=p
            for r in rs:cost(r,u)
            if u<c:rs=[r+m*((-((pow(r,o,m*p)-1)//m)*pow(o*pow(r,o-1,p),-1,p))%p) for r in rs]
    loss=math.prod(exc.values(),start=Fraction(1))
    print('price',p,c,'exceptions',len(exc),'loss bits',loss.numerator.bit_length()-loss.denominator.bit_length(),flush=True)
    return loss


p,e,t=11,396,2383
@lru_cache(None)
def losses():
    assert all(prime(k) for k in (p,t,397)) and t-1==2*3*397 and p-1==2*5
    assert math.gcd(5*p,3*397*t)==1 and 3**(p-1)>=p**4 and 3**(t-1)>=t**2
    return price(p,e,4,(1,5))*price(t,231,2,(1,3,397,1191))

def run():
    A=geom(p,e);assert A%t==0 and (A//t)%t; A//=t
    dom=[];f=1
    while p**e*A*t**f<=B:
        X=p**e*t**f;C=geom(t,f);S=A*t*C;D=S//math.gcd(S,X)
        if f%2==0 and math.gcd(D,X*19*7)==1 and S<=2*X and X*D<=B:dom.append(f)
        f+=1
    assert f==468 and dom==list(range(2,233,2))
    loss=losses();a,b=loss.as_integer_ratio();yes=[];no=[]
    for f in dom:
        if f<150:no.append(f);continue  # unclaimed, not proved feasible
        C=geom(t,f);X=p**e*t**f;c=e
        while C%p==0:C//=p;c-=1
        D=A*C;assert math.gcd(X,D)==1
        # For i,j with m=p^i t^j, an exterior Euler prime requires m <= floor((B/(XD)+1)/2).
        # To prove *all* large m are exterior, exclude each interior block via reciprocity or size.
        # Both targets are 3 mod 4. Thus q|A requires i=0; q|C requires j=0.
        # m then <=t^ct or p^c respectively, plus q<=Z => m<=(Z+1)/2.
        cap=max((B//(X*D)+1)//2,min(t**(f-1),(A+1)//2),min(p**c,(C+1)//2))
        # N >= X*p^(4c)*t^(2ct)/(U*p^(3i)*t^j) since q >= m.
        # For each t^j choose largest p^i allowed by m<=cap. No Euler exponent omitted.
        worst=0;powp=p**c; tj=1
        for j in range(f):
            while powp>=p and powp*tj>cap:powp//=p
            if powp*tj>cap:break
            worst=max(worst,powp**3*tj);tj*=t
        if X*p**(4*c)*t**(2*(f-1))*b>B*a*worst:yes.append(f)
        else:
            # Refine the weak common cap using individual windows. Once q is external,
            # any designated q-source supplies p^u t^v; y<=3BH/(2XDQ²).
            H=max(A,C) if math.gcd(A,C)==1 else D
            pp=[p**i for i in range(c+1)]; tt=[t**j for j in range(f)]
            K=X*pp[c]**4*tt[-1]**2*b;D0=X*D
            def outside(Z,m,Q):
                if Q>Z:return True
                if Z//Q>=4*m:return False
                k=Z*pow(Q,-1,4*m)%(4*m)
                return not(0<k<=Z//Q and Z%k==0)
            def covers():
                for j,n in enumerate(tt):
                    for i,z in enumerate(pp):
                        m=z*n;Q=2*m-1
                        if K*Q>B*a*z**4*n**2:continue
                        if not ((i or outside(A,m,Q)) and (j or outside(C,m,Q))):return False
                        if D0*Q>B:continue
                        limit=3*B*H//(2*D0*Q**2)
                        # For y=P*T<=limit, P^3*T<=limit*min(p^rp,limit)^2.
                        worst=min(limit*min(pp[c-i],limit)**2,pp[c-i]**3*tt[f-1-j])
                        if 2*K*Q**2<=3*B*a*z**4*n**2*worst:return False
                return True
            (yes if covers() else no).append(f)
    print('11^396 2383: closed',yes,'remain',no,flush=True)
    return yes,no
if __name__=='__main__':
    assert __debug__
    yes,no=run();assert yes==list(range(150,233,2)) and no==list(range(2,150,2))
