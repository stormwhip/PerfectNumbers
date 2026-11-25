"""Independent certificate for 3*5*17*31*r; pure exact arithmetic, no search results imported."""
from fractions import Fraction
from math import isqrt,prod
from itertools import product

def prime(n):return n>=2 and all(n%i for i in range(2,isqrt(n)+1))
def sigma(p,f):return (p**(f+1)-1)//(p-1)
def ratio(p,f):return Fraction(sigma(p,f),p**f)
PR=[p for p in range(3,2000) if prime(p)]
# Partition exponent of each anchor into finite head values and a single lower-bound tail, with Euler parity fixed.
def check(P,cut=16):
 Bs=[p for p in (3,5,17) if p in P];possible=[0]+[p for p in P if p%4==1];total=0
 for z in possible:
  def slabs(p):
   fs=list(range(1 if p==z else 2,cut+(4 if p==z else 2),4 if p==z else 2));return [(f,f<cut) for f in fs]
  for opts in product(*(slabs(p) for p in Bs)):
   V={p:1 for p in P};known={p:f for p,(f,exact) in zip(Bs,opts) if exact};
   for p,(f,_) in zip(Bs,opts):V[p]=f
   S=prod(sigma(p,f) for p,f in known.items());total+=1
   if any(S%(p**(f+1))==0 for p,f in known.items()):continue
   for p in PR:
    n=S;c=0
    while not n%p:c+=1;n//=p
    if c:V[p]=max(c,V.get(p,0))
   # Euler=z if internal. For external case independently let each outside prime use min ordinary/special. This gives a still weaker lower bound.
   def floor(p,v):
    if p==z:return v+(1-v)%4
    f=v+v%2
    if z==0 and p not in P and p%4==1:f=min(f,v+(1-v)%4)
    return f
   if prod(ratio(p,floor(p,v)) for p,v in V.items())<=2:return False,(z,opts)
 return True,total
if __name__=='__main__':
 base=[3,5,17,31];n=0;rs=[]
 for q in PR:
  if q>83:break
  if q in base:continue
  ok,k=check([*base,q],cut=8)
  if not ok:raise ValueError((q,k))
  n+=k;rs.append(q)
 print('GLOBAL: under 3*5*17*31|N, absent additional primes',rs,'Cartesian cells',n)
 print('negative boundary r=89:',check([*base,89],cut=8))
