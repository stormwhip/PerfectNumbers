"""No proof code imports: all high manifest cells/domains and every hybrid elementary endpoint at (19,280)."""
import json,gzip,time
from collections import Counter
from pathlib import Path
from math import gcd,prod
from fractions import Fraction as F
H=Path(__file__).resolve().parents[1]/'Ten276'/'Release280';s0=time.perf_counter();B=10**2400;s=353998162545967;y=16208389663;sg=lambda p,h:(p**(h+1)-1)//(p-1)
def state(P):
 X=prod(p**e for p,e in P);raw=prod(sg(p,e) for p,e in P);odd=sum(e%2 for p,e in P);S=raw//2**odd;D=S//gcd(X,S);ok=odd<=1 and all(not e%2 or e%4==p%4==1 for p,e in P) and X*D<=B and gcd(X,D)==1 and raw<=2*X;return X,D,odd,raw,ok
def val(x,p):
 h=0
 while not x%p:x//=p;h+=1
 return h
def dom(P,r):
 X,D,odd,raw,ok=state(P);h=val(D,r);assert ok and h and r not in dict(P);coef=X*D//r**h;z=[]
 while coef*r**h<=B:
  if state(P+[(r,h)])[4]:z.append(h)
  h+=1
 return z,h
read=lambda n:json.loads((H/n).read_bytes()) if (H/n).is_file() else json.loads(gzip.decompress((H/(n+'.gz')).read_bytes()))
src=read('HighManifest.json');classes=Counter();counts=Counter();seen=set();base=[(19,280)];la,raw=dom(base,s);assert la==list(range(2,59,2))
for h in [16,18]:
 P=base+[(s,h)];L,ta=dom(P,y);assert ta=={16:122,18:117}[h] and L==list(range(2,61 if h==16 else 59,2))
 for k in L:
  key=f'{h},{k}';seen.add(key);kind,param=src[key];classes[h,kind]+=1
  if kind!='hybrid': continue
  z=read(f'Hybrid280Case{param}.json');f=P+[(y,k)];assert [list(x) for x in f]==z['path'];visited=set();nodes=z['nodes'];stack=[f]
  while stack:
   path=stack.pop();sid=','.join(str(e) for p,e in path);assert sid not in visited;visited.add(sid);node=nodes[sid];tag=node['kind'];counts[tag]+=1;X,D,odd,S,ok=state(path);assert ok
   if tag=='split':
    r=node['q'];li,_=dom(path,r);stack.extend(path+[(r,e)] for e in li);continue
   if tag=='forest':continue
   fs=node['F'];assert tag in ('ab','parity') and len(set(fs))==len(fs) and all(D%r==0 for r in fs);vv={r:val(D,r) for r in fs};worst=None
   for euler in [None]+[r for r in fs if r%4==1 and not odd]:
    a=S if tag=='ab' else X*D;b=X if tag=='ab' else 1
    for r in fs:
     e=vv[r];v=e+(1-e)%4 if r==euler else e+e%2
     if tag=='ab':a*=sg(r,v);b*=r**v
     else:a*=r**(v-e)
    assert a>(2 if tag=='ab' else B)*b
  assert visited==nodes.keys()
assert seen==src.keys() and counts=={'split':160,'forest':3422,'ab':856,'parity':219}
G=H.parents[2]/'GeminiFrontier';sh=json.loads((G/'ShardToKeys.json').read_bytes());iv=json.loads((G/'KeyToShards.json').read_bytes());assert [(n,z) for n,z in sh.items() if [19,280] in z]==[('P19_I00058',[[19,280]])] and iv['19,280']==['P19_I00058'];print('PASS independent high 280 manifest domains and elementary endpoints',classes,counts,'first tail',raw,'elapsed',round(time.perf_counter()-s0,3))
