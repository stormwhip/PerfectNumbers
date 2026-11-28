"""Joint cubic/ninth-order pricing with a shared CRT modulus and square-aware filters."""
from fractions import Fraction
from math import gcd,isqrt,prod,lcm
from functools import cache
B=10**2400;p,e,t=19,292,10018843
G=lambda r,f:(r**(f+1)-1)//(r-1)
@cache
def prime(n):return n>=2 and all(n%d for d in range(2,isqrt(n)+1))
@cache
def levels(q,o,c):
 ds=[l for l in (2,3,41,139,293) if (q-1)%l==0];a=next(g for g in range(2,q) if all(pow(g,(q-1)//l,q)!=1 for l in ds));a=pow(a,(q-1)//o,q);rs=[pow(a,j,q) for j in range(1,o) if gcd(j,o)==1];m=1;out=[]
 for z in range(1,c+1):
    m*=q;out.append((m,rs));rs=[r+m*((-((pow(r,o,m*q)-1)//m)*pow(o*pow(r,o-1,q),-1,q))%q) for r in rs]
 return out

def viable(r):
 def prime_ok(q):return q>=3 and q%2 and q not in (p,t) and pow(2,q-1,q)==1
 return prime_ok(r) or (isqrt(r)**2==r and isqrt(r)%4==1 and prime_ok(isqrt(r)))
@cache
def get(c,D,X):
 assert all(prime(q) for q in (p,t,41,139,293)) and t-1==2*3*41*139*293 and p-1==18 and 3**(p-1)>p**2 and 3**7999>B and t>8000
 # For all shared low orders: enumerate exact o at p (3/9) and at t (3), or free.
 loss={};high={}
 def charge(r,M,h,target):
    if r<3 or not r%2 or h*(r.bit_length()-1)>=2*M.bit_length():return
    power=r**h
    if power.bit_length()>B.bit_length()-X.bit_length()+2:return
    if power//gcd(power,D)>B//(X*D):return
    if r**h<M*M and viable(r):target[r]=max(target.get(r,1),Fraction(M*M,r**h))
 for o,aa in [(1,[(1,[0])]),(3,levels(p,3,e)),(9,levels(p,9,e))]:
    for ot,bb in [(1,[(1,[0])]),(3,levels(t,3,c))]:
        h=lcm(o,ot)-1
        if not h:continue
        for n,ys in bb:
            pi=pow(p,-1,n);inv=pi if o>1 else 1
            for m,xs in aa:
                M=m*n
                for x in xs:
                    for y in ys:
                        r=x+m*((y-x)*inv%n);charge(r,M,h,loss)
                inv=inv*pi%n
 # High t-order uses o-9 powers, up to eight powers separately reserved for p.
 # o=41 among others; a unit shift at 19 has disjoint length from t-order.
 div=[1]
 for l in (3,41,139,293):div+=[l*x for x in div]
 for o in div:
    if o<=3 or o>8000 or 3**min(8000,o-9)>=t**(2*c):continue
    h=o-9
    if o>=123:
        R=3
        while R**h<t**(2*c):R*=2
        if R<=200000:
            for r in range(3,R,2):
                if pow(r,o,t)==1:charge(r,gcd(pow(r,o,t**c)-1,t**c),h,high)
            continue
    for m,roots in levels(t,o,c):
        for r in roots:charge(r,m,h,high)
 return prod(loss.values(),start=Fraction(1))*prod(high.values(),start=Fraction(1))

def prefix(P):
 X=prod(q**f for q,f in P); S=prod(G(q,f)//(1+f%2) for q,f in P);D=S//gcd(S,X);assert gcd(D,X)==1
 def vp(n,q):
    v=0
    while n%q==0:v+=1;n//=q
    return v
 cp=e-vp(S,p);ct=P[1][1]-vp(S,t);assert min(cp,ct)>=0;U=get(ct,D,X);M=p**cp*t**ct
 if any(f%2 for _,f in P):return X*M*M>B*U
 blocks=[G(q,f)//gcd(G(q,f),X) for q,f in P];assert prod(blocks)==D
 H=max(z*prod(gcd(z,k) for j,k in enumerate(blocks) if i!=j) for i,z in enumerate(blocks));K=X*M*M*U.denominator;A=U.numerator
 for i in range(cp+1):
    for j in range(ct+1):
        m=p**i*t**j;q=2*m-1
        if K*q>B*A*m*m:continue
        for (r,f),z in zip(P,blocks):
            if (r==p and i) or (r==t and j) or z<q:continue
            if z//q>=4*m:return False
            k=z*pow(q,-1,4*m)%(4*m)
            if 0<k<=z//q and z%k==0:return False
        if X*D*q>B:continue
        if 4*K*X*D*q**4<=9*B**2*A*H*m*m:return False
 return True
if __name__=='__main__':
 assert __debug__ and prefix([(p,e),(t,88),(435613618109571179,10)])
 print('PASS exact critical 88/10 terminal')
