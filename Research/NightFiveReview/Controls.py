"""Negative controls for tempting (wrong) simplifications, not counterexamples to perfectness."""
from LocalModel import *
# z^1 prepaid, z^4 actual, single unit: full 4log z charge double-counts one log z.
z=41;assert good(z,4) and vp(sig(z,4))==1 and z**(4-1)<z**4
# Per-origin 'paid' deletion obtained by gcd would double-use the same 29 if allowed.
a=sig(23,6);b=sig(53,6);assert good(23,6) and good(53,6) and math.gcd(a,b)==29
assert math.gcd(29,a)*math.gcd(29,b)!=29
# Secondary forced simple Euler cannot be discarded solely because it is a pivot.
assert sig(17,18)%229==0 and good(17,18) and good(229,1) and 229%4==1 and vp(230)==1
# f=5 or 9 is legitimate independently of first exponent, and one higher exponent
# can escape a forbidden divisor at a lower exponent. This is not monotone in f.
assert not good(17,8) and good(17,10)
print('PASS: fractional rough gift, overlapping origins, secondary odd Euler 229^1, nonmonotone exponent legality')
