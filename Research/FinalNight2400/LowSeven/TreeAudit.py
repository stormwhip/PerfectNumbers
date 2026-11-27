"""Optional reproducible partial-packet summary and exact independent first-level domains."""
from pathlib import Path
from math import gcd,prod
import json,gzip,hashlib,sys
H=Path(__file__).resolve().parent;B=10**2400
for path in map(Path,sys.argv[1:]):
 d=json.loads(gzip.decompress(path.read_bytes()));p,e,q=d['p'],d['e'],d['pivot'];assert p==7 and e in [16,18,48];A=(p**(e+1)-1)//(p-1);assert A%q==0 and A%(q*q)!=0;n=1;size=p**e*A;ds=[]
 while size<=B:
  if n%2==0 or n%4==q%4==1:
   X=p**e*q**n;S=A*((q**(n+1)-1)//(q-1))//(1+n%2);D=S
   while (g:=gcd(D,X))>1:D//=g
   if 19>S%19>0 and S%p**(e+1)!=0 and S%q**(n+1)!=0 and X*D<=B and (1+n%2)*S<=2*X:ds.append(n)
  n+=1;size*=q
 covered=set(map(int,d['cases']));assert covered<=set(ds) and all(c['type']=='forest' for c in d['cases'].values());print(p,e,'domain',len(ds),'tail',n,'strict forest-covered',len(covered),'open',sorted(set(ds)-covered),'ECPP',len(d['ecpp']),'sha',hashlib.sha256(path.read_bytes()).hexdigest())
