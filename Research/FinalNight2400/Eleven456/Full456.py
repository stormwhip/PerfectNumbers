"""One canonical exact exponent 11^456; exhaustive forced-pivot tree with strict arithmetic cut leaves."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Aux6 import *
from collections import Counter

def domain(row,q):
 s=C.State(row);v=val(s.D,q);assert v>0 and q not in s.rows and q not in s.bad;h=v;cs={}
 while s.base//q**v*q**h<=B:
  if s.possible(q,h,v):
   r=row+[(q,h)];u=C.State(r)
   if not u.conflict and u.base<=B and prod(sigma(z,k) for z,k in r)<=2*u.X:cs[str(h)]=r
  h+=1
 return cs,h

def square(row):
 s=C.State(row);ss=[C.nonsupport(C.sig_odd(z,h),s.X) for z,h in row];assert prod(ss)==s.D;low=[]
 for i,x in enumerate(ss):
  for y in ss[:i]+ss[i+1:]:x=C.nonsupport(x,y)
  if isqrt(x)**2!=x:low.append(next((j for j in range(3,1000,2)if x%j==0),1001))
 low.sort();return s.base*prod(low if s.fixed_euler else low[:-1])>B

def run():
 assert __debug__;data=json.loads(gzip.decompress((H/'Forest.json.gz').read_bytes()));book=json.loads(gzip.decompress((H/'Primes.json.gz').read_bytes()));seen=set();stats=Counter()
 @cache
 def prime(q):
  assert type(q)==int and q>2;y=q
  if q>=2**64:
   seen.add(str(q))
   for r in book[str(q)]:assert r[0]==y;y=C.pc.level(*r)
  assert C.pc.prime64(y);return True
 assert prime(p) and prime(t) and prime(Z) and all(prime(x)for x in zf) and prime(457) and p==11 and e==456 and P==[(11,456)] and tuple(C.ORDER[:C.ORDER.index(p)])==(19,7) and C.valuation(sigma(p,e),t)==1 and t-1==4*9*5*457 and 3**8000>B
 assert all((t-1)%x==0 and C.pc.prime64(x) for x in (3,5,457));assert t>8000
 def walk(row,tree):
  mode=tree['type'];stats[mode]+=1;s=C.State(row);assert not s.conflict and s.base<=B
  if mode=='split':
   q=tree['q'];assert prime(q);cs,h=domain(row,q);assert set(cs)==set(tree['cases']),(row,q,h)
   for k,r in cs.items():walk(r,tree['cases'][k])
   return
  if mode=='square':assert square(row);return
  ks=tree['roots'];assert len(ks)==len(set(ks)) and all(prime(z) and z not in s.rows and z not in s.bad and s.D%z==0 for z in ks)
  if mode=='forest':
   # Saturation: p may be fixed and all available p units already emitted, hence no future forest row can emit p.
   s.bad=tuple(set(s.bad)|{z for z,h in row if s.S%z**h==0});o=tree['owners'];h=tree['head'];C.validate_forest(s,ks,o,h,prime);assert C.Forest(s,ks,o,h).lower()[0]>B
  elif mode=='price':assert not windows(row,ks)
  elif mode=='joint':assert test(row,ks,4)==0
  else:assert mode=='rprice' and Z in dict(row) and not gtest(row,ks)
 cs,tail=domain(P,t);assert data['q']==t and len(cs)==74 and set(cs)==set(data['cases']);print('root 11,456 first domain',len(cs),'tail',tail,flush=True)
 for k,r in cs.items():walk(r,data['cases'][k]);print('first PASS',k,flush=True)
 assert seen==set(book);print('FULL canonical 11^456: all 74 first valuations, leaf counts',dict(stats),'ECPP',len(book),flush=True)
if __name__=='__main__':run()
