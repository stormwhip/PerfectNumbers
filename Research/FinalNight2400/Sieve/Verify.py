"""Offline stdlib replay of complete factorizations; no fiber closure implied."""
from pathlib import Path
import json,sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'NightSevenForest/Release'))
from PrimeCheck import level,prime64
D=json.loads((H/'Factors.json').read_bytes());assert __debug__ and {'22','24'}<=D.keys()
for e,rows in D.items():
 n=(2477**(int(e)+1)-1)//2476
 for label,chain in rows.items():
  p=q=int(label);assert p>1 and n%p==0
  for row in chain:
   assert q==row[0] and q>=2**64;q=level(*row)
  assert prime64(q)
  while n%p==0:n//=p
 assert n==1
 print('PASS complete prime support sigma(2477^%s)'%e,len(rows),'certified primes')
