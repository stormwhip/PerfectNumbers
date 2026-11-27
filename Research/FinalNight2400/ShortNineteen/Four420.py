"""At (19,420), exact first t^4 forces v_r in {1,2,4}."""
from math import prod
import sys,json,gzip
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from ExactTwo import C,B,Q,Root

def main():
 e=420;t=Q[e];r=72688845161;P=[(19,e),(t,4)];s=C.State(P);assert not s.conflict
 z=json.loads(gzip.decompress((H/'Four420.json.gz').read_bytes()));cases,book=z['cases'],z['ecpp'];used=set();memo=set()
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
 c=C.valuation(s.D,r);g=c;live=[]
 while s.base//r**c*r**g<=B:
  if s.possible(r,g,c):
   ss=C.State(P+[(r,g)])
   if not ss.conflict and ss.base<=B and prod(C.sigma(q,k) for q,k in ss.rows.items())<=2*ss.X:live.append(g)
  g+=1
 assert set(live)==set(map(int,cases))|{1,2,4} and len(live)==32
 for key,(K,O) in cases.items():
  ss=C.State(P+[(r,int(key))]);C.validate_forest(ss,K,O,128,prime);lo,_=C.Forest(ss,K,O,128).lower();assert lo>B
 assert used==set(book);print('PASS 420 first 4, secondary',r,'raw tail',g,'remaining [1,2,4]; full second rows',len(cases),'checked ECPP',len(book))
if __name__=='__main__':main()
