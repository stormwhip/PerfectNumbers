"""Independent geometric-sum partition for complete (7,12) / Q^12 / T^6 secondary."""
import json,gzip,hashlib
from pathlib import Path
from fractions import Fraction
from math import gcd,prod
H=Path(__file__).resolve().parents[1]/'SevenNext';B=10**2400;S=62936242392988051361;sig=lambda r,k:(r**(k+1)-1)//(r-1);Q=sig(7,12);T=sig(Q,12)//13
P=[(7,12),(Q,12),(T,6)]
def state(P,ban):
 X=prod(r**k for r,k in P);raw=prod(sig(r,k) for r,k in P);odd=sum(k%2 for _,k in P);s=raw//2**odd;D=s//gcd(X,s);return X,D,gcd(X,D)==1 and gcd(prod(ban),X*s)==1 and raw<=2*X and X*D<=B and all(not k%2 or r%4==k%4==1 for r,k in P) and odd<=1
def dom(P,r,ban):
 X,D,ok=state(P,ban);assert ok and D%r==0;h=0
 while not D%r:D//=r;h+=1
 accepted=[]
 while X*D*r**h<=B:
  if state(P+[(r,h)],ban)[2]:accepted.append(h)
  h+=1
 return accepted,h
L,tail=dom(P,S,[19]);J=340522774902395416760792885639672290356455394594605085885851976071;assert dom(P+[(S,4)],J,[3,19])==([2,4],12)
load=lambda k:json.load(gzip.open(H/(k+'.json.gz')));four=load('Four');assert set(four['nodes'])=={'2','4'}
old=set(map(int,load('Tertiary')['nodes']['6']));odd={j for j in L if j%2};assert (S+1)%(3*11)==0 and Fraction(sig(7,12),7**12)*prod(Fraction(sig(p,2),p*p) for p in [3,11,13])>2
n=set(map(int,load('Native')['nodes']));f=set(map(int,load('FinalSix')['nodes']));groups=[odd,{4},old-odd,n,f];assert old&odd=={13} and groups==[{1,5,9,13},{4},{14,16,18,20},{8,12},{2,6,10}]
assert sorted(set.union(*groups))==L and sum(map(len,groups))==len(L)==14 and tail==42
print('PASS disjoint 4+1+4+2+3, duplicate previous 13 not double-counted. Monotone tails 42 and 12.');
for n in ['Native','FinalSix']:print(n,hashlib.sha256((H/(n+'.json.gz')).read_bytes()).hexdigest())
