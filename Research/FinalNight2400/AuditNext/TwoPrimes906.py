"""New low-support Euler reduction: <=2 A primes forces q emitted only by an A-prime."""
from pathlib import Path
from math import prod
from fractions import Fraction
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Gain906 as Z;import Repeated906;Repeated906.run(160);X,A,B,U=Z.X,Z.A,Z.B,Z.U
mass_survive=[];exterior_survive=[]
for s in range(1,711):
 Y=7**s;q=2*Y-1
 ok=anyE=False
 for high in (False,True):
  # One of at most two A-prime bases has supply <=5. The other is fixed in each range; maximum payable supply at the cheapest feasible high premium.
  small,big=(164,258) if high else (0,163);u=max(small,min(big,906-s-5));K=(10**7*7**(u-4)) if high else 1
  v=max(0,906-s-5-u);cost=X*A*q*K
  # If an emitter is outside A it is also outside X and distinct from q. For emitter supply j, additional price is 7^(2 max(0,v-j)) and emitter > 2q*7^j/3, minimized at j=v. The main lower bounds are monotone through the endpoint used above (joint bound flat, not increasing, below v=0).
  if cost*7**(2*v)<=B*U:ok=True
  if cost*7**(2*v)<=B*U and 2*cost*q*7**v<=3*B*U:anyE=True
 if ok:mass_survive.append(s)
 if anyE:exterior_survive.append(s)
assert mass_survive==list(range(442,711)) and not exterior_survive
print('PASS <=2 A-primes forces linear exterior Euler, s>=442, every prime emitting q internal to A')
