from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'NightSevenForest/Release'))
from PrimeCheck import level,prime64
assert __debug__;D=json.loads((H/'Emissions.json').read_bytes());assert len(D)==2
for z,rows in D.items():
 n=int(z)**2+int(z)+1
 for s,chain in rows.items():
  p=q=int(s);assert n%p==0
  for row in chain:assert q==row[0] and q>=2**64;q=level(*row)
  assert prime64(q)
  while n%p==0:n//=p
 assert n==1;print('PASS complete square emission',z,len(rows))
