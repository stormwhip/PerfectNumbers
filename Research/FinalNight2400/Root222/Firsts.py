"""Root 19^222, exact first-pivot domain and unrestricted-Euler strict leaves."""
import sys,json,gzip
from pathlib import Path
from math import prod
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H.parents[1]/'Session20261126'));from PivotCheck import C,B
t=7579985624053;remain=[1,2,12,16,18,22,28,40,46]
def main():
 assert __debug__ and C.pc.prime64(t) and C.sigma(19,222)%t==0
 P=[(19,222)];s=C.State(P);c=C.valuation(s.D,t);assert c==1
 g=c;live=[];z=json.loads(gzip.decompress((H/'FirstForests.json.gz').read_bytes()));rows=z['cases'];book=z['ecpp'];used=set();memo=set()
 def prime(n):
  if n in memo:return True
  a=n
  if n>=2**64:
   ch=book[str(n)];assert ch;used.add(str(n))
   for rr in ch:assert rr[0]==a;a=C.pc.level(*rr)
  assert C.pc.prime64(a);memo.add(n);return True
 while s.base//t**c*t**g<=B:
  if s.possible(t,g,c):
   st=C.State(P+[(t,g)])
   if not st.conflict and st.base<=B and prod(C.sigma(q,h)for q,h in st.rows.items())<=2*st.X:live.append(g)
  g+=1
 assert len(live)==53 and sorted(set(live)-set(map(int,rows)))==remain and len(rows)==44
 for i,(K,O) in rows.items():
  st=C.State(P+[(t,int(i))]);C.validate_forest(st,K,O,128,prime);lo,_=C.Forest(st,K,O,128).lower();assert lo>B
 assert used==set(book);print('PASS (19,222) 44/53 firsts; raw tail',g,'remain',remain,'ECPP',len(book))
if __name__=='__main__':main()
