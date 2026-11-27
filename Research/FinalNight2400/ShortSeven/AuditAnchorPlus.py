"""Independent re-enumeration of the new six complete 173-anchor domains. No author imports."""
from pathlib import Path
from math import prod,gcd
import gzip,json,hashlib
H=Path(__file__).resolve().parents[1]/'SevenNext';fp=H/'AnchorPlusQ42.json.gz';Q=16148168401;R=173;B=10**2400;Z=json.loads(gzip.decompress(fp.read_bytes()));expected={126:[2],158:[2,4],184:[1,2,4,5,6,8]};assert set(map(int,Z['nodes']))==set(expected);seen=set();tails=[]
def val(x,p):
 i=0
 while x%p==0:i+=1;x//=p
 return i
def sig(p,h):return (p**(h+1)-1)//(p-1)
def state(row):
 X=prod(p**h for p,h in row);S=prod(sig(p,h)//(1+h%2) for p,h in row);D=S
 while (g:=gcd(D,X))>1:D//=g
 return X,S,D
for h,ex in expected.items():
 row=[(7,12),(Q,42),(R,h)];X,S,D=state(row);fs,child=Z['nodes'][str(h)];a=max(fs);seen.update(q for q in fs if q>=2**64);assert len(fs)==len(set(fs)) and all(D%q==0 and q not in dict(row) for q in fs);v=val(D,a);assert v>0;n=v;sz=X*D;live=[]
 while sz<=B:
  if n%2==0 or a%4==1 and n%4==1:
   rr=row+[(a,n)];x,s,d=state(rr)
   if gcd(x*s,19)==1 and x*d<=B and all(val(s,p)<=g for p,g in rr):live.append(n)
  sz*=a;n+=1
 assert ex==live and set(map(int,child))==set(live);tails.append(n)
 for e in live:
  x,s,d=state(row+[(a,e)]);extra=child[str(e)];assert all(d%z==0 and (sig(a,e)//(1+e%2))%z==0 and z not in dict(row+[(a,e)]) for z in extra);seen.update(z for z in extra if z>=2**64)
assert set(Z['ecpp'])=={str(q) for q in seen} and sum(map(len,expected.values()))==9
print('PASS anchors',expected,'strict tails',tails,'ECPP',len(seen),'SHA',hashlib.sha256(fp.read_bytes()).hexdigest())
