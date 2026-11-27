"""Independent rearrangement check for full (7,906) two-factor impossibility. Derive lower bounds by explicit 7-ary digit lifting; test A and component mass via a two-sided rational interval."""
import sys,time
from math import gcd,isqrt
from functools import cache
from fractions import Fraction
A=(7**907-1)//6;X=7**906;W=7*X;B=10**2400;U=579125;C=10**7;s0=time.perf_counter()
@cache
def root(n,k):
 if k==1:return n
 if k==2:return isqrt(n)
 v=1<<((n.bit_length()+k-1)//k)
 while True:
  w=((k-1)*v+n//(v**(k-1)))//k
  if w>=v:return v
  v=w
@cache
def roots(t,j,amod):
 if j%7==0:return ()
 b=[x for x in range(1,7) if pow(x,3*j,7)==1 and A*pow(x,-j,7)%7 in (pow(2,amod,7),pow(4,amod,7))];m=7
 for _ in range(1,t):
  n=m*7;u=pow(A,3,n);b=[y for x in b for k in range(7) if pow((y:=x+k*m),3*j,n)==u];m=n
 return tuple(x+m*((1-x)*pow(m,-1,1814)%1814) for x in b)
@cache
def bounds(t,a,j):
 m=7**t;r0=min(1+1814*((pow(y,7**(t-1),m)-1)*pow(1814,-1,m)%m) for y in (2,4));bs=roots(t,j,a%3);return (max(C*m,r0),max(C,min(bs))) if bs else (A+1,A+1)
assert C**110>A and all(root(A,k)**k!=A for k in range(2,110));assert A**3%49==22 and all(pow(k,21,49) in (1,48) for k in range(1,49) if k%7)
loQ=2*7**482-1;stats=[0,0];patterns=set();count=0;hard=set()
for u in range(82,144):
 base=C*7**(u-4);assert base**12>A
 for i in range(1,12):
  if base**i>A:break
  for j in range(1,110):
   if base**i*C**j>A:break
   if gcd(i,j)>1 or i==j==1:continue
   R0,L0=bounds(u-4,i,j)
   if R0**i*L0**j>A:continue
   for h in range(i+i%2,8001,2):
    if X*R0**h*loQ>B:break
    if (h+1)%3:continue
    l=h+1;v7=0
    while l%7==0:l//=7;v7+=1
    R,L=bounds(u-v7,i,j)
    if R**i*L**j>A:continue
    g=j+j%2
    while X*R**h*L**g*loQ<=B:
     for s in range(482,666):
      Q=2*7**s-1;budget=B*U//(X*Q*7**(2*max(0,901-u-s)));d=j*h-i*g
      if budget<1 or (R**d*A**g>budget**j if d>=0 else L**(-d)*A**h>budget**i):continue
      for who,ep,mult in [('r',h,i),('b',g,j)]:
       zmin=R if who=='r' else L;other=L if who=='r' else R;otm=j if who=='r' else i;ote=g if who=='r' else h
       lo=max(zmin,root((2*Q*(7**u if who=='r' else 1)-1)//3,ep)+1)
       if lo**mult*other**otm>A:continue
       rr,bb=(lo,L) if who=='r' else (R,lo)
       if (rr**d*A**g>budget**j if d>=0 else bb**(-d)*A**h>budget**i):continue
       count+=1;patterns.add((i,j,h,g,who));top=min(root(A//other**otm,mult),root(budget//other**ote,ep));Dmax=6*(A//lo**mult);deg=ep+1-mult;Y=7**s;assert deg>=1
       if Q*top**deg+(Q+1)*Dmax<Q*Y and (W-1)*top**deg<Q*Y:stats[0]+=1;continue
       assert (mult,ep)==(2,2) and otm==1 and (18*A)**2+9*A*Q<Y*Q**2;stats[1]+=1;hard.add(s)
     g+=2
assert count==1490 and stats==[1404,86] and patterns=={(1,2,2,2,'b'),(1,4,2,4,'b'),(2,1,2,2,'r'),(2,5,2,6,'b')};print('PASS independent full sparse enumeration',count,stats,'last s range',min(hard),max(hard),'seconds',round(time.perf_counter()-s0,3))
