"""Cross-check packed digit slopes, floor sums, and true-divisor preservation."""
from pathlib import Path
import sys,random
D=Path(__file__).resolve().parent;sys.path.insert(0,str(D));import Digits as A,DigitReplay as B
rng=random.Random(1139);cells=0
for i in range(4000):
 m=rng.randrange(1,60);a=rng.randrange(-200,200);b=rng.randrange(-300,300);n=rng.randrange(50)
 assert A.floors(n,m,a,b)==sum((a*j+b)//m for j in range(n));cells+=1
cases=0
for p in (7,11,13,19,31):
 for h in (3,5,7,11):
  for r in range(1+2*h,1900,2*h):
   if r%p in (0,1):continue
   for f in (2,4,6):
    n=(r**(f+1)-1)//(r-1);b=A.U.val(n,p)
    if not b:continue
    for s in (1,2):
     y=p**s
     for q in range(2*y-1,min(n//p**b,20000)+1,4*y):
      if n%(q*p**b):continue
      for lo,hi in ((r,r),(max(3,r-500),r+500)):
       C=r*r*211
       assert A.digit(C,2,p,f,b,s,h,lo,hi,q,128) and B.verifier(C,2,p,f,b,s,h,lo,hi,q);cases+=1
print('floor sums',cells,'actual source boxes',cases)
