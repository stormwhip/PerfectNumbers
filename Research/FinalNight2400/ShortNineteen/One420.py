"""(19,420): exclude t^4, r^1. Disjoint length factors pay three incoming valuations."""
import sys
from pathlib import Path
from math import gcd,prod
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Price import price,B,sig,T;from High import bound
from ExactTwo import C,Root
import json
p=19;t=T[420];r=72688845161;a=12114807527

def main():
 # t primality via historical elliptic certificate, others via deterministic 64-bit arithmetic.
 n=t
 for rr in json.loads((Root/'Night2400/C/PivotECPP.json').read_bytes()):assert rr[0]==n;n=C.pc.level(*rr)
 assert C.pc.prime64(n) and all(C.pc.prime64(z) for z in [p,r,a,20899,22639]);assert sig(p,420)%t==sig(t,4)%r==(r+1)%a==0
 assert r%4==1 and a%4==3 and gcd((a-1)//2*a,p*(p-1)*t*(t-1))==1
 P=[(p,420),(t,4),(r,1)];base=C.State(P);c=C.valuation(base.D,a);j=c;done=[]
 # The first three units are enough for all j>=4; previous exclusions not assumed.
 while base.base//a**c*a**j<=B:
  if base.possible(a,j,c):
   rows=P+[(a,j)];ss=C.State(rows)
   if not ss.conflict and ss.base<=B:
    cap=j-C.valuation(ss.S,a);k=min(cap,3);loss,_=bound(k,22)
    # For a target cap k smaller than actual, only price min(v,k) per atom.
    # Original total of truncated valuations >= k, and a given base is charged only once.
    v,_,_,_=price(rows,[2,2,0,0]);bonus=1
    if j==2:
     for b in (20899,22639):
      assert sig(a,j)%b==0 and all(pow(b,(z-1)//(z-1 & (1-z)),z)!=1 for z in (p,t,a));bonus*=b**2
    assert v*a**(22*k)*bonus>B*loss,(j,k)
    done.append(j)
  j+=1
 assert done==list(range(2,48,2));print('PASS 420 first 4 second 1, 23 fourth-component possibilities at',a,'tail',j)
if __name__=='__main__':main()
