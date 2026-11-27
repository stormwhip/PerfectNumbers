"""Verify all remaining f22 cases from the two/third-pivot validated domain."""
import sys,json,gzip
from pathlib import Path
from math import prod
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Two import t,r,C,B

def main():
 D=json.loads(gzip.decompress((H/'Sixteen.json.gz').read_bytes()));book=D['ecpp'];seen=set();memo=set();n=0
 def prime(p):
  if p in memo:return True
  v=p
  if p>=2**64:
   seen.add(str(p));ch=book[str(p)];assert ch
   for rr in ch:assert rr[0]==v;v=C.pc.level(*rr)
  assert C.pc.prime64(v);memo.add(p);return True
 def leaf(s,o):
  K,O=o;C.validate_forest(s,K,O,128,prime);assert C.Forest(s,K,O,128).lower()[0]>B
 needed={2:[1,12],16:[2,6,8,12,18,28]}
 assert set(D['cases'])=={f'{g}:{v}' for g in needed for v in needed[g]}
 for g,vs in needed.items():
  z=371183958661 if g==2 else 12463483
  for v in vs:
   P=[(19,222),(t,16),(r,g),(z,v)];s=C.State(P);assert not s.conflict and all(prime(p)for p,f in P) and all(any(C.sigma(p,h)%q==0 for p,h in P[:i]) for i,(q,_) in enumerate(P) if i)
   w=D['cases'][f'{g}:{v}'];
   if isinstance(w,list):leaf(s,w);n+=1;continue
   a=7397067664513;assert prime(a);c=C.valuation(s.D,a);assert c>0;h=c;live=[]
   while s.base//a**c*a**h<=B:
    if s.possible(a,h,c):
     sub=P+[(a,h)];ss=C.State(sub)
     if not ss.conflict and ss.base<=B and prod(C.sigma(q,f)for q,f in sub)<=2*ss.X:
      branch=w['children'][str(h)];live.append(h)
      if isinstance(branch,list):leaf(ss,branch);n+=1
      else:
       assert (g,v,h)==(16,2,18);b=7614097;assert prime(b);i=C.valuation(ss.D,b);assert i>0;j=i;legal=[]
       while ss.base//b**i*b**j<=B:
        if ss.possible(b,j,i):
         rp=sub+[(b,j)];sc=C.State(rp)
         if not sc.conflict and sc.base<=B and prod(C.sigma(q,k)for q,k in rp)<=2*sc.X:
          K,O,bad=branch['children'][str(j)];legal.append(j)
          if bad:
           from fractions import Fraction
           assert bad==[5] and 5 not in sc.rows and 5 not in K
           assert all(prime(q) and q not in sc.rows and sc.D%q==0 for q in K)
           I=Fraction(prod(C.sigma(q,k)for q,k in rp),sc.X);minI=I
           for q in K:
            c0=C.valuation(sc.D,q);expo=c0+(c0%2 if q%4==3 or sc.fixed_euler else 0);minI*=Fraction(C.sigma(q,expo),q**expo)
           assert minI*Fraction(6,5)>2;sc=C.State(rp,absent=(5,))
          leaf(sc,[K,O]);n+=1
        j+=1
       assert set(legal)==set(map(int,branch['children']))
    h+=1
   assert set(live)==set(map(int,w['children']))
 assert seen==set(book);print('PASS (19,222) entire first 16 by preceding Thirds union; final leaves',n,'ECPP',len(book))
if __name__=='__main__':main()