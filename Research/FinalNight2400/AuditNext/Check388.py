"""Independent three-target disjoint price and ordinary-only forest for 13,388 first6/second12."""
from pathlib import Path
from functools import cache
from fractions import Fraction
from math import gcd,isqrt,prod
import json,time
import gzip
s0=time.perf_counter();H=Path(__file__).resolve().parent.parent/'Others';f=json.loads(gzip.decompress((H/'Vertex388Forest.json.gz').read_bytes()));K=f['roots'];head=f['head'];edges=f['owners'];B=10**2400;no=(19,7,11,31);P=[(13,388),(3543791,6),(14199329591297809156875293,12)]
def sigma(p,e):return (p**(e+1)-1)//(p-1)
S=prod(sigma(p,e) for p,e in P);X=prod(p**e for p,e in P);D=S//gcd(S,X);assert gcd(D,X)==1
vs=set(K)|{a for a,z in edges};children={z:[] for z in vs}
for a,z in edges:children[z].append(a)
cp={z:prod(child) for z,child in children.items()};pool=X*D*prod(a for a,z in edges)
def val(n,z):
 k=0
 while n%z==0:k+=1;n//=z
 return k
def trim(z):
 while (g:=gcd(z,pool))!=1:z//=g
 return z
@cache
def low(z,h):
 e=h+h%2;best=B+1;cnt=0
 while z**e<best and cnt<head:
  s=sigma(z,e)
  if all(s%b for b in no):
   cnt+=1;g=gcd(s,cp[z]);n=z**e*trim(s)
   if g>1:n*=prod(low(a,val(s,a)) for a in children[z] if not g%a)
   best=min(n,best)
  e+=2
 return min(best,z**e)
root=X*D
for z in K:
 h=val(D,z);assert h>0;root//=z**h;root*=low(z,h)
assert root>B and len(str(root))-1==2681
@cache
def levels(p,o,c):
 a=next(w for g in range(2,p) if all(pow((w:=pow(g,(p-1)//o,p)),d,p)!=1 for d in range(1,o) if not o%d));m=p;ret=[]
 for _ in range(c):ret.append((m,[pow(a,i,m) for i in range(1,o) if gcd(i,o)==1]));m*=p;a=pow(a,p,m)
 return ret
facs=[(3,), (5,389,911),(7,11,503,9006499,10176375725767)];ws=[2,4,3];caps=[388,5,11];losses=[];costs=[];supp=[]
for (p,k),fs,w,c in zip(P,facs,ws,caps):
 n=p-1
 while n%2==0:n//=2
 assert n==prod(fs) and all(gcd(p*n,z)==1 for z in supp);supp.append(p*n);out={};ds=[1]
 for z in fs:ds +=[a*z for a in ds]
 for o in ds[1:]:
  h=o-1
  if o>8000 or 3**h>=p**(w*c):continue
  def add(r,m):
   if r<3 or not r%2 or (r.bit_length()-1)*h>=w*m.bit_length():return
   rr=r**h;nn=m**w
   if rr>=nn:return
   if p!=P[-1][0]:
    if any(r%k==0 and r not in (k,k*k) for k in (3,5,7,11,13,17,19,23,29,31,37)):return
    u=isqrt(r)
    if pow(2,r,r)!=2 and not (u*u==r and u%4==1 and pow(2,u,u)==2):return
   out[r]=max(out.get(r,1),Fraction(nn,rr))
  if 4096**h>=p**(w*c):
   for r in range(3,4096,2):
    if r**h>=p**(w*c):break
    if pow(r,o,p)==1:add(r,gcd(pow(r,o,p**c)-1,p**c))
  else:
   for m,zs in levels(p,o,c):
    for r in zs:add(r,m)
 losses+=list(out.values());costs.append(len(out))
U=prod(losses,start=Fraction(1));eligible=[z for z in vs if z%4==1];assert len(eligible)==414
assert all(X*q*prod((p**c//gcd(p**c,q+1))**w for (p,_),c,w in zip(P,caps,ws))>B*U for q in eligible)
def holes(file):
 z=json.loads(gzip.decompress((H/file).read_bytes()));todo=[(v,((13,388),(z['pivot'],int(f)))) for f,v in z['cases'].items()];opened=set()
 while todo:
  v,path=todo.pop()
  if v['type']=='open':opened.add(path)
  elif v['type']=='split':todo.extend((child,path+((v['q'],int(k)),)) for k,child in v['cases'].items())
 return opened
assert holes('Thirteen388Six.json.gz')=={((13,388),(3543791,42),(1113708120497983331,12),(217387,52)),((13,388),(3543791,66),(459911137111,10))} and holes('Thirteen388One.json.gz')=={tuple(P)}
G=H.parents[1]/'GeminiFrontier';sh=json.loads((G/'ShardToKeys.json').read_bytes());inv=json.loads((G/'KeyToShards.json').read_bytes());assert [(n,z) for n,z in sh.items() if [13,388] in z]==[('P13_I00076',[[13,388]])] and inv['13,388']==['P13_I00076'];print('PASS 3-way Euler tests',len(eligible),'ordinary floor',len(str(root))-1,'losses',costs,'seconds',round(time.perf_counter()-s0,3))
