"""Exclude h=1 at (7,12;Q,12;T,h) without any forest search."""
import sys,gzip,json
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Session20261126'));from PivotCheck import C,B
Q=16148168401;T=(Q**13-1)//(Q-1)//13;J=154168831365557905586436420483382101694649586851016856543013171742854124357951185973714712196987
if __name__=='__main__':
 assert __debug__ and C.pc.prime64(Q) and C.sigma(7,12)==Q
 for n,chain in [(T,json.load(gzip.open(H/'SevenForest.json.gz'))['ecpp'][str(T)]),(J,json.loads((H/'JPrime.json').read_bytes()))]:
  k=n
  for row in chain:assert row[0]==k;k=C.pc.level(*row)
  assert C.pc.prime64(k)
 S=C.sigma(7,12)*C.sigma(Q,12)*((T+1)//2);assert T%4==1 and J%4==3 and C.valuation(S,J)==1
 assert 3**5100>B and J>5101 and [k for k in range(3,5101,2) if (J-1)%k==0]==[89]
 x=next(y for g in range(2,100) if (y:=pow(g,(J-1)//89,J))!=1);assert pow(x,89,J)==1 and C.pc.prime64(89)
 roots={pow(x,i,J) for i in range(1,89)};assert len(roots)==88 and min(roots)**88>B
 print('PASS T^1: J is compelled once, must be ordinary, no external ordinary source. All 88 least order-89 representatives violate component size.',flush=True)
