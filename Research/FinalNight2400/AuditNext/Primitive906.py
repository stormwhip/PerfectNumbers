"""Independent exact integer universal 7^906 high-s emitter bounds; no repository-code imports."""
from functools import cache
from math import gcd,prod
A=(7**907-1)//6;X=7**906;W=7*X;B=10**2400;C=10**7
@cache
def root(n,e):
 if e==1:return n
 v=1<<((n.bit_length()+e-1)//e)
 while True:
  w=((e-1)*v+n//v**(e-1))//e
  if w>=v:return v
  v=w
allrows={}
for s in range(682,711):
 Y=7**s;Q=2*Y-1;T=B//(X*A*Q);allow=set()
 for m in range(1,110):
  if C**(m+2)>A:continue
  for h in range(m+m%2,8002,2):
   q0=2*Y-1;assert X*q0*(2*q0)**3>27*B and q0>5100 and 3**5100>B
   if X*q0*C**h>B or X*A*q0*C**(h-m)>B:break
   if (h+1)%7==0:continue
   M=pow(Y,-1,h+1);M+=0 if M%2 else h+1
   for _ in range(8):
    Q=2*M*Y-1
    if gcd(M,133)==1 and all(Q%z for z in range(3,98,2)):break
    M+=2*(h+1)
   Q=2*M*Y-1;T=B//(X*A*Q)
   lo=max(C+1,root((2*Q-1)//3,h)+1);hi=root(A//C**2,m)
   if h>m:hi=min(hi,root(T,h-m))
   if lo>hi:continue
   if h==m==2 and (18*A)**2+9*A*Q<Y*Q**2:continue
   if 3*W*T<Y*Q and 3*T<2*Y:hi=min(hi,2*(W//Y)+1)
   if hi<lo:continue
   d=h+1-m;Dmax=6*(A//lo**m);pos=(W-1)*hi**d;neg=Q*hi**d+(Q+1)*Dmax
   # A0 is nonzero and A0=-1-6A (mod1814) from z=1 (mod1814). Work directly in units of YQ, no floored upper-bounds computation.
   residue=((-1-6*A)*pow(Y,-1,1814))%1814
   if (residue or 1814)*Y*Q>pos and ((-residue)%1814 or 1814)*Y*Q>neg:continue
   allow.add((m,h))
 allrows[s]=allow
count=[]
for s in range(682,711):
 assert allrows[s]==({(2,4)} if s<=684 else set());Y=7**s
 for m,h in allrows[s]:
  cap=root((B//(X*A))**h*3**(h-m)//2**(h-m),2*h-m);K=(cap+1)//(2*Y);count.append(K)
  for n in range(1,K+1,2):
   q=2*n*Y-1
   if gcd(n,133)==1 and (q-1)%(h+1)==0:assert pow(2,q-1,q)!=1
assert count==[300,42,6];print('PASS all-support 7,906 new s<=681; three surviving 4/2 shapes composed via Euler candidates, counts',count)
