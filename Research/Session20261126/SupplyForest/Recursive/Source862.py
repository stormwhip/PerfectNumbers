"""Standalone all-Euler-position and q-source replay for the exact residual branch (7,862;683845718669,30).
Resources: Internal862Data.json.gz and Square862{A2,A4,S2,S4}.json.gz, beside this module.
"""
from math import gcd,isqrt,prod
from pathlib import Path
from fractions import Fraction as F
import gzip,json,sys
H=Path(__file__).resolve().parent

def verify(R):
 sys.path[:0]=[str(R/'TeichmullerValuation'),str(R/'NightMerge')];import VerifyTeichmullerValuation2400 as T, LatticeLeaf as L
 B=10**2400;p=7;e=862;t=683845718669;f=30;A=T.sigma(p,e);S=T.sigma(t,f);C=A//t;V=p**(3*e)*t**f;P=T.Profile(p,e);U,D=P.U(e),P.D(e);Y=p**160;Q=2*Y-1
 assert T.check_lemmas(p) and T.kappa(p)==2 and U==579125 and D==1 and A%t==0 and gcd(C,S)==gcd(t,C*S)==gcd(p,C*S)==1 and S%7 and t%7==1
 assert V>B*U*D # Euler >=5, using fixed nonsupplier t^30
 assert all(V*max(1,2*7**s-1)>B*U*7**(2*s) for s in range(160))
 # For q||N and s>=160: q cannot divide A by quadratic reciprocity since q=1 mod4, q=-1 mod7. It cannot equal t, which has even exponent.
 assert t%31!=0 and S%31!=0;M=4*Y;n=31;z=Q+M*((1-Q)*pow(M,-1,n)%n);M*=n;assert gcd(S,M)==1;lo=z;hi=S//(S*pow(z,-1,M)%M)
 packet=json.loads(gzip.decompress((H/'Internal862Data.json.gz').read_bytes()));assert [packet[k] for k in ['p','e','t','f','smin']]==[p,e,t,f,160]
 for l,h,w in packet['leaves']:
  assert l==lo and l<=h<=hi and L.verify(S,1,z,M,l,h,w);lo=h+1
 assert lo==hi+1
 # q outside the two seed sigma values; (odd) sigma(r^g) must contain q for some ordinary prime r different from p,t and q itself.
 assert 2*V*Q**2>3*U*B*Y**2*7**159
 assert 3**9999>B and 7**5>10000
 R0=7**154;roots=[pow(a,7**153,R0) for a in (2,4)];assert all(z%p==a and pow(z,3,R0)==1 for a,z in zip((2,4),roots));X=p**e*t**f*C*S;assert X*Q*min(roots)>B
 # Let c=v_r(C*S), b=v_p(sigma(r^g)). b>=160 and g even imply r==roots[i] mod R0; g>c gives X*q*r | N, too large. Hence g=c>=2, r^2 divides exactly one block.
 counts=[]
 for label,K,n in [('A',C,863),('S',S,31)]:
  assert n in (31,863) and all(n%d for d in range(2,isqrt(n)+1)) and K%n and gcd(K,2*n*R0)==1
  for a,u in zip((2,4),roots):
   T0=2*n*R0;z=1+2*n*((u-1)*pow(2*n,-1,R0)%R0);assert z%R0==u and 0<z<T0;lo=z;hi=isqrt(K);ss=getattr(sys,'get_int_max_str_digits',lambda:0)();
   if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(30000)
   try:rows=json.loads(gzip.decompress((H/f'Square862{label}{a}.json.gz').read_bytes()))
   finally:
    if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(ss)
   for l,h,w in rows:
    assert l==lo and l<=h<=hi and L.verify(K,2,z,T0,l,h,w);lo=h+1
   assert lo==hi+1;counts.append(len(rows))
 return {'internal':len(packet['leaves']),'square':counts}
if __name__=='__main__':
 if not __debug__:raise RuntimeError('assertions required')
 print(verify(Path(sys.argv[1]).resolve()))
