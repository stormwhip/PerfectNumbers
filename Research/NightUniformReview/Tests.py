"""Compare the released arithmetic with exhaustive small grids."""
import itertools
from math import gcd
import Replay as R
nfs=nrect=nplant=nroot=0
for n,m,a,b in itertools.product(range(9),range(1,11),range(-4,11),range(-12,12)):
 assert R.fs(n,m,a,b)==sum((a*i+b)//m for i in range(n));nfs+=1
for T in range(2,12):
 for z in range(1,T):
  if gcd(T,z)>1:continue
  for c,C,L,H in itertools.product(range(1,4),range(1,70),range(1,8),range(7,15)):
   w=C*pow(z,-c,T)%T;u0=(C+H**c-1)//H**c;u1=C//L**c;exact=any(not (r**c*u-C)%(T*T) for r in range(L,H+1) if r%T==z for u in range(u0,u1+1) if u%T==w)
   b=R.rect(C,c,z,T,L,H,0);assert b==exact,(C,c,z,T,L,H);nrect+=1
   if any(C%r**c==0 for r in range(L,H+1) if r%T==z):assert b;nplant+=1
for p,f,h,b in itertools.product((7,11,19,31),range(2,22,2),range(1,14,2),range(1,4)):
 roots=R.lifts(p,h,b,f)
 for r in range(3,501,2):
  if r%p==0 or (r-1)%(2*h) or R.val(R.sig(r,f),p)<b:continue
  assert roots is None or any(r%T==z for z,T in roots);nroot+=1
print('floor instances',nfs,'rectangles',nrect,'planted exact divisors',nplant,'admissible LTE residues',nroot)
