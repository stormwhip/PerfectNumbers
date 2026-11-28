"""Independent full split inventory of (3,12) / 797161^66 old-new join, without repo imports."""
import json,gzip,hashlib
from math import gcd,prod
from pathlib import Path
from collections import Counter
H=Path(__file__).resolve().parents[1];old=json.load(gzip.open(H.parent/'Night2400/B/Fiber66.json.gz'));new=json.load(gzip.open(H/'Three/WholeR.json.gz'));B=10**2400;bad=7*11*13*19*31
sg=lambda q,e:(q**(e+1)-1)//(q-1)
def state(P):
 X=prod(q**e for q,e in P);raw=prod(sg(q,e) for q,e in P);odd=sum(e%2 for q,e in P);S=raw//2**odd;D=S//gcd(X,S);return X,D,gcd(bad,X*raw)==1 and gcd(D,X)==1 and X*D<=B and raw<=2*X and odd<=1 and all(not e%2 or q%4==e%4==1 for q,e in P)
def domain(P,r):
 X,d,ok=state(P);assert ok and d%r==0 and r not in dict(P);h=0;L=[]
 while d%r==0:d//=r;h+=1
 while X*d*r**h<=B:
  if state(P+[(r,h)])[2]:L.append(h)
  h+=1
 return L,h
P=[(3,12),(797161,66)];L,tail=domain(P,5897);assert len(L)==97 and tail==430 and set(L)-set(map(int,old['tree']['cases']))=={6} and len(old['tree']['cases'])==96
P+=[(5897,6)];R=sg(5897,6);L,tail2=domain(P,R);assert L==[2,4,8,10,12,16,22,24,26,28,30,32] and R==new['tree']['q'];counts=Counter()
def walk(P,n):
 assert n is not None;kind=n['type'];counts[kind]+=1
 if kind=='split':
  r=n['q'];live,_=domain(P,r);assert set(live)==set(map(int,n['cases']))
  for k in live:walk(P+[(r,k)],n['cases'][str(k)])
walk(P,new['tree']);assert counts=={'split':294,'forest':7916,'pair':1,'hard':1,'four-parity':1};print('PASS all independent exact split domains, old secondary tail',tail,'new tertiary tail',tail2,'new results',counts)
