"""Check every sibling at every split and both independent forest costs. No discovery code."""
import sys,json,gzip
from pathlib import Path
from functools import cache
from math import prod
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Session20261126'));import PivotCheck as PC
C=PC.C;B=PC.B

def viable(s):return not s.conflict and s.base<=B and prod(C.sigma(z,h) for z,h in s.rows.items())<=2*s.X

def verify(f):
 assert __debug__ and f in (1,2,5,8,16,18,22,96,102,106,126,130,148,156,166,180,190,192,196,226,240,250,256)
 d=json.loads(gzip.decompress((H/f'Full{f}.json.gz').read_bytes()));book=d['ecpp'];seen=set();hist=[];floors=[]
 @cache
 def prime(z):
  assert type(z) is int and z>=3;t=z
  if t>=2**64:
   seen.add(str(z))
   for row in book[str(z)]:assert row[0]==t;t=C.pc.level(*row)
  assert C.pc.prime64(t);return True
 def visit(P,n):
  s=C.State(P);assert viable(s)
  if n['type']=='weighted':
   sys.path.insert(0,str(H));from FastEvenPrice import prove as EP
   q,r,a,b,w,v=n['args'];assert q!=r and q in s.rows and r in s.rows and s.fixed_euler and 2<=w<=8 and 2<=v<=8 and EP(P,q,r,a,b,w,v);return
  if n['type']=='fastpair':
   sys.path.insert(0,str(H));from FastPair import prove
   q,r,a,b=n['args'];assert q!=r and q in s.rows and r in s.rows and prove(P,q,r,a,b);return
  if n['type']=='pair126':
   sys.path.insert(0,str(H));import GeneralPair as G
   assert f==126 and P[2][0]==30228287 and P[2][1] in (42,58,60) and P[-2:]==[(11939,66),(485816396265547,6)] and G.score(P,1093,30228287)==('result',0,0,0,None);return
  if n['type']=='forest':
   k,o,h=n['roots'],n['owners'],n['head'];C.validate_forest(s,k,o,h,prime);a=C.Forest(s,k,o,h).lower()[0];b=PC.exact_leaf(P,k,o,h);assert min(a,b)>B;floors.append(PC.floor10(min(a,b)));return
  assert n['type']=='split';q=n['q'];assert prime(q) and q not in s.rows and q not in s.bad and s.D%q==0;c=C.valuation(s.D,q);h=c;live=[];size=s.base//q**c
  while size*q**h<=B:
   if s.possible(q,h,c):
    U=P+[(q,h)];u=C.State(U)
    if viable(u):live.append(h);visit(U,n['cases'][str(h)])
   h+=1
  assert set(n['cases'])==set(map(str,live));hist.append((q,h,len(live)))
 assert C.sigma(3,6)==1093 and prime(1093) and set(C.ORDER[:C.ORDER.index(3)])=={19,7,11,31,13}
 visit([(3,6),(1093,f)],d['tree']);assert set(book)==seen
 print('FULL',f,'splits',len(hist),'forests',len(floors),'minfloor',min(floors),'ECPP',len(seen),'root',hist[-1],'child samples',hist[:3],flush=True)
if __name__=='__main__':
 for f in map(int,sys.argv[1:] or [18]):verify(f)
