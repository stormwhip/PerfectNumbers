"""At (19,420), exact first t^4 forces v_r in {1,2,4}."""
from math import prod
import sys,json,gzip
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from ExactTwo import C,B,Q,Root

def main():
 e=420;t=Q[e];a=54138880391625933029911659199743811;r=72688845161;P=[(19,e),(t,4),(r,4)];s=C.State(P);assert not s.conflict
 z=json.loads(gzip.decompress((H/'SecondaryFour.json.gz').read_bytes()));cases,book=z['cases'],z['ecpp'];used=set();memo=set()
 def prime(n):
  if n in memo:return True
  a=n
  if a>=2**64:
   if a==t:rows=json.loads((Root/'Night2400/C/PivotECPP.json').read_bytes())
   else:used.add(str(n));rows=book[str(n)]
   assert rows
   for row in rows:assert row[0]==a;a=C.pc.level(*row)
  assert C.pc.prime64(a);memo.add(n);return True
 assert prime(19) and prime(t) and prime(r) and C.sigma(19,e)%t==0 and C.sigma(t,4)%r==0
 assert prime(a) and C.sigma(r,4)%a==0
 c=C.valuation(s.D,a);g=c;live=[]
 while s.base//a**c*a**g<=B:
  if s.possible(a,g,c):
   ss=C.State(P+[(a,g)])
   if not ss.conflict and ss.base<=B and prod(C.sigma(q,k) for q,k in ss.rows.items())<=2*ss.X:live.append(g)
  g+=1
 assert set(live)==set(map(int,cases))=={2,4,6,8,10,12}
 for key,(K,O) in cases.items():
  rows=P+[(a,int(key))];ss=C.State(rows);C.validate_forest(ss,K,O,128,prime)
  if key in ['4','6']:
   from Price import price
   from math import gcd
   v,qs,_,_=price(rows,[2,2,0,2]);assert v>B;M=prod(p**c for p,c,w in qs)
   for euler in set(K)|{b for b,z in O}:
    if euler%4==1:assert v*euler>B*gcd(M,euler+1)**2
   ss.fixed_euler=True
  lo,_=C.Forest(ss,K,O,128).lower();assert lo>B
 assert used==set(book);print('PASS (19,420) first 4, secondary 4 fully excluded; tertiary raw tail',g,'complete 6 cases; ECPP',len(book))
if __name__=='__main__':main()