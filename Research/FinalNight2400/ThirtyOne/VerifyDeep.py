"""Final 37 split under (31^16,t^22,47^2), restricted to independently proved j=16..20."""
from pathlib import Path
import sys,json
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Verify22 import domain,check
from EulerForest import *
from functools import cache

def deep():
 assert __debug__;row=[(31,16),(T,22),(47,2)];P=json.loads((H/'DeepPacket.json').read_bytes());book=json.loads((H/'CertDeep.json').read_bytes())|json.loads((H/'DeepExtras.json').read_bytes());used=set();
 @cache
 def prime(z):
  q=z
  if q>=2**64:
   used.add(str(q))
   for r in book[str(q)]:assert r[0]==q;q=level(*r)
  assert prime64(q);return True
 assert sig(47,2)==37*61 and prime(37) and prime(T);D=domain(row,37);assert P['q']==37 and set(D)==set(map(int,P['cases']));remaining={};count=[0,0,0]
 for h in D:
  t=P['cases'][str(h)];r=row+[(37,h)];s=C.State(r);assert h%2==0 and not s.conflict;k=t['roots'];o=t['owners'];head=t['head'];C.validate_forest(s,k,o,head,prime);assert all(z%4!=1 or val(z+1,T)<16 for z in set(k)|{q for q,p in o});s.fixed_euler=True
  if C.Forest(s,k,o,head).lower()[0]>B:count[0]+=1;continue
  em=status(r,k);jlist=[j for j,*_ in em if 16<=j<=20];
  if not jlist:count[1]+=1;continue
  left=[j for j in jlist if ef(r,t,j)<=B];
  if left:remaining[h]=left
  else:count[2]+=1
 print('Final 37 domain',len(D),count,'left',remaining,flush=True);return remaining
if __name__=='__main__':assert not deep()
