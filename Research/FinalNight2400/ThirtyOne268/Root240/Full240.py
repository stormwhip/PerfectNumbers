"""Seal honest conditional or full exact firsts; unknown markers are not exclusion evidence."""
from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Kernel import *
from collections import Counter

def domain(row,z):
 s=C.State(row);v=val(s.D,z);assert v and z not in s.rows and z not in s.bad;h=v;cs={}
 while s.base//z**v*z**h<=B:
  if s.possible(z,h,v):
   r=row+[(z,h)];ss=C.State(r)
   if not ss.conflict and ss.base<=B and prod(sigma(q,k)for q,k in r)<=2*ss.X:cs[str(h)]=r
  h+=1
 return cs,h

def square(row):
 s=C.State(row);blocks=[C.nonsupport(C.sig_odd(q,h),s.X) for q,h in row];assert prod(blocks)==s.D;ls=[]
 for i,v in enumerate(blocks):
  for j,z in enumerate(blocks):
   if i!=j:v=C.nonsupport(v,z)
  if isqrt(v)**2!=v:ls.append(next((x for x in range(3,1000,2) if v%x==0),1001))
 return s.base*prod(sorted(ls) if s.fixed_euler else sorted(ls)[:-1])>B

def run(only=()):
 assert __debug__;pack=json.loads(gzip.decompress((H/'Forest.json.gz').read_bytes()));book=json.loads(gzip.decompress((H/'Primes.json.gz').read_bytes()));seen=set();stats=Counter()
 @cache
 def prime(q):
  assert type(q)==int and q>2;y=q
  if y>=2**64:
   seen.add(str(q))
   for row in book[str(q)]:assert row[0]==y;y=C.pc.level(*row)
  assert C.pc.prime64(y);return True
 assert (p,e,t)==(31,240,4339) and C.ORDER[:C.ORDER.index(p)]==(19,7,11) and prime(p) and prime(t) and prime(241) and t-1==18*241 and val(sigma(p,e),t)==1
 def walk(row,node):
  s=C.State(row);assert not s.conflict;kind=node['type'];stats[kind]+=1
  if kind=='open':raise AssertionError('unproved endpoint')
  if kind=='high':
   from High82 import side,B72;assert prime(B72) and row==P+[(t,82),(B72,36)] and not side(row,B72);return 0
  if kind=='split':
   z=node['q'];assert prime(z);cs,_=domain(row,z);assert set(cs)==set(node['cases']);return sum(walk(r,node['cases'][h])for h,r in cs.items())
  if kind=='square':assert square(row);return 0
  k=node['roots'];assert len(k)==len(set(k)) and all(prime(z) and z not in s.rows and z not in s.bad and s.D%z==0 for z in k)
  if kind=='price':assert not windows(row,k);return 0
  assert kind=='forest';s.bad=tuple(set(s.bad)|{q for q,h in row if s.S%q**h==0});o=node['owners'];h=node['head'];C.validate_forest(s,k,o,h,prime);assert C.Forest(s,k,o,h).lower()[0]>B;return 0
 cs,tail=domain(P,t);assert pack['q']==t and len(cs)==62 and set(cs)==set(pack['cases']);bad={};good=[]
 for h,r in cs.items():
  if only and int(h) not in only:continue
  n=walk(r,pack['cases'][h]);
  if n:bad[int(h)]=n
  else:good.append(int(h))
  print('first',h,'unresolved',n,flush=True)
 if not only:assert seen==set(book)
 assert not bad;print('FULL exact canonical 31^240',len(good),'complete firsts, remaining',bad,'counts',stats,'tail',tail,flush=True);return bad
if __name__=='__main__':run(tuple(map(int,sys.argv[1:])))