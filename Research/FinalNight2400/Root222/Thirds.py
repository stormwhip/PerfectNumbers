"""Exact two/three-pivot certificate for previously open residual pairs."""
from pathlib import Path
import sys,json,gzip
from math import prod
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Two import C,B,t,r,missing

def main():
 assert __debug__ and all(C.pc.prime64(x) and C.sigma(19,222)%x==0 for x in (r,t))
 z=json.loads(gzip.decompress((H/'ThirdForests.json.gz').read_bytes()));book=z['ecpp'];lhs=z['cases'];seen=set();memo=set();full=0;extra=0;res=[]
 def prime(q):
  if q in memo:return True
  v=q
  if v>=2**64:
   seen.add(str(v));arr=book[str(v)];assert arr
   for x in arr:assert x[0]==v;v=C.pc.level(*x)
  assert C.pc.prime64(v);memo.add(q);return True
 def leaf(s,code):
  K,O=code;C.validate_forest(s,K,O,128,prime);assert C.Forest(s,K,O,128).lower()[0]>B
 for f,gg in missing.items():
  for g in gg:
   k=f'{f}:{g}';P=[(19,222),(t,f),(r,g)];s=C.State(P);assert not s.conflict
   if k not in lhs:res.append((f,g,None));continue
   row=lhs[k]
   if isinstance(row,list):leaf(s,row);full+=1;continue
   a=row['q'];assert prime(a) and a not in s.rows and s.D%a==0
   cs=row['children'];c=C.valuation(s.D,a);j=c;domain=[];left=[]
   while s.base//a**c*a**j<=B:
    if s.possible(a,j,c):
     pre=P+[(a,j)];st=C.State(pre)
     if not st.conflict and st.base<=B and prod(C.sigma(q,h)for q,h in pre)<=2*st.X:
      domain.append(j)
      if str(j) in cs:leaf(st,cs[str(j)]);extra+=1
      else:left.append(j)
    j+=1
   assert left==row['left'] and set(map(int,cs))|set(left)==set(domain)
   if left:res.append((f,g,left))
   else:full+=1
 assert seen==set(book);print('PASS root-222 third packet: further full secondary',full,'extra exact third children',extra,'ECPP',len(book),'remaining second prefixes',len(res));print('Residual domains:',res)
if __name__=='__main__':main()
