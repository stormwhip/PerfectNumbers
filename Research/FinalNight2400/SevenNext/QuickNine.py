"""Elementary abundance proof for the exact R=173^9 case at Q^42."""
from fractions import Fraction
from math import prod,isqrt
Q=16148168401;R=173
sig=lambda p,e:(p**(e+1)-1)//(p-1)
ab=lambda p,e:Fraction(sig(p,e),p**e)
if __name__=='__main__':
 assert __debug__ and sig(7,12)==Q and all(all(z%d for d in range(2,isqrt(z)+1)) for z in (3,7,11,13,29,43,131,R,Q))
 S=sig(Q,42)*(sig(R,9)//2);ps=(3,11,29,43,131);assert all(S%p==0 for p in ps)
 base=ab(7,12)*ab(R,9)*prod(ab(p,2) for p in ps)
 assert base*ab(3,4)/ab(3,2)>2 and sig(3,2)==13 and base*ab(13,2)>2
 print('PASS exact R^9: 3^4 impossible; 3^2 forces 13 ordinary and exceeds abundance 2.')
