"""Deterministic two-target supply pricing at a fixed Euler prefix. Possible suppliers of exact trace-state t are bounded by enumerating LTE-level Teichmueller classes. All comparisons rational on log-free powers."""
from math import gcd,prod,isqrt
from functools import cache
from pathlib import Path
from bisect import bisect_left
import json,time,sys
L=Path(__file__).resolve().parent
@cache
def ds(n):return sorted({x for j in range(1,isqrt(n)+1) if n%j==0 for x in [j,n//j]})
@cache
def vp(n,p):
 j=0
 while n%p==0:n//=p;j+=1
 return j
@cache
def primitive(q):return next(g for g in range(2,q) if all(pow(g,(q-1)//u,q)!=1 for u in ds(q-1) if u>1))
# only odd-order roots; group of exact order d
@cache
def roots(q,d,t):
 if t==1:
  z=pow(primitive(q),(q-1)//d,q);return tuple(pow(z,j,q) for j in range(1,d+1) if gcd(j,d)==1)
 mod=q**(t-1);nx=mod*q;x0=roots(q,d,t-1);return tuple(x+(-((pow(x,d,nx)-1)//mod)*pow(d*pow(x,d-1,q),-1,q)%q)*mod for x in x0)

def prime64_or_bigger(x):
 if x<2:return False
 return all(x==p or x%p for p in (2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97))

def small(x,m,bad):
 while x<=1 or x in bad or not prime64_or_bigger(x):x+=m
 return x
@cache
def ranges(q,f,cap,bad,rmax):
 n=f+1;j=vp(n,q);ds0=ds(gcd(n,q-1));out=[(0,1,(0,),min(bad) if False else 5)]
 if j:
  zs=(1,);out.append((j,q,zs,small(1,q,bad)))
 for t in range(1,cap-j+1):
  zs=tuple(x for d in ds0 if d>1 for x in roots(q,d,t));
  if not zs:break
  m=q**t;low=min(small(x,m,bad) for x in zs);out.append((t+j,m,zs,low));
  if low>rmax:break
 return out

def run(P,weights):
 Q,U=797161,3391;A0,B0,den=weights;d=dict(P);assert d[Q]==112 and d[U]==102;g=prod((z**(h+1)-1)//(z-1)//(1+h%2) for z,h in P);a=d[Q]-vp(g,Q);b=d[U]-vp(g,U);B=10**2400;X=prod(z**h for z,h in P);budget=B//X;bad=tuple(sorted({3,7,11,13,19,31,*d}));assert sum(h%2 for z,h in P)==1
 def good(r,f):return all((f+1)%k if r%k==1 else pow(r,f+1,k)!=1 for k in [7,11,13,19,31]);
 # Bounding all independent losses by ratios is not enough: only finite offending actual r may cost. Enumerate every residual r where price is violated, retain worst denominator/numerator per r. Stop on intractable branches.
 exc={};ncrt=0;probes=0;st=time.monotonic();totalmax=Q**(A0*a)*U**(B0*b);powq=[Q**(A0*i) for i in range(a+1)];powu=[U**(B0*i) for i in range(b+1)];
 assert 5**10000>budget and all(z>2 for z in d) and a==111 and b==101 and list(weights)==[19,5,10];
 for h in range(2,10000,2):
  if 5**h>budget or 5**(den*h)>=totalmax:break
  rmax=1<<((budget.bit_length()+h-1)//h);l1=ranges(Q,h,a,bad,rmax);l2=ranges(U,h,b,bad,rmax);power=h*den
  if len(l1)==len(l2)==1:continue
  # For each h compute target's h-th-root integer log estimate safely by using str bit length prefilter, exact near boundary.
  for i,m,xs,lo in l1:
   for j,n,ys,low in l2:
    target=powq[i]*powu[j];z=max(lo,low);bits=target.bit_length();
    if (z.bit_length()-1)*power>=bits or z**power>=target:continue
    ncrt+=1;assert gcd(m,n)==1;inv=pow(m,-1,n) if n>1 else 0;mn=m*n
    for x in xs:
     for y in ys:
      r=x+((y-x)*inv%n)*m if n>1 else x;r=small(r,mn,bad)
      while (r.bit_length()-1)*power<bits and r**power<target:
       probes+=1
       if good(r,h):
        # A composite may occur as extra loss, still conservative. Exact valuations must fit target ledger.
        nr=(r**(h+1)-1)//(r-1);ai=vp(nr,Q);bj=vp(nr,U)
        if ai==i and bj==j:
         key=r;num=powq[i]*powu[j];dd=r**power;old=exc.get(key,(1,1,0,0,0));
         if num*old[1]>dd*old[0]:exc[key]=(num,dd,i,j,h)
       r=small(r+mn,mn,bad)
    if probes>100000:raise ValueError(('probe limit',h,i,j))
  if h in [2,4,6,10,100]:print('h',h,'secs',round(time.monotonic()-st,1),'crt',ncrt,'probes',probes,'losses',len(exc),flush=True)
 from math import log10
 numer=X**den*Q**(A0*a)*U**(B0*b)*prod(v[1] for v in exc.values());div=prod(v[0] for v in exc.values());ok=numer>B**den*div
 print('RESULT',P,weights,'ok',ok,'floorlog',round((log10(numer)-log10(div))/den,6),'losses',len(exc),'crt',ncrt,'probes',probes,flush=True)
 assert ok and not exc and probes==0;return ok
if __name__=='__main__':run([(3,12),(797161,112),(6781,1),(3391,102)],list(map(int,sys.argv[1:])) or [19,5,10])
