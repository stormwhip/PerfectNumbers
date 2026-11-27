from pathlib import Path
import sys,json,math
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Win12 import *
from functools import cache

def check():
 assert __debug__;pack=json.loads((H/'Packet12.json').read_bytes());book=json.loads((H/'Cert12.json').read_bytes());
 @cache
 def prime(z):
  y=z
  if y>=2**64:
   for r in book[str(y)]:assert r[0]==y;y=C.pc.level(*r)
  return C.pc.prime64(y)
 assert prime(7) and prime(Q) and all(prime(z) for z in qfactor) and Q-1==2*prod(qfactor) and 3**8000>B and Q>8000
 w=pack['q'];assert prime(w);r=root+[(Q,12)];s=C.State(r);v=val(s.D,w);assert v>=1;h=v;domain=[]
 while s.base//w**v*w**h<=B:
  if s.possible(w,h,v):
   row=r+[(w,h)];st=C.State(row)
   if not st.conflict and st.base<=B and prod(sig(q,k) for q,k in row)<=2*st.X:domain.append(h)
  h+=1
 assert set(domain)==set(map(int,pack['cases']));
 # High orders and length budgets checked independently from the costly unfiltered joint CRT multiplier.
 assert 3**(6*3)>=7**2 and Q>8000
 orders=[1]
 for x in qfactor:orders+=[k*x for k in orders]
 gen=next(g for g in range(2,400) if all(pow(g,(Q-1)//s,Q)!=1 for s in (2,*qfactor)))
 for o in orders:
  if o<=3 or o>=8000 or 3**(o-3)>=Q**22:continue
  v=pow(gen,(Q-1)//o,Q);m=Q
  for j in range(1,12):
   x=1;bits=(m*m).bit_length()
   for i in range(1,o):
    x=x*v%m
    if gcd(i,o)==1 and x>=3 and x%2 and (x.bit_length()-1)*(o-3)<bits:assert x**(o-3)>=m*m
   m*=Q;v=pow(v,Q,m)
 for j in domain:
  row=r+[(w,j)];s=C.State(row);fs=pack['cases'][str(j)]['roots'];assert len(fs)==len(set(fs)) and all(prime(z) and z>2 and z not in s.rows and z not in s.bad and s.D%z==0 for z in fs);assert not win(row,fs),(j,'open')
 print('PASS (7,430) exact Q^12, weighted cubic joint price, all eight child exponents',domain,flush=True)
if __name__=='__main__':check()
