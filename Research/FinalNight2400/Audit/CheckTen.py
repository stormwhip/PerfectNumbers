"""Independent C10 null inventory and exact gain/tail tree walk. Shares only base price enumerator and prime certification with primary replay."""
from pathlib import Path
from fractions import Fraction as F
from functools import cache
from math import prod,gcd
import gzip,json,sys,time
H=Path(__file__).resolve().parent;T=H.parent/'Ten';R=H.parents[1];sys.path.insert(0,str(T))
import PriceCore,Weighted
start=time.perf_counter();B=10**2400
C10=json.loads(gzip.decompress((R/'Night2400/C10/EulerF1.json.gz').read_bytes())); q=C10['pivot']; t=C10['tree']['q']
front=[(C10['tree'],((19,58),(q,1)))];opens=set()
while front:
 n,path=front.pop()
 if n is None:opens.add(path);continue
 if n['type']=='split':front.extend((c,path+((n['q'],int(e)),)) for e,c in n['cases'].items())
 else:assert n['type'] in ('forest','price')
two=[i for i in opens if i[2]==(t,2)];assert len(two)==2 and set(r[3:] for r in two)=={((172900527934963165844668988041369220224337976000897153058459631342970404239133047,2),(7627802356190118487344916013429102813353772289568699,k)) for k in (2,4)}
assert prod(sum(F(1,p**j) for j in range(e+1)) for p,e in ((3,4),(7,2),(13,2),(19,2),(61,2)))==2+F(14033,738283)
assert tuple(((19,58),(q,1),(t,10))) in opens
remaining=opens-set(two)-{((19,58),(q,1),(t,10))};assert len(remaining)==8
for index in range(3,11):
 weighted=index in (3,9,10); z=json.loads((T/(('Weight' if weighted else 'Tree')+str(index)+'.json')).read_bytes());P=tuple(map(tuple,z['path']));remaining.remove(P)
 V,targets,caps,exc=(Weighted if weighted else PriceCore).excludes(P,(),[x for x in range(len(P)) if x!=1]);W=[6 if weighted and p==3291622576015727423 else 2 for p in targets]
 S=prod((p**(k+1)-1)//(p-1) for p,k in P)//2; X=prod(p**k for p,k in P);C=S//gcd(X,S)
 powers=[p**(c+1) for p,c in zip(targets,caps)];M=prod(p**(c*w) for p,c,w in zip(targets,caps,W))
 assert V==F(X*M,prod(exc.values())) and gcd(X,C)==1
 def net(r,k):
  s=(r**(k+1)-1)//(r-1);ds=[gcd(m,s) for m in powers]
  if any(x==m for x,m in zip(ds,powers)):return None
  return F(r**k,prod(x**w for x,w in zip(ds,W)))
 @cache
 def least(r,k):
  best=None
  for e in range(k+(k%2),8000,2):
   if best is not None and F(r**e,M)>=best: return best
   if (n:=net(r,e)) is not None:best=n if best is None else min(n,best)
  raise AssertionError('no lower envelope stop')
 def vp(n,r):
  k=0
  while n%r==0:k+=1;n//=r
  return k
 def walk(node,paid,pending):
  spent=dict(P);spent.update(paid); assert len(spent)==len(P)+len(paid) and not set(pending)&set(spent)
  def price(pend):
   corr=prod(exc.get(r,1)*net(r,k) for r,k in paid.items());corr*=prod(exc.get(r,1)*least(r,h) for r,h in pend.items());return V*corr
  if node is True:assert price(pending)>B;return
  r=node['q'];h=pending[r]; unseen=dict(pending);del unseen[r]
  es=sorted(map(int,node['cases']));tail=h+h%2+2*len(es);assert es==list(range(h+h%2,tail,2))
  assert price({**unseen,r:tail})>B
  for k in es:
   cn=node['cases'][str(k)];n=net(r,k)
   if n is None: assert cn=='conflict';continue
   added,child=cn; s=(r**(k+1)-1)//(r-1);assert len(set(added))==len(added) and all(s%a==0 for a in added) and not (set(added)&(set(pending)|set(spent)))
   walk(child,{**paid,r:k},{**unseen,**dict.fromkeys(added,1)})
 roots=z['roots'];assert len(set(roots))==len(roots) and all(C%r==0 for r in roots);walk(z['tree'],{},{r:vp(C,r) for r in roots}); print('PASS net tree',index,flush=True)
assert not remaining;print('PASS: disjoint 2+8+1 null inventory and eight forced-price certificates,',round(time.perf_counter()-start,3),'s',flush=True)
