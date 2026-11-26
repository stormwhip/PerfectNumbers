"""Independent exact checker for the exceptional 3^12:797161^112:6781^1:3391^102 leaf.
Rebuild root classes at a target without primitive roots: use complete polynomial roots at level 1 via direct residue enumeration for small relevant orders, and modular Frobenius powering for lifting. Pair CRT only for cases not paid by one residue minimum. Self-contained; no original verifier imports.
"""
from math import gcd,isqrt,prod
from functools import cache
T,U=797161,3391
P=((3,12),(T,112),(6781,1),(U,102));X=prod(r**k for r,k in P);LIMIT=10**2400//X

def val(n,q):
 k=0
 while n%q==0:n//=q;k+=1
 return k

def primes(n):return n>1 and all(n%u for u in range(2,isqrt(n)+1))

def ok(x):return x>1 and x not in {3,7,11,13,19,31,6781,T,U} and all(x==j or x%j for j in [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97])

def next_ok(x,m):
 while not ok(x):x+=m
 return x
@cache
def basic(q,d):
 # Ord dividing d (includes all proper nontrivial divisors!) No primitive element needed. Verify exact cardinality d-1.
 arr=[i for i in range(2,q) if pow(i,d,q)==1];assert len(arr)==d-1;return tuple(arr)
@cache
def lifts(q,d,n):
 if n==1:return basic(q,d)
 m=q**n;return tuple(pow(x,q,m) for x in lifts(q,d,n-1))

def tab(q,k,cap,top):
 n=k+1;d=gcd(n,q-1);j=val(n,q);rs=[(0,1,(0,),5)];
 if j:rs.append((j,q,(1,),next_ok(1,q)))
 if d>1:
  for t in range(1,cap-j+1):
   m=q**t;rr=lifts(q,d,t);low=min(next_ok(x,m) for x in rr);assert rr
   if low>top:break
   rs.append((j+t,m,rr,low))
 return rs

def run():
 assert __debug__ and all(primes(r) for r,k in P);sigma=prod((r**(k+1)-1)//(r-1) for r,k in P);a=112-val(sigma,T);b=102-val(sigma,U);assert (a,b)==(111,101);pw=[T**(19*i) for i in range(a+1)];pu=[U**(5*j) for j in range(b+1)];
 # for large h, raising both target valuations below a,b at r>=5 bounds all possible violations. Orders for q|h+1 are correctly included below.
 h=2;ncrt=0;high=pw[-1]*pu[-1]
 while 5**h<=LIMIT and 5**(10*h)<high:
  # Avoid enumerating enormous Fq root sets when no r size can yield higher t. Entire order d may be bounded by searching all r up to top directly if top small.
  top=1<<((LIMIT.bit_length()+h-1)//h)
  if top<10000:
   for r in range(5,top+1,2):
    if not ok(r) or r**h>LIMIT:continue
    g=(r**(h+1)-1)//(r-1);i=val(g,T);j=val(g,U)
    if i<=a and j<=b:assert r**(10*h)>=pw[i]*pu[j]
   h+=2;continue
  for i,m,rr,l in tab(T,h,a,top):
   for j,n,ss,v in tab(U,h,b,top):
    goal=pw[i]*pu[j];power=10*h
    if max(l,v)**power>=goal:continue
    ncrt+=1;M=m*n;am=pow(m,-1,n) if n>1 else 0
    for x in rr:
     for y in ss:
      z=x+m*((y-x)*am%n);assert next_ok(z,M)**power>=goal
  h+=2
 assert X**10*pw[a]*pu[b]>10**24535;print('SECOND CHECK PASS',a,b,'crt',ncrt,'exclusive h cap',h,'log10 N >2453.5',flush=True)
if __name__=='__main__':run()
