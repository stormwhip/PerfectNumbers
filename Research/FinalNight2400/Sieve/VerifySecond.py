from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'NightSevenForest/Release'))
from PrimeCheck import level,prime64
assert __debug__;p=8383027;D=json.loads((H/'SecondProof.json').read_bytes());assert {4,6,10,28}==set(map(int,D))
for e,rows in D.items():
 n=(p**(int(e)+1)-1)//(p-1)
 for label,chain in rows.items():
  q=z=int(label);assert n%q==0
  for row in chain:
   assert row[0]==z and z>=2**64;z=level(*row)
  assert prime64(z)
  while n%q==0:n//=q
 assert n==1; print('PASS complete sigma',p,e,len(rows))
