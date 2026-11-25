"""Short integer/fraction certificate of mutually incompatible actual exponent divisibility predicates. For odd perfect N, p^e||N, q^f||N imply sigma(p^(h-1))*sigma(q^(k-1))|N when h,k odd divide e+1,f+1. (Both geometrical sums odd.) If p,q witnesses overlap the roots themselves, those factors already accounted by known root exponents; skip them. Each other certified odd prime power pays ordinary minimum rounded to even exponent, then subtract at most one legal Euler discount across all remaining primes. No size restriction required. Emits rules, not closed canonical shards. Independent verification by trial division only, no additional libraries."""
import json,sys,math,argparse
from fractions import Fraction
from functools import cache
@cache
def sg(p,f):return (p**(f+1)-1)//(p-1)
@cache
def gain(p,f):return Fraction(sg(p,f),p**f)
@cache
def prime(p):return 2<=p<10**8 and all(p%j for j in range(2,math.isqrt(p)+1))
def rule(p,h,q,k,R):
 if not(all(type(v)==int for v in [p,h,q,k]) and prime(p) and prime(q) and p>2 and q>2 and p!=q and 3<=h<=5000 and 3<=k<=5000 and h%2 and k%2 and len(R)==len(set(R))):raise ValueError('bad rule')
 z=sg(p,h-1)*sg(q,k-1);a=gain(p,h-1)*gain(q,k-1);d=Fraction(1)
 for r in R:
  if type(r)!=int or r in (p,q) or r<=2 or not prime(r) or z%r:raise ValueError('invalid divisor');
  m=0;n=z
  while n%r==0:m+=1;n//=r
  g=gain(r,m+m%2);a*=g
  if r%4==1:d=min(d,gain(r,m+(1-m)%4)/g)
 return a*d
if __name__=='__main__':
 if not __debug__:raise SystemExit('never -O')
 a=argparse.ArgumentParser();a.add_argument('packet');o=a.parse_args();D=json.load(open(o.packet));seen=set();g=[]
 for p,h,q,k,R in D:
  assert (p,h,q,k) not in seen;seen.add((p,h,q,k));z=rule(p,h,q,k,R);assert z>2;g.append(z)
 print('proved',len(g),'smallest excess, units 1e-9:',(min(g)-2)*10**9//1)
