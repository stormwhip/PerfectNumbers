"""Tiny independent models of the strengthened block cost, up to six distinct primes.
Not odd-perfect examples; test the precise mapping that any true N must satisfy.
"""
from itertools import product
from math import prod,gcd,isqrt
from fractions import Fraction
P=(13,17,19,23,29,31);cnt=zero=refund_needed=nr=0
for ex in product(range(3),repeat=6):
 n=prod(p**a for p,a in zip(P,ex));supp=[p for p,a in zip(P,ex) if a]
 if n==1:continue
 L=min(supp);normal=[e+(e%2) for e in ex]
 for ep in (None,*[p for p in supp if p%4==1]):
  ge=[f if p!=ep else a+(1-a)%4 for p,f,a in zip(P,normal,ex)];M=prod(p**f for p,f in zip(P,ge));nonsq=isqrt(n)**2!=n;requested=int(ep is not None and n%4==1 and nonsq);fee=n*(L if nonsq else 1)//(L if requested else 1);assert M>=fee and n!=0
  if n%4==3:assert M>=n*L;nr+=1
  if n%4==1 and nonsq and M<n*L:assert requested;refund_needed+=1
  cnt+=1
# Same source exact exponents 2,8 cannot co-occur although both emit 13.
sg=lambda p,e:(p**(e+1)-1)//(p-1)
assert sg(3,2)%13==sg(3,8)%13==0
# Different source symbols can co-occur. If an anonymous 13 is simultaneously
# attached to both, 13^2 need not divide N solely because both blocks divide N
# as set constraints; actual sigma multiplicities alter the N parity argument:
# even v13(N)=2 may already pay both receipts; charging each block 13^2 would assert 13^4.
assert sg(29,2)%13==0 and sg(3,2)%13==0
# Two alternatives same-base negative reduced costs: y in simplex need not be
# integral. Min corner bound holds for nontrivial fractional weights.
for a,b in product(range(6),repeat=2):
 if a+b<=5:assert Fraction(-9*a-6*b,5)>=min(0,-9,-6)
print(dict(integer_mappings=cnt,euler_refund_required_witnesses=refund_needed,mod3_always_extra=nr,same_base_shared_prime=13,cross_base_warning=13))
