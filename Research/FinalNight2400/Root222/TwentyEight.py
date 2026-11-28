"""Full first 28 at (19,222); no restriction on Euler location."""
from pathlib import Path
import sys,json,gzip
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Firsts import C,B,t

def main():
 assert __debug__ and C.pc.prime64(t) and C.sigma(19,222)%t==0
 o=json.loads(gzip.decompress((H/'TwentyEight.json.gz').read_bytes()));K,O=o['cases']['28'];bk=o['ecpp'];seen=set()
 def prime(q):
  n=q
  if n>=2**64:
   seen.add(str(n));chain=bk[str(n)];assert chain
   for row in chain:assert row[0]==n;n=C.pc.level(*row)
  assert C.pc.prime64(n);return True
 s=C.State([(19,222),(t,28)]);assert not s.conflict and not s.fixed_euler;C.validate_forest(s,K,O,128,prime);assert seen==set(bk);v,_=C.Forest(s,K,O,128).lower();assert v>B
 print('PASS (19,222) first 28 exact free-Euler forest, floor',len(str(v))-1,'vertices',len(K)+len(O),'ECPP',len(bk))
if __name__=='__main__':main()
