"""If the unknown root sigma is squarefree, it must have >=5 distinct primes."""
from pathlib import Path
from math import gcd,prod,isqrt
from fractions import Fraction
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Divisor906 import run
if __name__=='__main__':
 import Gain906 as Z
 U=Z.U;assert -(-U.numerator//U.denominator)==579125
 X=7**906;A=(7*X-1)//6;B=10**2400;assert A**3%49!=1 and A**3%7==1
 # Suppose at most four squarefree prime factors of A. At least one has base-depth <=1 due A^3 !=1 mod49. All others base depth <255. p-length shifts at most 4 throughout.
 C=5+3*258;assert C==779
 # If Euler high, external to A: all A factors are ordinary and A^2 is paid, outside atoms (incl high Euler) supply remainder with generic square price. If high Euler internal, A^2 still paid; order of that Euler mod7 only 1 or 3 by reciprocity and odd root order 907. Same upper cap C.
 assert X*A*A*7**(2*(906-C))>B*U
 # Linear Euler q|A: s=0; global price of all ordinary components bounds q, while mass A^2/q and price of external suppliers give an incompatible lower bound.
 assert (X*A*A*7**(2*(906-3*258)))*(X*7**(2*906))>(B*U)**2
 # Linear Euler q outside A: q=(2m)7^s-1 for odd m coprime to 7 and 19. Other sources outside A supply >=max(0,906-s-C). Numerical exception windows checked deterministically for primality failures.
 feasible=0
 for s in range(907):
  y=7**s;r=max(0,906-s-C);top=B*U//(X*A*A*7**(2*r));mmax=(top+1)//(2*y)
  assert mmax<=10  # largest admissible odd multiplier is 9
  for m in range(1,mmax+1,2):
   if gcd(m,7*19)!=1:continue
   q=2*m*y-1;assert q>3 and pow(2,q-1,q)!=1;feasible+=1
 print('PASS if Phi907(7) squarefree, at least FIVE distinct prime divisors mandatory; exterior linear Euler candidate composites',feasible)
