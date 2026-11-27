"""Independent F2/F4 domain, odd-parity reserve and Euler price/window check. No author modules imported."""
from pathlib import Path
from math import prod,gcd,isqrt
from fractions import Fraction
from functools import cache
from collections import Counter
import sys,json,gzip,hashlib
H=Path(__file__).resolve().parent.parent/'Seven882';B=10**2400;primes=(19,7,11,31,13,3,5,17)
@cache
def sig(p,e):return (p**(e+1)-1)//(p-1)
def vp(n,p):
 a=0
 while n%p==0:n//=p;a+=1
 return a
def strip(v,m):
 while(g:=gcd(v,m))>1:v//=g
 return v
@cache
def prefix(row):
 X=prod(p**h for p,h in row);odd=sum(h%2 for p,h in row);S=prod(sig(p,h) for p,h in row)//(1+odd);return X,S,strip(S,X),odd

def bad(row,no):
 X,S,D,odd=prefix(row)
 return odd>1 or any(h%2 and (p%4!=1 or h%4!=1) for p,h in row) or gcd(S*X,prod(no))>1 or any(vp(S,p)>h for p,h in row)
@cache
def children(row,q):
 X,S,D,odd=prefix(row);assert D%q==0 and q not in dict(row) and q!=19;a=vp(D,q);size=X*D;out=[];h=a
 while size<=B:
  rr=row+((q,h),)
  if (not h%2 or not odd and q%4==1 and h%4==1) and not bad(rr,(19,)):
   y,z,d,od=prefix(rr)
   if y*d<=B and z*(1+od)<=2*y:out.append(h)
  size*=q;h+=1
 return out
@cache
def loss():
 # Derivative Hensel update, not exponentiating y->y^7. Both primitive roots recomputed independently.
 rr=[2,4];m=7;E={}
 for i in range(1,883):
  for y in rr:
   if y<3 or y%2==0:continue
   def possible(x):return x>=3 and x not in (7,19,21193) and pow(2,x-1,x)==1
   z=isqrt(y)
   if possible(y) or z*z==y and possible(z):E[y]=max(E.get(y,1),Fraction(m*m,y*y))
  rr=[y+m*((-((y*y+y+1)//m)*pow(2*y+1,-1,7))%7) for y in rr];m*=7
 assert len(E)==8;return prod(E.values(),start=Fraction(1))

def check_win(row,K):
 X,S,D,odd=prefix(row);a=882-vp(S,7);U=loss();u=-(-U.numerator//U.denominator)
 if odd:assert X*7**(2*a)>B*U;return
 em=[sig(p,h) for p,h in row];F=prod(z**(vp(D,z)%2) for z in K);blocks=[strip(s,X*prod(K)) for s in em];G=[]
 for b in blocks:
  # G is pairwise coprime; multiplying all connected blocks cannot introduce a new prime.
  ids=[x for x in G if gcd(x,b)>1];G=[x for x in G if x not in ids]+[b*prod(ids)]
 rounded=[z**(vp(D,z)+vp(D,z)%2) for z in K];assert prod(G+rounded)==D*F
 H=max(G+rounded+[1]);cnt=[0,0,0]
 for i in range(a+1):
  m=7**i;Q=2*m-1;A=7**(2*(a-i))
  if X*Q*A>B*u:cnt[0]+=1;continue
  for j,n in enumerate(em):
   if n<Q or (j==0 and i):continue
   k=n*pow(Q,-1,4*m)%(4*m);assert n//Q<4*m and (k==0 or k>n//Q or n%k)
  if X*D*F*Q>B:cnt[1]+=1;continue
  assert (2*X*Q**2*A)*(2*X*D*F*Q**2)>9*B*B*u*H;cnt[2]+=1
 return cnt

def run(f):
 d=json.loads(gzip.decompress((H/f'Done{f}.json.gz').read_bytes()));assert d['first']==f;c=Counter();large=set();masks=set()
 def walk(row,m,t):
  typ=t['type'];c[typ]+=1;no=[19] if not m else [p for j,p in enumerate(primes) if not m>>j&1];yes=[] if not m else [p for j,p in enumerate(primes) if m>>j&1];X,S,D,odd=prefix(row);sat=[p for p,h in row if S%p**h==0];ban=set(no+sat)
  if typ=='conflict':assert bad(row,no);return
  if typ=='ban':assert bad(row,no) or gcd(D,prod(ban))>1 or bool(set(yes)&(ban-set(dict(row))));return
  assert not bad(row,no)
  if typ=='masks':assert not m and set(map(int,t['cases']))=={50,58,178};masks.update(map(int,t['cases']));[walk(row,int(i),v) for i,v in t['cases'].items()];return
  if typ=='split':z=t['q'];large.add(z);ls=children(row,z);assert set(ls)==set(map(int,t['cases']));[walk(row+((z,h),),m,t['cases'][str(h)]) for h in ls];return
  if typ=='forest':
   k=t['roots'];o=dict(t['owners']);large.update(k);large.update(o);assert not set(k)&set(o) and all((D%z==0 or z in yes) and z not in ban and z not in dict(row) for z in k);assert all(D%z and z not in yes and z not in ban for z in o);return # dual numeric replay is done in the independent full cold run.
  if typ=='win':K=t['roots'];assert len(K)==len(set(K)) and all(D%z==0 and z not in dict(row) and z not in ban for z in K);large.update(K);check_win(row,K);return
  if typ=='price':assert odd and X*7**(2*(882-vp(S,7)))>B*loss();return
  if typ=='square':
   z=[strip(sig(p,h)//(1+h%2),X) for p,h in row];bs=[]
   for i,b in enumerate(z):
    n=strip(b,prod(z[:i]+z[i+1:]));
    if n>1 and isqrt(n)**2!=n:bs.append(next((r for r in range(3,1001,2) if n%r==0),1001))
   bs.sort();assert X*D*prod(bs if odd else bs[:-1])>B;return
  assert typ=='abun';K=t['roots'];large.update(K);assert len(K)==len(set(K));a=Fraction(prod(sig(p,h) for p,h in row),X);saves=[Fraction(1)]
  for z in K:
   assert z not in dict(row) and z not in ban and (D%z==0 or z in yes);v=max(1,vp(D,z));h=v+(v%2)
   while gcd(sig(z,h),prod(ban))>1:h+=2
   ab=Fraction(sig(z,h),z**h);a*=ab
   if not odd and z%4==1 and gcd(z+1,prod(ban))==1:
    h=v+(1-v)%4
    while gcd(sig(z,h),prod(ban))>1:h+=4
    saves.append(Fraction(sig(z,h),z**h)/ab)
  assert a*min(saves)>2
 walk(((7,882),(21193,f)),0,d['tree']);assert set(d['ecpp'])=={str(q) for q in large if q>=2**64};print(f,dict(c),sorted(masks),'price losses',loss(),'ecpp',len(d['ecpp']),flush=True)
if __name__=='__main__':
 assert __debug__;run(2);run(4)
