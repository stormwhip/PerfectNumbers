"""Bounds on total actual incoming 7-valuation emitted from prime factors of A, not estimates of probable factor sizes."""
from math import gcd
X=7**906;A=(7*X-1)//6;B=10**2400;U=579125
# Existing exact certificates: generic subset ordinary/high-Euler price U, s<=710, per-A-base bound 258 including Euler q|A by quadratic reciprocity, and if <=2 A factors one base has v7(r^3-1)<=1.
def least(lower,s):
 return next(i for i in range(907) if lower*7**(2*max(0,906-s-i))<=B*U)
assert A**3%49!=1 and A**3%7==1;hi=least(X*A,0);assert hi==389
small=[least(X*A*(2*7**s-1),s) for s in range(711)];assert min(small)==34 and small[453]==163
assert [s for s in range(711) if small[s]<=263]==list(range(252,711));assert hi>5+258
print('PASS genuine A-support supply ≥389 for high Euler or s=0; ≥34 for all Euler and ≥163 at s453; ≤2 A-primes implies 252<=s<=710 and exterior linear Euler')
