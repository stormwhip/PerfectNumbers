"""Cold exact coverage of all first secondary Q-powers except 46 under 3^6 1093^156."""
from pathlib import Path
from functools import cache
from collections import Counter
import json,gzip,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Full as W;C=W.C

def make():
 d=json.loads(gzip.decompress((H/'CutDeeper156.json.gz').read_bytes()));pr=json.loads((H/'PCutDeeper156.json').read_bytes());M={tuple(map(tuple,p)):[q,r,a,b] for p,q,r,a,b,ok in pr if ok};Z=set()
 def trim(n,P):
  if P in M:return {'type':'fastpair','args':M[P]}
  if n is None:
   assert len(P)==3 and P[-1][0]==2035349
   if P[-1][1]==46:return None
   assert P[-1][1]==66;return {'type':'inverse'}
  if n['type']=='split':
   q=n['q'];Z.add(q);n['cases']={k:trim(v,P+((q,int(k)),)) for k,v in n['cases'].items()}
  elif n['type']=='forest':Z.update(n['roots']);Z.update(z for z,parent in n['owners'])
  return n
 t=trim(d['tree'],((3,6),(1093,156)));B={str(z):d['ecpp'][str(z)] for z in sorted(Z) if z>=2**64};(H/'Almost156.json.gz').write_bytes(gzip.compress(json.dumps(dict(tree=t,ecpp=B),separators=(',',':')).encode(),mtime=0))

def verify():
 assert __debug__;d=json.loads(gzip.decompress((H/'Almost156.json.gz').read_bytes()));book=d['ecpp'];seen=set();stats=Counter();gaps=[];floors=[];P0=[(3,6),(1093,156)]
 @cache
 def prime(z):
  assert type(z)is int and z>=3;t=z
  if t>=2**64:
   seen.add(str(z))
   for a in book[str(z)]:assert a[0]==t;t=C.pc.level(*a)
  assert C.pc.prime64(t);return True
 assert C.sigma(3,6)==1093 and prime(1093) and set(C.ORDER[:C.ORDER.index(3)])=={19,7,11,31,13}
 def walk(P,n):
  s=C.State(P);assert W.viable(s)
  if n is None:gaps.append(P);return
  t=n['type'];stats[t]+=1
  if t=='inverse':
   import Inverse156 as I
   assert P==P0+[(2035349,66)] and I.test(66);return
  if t=='fastpair':
   from FastPair import prove
   q,r,a,b=n['args'];assert q!=r and q in s.rows and r in s.rows and prove(P,q,r,a,b);return
  if t=='forest':
   r,o,h=n['roots'],n['owners'],n['head'];C.validate_forest(s,r,o,h,prime);v=min(W.PC.exact_leaf(P,r,o,h),C.Forest(s,r,o,h).lower()[0]);assert v>W.B;floors.append(W.PC.floor10(v));return
  assert t=='split';q=n['q'];assert prime(q) and q not in s.rows and q not in s.bad and s.D%q==0;c=C.valuation(s.D,q);h=c;live=set()
  while s.base//q**c*q**h<=W.B:
   if s.possible(q,h,c):
    T=P+[(q,h)]
    if W.viable(C.State(T)):live.add(str(h));walk(T,n['cases'][str(h)])
   h+=1
  assert live==set(n['cases'])
 walk(P0,d['tree']);assert gaps==[P0+[(2035349,46)]] and seen==set(book);print('PASS 156 exact remaining only 2035349^46',dict(stats),'ECPP',len(seen),'min floor',min(floors),flush=True)
if __name__=='__main__':
 if sys.argv[1:]==['--make']:make()
 else:verify()
