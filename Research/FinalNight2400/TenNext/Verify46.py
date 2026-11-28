"""Conditional reductions (19,46); not a full key."""
import sys,gzip,json,hashlib
from pathlib import Path
from math import gcd,prod
from itertools import product,count
from collections import Counter
assert __debug__
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(H),str(R/'RootFiveNext'),str(R/'Night2400/B'),str(R/'Night2400')]
from Price46 import sig,price,B
from InteriorPrice import Interior
from Balance import lower
import PrimeCheck as pc
q=70169234660105574400577005075855017842743056666917902427141
A6=2247860239402417332211;A10=4098026841288271
pkt=R/'Night2400/C11/DeepLeaves.json.gz';b=pkt.read_bytes();assert hashlib.sha256(b).hexdigest()=='ba8eefff35a63aa1dc0c45fb0cd29d565d4f017ed9a2caa200f5930599a5d72b';book=json.loads(gzip.decompress(b))['ecpp']
def prime(n):
 if n>=2**64:
  for row in book[str(n)]:assert n==row[0];n=pc.level(*row)
 assert pc.prime64(n)
for p in (19,q,A6,A10):prime(p)
assert sig(19,46)==q and sig(q,6)%A6==0 and sig(q,10)%A10==0

def dom(k,r):
 P=[(19,46),(q,k)];S=prod(sig(p,e) for p,e in P);X=19**46*q**k;C=S//gcd(S,X);assert gcd(C,X)==1;c=0;s=C
 while s%r==0:c+=1;s//=r
 live=[]
 for f in count(c):
  Y=X*r**f
  if Y*s>B:return live
  if f%2 and not (r%4==f%4==1):continue
  Z=S*sig(r,f);D=Z//gcd(Z,Y)
  if not gcd(D,Y)>1 and Z<=2*Y and Y*D<=B:live.append(f)

def run(P,weights,reduce=False):
 V,Q,exc,(X,C,blocks)=price(P,weights);assert V>B;I=Interior({});left={};ct=Counter()
 for vs in product(*(range(c+1) for p,c,w in Q)):
  m=prod(p**u for (p,c,w),u in zip(Q,vs));lo=2*m-1;k=prod(p**(w*u) for (p,c,w),u in zip(Q,vs));top=B*k//V
  if lo>top:ct['price']+=1;continue
  if X*C*lo>B and all(b<lo for b in blocks):ct['size']+=1;continue
  if not reduce and X*C*lo<=B:raise AssertionError(('undischarged external Euler',P,vs))
  for j,((p,e),b) in enumerate(zip(P,blocks)):
   if b>=lo:assert I(j,p,e,b,m,lo,top,vs)
  if X*C*lo>B:ct['external_size']+=1;continue
  assert reduce and P==[(19,46),(q,12)] and blocks==[1,sig(q,12)] and gcd(C,q-1)==1 and vs[1]>0
  # Every exterior Euler must be emitted by another component r^h. It is
  # ordinary (the Euler exponent is one and both exact prefix rows ruled out).
  minmass=(2*lo+2)//3;out=(X*C*lo*minmass<=B)
  inside=(X*C*lo*max(1,lower(q,13,vs[1],lo,12))<=B)
  if not out and not inside:ct['source']+=1;continue
  assert inside;left[vs]=(out,inside);ct['unresolved']+=1
 if reduce:
  assert len(left)==222 and sum(o for o,i in left.values())==81
  expected={j:list(range(7 if j==6 else 0,41 if j==10 else 47)) for j in range(6,11)}
  assert set(left)=={(a,j) for j,az in expected.items() for a in az}
 else:assert not left
 return ct
if __name__=='__main__':
 print('q^12',run([(19,46),(q,12)],[2,4],True),flush=True)
 for k,r,low,hi in [(10,A10,22,36),(6,A6,30,38)]:
  L=dom(k,r);assert L==list(range(2,hi+1,2))
  for f in L:
   if f>=low:print(k,f,run([(19,46),(q,k),(r,f)],[2,4,0 if k==10 and f>=28 else 2]),flush=True)
 print('PASS: 13 exact children; q^12 only external linear Euler (222 necessary level pairs, 141 require an emitter inside C). No full key.')
