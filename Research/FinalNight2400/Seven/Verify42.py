"""Exact secondary valuations remaining at (7,12; Q,42; 173,h)."""
from math import gcd,prod,isqrt
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'Session20261126')];from PivotCheck import C,B
from Verify438 import v,outside,sigma
from Prices import loss
Q=16148168401;R=173

def ds(n):return sorted({j for i in range(1,isqrt(n)+1) if n%i==0 for j in (i,n//i)})
def phi_blocks(b,n):
 phi={}
 for j in ds(n):phi[j]=(b**j-1)//prod(phi[i] for i in phi if j%i==0)
 return list(phi.values())[1:]
def run():
 assert __debug__ and C.pc.prime64(Q) and C.pc.prime64(R) and sigma(7,12)==Q
 base=[(7,12),(Q,42)];s0=C.State(base);assert s0.D%R==0 and v(s0.D,R)==1
 highs=[];lives=[];raw=[];cost=loss(R,342,20,1);a,b=cost.as_integer_ratio()
 h=1;scale=s0.base//R
 while scale*R**h<=B:
  if s0.possible(R,h,1):
   s=C.State(base+[(R,h)])
   if not s.conflict and s.base<=B and prod(C.sigma(q,k) for q,k in s.rows.items())<=2*s.X:raw.append(h)
  h+=1
 assert len(raw)==247 and h==686 and max(raw)==342
 for h in raw:
  s=C.State(base+[(R,h)]);c=h-v(s.S,R); assert c==h-1
  if h%2:
   alive=(s.X*R**(20*c)*b<=B*a)
  else:
   blocks=[s0.D//R]+phi_blocks(R,h+1)
   for i,Z in enumerate(blocks):
    for p in s.rows:Z//=p**v(Z,p)
    blocks[i]=Z
   assert prod(blocks)==s.D
   active=[x for x in blocks if x>1]
   while any(gcd(x,y)>1 for i,x in enumerate(active) for y in active[i+1:]):
    i,j=next((i,j) for i,x in enumerate(active) for j,y in enumerate(active) if j>i and gcd(x,y)>1);active[i]*=active.pop(j)
   M=max(active+[1]);alive=False
   for u in range(c+1):
    m=R**u;L=2*m-1
    if s.X*L*R**(20*(c-u))*b>B*a:continue
    if all(outside(Z,m) for Z in blocks):
     if s.base*L>B:continue
     # ordinary supplier of q; the Euler square residual need not supply q since q cannot divide its own sigma.
     lo,hi=0,c-u+1
     while lo<hi:
      mid=(lo+hi)//2
      if 2*s.base*L**2*R**mid>3*B*M:hi=mid
      else:lo=mid+1
     k=lo-1
     if k<0 or 2*s.X*L**2*R**k*R**(20*(c-u-k))*b>3*B*a:continue
    alive=True;break
  (lives if alive else highs).append(h)
 print('42:173 direct',len(raw),'excluded',len(highs),'residual',len(lives),'even', [k for k in lives if not k%2],'odd',[k for k in lives if k%2],flush=True)
 assert len(highs)==122 and lives==sorted(list(range(2,230,2))+[232,1,5,9,13,21,25,29,33,37,41]);return lives,highs
if __name__=='__main__':run()
