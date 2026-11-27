"""Further exact reductions for the nine missing first values of Firsts.py."""
import sys,json,gzip
from math import prod
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Firsts import C,B,t,remain
r=3705121363
missing={1:[2,4,12,16,22,30,36,40,42,46,52,58],2:[2,16,22,46],12:[2,16,22],16:[2,16,22],18:[2,4,8,12,16,22,28,30,36,40,42,46,52,58],22:[2,16,22],28:[2,16,22]}
def main():
 assert __debug__ and C.pc.prime64(r) and C.pc.prime64(t) and C.sigma(19,222)%(r*t)==0
 D=json.loads(gzip.decompress((H/'TwoForests.json.gz').read_bytes()));cases,book=D['cases'],D['ecpp'];seen=set();memo=set();n=0
 def prime(q):
  if q in memo:return True
  x=q
  if q>=2**64:
   seen.add(str(q));ch=book[str(q)];assert ch
   for row in ch:assert row[0]==x;x=C.pc.level(*row)
  assert C.pc.prime64(x);memo.add(q);return True
 def forest(ss,k):
  K,O=k;C.validate_forest(ss,K,O,128,prime);v,_=C.Forest(ss,K,O,128).lower();assert v>B
 assert set(map(int,cases))==set(remain)
 for fstr,case in cases.items():
  f=int(fstr);P=[(19,222),(t,f)];s=C.State(P);assert not s.conflict and s.base<=B
  if f in [40,46]:forest(s,case);continue
  c=C.valuation(s.D,r);assert c>=1;g=c;live=[];left=[]
  while s.base//r**c*r**g<=B:
   if s.possible(r,g,c):
    parts=P+[(r,g)];ss=C.State(parts)
    if not ss.conflict and ss.base<=B and prod(C.sigma(p,h)for p,h in parts)<=2*ss.X:
     live.append(g)
     if str(g) in case:forest(ss,case[str(g)]);n+=1
     else:left.append(g)
   g+=1
  assert left==missing[f] and set(live)==set(map(int,case))|set(left)
 assert seen==set(book);print('PASS root 222 further full firsts 40,46; remaining firsts',sorted(missing),'second exclusions',n,'remaining exact pairs',sum(map(len,missing.values())),'ECPP',len(book))
if __name__=='__main__':main()
