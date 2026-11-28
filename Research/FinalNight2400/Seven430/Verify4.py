"""Exact Q^4 proof / checkpoint, no online or discovery inputs."""
from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Multi4 import *
from functools import cache

def run(path=None,bookpath=None,partial=False):
 assert __debug__;x=json.loads((path or H/'Pack4.json').read_bytes());book=json.loads((bookpath or H/'Cert4.json').read_bytes());
 @cache
 def prime(z):
  assert type(z)==int and z>2;q=z
  if z>=2**64:
   for r in book[str(z)]:assert r[0]==q;q=C.pc.level(*r)
  assert C.pc.prime64(q);return True
 assert prime(7) and prime(Q) and prime(W) and x['q']==W and all(prime(v) for v in (*qfactor,*wf)) and Q-1==2*prod(qfactor) and W-1==8*prod(wf) and gcd(W*prod(wf),7*3*Q*prod(qfactor))==1 and 3**8000>B
 # Joint Q order>3 admits no exceptions: at cap 3, the smallest o>3=131 suffices except possibly one low-order root interval, tested directly.
 orders=[1]
 for z in qfactor:orders+=[y*z for y in orders]
 for o in orders:
  if o<=3 or o>8000:continue
  r=3
  while r**(o-3)<Q**6:
   if pow(r,o,Q)==1:assert r**(o-3)>=gcd(pow(r,o,Q**3)-1,Q**3)**2
   r+=2
 stats={'split':0,'forest':0,'price':0,'square':0,'open':0};un=[]
 def domain(row,q):
  s=C.State(row);assert prime(q) and q not in s.rows and q not in s.bad and not s.conflict;v=val(s.D,q);assert v>=1;h=v;out={}
  while s.base//q**v*q**h<=B:
   if s.possible(q,h,v):
    r=row+[(q,h)];u=C.State(r)
    if not u.conflict and u.base<=B and prod(sig(x,e) for x,e in r)<=2*u.X:out[str(h)]=r
   h+=1
  return out
 def walk(row,t):
  s=C.State(row);kind=t['type'];stats[kind]+=1
  if kind=='split':
   cs=domain(row,t['q']);assert set(cs)==set(t['cases']),(row,t['q'],set(cs)^set(t['cases']))
   for k,r in cs.items():walk(r,t['cases'][k]);
  elif kind=='forest':
   k=t['roots'];o=t['owners'];h=t['head'];C.validate_forest(s,k,o,h,prime);assert C.Forest(s,k,o,h).lower()[0]>B
  elif kind=='square':
   from SquareLast import check as parity;assert parity(row)
  elif kind=='price':
   assert row==[(7,430),(Q,4),(W,9)] and s.fixed_euler;assert multi(row,[])==[]
  else:
   assert kind=='open' and partial;un.append(tuple(row))
 walk(root+[(Q,4)],dict(type='split',q=x['q'],cases=x['cases'])); print('Q4 partition',stats,'open',len(un),flush=True);return un
if __name__=='__main__':assert not run()
