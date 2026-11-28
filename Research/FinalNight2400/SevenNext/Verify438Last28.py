"""Add 27431^28 at exact 7^438 t^12 using an exact forced ordinary child."""
from pathlib import Path
import sys,gzip,json
from functools import cache
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Anchor438B import go,T,t,V,C,B
if __name__=='__main__':
 assert __debug__;V.prove_prime(t);data=json.load(gzip.open(H/'C438Last28.json.gz'));used=set();r=27431;h=28;fs=data['fs'];a=max(fs);rows=[(7,438),(t,12),(r,h)];s=C.State(rows);assert C.pc.prime64(r) and r-1==2*5*13*211 and not s.conflict
 @cache
 def prime(n):
  y=n
  if y>=2**64:
   used.add(str(n))
   for row in data['ecpp'][str(n)]:assert row[0]==y;y=C.pc.level(*row)
  return C.pc.prime64(y)
 assert all(prime(y) and C.sigma(r,h)%y==0 and s.D%y==0 for y in fs);assert a<2*T-1 and V.v(s.D,a)==1
 k=2;ds=[]
 while s.base//a*a**k<=B:
  u=C.State(rows+[(a,k)])
  if not u.conflict and u.base<=B and C.sigma(a,k)%t:
   ds.append(k);ff=data['children'][str(k)];assert all(prime(y) and u.D%y==0 and C.sigma(a,k)%y==0 for y in ff);ok,fail=go(h,sorted(set(fs)|set(ff)),a,k);assert ok,fail
  k+=2
 assert ds==[4,6] and used==set(data['ecpp']);print('PASS exact 27431^28, forced ordinary anchor',a,'live',ds,'first even size tail',k,flush=True)
