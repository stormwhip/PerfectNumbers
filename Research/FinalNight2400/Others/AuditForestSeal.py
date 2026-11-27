"""Independent all-ordinary recurrence and worst-on-vertex comparison. Original joint loss reused."""
from math import gcd,prod
from pathlib import Path
from functools import cache
import json,sys
H=Path(__file__).resolve().parents[1]/'Eleven';sys.path.insert(0,str(H));import ForestSeal as src
P,T,E,B=11,879701,462,10**2400
def sig(x,h):return (x**(h+1)-1)//(x-1)
def val(n,q):
 a=0
 while n%q==0:a+=1;n//=q
 return a
def strip(n,m):
 while (g:=gcd(n,m))>1:n//=g
 return n
for f in (4,6):
 X=P**E*T**f;S=sig(P,E)*sig(T,f);M=X//gcd(X,S);D=strip(S,P*T);U=src.check(f);d=json.loads((H/f'OrdinaryForest{f}.json').read_bytes());K=d['roots'];edge=dict(d['owners']);V=set(K)|set(edge);qset=sorted(q for q in V if q%4==1);kids={q:[] for q in V};
 for q,z in edge.items():kids[z].append(q)
 pool=X*D*prod(edge);childprod={p:prod(v) for p,v in kids.items()}
 @cache
 def node(q,a):
  n=a+a%2;left=128;best=B+1
  while left and q**n<best:
   s=sig(q,n)
   if gcd(s,7*19)==1:
    left-=1;g=gcd(s,childprod[q]);subs=prod(node(v,val(s,v)) for v in kids[q] if g%v==0) if g>1 else 1
    best=min(best,q**n*strip(s,pool)*subs)
   n+=2
  return min(best,q**n)
 v=X*(D//prod(q**val(D,q) for q in K))*prod(node(q,val(D,q)) for q in K);assert v>B
 worst=min((X*q)**5*(M//gcd(M,q+1))**19 for q in qset);rhs=B**5*U
 if f==6:assert worst>rhs
 else:
  r,y=202615377649735751,4495983470863039;assert len({P,T,r,y})==4 and r%4==y%4==3 and sig(T,f)%r==0 and sig(r,2)%y==0 and pow(r,5,11)!=1 and y%11==1 and pow(r,(T-1)//4,T)!=1 and pow(y,(T-1)//4,T)!=1;assert 3**(11**4-1)>B
  assert worst*r**20>rhs and worst*(r*y)**10>rhs*11**57
 print(f,'eligible Euler vertices',len(qset),'all vertices',len(V),'ordinary',len(str(v))-1,'ceil U',U,flush=True)
