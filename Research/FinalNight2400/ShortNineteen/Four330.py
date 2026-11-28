"""Complete f=4 at (19,330), unrestricted Euler forest."""
from pathlib import Path
import sys,json,gzip
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from ExactTwo import C,Q,B
if __name__=='__main__':
 t=Q[330];P=[(19,330),(t,4)];s=C.State(P);assert not s.conflict and not s.fixed_euler and C.sigma(19,330)%t==0
 o=json.loads((H/'Rich330x4.json').read_bytes());book=json.loads(gzip.decompress((H/'RichPrimes330x4.json.gz').read_bytes()));used=set()
 def prime(n):
  a=n
  if n>=2**64:
   chain=book[str(n)];used.add(str(n));assert chain
   for rr in chain:assert rr[0]==a;a=C.pc.level(*rr)
  assert C.pc.prime64(a);return True
 assert prime(t);K,O=o['roots'],o['owners'];C.validate_forest(s,K,O,128,prime);assert used==set(book)
 lo,_=C.Forest(s,K,O,128).lower();assert lo>B
 print('PASS (19,330) first 4 unrestricted Euler; floor',len(str(lo))-1,'vertices',len(K)+len(O),'ECPP',len(book))
