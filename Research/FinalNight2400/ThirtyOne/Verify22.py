"""Offline independent-domain replay of the new conditional 47-valuation partition, exact remaining intervals reported."""
import sys,json
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path[:0]=[str(H),str(H.parents[1]/'Session20261126')];from EulerForest import *
from functools import cache
row=[(31,16),(T,22)];g=json.loads((H/'Cert22.json').read_bytes());P=json.loads((H/'Packet22.json').read_bytes());seen=set()
@cache
def prime(z):
 assert type(z)==int and z>2;q=z
 if q>=2**64:
  seen.add(str(q))
  for r in g[str(q)]:assert r[0]==q;q=level(*r)
 assert prime64(q);return True

def domain(row,p):
 s=C.State(row);a=val(s.D,p);assert a>=1 and prime(p);h=a;v=s.base;res=[]
 while v<=B:
  if s.possible(p,h,a):
   new=C.State(row+[(p,h)]);
   if not new.conflict and new.base<=B and prod(sig(z,f) for z,f in new.rows.items())<=2*new.X:res.append(h)
  h+=1;v*=p
 return res

def check():
 assert __debug__ and prime(31) and prime(T) and sig(31,16)==T and (sig(T,22)%47)==0 and sig(T,22)%T==1
 R0=C.State(row);U,k=bound(21,12);assert (U,k)==(1,0);assert all(R0.X*(2*T**j-1)*T**(12*(21-j))>B for j in range(16));assert P['q']==47 and set(map(int,P['cases']))==set(domain(row,47));miss={}
 for h,case in P['cases'].items():
  r=row+[(47,int(h))];s=C.State(r);t=case.get('forest',case);z=t['roots'];o=t['owners'];head=t['head'];C.validate_forest(s,z,o,head,prime);vertices=set(z)|{q for q,p in o};assert all(q%4!=1 or val(q+1,T)<16 for q in vertices)
  # Every vertex is ordinary since j>=16. Can rely solely on the conservative frozen ordinary forest.
  s.fixed_euler=True
  if case['kind']=='ordinary':assert C.Forest(s,z,o,head).lower()[0]>B;continue
  assert case['kind']=='window';cand=[j for j,*_ in status(r,z) if j>=16];unresolved=[j for j in cand if ef(r,t,j)<=B];assert unresolved==case['miss'];
  if unresolved:miss[int(h)]=unresolved
 return miss
if __name__=='__main__':
 m=check();assert m=={2:[16,17,18,19,20]};print('PASS (31,16), t^22 conditional: 139/140 next exponents excluded. Sole remaining h=2, Euler j=16..20.')
