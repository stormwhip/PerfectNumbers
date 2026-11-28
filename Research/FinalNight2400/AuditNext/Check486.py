"""Independent raw domain, compulsory-s source and joint-price 755/1517 cell audit."""
from math import gcd,lcm,isqrt,prod
from fractions import Fraction
from itertools import product
import time
st=time.perf_counter();p,s,t=7,349667,1229048719;B=10**2400;e=486;x=p**e;g=lambda q,h:(q**(h+1)-1)//(q-1);A=g(p,e);assert A%(s*t)==0 and gcd(A//s//t,s*t)==1 and gcd(A,487*6)==1
isprime=lambda n:n>=2 and all(n%i for i in range(2,isqrt(n)+1));assert all(map(isprime,[p,s,t,359,487,41,10259]));assert s-1==2*359*487 and 3**7999>B and s>8000 and t-1==2*3*41*487*10259
def domain(k):
 u=1
 while x*A//k*k**u<=B:u+=1
 return u
assert domain(s)==286 and domain(t)==175
for o in [359,487,718,974]:
 for inside in [False,True]:
  n=(975 if inside else 3);step=974 if inside else 2
  while x*(1 if inside else A)*n**(o-1)<=B:
   if n!=p and (not inside or A%n==0) and pow(n,o,s)==1 and isprime(n):
    Z=g(n,o-1);assert lcm(x*n**(o-1),A*(Z//gcd(2,Z)))>B
   n+=step
# Regenerate weighted exclusions with opposite CRT and power lifts.
low={};hi={};maxsize=B//(x*s*s*t*t)
def lev(q,o,c):
 a=next(z for y in range(2,q) if all(pow((z:=pow(y,(q-1)//o,q)),j,q)!=1 for j in range(1,o) if o%j==0));m=q
 for k in range(c):yield m,[pow(a,i,m) for i in range(1,o) if gcd(i,o)==1];m*=q;a=pow(a,q,m)
def put(store,r,m,h):
 if r<3 or r%2==0 or r in (7,19,s,t) or 10*h*(r.bit_length()-1)>=19*m.bit_length() or (r.bit_length()-1)*h>=maxsize.bit_length():return
 if any(r%d==0 and r not in (d,d*d) for d in (3,5,7,11,13,17,19,23,29,31,37,41,43)):return
 z=isqrt(r)
 if pow(2,r,r)!=2 and not(z*z==r and z%4==1 and z not in (7,19,s,t) and pow(2,z,z)==2):return
 n=r**(10*h);a=m**19
 if n<a:store[r]=max(store.get(r,1),Fraction(a,n))
lt=[(1,[0]),*lev(t,3,85)]
for a,rr in [(1,[0]),*lev(p,3,e)]:
 for b,ss in lt:
  inv=pow(b,-1,a) if a>1 else 0
  for x0,y in product(rr,ss):put(low,y+b*(((x0-y)*inv)%a),a*b,2)
orders=[1]
for k in (3,41,487,10259):orders +=[n*k for n in orders]
for o in orders:
 if o<=3 or o>8000 or 3**(o-3)>=t**170:continue
 h=o-3
 if 10000**h>=t**170:
  for z in range(3,10000,2):
   if z**h>=t**170:break
   if pow(z,o,t)==1:put(hi,z,gcd(pow(z,o,t**85)-1,t**85),h)
 else:
  for m,rr in lev(t,o,85):
   for z in rr:put(hi,z,m,h)
U=prod(low.values(),start=Fraction(1))*prod(hi.values(),start=Fraction(1));U=-(-U.numerator//U.denominator);rem=[];done=[]
def val(a,q):
 n=0
 while a%q==0:n+=1;a//=q
 return n
for i,j in product(range(2,286,2),range(2,175,2)):
 X=x*s**i*t**j;Z=[A,g(s,i),g(t,j)];S=prod(Z);D=S//gcd(S,X)
 if gcd(D,19*X)>1 or X*D>B or S>2*X:continue
 cp=e-val(S,p);ct=j-val(S,t);cs=i-val(S,s);assert cs==i-1 and 0<=ct<=85
 T=s**cs;M=p**cp*t**ct;Z=[b//gcd(b,X) for b in Z];assert prod(Z)==D
 # Direct upper bound for T*m in the three mutually exhaustive locations. Multiple eligible locations never earn cumulative credit.
 cap=max((B//(X*D)+1)//2,min((Z[0]+1)//2,T*t**ct),min((Z[2]+1)//2,T*p**cp))
 (done if (X*T)**10*M**19*T**9>B**10*U*cap**9 else rem).append((i,j))
assert len(rem)==762 and len(done)==755 and max(i for i,j in rem)==98 and max(j for i,j in rem)==60;print('PASS 7,486 exact compound-source and CRT labels',len(low),len(hi),'live/cut/survive',len(rem)+len(done),len(done),len(rem),'elapsed',round(time.perf_counter()-st,3))
