"""Strong joint-source obstruction: if an ordinary prime provides 173, its Q supply is bounded."""
from pathlib import Path
import sys,math
from functools import cache
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Odd42 import Q,R,C,B
@cache
def lift(o,k):
 ds=[p for p in range(2,o+1) if o%p==0 and C.pc.prime64(p)];g=2
 while True:
  a=pow(g,(Q-1)//o,Q)
  if a and all(pow(a,o//p,Q)!=1 for p in ds):break
  g+=1
 # Newton generator lifted once per level; primitive powers generated at target modulus only.
 m=Q;inv=pow(o*pow(a,o-1,Q),-1,Q)
 for i in range(1,k):a+=m*(-((pow(a,o,m*Q)-1)//m)*inv%Q);m*=Q
 return [pow(a,j,m) for j in range(1,o+1) if math.gcd(o,j)==1]
def check(k):
 # X can be even smaller than any tested scope. Only terms sharing both targets tested.
 X=7**12*Q**42*R**2; survivors=[];M=Q**k
 for o in range(3,5101,2):
  if (Q-1)%o:continue
  for rlen in [43,173]:
   g=math.lcm(o,rlen)-1
   if g>=5100 or X*3**g>B:continue
   assert M**g*X>B,(k,o,rlen)
   if X*5000**g>B:
    ys=[v for v in range(3,5000,2) if pow(v,o,M)==1 and v%Q!=1]
   else:ys=lift(o,k)
   for y in ys:
    if y%2==0 or y<3 or y in (7,Q,R,19) or (y.bit_length()-1)*g>(B//X).bit_length() or X*y**g>B:continue
    if (rlen==173 and y%R!=1) or (rlen==43 and (y%R==1 or pow(y,43,R)!=1)):continue
    if pow(2,y-1,y)!=1:continue
    survivors.append((y,o,rlen,g))
 return survivors
if __name__=='__main__':
 for k in (6,5,4):
  try:print('threshold',k,check(k),flush=True)
  except AssertionError as err:print(err,flush=True)
