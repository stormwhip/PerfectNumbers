"""Two support masks at the historical shared R^4 residual of (7,882), t^8."""
import json,gzip,hashlib
from fractions import Fraction as F
from math import prod
from pathlib import Path
assert __debug__
H=Path(__file__).resolve().parents[3]/'Night2400'/'G7'; p,t,R=7,21193,30201838022902600352247769
s=lambda q,e:(q**(e+1)-1)//(q-1)
r=lambda q,e:F(s(q,e),q**e)
assert s(t,8)%(9*13*R)==0
assert s(t,2)%(3*13)==0
# Lower bound for either exact exponent 2 or 8; R is not required.
P={p:882,t:2};raw=(H/'Seven882.json.gz').read_bytes();assert hashlib.sha256(raw).hexdigest()=='0c2126c026c9aec5fd86f2dde96a8fedae3f8498dd274f57a0052d20630a302f'
tree=json.loads(gzip.decompress(raw))
def pending(node):return node['type']=='open' or node['type']=='split' and any(pending(z) for z in node['cases'].values())
for k in (2,8):assert [m for m in range(2,256,4) if str(k) in tree['cases'][str(m)]['cases'] and pending(tree['cases'][str(m)]['cases'][str(k)])]==[50,54,58,178,186]
for mask,yes in [(54,[3,11,13]),(186,[3,13,17,31])]:
 assert sorted(int(k) for k,node in tree['cases'][str(mask)]['cases'].items() if pending(node))==[2,8,72]
 O=[19,7,11,31,13,3,5,17]; assert set(yes)|{7}=={q for i,q in enumerate(O) if mask>>i&1}
 for euler in [0]+[q for q in yes if q%4==1]:
  lo={q:2 for q in yes};lo[3]=2
  if euler:lo[euler]=1
  for exp in ([1,5] if euler else [0]):
   v=dict(lo)
   if euler:v[euler]=exp
   if euler==13 and exp==1:
    # 3^2||N would supply another 13 in addition to the copy in sigma(t^8).
    assert s(3,2)%13==0 and all(s(t,k)%13==0 for k in (2,8));v[3]=4
   if euler==17 and exp==1:
    assert s(17,1)%9==0 and all(s(t,k)%3==0 for k in (2,8));v[3]=4
   bound=prod(r(q,e) for q,e in (P|v).items());assert bound>2,(mask,euler,exp)
   print('PASS mask/Euler/lower exponent',mask,euler,exp,'excess times 100000 floor',int((bound-2)*100000))
