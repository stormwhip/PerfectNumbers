"""Independent anchor split, residual credit extrema, and loss-product check using immutable exceptions."""
from pathlib import Path
from math import gcd,prod
from fractions import Fraction
import json,gzip,hashlib
B=10**2400;Q=16148168401;T=(Q**13-1)//(Q-1)//13;L=3453283;A=(L**61-1)//(L-1)
def sig(q,h):return (q**(h+1)-1)//(q-1)
def val(n,q):
 a=0
 while n%q==0:n//=q;a+=1
 return a
def state(row):
 X=prod(q**h for q,h in row);S=prod(sig(q,h)//(1+h%2) for q,h in row);D=S
 while (g:=gcd(D,X))>1:D//=g
 return X,S,D
row=[(7,12),(Q,12),(T,2),(L,60)];X,S,D=state(row);assert val(D,A)==1;v=1;live=[]
while X*D//A*A**v<=B:
 rr=row+[(A,v)];x,s,d=state(rr)
 if (not v%2 or v%4==A%4==1) and gcd(5*11*19,x*s)==1 and x*d<=B and all(s%q**(h+1)!=0 for q,h in rr):live.append(v)
 v+=1
assert live==[1] and v==4;X,S,D=state(row+[(A,1)]);P=[Q,T,L];demand=[12-val(S,Q),2-val(S,T),60-val(S,L)];assert demand==[11,1,59];G=1
for y in (3,13,73,431):
 assert D%y==0;lo=None;h=2
 while y**h<=B:
  ss=sig(y,h);cost=Fraction(y**h,prod(q**(2*val(ss,q)) for q in P));lo=cost if lo is None else min(lo,cost);h+=2
 assert lo==y*y;G*=lo
assert G==1505668881249;print('PASS unique anchor [1], tail 4, caps',demand,'G',G,'A bits',A.bit_length())
