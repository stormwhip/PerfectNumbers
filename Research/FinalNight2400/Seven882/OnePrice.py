"""Sharp universal squared 7-supply price with fixed Euler. Uses single 7 order 3."""
from Domain import *
from fractions import Fraction
@cache
def loss():
 r=2;m=7;L={}
 for i in range(1,883):
  for x in (r,m-1-r):
   if x<3 or x%2==0:continue
   y=isqrt(x);ok=lambda z:z>=3 and z not in (7,19,21193) and pow(2,z-1,z)==1
   if not(ok(x) or y*y==x and ok(y)):continue
   L[x]=max(L.get(x,1),Fraction(m*m,x*x))
  m*=7;r=pow(r,7,m)
 return prod(L.values(),start=Fraction(1))
def priced(row):
 s=state(row);assert s.fixed_euler;a=882-C.valuation(s.S,7);L=loss();return s.X*7**(2*a)*L.denominator//L.numerator
if __name__=='__main__':
 from Holes import count
 for f in (1,8):
  for row,t in count(f):
   if state(row).fixed_euler:print(f,[(str(p)[:8],h)for p,h in row],floor10(priced(row)),flush=True)
