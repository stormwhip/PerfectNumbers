"""Independent no-author-import audit: exact geometry, Hensel-based scalar and joint losses and sufficient window inequalities."""
from pathlib import Path
from functools import cache
from collections import Counter
from fractions import Fraction
from math import gcd,prod,isqrt
import gzip,json,hashlib
H=Path(__file__).resolve().parents[1]/'Eleven456';B=10**2400;p,t,Z=11,82261,309862619201513446309679813467;sf={11:[2,5],t:[2,3,5,457],Z:[2,3,7,13,37,661,82261,41131,787477,8709079]};ban=7*19
@cache
def sig(p,e):return (p**(e+1)-1)//(p-1)
def val(n,p):
 k=0
 while n%p==0:n//=p;k+=1
 return k
def strip(n,m):
 while (g:=gcd(n,m))>1:n//=g
 return n
@cache
def state(rr):
 odd=sum(h%2 for q,h in rr);X=prod(q**h for q,h in rr);S=prod(sig(q,h)//(1+h%2) for q,h in rr);D=strip(S,X)
 if odd>1 or any(h%2 and (h%4!=1 or q%4!=1) for q,h in rr) or gcd(S*X,ban)>1 or any(val(S,q)>h for q,h in rr) or (1+odd)*S>2*X or X*D>B:return None
 return X,S,D,odd
@cache
def domain(rr,s):
 X,S,D,odd=state(rr);a=val(D,s);assert a and s not in dict(rr) and ban%s!=0;size=X*D;h=a;ok={}
 while size<=B:
  r2=rr+((s,h),)
  if state(r2):ok[str(h)]=r2
  h+=1;size*=s
 return ok,h
@cache
def gen(s):
 for r in range(2,200):
  if pow(r,s-1,s)==1 and all(gcd(pow(r,(s-1)//j,s)-1,s)==1 for j in sf[s]):return r
 raise AssertionError
@cache
def lifts(s,o,a):
 g=pow(gen(s),(s-1)//o,s);rs=[pow(g,j,s) for j in range(1,o) if gcd(o,j)==1];out=[(1,(0,))];m=s
 for level in range(1,a+1):
  out.append((m,tuple(rs)));rs=[v+m*((-((pow(v,o,m*s)-1)//m)*pow(o*pow(v,o-1,s),-1,s))%s) for v in rs];m*=s
 return out

def good(r,excluded):
 def may(z):return z>=3 and z%2 and z not in excluded and pow(2,z-1,z)==1
 y=isqrt(r);return may(r) or y*y==r and may(y)
@cache
def scalar(s,w,cap):
 fac=sf[s];orders=[1]
 if s==11:orders=[1,5]
 else:
  for z in fac[1:]:orders += [z*k for k in orders]
 E={}
 for o in orders:
  if o==1 or o>8000 or 3**(o-1)>=s**(w*cap):continue
  for m,rs in lifts(s,o,cap)[1:]:
   for r in rs:
    if r>=3 and r%2 and (r.bit_length()-1)*(o-1)<(m**w).bit_length() and r**(o-1)<m**w and good(r,{7,19,11,t} | ({Z} if s==Z else set())):E[r]=max(E.get(r,1),Fraction(m**w,r**(o-1)))
 return prod(E.values(),start=Fraction(1))
def joint(row,a,b):
 X,S,D,odd=state(row);E={};E2={};excluded=set(dict(row))|{7,19}
 def add(table,r,h,goal):
  if r<3 or not r%2 or (r.bit_length()-1)*h>=goal.bit_length():return
  n=r**h
  if n<goal and n//gcd(n,D)<=B//(X*D) and good(r,excluded):table[r]=max(table.get(r,1),Fraction(goal,n))
 for m,rs in lifts(p,5,a):
  for n,ts in lifts(t,5,b):
   inv=pow(n,-1,m)
   for y in ts:
    for x in rs:add(E,y+n*((x-y)*inv%m),4,m**4*n*n)
 for o in (3,9,15,45,457,1371,2285,4113,6855):
  h=o-5 if o%5==0 else o-1
  if 3**h>=t**(2*b):continue
  for m,rs in lifts(t,o,b)[1:]:
   for r in rs:add(E2,r,h,m*m)
 return prod(E.values(),start=Fraction(1))*prod(E2.values(),start=Fraction(1))
def price(row,fs,typ):
 X,S,D,odd=state(row);a=456-val(S,11);s=Z if typ=='rprice' else t;b=dict(row)[s]-val(S,s) if typ!='price' else 0
 U=joint(row,a,b) if typ=='joint' else scalar(11,4,456)*(scalar(Z,2,b) if typ=='rprice' else 1);u=-(-U.numerator//U.denominator)
 if odd:assert X*p**(4*a)*s**(2*b)>B*u;return
 em=[sig(q,h) for q,h in row];fs=set(fs);F=prod(q**(val(D,q)%2) for q in fs);blocks=[];sc=X*prod(fs)
 for e0 in em:
  n=strip(e0,sc);over=[z for z in blocks if gcd(z,n)>1];blocks=[z for z in blocks if z not in over]+[n*prod(over)]
 G=blocks+[q**(val(D,q)+val(D,q)%2) for q in fs];assert prod(G)==D*F;HH=max(G)
 for j in range(b+1):
  for i in range(a+1):
   m=p**i*s**j;q=2*m-1;V=p**(4*(a-i))*s**(2*(b-j))
   if X*q*V>B*u:continue
   for ix,e0 in enumerate(em):
    if e0<q or (ix==0 and i):continue
    k=e0*pow(q,-1,4*m)%(4*m);assert e0//q<4*m and (k==0 or k>e0//q or e0%k)
   if X*D*F*q>B:continue
   # independent discrete bound on p-prime units for each actual remaining secondary supply.
   for v in range(b-j+1):
    y=s**v;lim=min(p**(a-i),3*B*HH//(2*X*D*F*q*q*y),isqrt(isqrt(B*u*HH//(X*D*F*q*y*y))))
    if not lim:continue
    c=0
    while p**(c+1)<=lim:c+=1
    assert 2*X*q*q*V>3*B*u*(p**c)**3*y,(typ,i,j,v)

def run():
 d=json.loads(gzip.decompress((H/'Forest.json.gz').read_bytes()));book=json.loads(gzip.decompress((H/'Primes.json.gz').read_bytes()));labels={p,t,Z,457,*sf[Z]};c=Counter();dom,tail=domain(((11,456),),t);assert len(dom)==74 and tail==297 and set(dom)==set(d['cases']);assert prod(sf[Z])==Z-1 and t-1==4*9*5*457 and p-1==10
 def walk(row,n):
  X,S,D,odd=state(row);k=n['type'];c[k]+=1
  if k=='split':q=n['q'];ds,_=domain(row,q);assert set(ds)==set(n['cases']);labels.add(q);[walk(rr,n['cases'][h]) for h,rr in ds.items()];return
  if k=='square':
   em=[strip(sig(q,h)//(1+h%2),X) for q,h in row];ls=[]
   for j,z in enumerate(em):
    w=strip(z,prod(em[:j]+em[j+1:]));
    if isqrt(w)**2!=w:ls.append(next((r for r in range(3,1000,2) if w%r==0),1001))
   ls.sort();assert X*D*prod(ls if odd else ls[:-1])>B;return
  fs=n['roots'];assert len(set(fs))==len(fs) and all(D%r==0 and r not in dict(row) and ban%r for r in fs);labels.update(fs)
  if k=='forest':labels.update(q for q,r in n['owners']);return
  assert k in ('price','joint','rprice');price(row,fs,k)
 for h,rr in dom.items():walk(rr,d['cases'][h])
 assert set(book)=={str(x) for x in labels if x>=2**64};print('PASS independent 74/tail297',dict(c),'large labels',len(book),flush=True)
if __name__=='__main__':assert __debug__;run()
