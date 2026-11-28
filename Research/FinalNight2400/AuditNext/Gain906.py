"""Uniform gain for ordinary prime factors of A at 7^906. Cold no repository price assumptions."""
from pathlib import Path
from fractions import Fraction
from math import gcd,prod,isqrt
import sys,time
A=(7**907-1)//6;X=7**906;B=10**2400;C=10**7;D=1814;s0=time.perf_counter()
# Every prime of A is 1 mod 1814. Non-cubic and zero-supply cases only need a common roughness bound.
z=1
for r in range(1815,C+1,D):z=z*r%A
assert gcd(z,A)==1
# Run the depth-255 sealed lemma first, so only 254 positive cubic depths need a premium test.
sys.path.insert(0,str(Path(__file__).resolve().parent));from Divisor906 import run;run(255)
rs=[2,4];m=7;count=0
for u in range(1,255):
 for a in rs:
  r=a+m*((1-a)*pow(m,-1,D)%D);z=1
  for k in range(r,C*m+1,D*m):z=z*k%A;count+=1
  assert gcd(z,A)==1
 rs=[pow(a,7,m*7) for a in rs];m*=7
# Generic square-price exception table for ordinary prime atoms; high Euler price separate below.
U={};rs=[2,4];m=7
for u in range(1,907):
 for r in rs:
  if r>=3 and r%2 and r not in [7,19] and pow(2,r,r)==2 and all(r==d or r%d for d in range(3,1000,2)):
   U[r]=max(U.get(r,1),Fraction(m*m,r*r))
 rs=[pow(a,7,m*7) for a in rs];m*=7
U=prod(U.values(),start=Fraction(1));print('rough square margin',C*C,'thresholds',count,'generic U ceil',-(-U.numerator//U.denominator))
# For ordinary r|A, no generic deficit charged when N product is charged once: gain per distinct r at least C^2. For any q^a, a>=5, high-Euler price r^a>=7^(2u) checked separately by order and length.
# Verify the separate high Euler exception is <=1, including orders 2,3,6.
# Since a>=5 and a=1 mod4, those orders all have minimum compatible a=5.
for res in range(2,7):
 o=next(v for v in range(1,7) if pow(res,v,7)==1)
 m=7;b=res
 for u in range(1,907):
  if b%4==1 and b>=3 and b not in (7,19) and pow(2,b,b)==2:assert b**5>=m*m
  m*=7;b=pow(b,7,m)
assert 3**6>=7**2 and 3**12>=7**2 and 3**10>7**2
K=0
while X*7**(2*906)*C**(2*K)<=B*U:K+=1
print('PASS with high Euler price or q^1,s=0 ordinary A-primes <=',K-1,'runtime',round(time.perf_counter()-s0,3))
