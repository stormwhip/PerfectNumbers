"""Verify all remaining f22 cases from the two/third-pivot validated domain."""
import sys,json,gzip
from pathlib import Path
from math import prod
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Two import t,r,C,B

def main():
 D=json.loads(gzip.decompress((H/'TwentyTwo.json.gz').read_bytes()));book=D['ecpp'];seen=set();memo=set();n=0
 def prime(p):
  if p in memo:return True
  v=p
  if p>=2**64:
   seen.add(str(p));ch=book[str(p)];assert ch
   for rr in ch:assert rr[0]==v;v=C.pc.level(*rr)
  assert C.pc.prime64(v);memo.add(p);return True
 def leaf(s,o):
  K,O=o;C.validate_forest(s,K,O,128,prime);assert C.Forest(s,K,O,128).lower()[0]>B
 needed={2:[12],16:[1,2,4,6,10,16,22,24,28,30,36]}
 assert set(D['cases'])=={f'{g}:{v}' for g in needed for v in needed[g]}
 for g,vs in needed.items():
  z=371183958661 if g==2 else 1355978893
  for v in vs:
   P=[(19,222),(t,22),(r,g),(z,v)];s=C.State(P);assert not s.conflict and all(prime(p)for p,f in P) and all(any(C.sigma(p,h)%q==0 for p,h in P[:i]) for i,(q,_) in enumerate(P) if i)
   w=D['cases'][f'{g}:{v}'];
   if isinstance(w,list):leaf(s,w);n+=1;continue
   a=2677;assert prime(a);c=C.valuation(s.D,a);assert c>0;h=c;live=[]
   while s.base//a**c*a**h<=B:
    if s.possible(a,h,c):
     sub=P+[(a,h)];ss=C.State(sub)
     if not ss.conflict and ss.base<=B and prod(C.sigma(q,f)for q,f in sub)<=2*ss.X:
      leaf(ss,w['children'][str(h)]);n+=1;live.append(h)
    h+=1
   assert set(live)==set(map(int,w['children']))
 assert seen==set(book);print('PASS (19,222) entire first 22 by preceding Thirds union; final leaves',n,'ECPP',len(book))
if __name__=='__main__':main()
