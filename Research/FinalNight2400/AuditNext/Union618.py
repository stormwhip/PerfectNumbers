"""Independent exact root domain and disjoint coverage-group audit; does not replay proof mechanisms."""
import json
from pathlib import Path
from math import gcd,prod
H=Path(__file__).resolve().parents[1]/'Nineteen';G=H.parents[1]/'GeminiFrontier';p=19;t=2477;B=10**2400;sg=lambda p,h:(p**(h+1)-1)//(p-1);X=p**618;S=sg(p,618);assert S%t==0 and S%t**2!=0;raw=1;domain=[]
while X*(S//t)*t**raw<=B:
 e=raw;xx=X*t**e;sig=S*sg(t,e);z=sig//(1+e%2);D=z//gcd(z,xx)
 if (not e%2 or t%4==e%4==1) and gcd(D,xx)==1 and xx*D<=B and sig<=2*xx:domain.append(e)
 raw+=1
assert raw==243 and set(domain)=={1,*range(2,121,2),*range(5,122,4)}
hist={*range(5,122,4),*range(70,122,2)};assert len(hist)==56 and set(domain)-hist=={1,*range(2,69,2)}
groups=[hist,{26,*range(30,69,2)},{1,18,20,22,24,28},{14,16},{10,12},{8},{6},{4},{2}];assert sum(map(len,groups))==len(set.union(*groups))==len(domain)==91 and set.union(*groups)==set(domain)
for name,f in [('Solved8.json',8),('Solved6.json',6),('Solved4.json',4),('Solved2.json',2)]:assert set(json.loads((H/name).read_bytes())['cases'])=={str(f)}
ledger=json.loads((G/'ShardToKeys.json').read_bytes());inv=json.loads((G/'KeyToShards.json').read_bytes());assert [(s,v) for s,v in ledger.items() if [19,618] in v]==[('P19_I00112',[[19,618]])] and inv['19,618']==['P19_I00112'];print('PASS raw first tail',raw,'domain',len(domain),'disjoint groups',list(map(len,groups)),'singleton P19_I00112')
