"""Full S^4 child below the exact T^6 prefix by forced 5 and a new 218-bit J."""
from fractions import Fraction
from math import gcd,prod
from pathlib import Path
import sys,json,gzip
from functools import cache
H=Path(__file__).resolve().parent;R=H.parents[1];sys.path[:0]=[str(R/'Session20261126'),str(R/'Night2400/A')];from PivotCheck import C,B;from MaskedForest import exact_absence_bound
Q=16148168401;T=C.sigma(Q,12)//13;S=62936242392988051361;J=340522774902395416760792885639672290356455394594605085885851976071
def main():
 assert __debug__;z=json.load(gzip.open(H/'Four.json.gz'));seen=set();used=set()
 @cache
 def prime(n):
  if n<2**64:return C.pc.prime64(n)
  if str(n) in z['lucas']:
   used.add(str(n));g,fs=z['lucas'][str(n)];assert prod(int(u)**w for u,w in fs.items())==n-1 and pow(g,n-1,n)==1 and all(w>=1 and prime(int(u)) and gcd(pow(g,(n-1)//int(u),n)-1,n)==1 for u,w in fs.items());return True
  seen.add(str(n));k=n
  for row in z['ecpp'][str(n)]:assert row[0]==k;k=C.pc.level(*row)
  assert C.pc.prime64(k);return True
 assert all(prime(q) for q in [Q,T,S,J]);assert C.sigma(7,12)==Q and C.sigma(Q,12)==13*T and C.sigma(T,6)%S==0 and C.sigma(S,4)%J==0 and C.sigma(S,4)%5==0
 assert Fraction(C.sigma(7,12),7**12)*Fraction(13,9)*Fraction(6,5)>2
 rows=[(7,12),(Q,12),(T,6),(S,4)];s=C.State(rows,absent=(3,));c=C.valuation(s.D,J);assert c==1 and J%4==3 and set(s.bad)=={3,19};k=c;ds=[]
 while s.base//J**c*J**k<=B:
  if s.possible(J,k,c):
   u=C.State(rows+[(J,k)],absent=(3,))
   if not u.conflict and u.base<=B and prod(C.sigma(p,h) for p,h in u.rows.items())<=2*u.X:ds.append(k)
  k+=1
 assert ds==[2,4] and k==12 and set(z['nodes'])=={'2','4'}
 for e in ds:
  rs=rows+[(J,e)];u=C.State(rs,absent=(3,));rt,es,head=z['nodes'][str(e)];C.validate_forest(u,rt,es,head,prime);v=min(C.Forest(u,rt,es,head).lower()[0],exact_absence_bound(rs,rt,es,head,u.bad,B));assert v>B;print(e,'floor',len(str(v))-1,'strict',v>B,flush=True)
 assert set(z['ecpp'])==seen and set(z['lucas'])==used;print('PASS T^6 S^4 entire exact child')
if __name__=='__main__':main()
