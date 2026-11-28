"""All odd bases. Price is 19/5 at each target; common order five by CRT."""
from fractions import Fraction
from math import gcd,isqrt,prod
from functools import lru_cache
P,T,E=11,879701,462
B=10**2400

def divs(n):return [d for d in range(1,n+1,2) if n%d==0]
@lru_cache(None)
def generator(p):
    fac={q for q in range(2,p) if (p-1)%q==0 and all(q%d for d in range(2,isqrt(q)+1))}
    return next(g for g in range(2,p) if all(pow(g,(p-1)//q,p)!=1 for q in fac))
def levels(p,o,c):
    g=pow(generator(p),(p-1)//o,p)
    a=[pow(g,j,p) for j in range(1,o) if gcd(o,j)==1];m=1
    for u in range(1,c+1):
        m*=p;yield m,a
        if u<c:a=[r+m*((-((pow(r,o,m*p)-1)//m)*pow(o*pow(r,o-1,p),-1,p))%p) for r in a]

def check(f):
    p,t=P,T
    assert all(t%i for i in range(2,isqrt(t)+1)) and t-1==4*25*19*463
    X=p**E*t**f;A=(p**(E+1)-1)//(p-1);C=(t**(f+1)-1)//(t-1)
    assert gcd(A*C,X) in (t,p*t)
    D=A*C//t; ct=f-1
    assert 3**8000>B and t>8000 and 3**(5*(p-1))>=p**19
    # Common order 5 joint and both single 5 options. High t orders
    # reserve four powers of the base for p at order five.
    a5=[(1,(0,)),*levels(p,5,E)];b5=[(1,(0,)),*levels(t,5,ct)]
    small={};large={}
    def charge(store,r,m,h):
        if r<3 or not r%2 or 5*h*(r.bit_length()-1)>=19*m.bit_length():return
        if any(r%k==0 and r not in (k,k*k) for k in (3,5,7,11,13,17,19,23,29,31,37,41,43)):return
        if r**(5*h)<m**19:store[r]=max(store.get(r,1),Fraction(m**19,r**(5*h)))
    for n,bb in b5:
        inv=1;pi=pow(p,-1,n)
        for m,aa in a5:
            for a in aa:
                for b in bb:charge(small,a+m*((b-a)*inv%n),m*n,4)
            inv=inv*pi%n
    for o in divs((t-1)//4):
        if o<=5:continue
        h=o-5
        if 3**(5*min(h,8000))>=t**(19*ct):continue
        if o>100:
            R=3
            while R**(5*h)<t**(19*ct):R*=2
            assert R<100000
            for r in range(3,R,2):
                if pow(r,o,t)!=1:continue
                m=gcd(r**o-1,t**ct);charge(large,r,m,h)
        else:
            for m,aa in levels(t,o,ct):
                for r in aa:charge(large,r,m,h)
    U=prod(small.values(),start=Fraction(1))*prod(large.values(),start=Fraction(1));M=p**E*t**ct
    return Fraction((U.numerator+U.denominator-1)//U.denominator)
from pathlib import Path
import json,gzip,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Session20261126'));from PivotCheck import C

def certify(f):
 X=P**E*T**f;M=X//gcd(X,C.sigma(P,E)*C.sigma(T,f));U=check(f)
 s=C.State([(P,E),(T,f)]);assert not s.conflict and not s.fixed_euler and set(s.bad)=={7,19}
 D=json.loads((H/('OrdinaryForest'+str(f)+'.json')).read_bytes());K=D['roots'];O=D['owners'];V=set(K)|{q for q,_ in O}
 Bk=json.loads(gzip.decompress((H/('PrimeForest'+str(f)+'.json.gz')).read_bytes()));used=set()
 def prime(n):
  a=n
  if n>=2**64:
   used.add(str(n))
   for row in Bk[str(n)]:assert row[0]==a;a=C.pc.level(*row)
  assert C.pc.prime64(a);return True
 assert prime(P) and prime(T)
 C.validate_forest(s,K,O,128,prime);assert used==set(Bk)
 if f==4:
  r=202615377649735751;y=4495983470863039
  assert prime(r) and prime(y) and r%4==y%4==3 and C.sigma(T,4)%r==0 and C.sigma(r,2)%y==0
  assert pow(r,5,P)!=1 and pow(r,(T-1)//4,T)!=1 # r always inert
  assert y%P==1 and pow(y,(T-1)//4,T)!=1 and 3**(P**4-1)>B
 for q in V:
  if q%4==1:
   m=gcd(M,q+1);initial=(X*q)**5*(M//m)**19
   if f==4:
    assert initial*r**20>B**5*U # r^>=4
    assert initial*(r*y)**10>B**5*U*P**(3*19) # r^2 forces y^>=2, with y supply at most three 11s
   else:assert initial>B**5*U
 s.fixed_euler=True;lb,w=C.Forest(s,K,O,128).lower();assert lb>B and w is None
 print('PASS',f,'vertex count',len(V),'ECPP',len(Bk),'ordinary forest floor',len(str(lb))-1)
if __name__=='__main__':
 for f in [int(x) for x in sys.argv[1:]] or [4,6]:certify(f)
