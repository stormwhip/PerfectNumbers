"""Independent replay with certificate-selected pivot among compulsorily present unassigned primes. Prime and edge validation is performed by Verify.py before calling."""
from functools import cache
from bisect import bisect_right
from math import prod,gcd
import Verify as V
E=V.E;B=E.B

def check(row):
 e=row['e'];root=set(map(int,row['root']));edges={};pivs=row.get('pivots',{});seen=set();nodes=0;md=0
 for r,f,q in row['edges']:edges.setdefault((int(r),f),set()).add(int(q))
 def visit(ex):
  nonlocal nodes,md
  nodes+=1;md=max(md,len(ex)-1);V.require(nodes<=60000 and len(ex)<=60,'pivot safety cap');X=prod(z**f for z,f in ex);S=prod(E.sigma(z,f) for z,f in ex);D=S//gcd(2*X,S);eu=any(f&1 for z,f in ex)
  if S>2*X or X*D>B or gcd(D,X*prod(E.BANNED))!=1:return True
  pool=root|set(E.SM)
  for sf in ex:pool.update(edges.get(sf,()))
  m=X;u=D;ds={};saves={}
  for z in pool:
   if u%z:continue
   c=E.val(u,z);u//=z**c;g=E.lower(z,c,False);o=None if eu else E.lower(z,c,True);ds[z]=g,o;m*=z**g
   if o is not None:saves[z]=z**max(g-o,0)
  m*=u;save=max([1,*saves.values()]);room=B*save//m
  if room==0:return True
  k=E.ilog(u,2001);ps=tuple(z for z in E.PR[:18] if z in ds or X%z==0);sx,ab=E.tails(ps,eu);an,ad=ab[bisect_right(sx,room)-1]
  if S*an*2001**k*prod(ds)<2*X*ad*2000**k*prod(z-1 for z in ds):return True
  k=e-E.val(S,3);V.require(k>=0,'surplus unclosed')
  for cut in (12,17,22,27):
   loss=E.small_discount(cut)+sum(E.discount(z,f,cut) for z,(f,o) in ds.items())+(u.bit_length() if u>1 else 0);rhs=B<<loss
   if eu and m<<(cut*k)>rhs:return True
   if not eu and m*3**k>rhs*u and all(o is None or (m*z**o//z**f)<<(cut*max(0,k-7-(E.val(z+1,3) if z%3==2 else 0)))>rhs for z,(f,o) in ds.items()):return True
  if not ds:return False
  path=';'.join(f'{z}:{f}' for z,f in ex);r=int(pivs.get(path,max(ds)));V.require(r in ds,'pivot not compelled');seen.add(path);f,o=ds[r];fixed=m//r**f
  for start,step,cap in [(f,2,B*max([1]+[s for z,s in saves.items() if z!=r]))]+([] if o is None else [(o,4,B)]):
   j=start
   while fixed*r**j<=cap:
    if E.legal(r,j) and not visit(ex+[(r,j)]):return False
    j+=step
  return True
 V.require(visit([(3,e)]),'unproved dynamic tree');V.require(not set(pivs)-seen or row.get('relaxed_unused') is True,'unvisited declared pivots');return {'nodes':nodes,'depth':md,'user_pivots':len(set(pivs)&seen)}
