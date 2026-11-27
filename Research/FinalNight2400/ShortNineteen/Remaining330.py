"""At (19,330) first two and second two only two sister exponents remain."""
import sys,gzip,json
from fractions import Fraction
from math import prod
from pathlib import Path
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from ExactTwo import C,B,Q,R,L,Root
from Ab330 import verify,book as abbook

def main():
 t=Q[330];r=R[330];a=L;pre=[(19,330),(t,2),(r,2)];s=C.State(pre);obj=json.loads(gzip.decompress((H/'Remaining330.json.gz').read_bytes()));book=obj['ecpp'];used=set();certs={t:'PivotECPP.json',r:'Split8ECPP.json'}
 def prime(n):
  a0=n
  if n>=2**64:
   if str(n) in book:ch=book[str(n)];used.add(str(n))
   elif n==a:
    fs=[2,2,2,2,3,7,7,7,619,2347,157823,143329732348247561];assert prod(fs)==n-1 and all(C.pc.prime64(k)for k in fs);from math import gcd
    assert any(pow(b,n-1,n)==1 and all(gcd(pow(b,(n-1)//k,n)-1,n)==1 for k in set(fs)) for b in range(2,100));return True
   else:ch=json.loads((Root/'Night2400/C2'/certs[n]).read_bytes())
   for rr in ch:assert rr[0]==a0;a0=C.pc.level(*rr)
  assert C.pc.prime64(a0);return True
 assert all(prime(p) for p,h in pre) and prime(a) and C.sigma(t,2)%a==0 and C.sigma(t,2)%r==0 and C.sigma(19,330)%t==0
 c=C.valuation(s.D,a);j=c;live=[]
 while s.base//a**c*a**j<=B:
  if s.possible(a,j,c):
   ss=C.State(pre+[(a,j)])
   if not ss.conflict and ss.base<=B and prod(C.sigma(p,h) for p,h in ss.rows.items())<=2*ss.X:live.append(j)
  j+=1
 assert set(live)=={1,2,4,5,6,8,9,10,12,13,14,16,17}
 for fn in H.glob('Ab330Book*.json.gz'):abbook.update(json.loads(gzip.decompress(fn.read_bytes())))
 verify(5) # exact sister fourth power; the verified abundance tree has one leaf
 for k,(roots,O,bad) in obj['cases'].items():
  g=int(k);P=pre+[(a,g)];st=C.State(P)
  assert all(prime(b) and st.D%b==0 for b in roots)
  if bad:
   def I(b,h):return Fraction(C.sigma(b,h),b**h)
   from Ab330 import nextf
   d=set()
   while True:
    e0={b:C.valuation(st.D,b) for b in roots};even={b:nextf(b,v,tuple(sorted(d)),False) for b,v in e0.items()};assert all(x is not None for x in even.values())
    base=prod(I(q,h) for q,h in P)*prod(I(b,h) for b,h in even.items());lower=base
    if not st.fixed_euler:
     for b in roots:
      if b%4!=1:continue
      i=nextf(b,e0[b],tuple(sorted(d)),True)
      if i is not None:lower=min(lower,base/I(b,even[b])*I(b,i))
    new={p for p in bad if p not in d and p not in st.rows and p not in roots and prime(p) and lower*I(p,1 if not st.fixed_euler and p%4==1 else 2)>2}
    if not new:break
    d|=new
   assert set(bad)==d
  st=C.State(P,(),tuple(bad));C.validate_forest(st,roots,O,128,prime);assert C.Forest(st,roots,O,128).lower()[0]>B
 assert used==set(book) and set(map(int,obj['cases']))|{1,4,6}==set(live)
 print('PASS (19,330) r^2 secondary sister',a,'raw tail',j,'only [1,6] remain; large labels',len(book))
if __name__=='__main__':main()
