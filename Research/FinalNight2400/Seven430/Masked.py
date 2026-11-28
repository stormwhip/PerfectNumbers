from Score import *
from functools import cache

def states(f,j):
 a=json.loads((D/f'Even430F{f}.json').read_bytes());z=max(a['roots']);r=root+[(Q,f),(z,j)]
 for mask in range(2,256,4):
  present={a for i,a in enumerate(C.ORDER) if mask>>i&1};absent=set(C.ORDER)-present
  s=C.State(r,present,absent);
  if s.conflict:continue
  yield mask,s,r

def adapt(s,a):
 k=sorted(set(a['roots'])|s.present-set(s.rows));assert not set(k)&set(s.bad)
 vis=set(k);o=[]
 for z,p in a['owners']:
  if p in vis and z not in vis and z not in s.rows and z not in s.bad and s.D%z:vis.add(z);o.append((z,p))
 return k,o
if __name__=='__main__':
 for j in (2,6):
  a=json.loads((D/f'Even430F2J{j}.json').read_bytes());
  for m,s,r in states(2,j):
   if m not in (50,58,178):continue
   k,o=adapt(s,a);F=C.Forest(s,k,o,180,record=True);v,mark=F.lower();print(m,j,floor10(v),mark,'witness',[(str(z)[:12],h) for z,h,c in F.witness(mark)],flush=True)
