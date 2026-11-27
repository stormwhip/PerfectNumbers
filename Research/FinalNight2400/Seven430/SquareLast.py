"""Final leaf: independent nonsquare blocks require distinct extra parity repairs."""
from Score import *
def check(row):
 assert row==root+[(Q,4),(62619225867394162638521,6),(1112651,52),(14969459,16),(17155781,16)];s=C.State(row);S=[C.nonsupport(sig(z,h),s.X)for z,h in row];assert math.prod(S)==s.D and all(math.gcd(a,b)==1 for i,a in enumerate(S) for b in S[:i]);lower=1000
 assert all(math.isqrt(a)**2!=a and all(a%k for k in range(2,lower+1)) for a in S);assert s.base*lower**(len(S)-1)>B;return True
if __name__=='__main__':print(check(root+[(Q,4),(62619225867394162638521,6),(1112651,52),(14969459,16),(17155781,16)]))
