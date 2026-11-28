"""Independent traversal of explicit ordinary anchor skeleton, not a duplicate of terminal price proof."""
from pathlib import Path
import json,sys,hashlib
from math import prod,gcd
H=Path(__file__).resolve().parents[1]/'Nineteen';d=json.loads((H/sys.argv[1]).read_bytes());p,t=19,2477;B=10**2400;sigma=lambda p,e:(p**(e+1)-1)//(p-1)
def check(f,node,Xrows,hints):
 global splits,visited,maxdepth
 if node is None:return
 r=node['r'];P={p:618,t:f,**Xrows};X=prod(x**k for x,k in P.items());S=prod(sigma(x,k) for x,k in P.items());D=S//gcd(S,X);assert gcd(X,D)==1 and r in hints and r not in P and D%r==0 and r%(4*t**(f-1))!=2*t**(f-1)-1
 a=0
 while D%r==0:a+=1;D//=r
 j=a+a%2;ex=[]
 while X*D*r**j<=B:ex.append(j);j+=2
 assert set(map(int,node['kids']))<=set(ex)
 splits+=1;visited+=len(ex);maxdepth=max(maxdepth,len(Xrows)+1)
 for k in ex:check(f,node['kids'].get(str(k)),Xrows|{r:k},hints|set(map(int,d['forced'].get(str(r),{}).get(str(k),{}))))
for table in (d['root'],d['forced']):
 for r,hs in table.items():
  for k,hints in hs.items():assert all(sigma(int(r),int(k))%int(z)==0 for z in hints)
splits=0;visited=1;maxdepth=0
for f,node in d['cases'].items():check(int(f),node,{},set(map(int,d['root'][str(t)][f]))-{p})
print('PASS explicit compulsory ordinary split skeleton',splits,'calls if traversed',visited,'depth',maxdepth,'SHA256',hashlib.sha256((H/sys.argv[1]).read_bytes()).hexdigest())
