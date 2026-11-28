"""Both old T^2 null leaves are abundant, using only exact arithmetic."""
import gzip, hashlib, json
from math import prod,isqrt
from pathlib import Path
assert __debug__
H=Path(__file__).resolve().parents[2]/'Night2400'/'C10'/'EulerF1.json.gz'
b=H.read_bytes();assert hashlib.sha256(b).hexdigest()=='f52b0f8b3fd0f8e869e0e38f7d6ac34cf0254a1082dce5c2ad8df3f2ca7f5c90'
d=json.loads(gzip.decompress(b))
def sig(p,e):return (p**(e+1)-1)//(p-1)
Q,T,A=(155306613932666028670208812450645212905178047040045530562317564121001023821,25884435655444338111701468741774202150863007840007588427052927353500170637,172900527934963165844668988041369220224337976000897153058459631342970404239133047)
assert (d['p'],d['e'],d['pivot'],d['tree']['q'])==(19,58,Q,T)
t=d['tree']['cases']['2'];assert t['q']==A
opens=[]
def walk(t,path):
 if t is None:opens.append(tuple(path));return
 if t['type']=='split':
  for f,c in t['cases'].items():walk(c,path+[(t['q'],int(f))])
walk(t,[])
L=7627802356190118487344916013429102813353772289568699
assert set(opens)=={((A,2),(L,2)),((A,2),(L,4))}
assert sig(19,58)==Q and Q+1==6*T and sig(T,2)%A==0
assert sig(T,2)%(3*7*61)==0 and sig(A,2)%(3*13)==0
assert len({Q,T,A,19,3,7,13,61})==8
for p in [3,7,13,19,61]:assert all(p%i for i in range(2,isqrt(p)+1))
E=[(3,4),(7,2),(13,2),(19,58),(61,2)]
u=prod(sig(p,e) for p,e in E);v=prod(p**e for p,e in E);assert u>2*v
print('PASS T^2: 2/2 historical open leaves, shared A^2 prefix; exact excess numerator',u-2*v,'denominator',v)
