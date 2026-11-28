"""Two unconditional progression contradictions, canonical (7,12), Q^12, T^2 or T^6."""
from fractions import Fraction as F
from pathlib import Path
import gzip,json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Session20261126'));from PivotCheck import C
Q=16148168401;T=C.sigma(Q,12)//13;L=3453283;S=62936242392988051361
cert=json.load(gzip.open(H/'Tertiary.json.gz'))['ecpp']
def prime(n):
 y=n
 if y>=2**64:
  for row in cert[str(n)]:assert y==row[0];y=C.pc.level(*row)
 assert C.pc.prime64(y)
def ab(r,h):return F(C.sigma(r,h),r**h)
if __name__=='__main__':
 assert __debug__
 for r in [3,7,11,13,151,Q,T,L,S]:prime(r)
 assert C.sigma(7,12)==Q and C.sigma(Q,12)==13*T
 assert C.sigma(T,2)%(3*L)==0 and C.sigma(L,4)%(11*151)==0
 assert ab(7,12)*ab(3,2)*ab(11,2)*ab(13,1)*ab(151,2)>2
 assert C.sigma(T,6)%S==0 and (S+1)%(3*11)==0
 assert ab(7,12)*ab(3,2)*ab(11,2)*ab(13,2)>2
 print('PASS T^2: 5 divides v_L+1 impossible. T^6: odd v_S impossible.')
