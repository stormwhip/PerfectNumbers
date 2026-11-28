"""Root-twelve, quantitative partial cover with explicit null gaps. All leaves rechecked."""
from pathlib import Path
import sys,gzip,json
from collections import Counter
from functools import cache
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Full as W;import Hard66 as K;from PriceOther import score

def audit(name='Partial66.json.gz'):
 assert __debug__ and name in ('Partial66.json.gz','WholeR.json.gz');d=json.loads(gzip.decompress((H/name).read_bytes()));book=d['ecpp'];seen=set();stats=Counter();gaps=[];whole=[];floors=[]
 @cache
 def prime(z):
  assert type(z)is int and z>=3;t=z
  if z>=2**64:
   seen.add(str(z))
   for r in book[str(z)]:assert r[0]==t;t=W.C.pc.level(*r)
  assert W.C.pc.prime64(t);return True
 def visit(P,n):
  s=W.C.State(P);assert W.viable(s)
  if n is None:gaps.append(P);return False
  k=n['type'];stats[k]+=1
  if k=='hard':assert tuple(P)==K.F;K.run();return True
  if k=='four-parity':
   import Parity16
   assert tuple(P)==Parity16.F and Parity16.run();return True
  if k=='pair':assert P==[*K.F[:3],(K.R,8),(K.P,12)] and score(P)==('result',0,0,0,None);return True
  if k=='forest':
   r,o,h=n['roots'],n['owners'],n['head'];W.C.validate_forest(s,r,o,h,prime);z=min(W.C.Forest(s,r,o,h).lower()[0],W.PC.exact_leaf(P,r,o,h));assert z>W.B;floors.append(W.PC.floor10(z));return True
  assert k=='split';q=n['q'];assert prime(q) and q not in s.rows and q not in s.bad and s.D%q==0;c=W.C.valuation(s.D,q);j=c;live=set();done=True
  while s.base//q**c*q**j<=W.B:
   if s.possible(q,j,c):
    U=P+[(q,j)];u=W.C.State(U)
    if W.viable(u):
     live.add(str(j));ok=visit(U,n['cases'][str(j)]);done=done and ok
     if len(P)==3 and ok:whole.append(j)
   j+=1
  assert set(n['cases'])==live;return done
 F=list(K.F[:3]);assert all(prime(z) for z,h in F) and W.C.sigma(3,12)==K.Q and W.C.sigma(K.Q,66)%5897==0
 visit(F,d['tree']);assert seen==set(book)
 if name=='WholeR.json.gz':assert not gaps and whole==[2,4,8,10,12,16,22,24,26,28,30,32] and stats=={'split':294,'forest':7916,'hard':1,'pair':1,'four-parity':1}
 print('PASS partial 66/6',dict(stats),'whole R exponents',whole,'open terminals',len(gaps),'minfloor',min(floors),'ECPP',len(seen),flush=True)
if __name__=='__main__':audit(*sys.argv[1:])
