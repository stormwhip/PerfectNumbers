"""No project imports: all split domains, references, exact independent forest recurrence on two final reopened rows."""
from pathlib import Path
from functools import cache
from math import prod,gcd
from collections import Counter
import json,gzip,hashlib
H=Path(__file__).resolve().parent.parent/'ThirtyOne268/SmallEleven';P=(11,12);Q=3158528101;B=10**2400;ban=(19,7)
@cache
def sig(q,h):return (q**(h+1)-1)//(q-1)
def val(n,q):
 a=0
 while n%q==0:n//=q;a+=1
 return a
def strip(n,m):
 while(g:=gcd(n,m))>1:n//=g
 return n
@cache
def state(rr):
 X=prod(q**h for q,h in rr);S=prod(sig(q,h)//(1+h%2) for q,h in rr);D=strip(S,X);od=sum(h%2 for q,h in rr)
 if od>1 or any(h%2 and (q%4!=1 or h%4!=1) for q,h in rr) or gcd(X*S,133)>1 or S*(1+od)>2*X or any(val(S,q)>h for q,h in rr) or X*D>B:return None
 return X,S,D,od
@cache
def domain(rr,q):
 X,S,D,od=state(rr);a=val(D,q);assert a>0 and q not in dict(rr);h=a;sz=X*D;ls={}
 while sz<=B:
  r2=rr+((q,h),)
  if state(r2):ls[str(h)]=r2
  h+=1;sz*=q
 return ls,h
def ordinary(rr,K,O,n):
 X,S,D,od=state(rr);assert od==1;ban2=prod([*ban,*[q for q,h in rr if val(S,q)==h]]);pool=X*D*prod(q for q,p in O);kids={x:[] for x in K+[q for q,p in O]}
 for q,p in O:kids[p].append(q)
 @cache
 def cost(q,a):
  h=a+a%2;count=0;best=B+1
  while count<n and q**h<best:
   out=sig(q,h)
   if gcd(out,ban2)==1:
    count+=1;best=min(best,q**h*strip(out,pool)*prod(cost(v,val(out,v)) for v in kids[q] if out%v==0))
   h+=2
  return min(best,q**h)
 return X*(D//prod(q**val(D,q) for q in K))*prod(cost(q,val(D,q)) for q in K)

def audit():
 d=json.load(gzip.open(H/'Forest.json.gz'));book=json.load(gzip.open(H/'Primes.json.gz'));assert sig(*P)==1093*Q and d['q']==Q;root,tail=domain((P,),Q);assert len(root)==77 and tail==252 and set(root)==set(d['cases']);labels=set();C=Counter();found={};historical=[]
 def walk(rr,t):
  X,S,D,od=state(rr);k=t['type'];C[k]+=1
  if k=='c9':historical.append(rr);assert rr==((11,12),(Q,4));return
  if k=='split':q=t['q'];labels.add(q);ls,h=domain(rr,q);assert set(ls)==set(t['cases']);[walk(row,t['cases'][h0]) for h0,row in ls.items()];return
  assert k=='forest',k;K=t['roots'];O=t['owners'];labels.update(K);labels.update(x for x,y in O);assert len(K)==len(set(K)) and all(D%q==0 and q not in dict(rr) for q in K);assert len(O)==len(dict(O));assert all(D%q and q not in dict(rr) for q,y in O)
  if len(rr)==6 and rr[:5]==((11,12),(Q,2),(3325433255988398101,1),(269117,4),(5245249427625080830141,6)) and rr[-1] in [(31012561,2),(31012561,4)]:
   v=ordinary(rr,K,O,t['head']);assert v>B;found[rr[-1][1]]=len(str(v))-1
 for h,rr in root.items():walk(rr,d['cases'][h])
 assert found=={2:2710,4:2828} and historical==[((11,12),(Q,4))] and C=={'c9':1,'forest':1131,'split':41} and {str(q) for q in labels if q>=2**64}==set(book)
 print('PASS independent',len(root),'firsts; tail',tail,'counts',dict(C),'separate ordinary floors',found,'large',len(book),'hashes',[(p.name,hashlib.sha256(p.read_bytes()).hexdigest()) for p in [H/'Verifier.py',H/'Forest.json.gz',H/'Primes.json.gz']])
if __name__=='__main__':assert __debug__;audit()
