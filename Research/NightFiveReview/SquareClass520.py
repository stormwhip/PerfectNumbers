"""Nonfactorization calculation: congruence lower bound on the squarefree kernel K
of A=Phi_521(5). No factor search/divisibility of A by a candidate K/ECM.
A=K t^2 => when A nonzero mod ell, K has the same Legendre symbol as A.
"""
import math
E=520;P=5**521;A=(P-1)//4;H=1042
# Every prime divisor r of A is 1 mod 2*521: r=521 excluded since A=1 mod 521.
assert A%521==1 and A%5==1 and all(521%d for d in range(2,23))
# 5 is a square mod r by odd order, whence r=+/-1 mod 5 by reciprocity.
# Thus t=+/-1 mod 5 and K=1 mod 5; combine to 1 mod 5210.
mod=5*H;bound=10**11;n=(bound-1)//mod+1;jvals=bytearray(b'\1')*n
for ell in range(3,402,2):
 if any(ell%d==0 for d in range(2,math.isqrt(ell)+1)) or mod%ell==0:continue
 target=pow(A%ell,(ell-1)//2,ell)
 if not target:continue  # deliberately no division/identification of any prime of A
 for j in range(ell):
  if pow((1+mod*j)%ell,(ell-1)//2,ell)!=target:jvals[j::ell]=bytes(len(jvals[j::ell]))
 if not any(jvals):break
ix=jvals.find(b'\1');assert ix<0
print('e=520; order=521; K == 1 mod',mod,'; candidates',n,'; auxiliary primes up to',ell,'; all rejected; K >',bound)
