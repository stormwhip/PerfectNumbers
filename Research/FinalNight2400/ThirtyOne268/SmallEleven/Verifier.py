from pathlib import Path
import sys,gzip,json,importlib.util
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Kernel import *
from collections import Counter
from fractions import Fraction

def dom(r,z):
 s=C.State(r);v=val(s.D,z);assert v and z not in s.rows and z not in s.bad;h=v;cs={}
 while s.base//z**v*z**h<=B:
  if s.possible(z,h,v):
   new=r+[(z,h)];u=C.State(new)
   if not u.conflict and u.base<=B and prod(sigma(q,k) for q,k in new)<=2*u.X:cs[str(h)]=new
  h+=1
 return cs,h

def square(row):
 s=C.State(row);blocks=[C.nonsupport(C.sig_odd(z,h),s.X) for z,h in row];ls=[]
 for i,v in enumerate(blocks):
  for j,x in enumerate(blocks):
   if i!=j:v=C.nonsupport(v,x)
  if isqrt(v)**2!=v:ls.append(next((n for n in range(3,1000,2) if v%n==0),1001))
 return s.base*prod(sorted(ls) if s.fixed_euler else sorted(ls)[:-1])>B

def run(partial=False):
 assert __debug__;g=json.loads(gzip.decompress((H/'Forest.json.gz').read_bytes()));book=json.loads(gzip.decompress((H/'Primes.json.gz').read_bytes()));seen=set();S=Counter();c9=R/'Night2400/C9/Verify.py';sp=importlib.util.spec_from_file_location('frozenC9',c9);hist=importlib.util.module_from_spec(sp);sp.loader.exec_module(hist);assert hist.KEY==(p,e)==(11,12) and hist.Q==t and hist.HOLES==(36,44,52,60,100,164,172,180,188);hist.verify()
 @cache
 def prime(q):
  assert type(q)==int and q>2;y=q
  if y>=2**64:
   seen.add(str(q))
   for r in book[str(q)]:assert r[0]==y;y=C.pc.level(*r)
  assert C.pc.prime64(y);return True
 assert prime(p) and prime(t) and val(sigma(p,e),t)==1
 def walk(row,node,mask=0):
  yes={z for i,z in enumerate(C.ORDER)if mask>>i&1} if mask else set();no=set(C.ORDER)-yes if mask else {19,7};s=C.State(row,yes,no);s.bad=tuple(set(s.bad)|{z for z,h in row if s.S%z**h==0});mode=node['type'];S[mode]+=1
  if mode=='open':assert partial;return 1
  if mode=='c9':assert row in ([P[0],(t,4)],[P[0],(t,5)]);return 0
  if mode=='split':
   q=node['q'];assert prime(q);cs,tail=dom(row,q);assert set(cs)==set(node['cases']);return sum(walk(cs[k],v,mask) for k,v in node['cases'].items())
  if mode=='masks':
   assert row[1][1]==2 and not mask and set(node['cases'])==set(map(str,hist.HOLES));return sum(walk(row,v,int(m))for m,v in node['cases'].items())
  if mode=='square':assert square(row);return 0
  ks=node['roots'];assert len(set(ks))==len(ks) and all(prime(q) and q not in s.rows and (s.D%q==0 or q in yes) for q in ks)
  if mode=='conflict':assert s.conflict or set(ks)&set(s.bad);return 0
  assert not s.conflict and not set(ks)&set(s.bad)
  if mode=='forest':
   o=node['owners'];h=node['head'];C.validate_forest(s,ks,o,h,prime);assert C.Forest(s,ks,o,h).lower()[0]>B
  elif mode=='abun':
   a=Fraction(prod(sigma(q,h) for q,h in row),s.X);save=[Fraction(1)]
   for z in ks:
    v=max(1,val(s.D,z));h=v+v%2
    while not C.permitted(z,h,s.bad):h+=2
    unit=Fraction(sigma(z,h),z**h);a*=unit
    if not s.fixed_euler and C.euler(z,s.bad):
     h=v+(1-v)%4
     while not C.permitted(z,h,s.bad):h+=4
     save.append(Fraction(sigma(z,h),z**h)/unit)
   assert a*min(save)>2
  else:assert mode=='price' and not windows(row,ks)
  return 0
 cs,tail=dom(P,t);assert g['q']==t and set(cs)==set(g['cases']) and len(cs)==77 and tail==252;open_={}
 for h,r in cs.items():
  n=walk(r,g['cases'][h]);print('first',h,'remaining',n,flush=True)
  if n:open_[h]=n
 assert seen==set(book);print('canonical 11^12, 77 firsts, remaining',open_,dict(S),'ECPP',len(book),flush=True);return open_
if __name__=='__main__':assert not run()
