"""Data-only raw domain reconstruction; arithmetic forest endpoints are separately replayed."""
from math import gcd,prod
from pathlib import Path
import json,gzip,hashlib
B=10**2400;H=Path(__file__).resolve().parents[1]/'Nineteen';raw=(H/'Packet28Inner.json.gz').read_bytes();d=json.loads(gzip.decompress(raw));base=[(19,282),(1735317810514627,10),(8383027,28)];Q=d['Q'];sig=lambda p,k:(p**(k+1)-1)//(p-1);assert 59*Q==sig(*base[-1]);stats=[0,0];tails=[]
def state(P):
 X=prod(p**k for p,k in P);Z=prod(sig(p,k) for p,k in P);s=Z//2**sum(k%2 for p,k in P);c=s//gcd(X,s);good=(gcd(X,c)==1 and X*c<=B and Z<=2*X and sum(k%2 for p,k in P)<=1 and all(not k%2 or p%4==k%4==1 for p,k in P));return X,c,good
def dom(P,r):
 X,c,ok=state(P);assert ok and c%r==0 and r not in dict(P);h=0
 while c%r==0:c//=r;h+=1
 li=[]
 while X*c*r**h<=B:
  if state(P+[(r,h)])[2]:li.append(h)
  h+=1
 tails.append(h);return li
assert dom(base,Q)==[2];rows=base+[(Q,2)];n=dom(rows,23773);assert len(n)==37 and sorted(tails)==[7,100]
def walk(P,node):
 if node['type']=='forest':stats[0]+=1;return
 assert node['type']=='split';stats[1]+=1;r=node['q'];exps=dom(P,r);assert set(exps)==set(map(int,node['cases']))
 for k in exps:walk(P+[(r,k)],node['cases'][str(k)])
for f,N in d['nodes'].items():walk(rows+[(23773,int(f))],N)
assert set(n)=={1,4,*map(int,d['nodes'])} and len(d['nodes'])==35 and stats==[532,25];print('PASS exact Q identity, tails 7/100, 35/37, 25 splits and 532 forests, SHA256',hashlib.sha256(raw).hexdigest())
