"""Final three T^12 exact cells; combine Firsts, Two, Thirds, then this checker."""
from pathlib import Path
import json,sys,gzip
from math import prod
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Two import C,B,t,r

def main():
 z=50935324949359682417;obj=json.loads(gzip.decompress((H/'Twelve.json.gz').read_bytes()));bk=obj['ecpp'];seen=set();memo=set();n=0
 def prime(p):
  if p in memo:return True
  q=p
  if p>=2**64:
   seen.add(str(p));arr=bk[str(p)];assert arr
   for rr in arr:assert rr[0]==q;q=C.pc.level(*rr)
  assert C.pc.prime64(q);memo.add(p);return True
 assert set(obj['cases'])=={'2','16','22'}
 for k,forest in obj['cases'].items():
  g=int(k);a=371183958661 if g==2 else 4873207;P=[(19,222),(t,12),(r,g),(z,6)];s=C.State(P);assert all(prime(p) for p,h in P) and prime(a) and all(any(C.sigma(v,h)%p==0 for v,h in P[:i]) for i,(p,h) in enumerate(P) if i) and s.D%a==0
  c=C.valuation(s.D,a);j=c;live=[]
  while s.base//a**c*a**j<=B:
   if s.possible(a,j,c):
    pre=P+[(a,j)];ss=C.State(pre)
    if not ss.conflict and ss.base<=B and prod(C.sigma(p,h)for p,h in pre)<=2*ss.X:
     K,O=forest[str(j)];C.validate_forest(ss,K,O,128,prime);assert C.Forest(ss,K,O,128).lower()[0]>B;live.append(j);n+=1
   j+=1
  assert set(map(int,forest))==set(live);print('g',g,'children',len(live),'raw tail',j)
 assert seen==set(bk);print('PASS (19,222) first 12 via 3 residual secondary/tertiary prefixes;',n,'complete fourth children; ECPP',len(bk))
if __name__=='__main__':main()
