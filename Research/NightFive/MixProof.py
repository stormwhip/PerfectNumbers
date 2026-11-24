"""All-Euler exponent-independent conditional leaf. Enumerate assignment, then split missing branches; always retain possible odd Euler exponents."""
from RefundProof import *
from BankSieve import mentioned
from FastBound import size,pmin
from Tree import tail_table,PR
from bisect import bisect_right
class AnyTree:
 def __init__(self,e,roots,ds,secs):self.e=e;self.roots=roots;self.ds=ds;self.secs=secs;self.ps=I.sieve_primes(100000);self.nodes=0;self.first=None;self.used=set()
 def visit(self,x,depth,lim):
  self.nodes+=1
  if self.nodes>lim:return False
  B=10**2400;T=100000;X=math.prod(p**f for p,f in x);sig=math.prod((p**(f+1)-1)//(p-1) for p,f in x);D=sig//math.gcd(2*X,sig);eu=any(f%2 for p,f in x);V=self.e;ss=sig
  while ss%5==0:V-=1;ss//=5
  if X*D>B or math.gcd(D,X*math.prod(F))>1 or V<0:return True
  rs=set(self.roots);self.used.update(x)
  for p,f in x:rs.update(map(int,self.secs.get(f'{p}:{f}',[])))
  dc,u=parts(D,rs,set().union(*(mentioned((p**(f+1)-1)//(p-1),T) for p,f in x)));
  if size(X,u,dc,eu,B):return True
  full=X*u;rebate=1
  for z,v in dc.items():
   val,saving=pmin(z,v,eu);full*=val;rebate=max(rebate,saving)
  paid=full//rebate;n=I.ilog(u,T);zn=sig*(T+1)**n;zd=X*T**n
  for z in dc:zn*=z;zd*=z-1
  banned=tuple(z for z in PR[:20] if z in dc or z in {p for p,f in x});costs,av=tail_table(banned,eu);aa,ab=av[bisect_right(costs,B//paid)-1]
  if zn*aa<2*ab*zd:return True
  AB=I.LN2_LO-sum(abhi(p) for p,f in x)-sum(map(abhi,dc))-n*abhi(T);gone={p for p,f in x}|set(dc);terms=[];closed1=eu;closed2=eu or u==1;closed3=eu
  for d in self.ds:
   L=min(d.lam_p*LP,4*lnlo(T)) if u>1 else d.lam_p*LP;pm={p:point(p,c,False,L) for p,c in dc.items()};common=lnlo(X*D)+d.mu*AB+d.const_no_target+sum(d.refund(z) for z in gone if z!=5)-sum(th for z,th in d.theta_map.items() if z in gone or u%z==0)-(n*L+3)//4+sum(pm.values())+L*V
   if eu and common>I.LN_B_HI:return True
   even=[point(p,c,True,L)-pm[p] for p,c in dc.items() if point(p,c,True,L) is not None];closed1|=not even or common+min(even)>I.LN_B_HI
   # Euler on rough block; bound how many units can have been paid already; preserve high-a extra cost as max lower bound.
   h=min(V,I.ilog(u+1,5)+5);closed2|=common-L*h>I.LN_B_HI
   terms.append((common,L,d))
  if not eu and closed1 and closed2:
   # q outside assigned/forced. Stamp compatible s separately, use q^a price high or low. Cost high>=low - crude conventional upper.
   closed3=all(any(c-L*s+max(0,(s-1))*LP-d.delta_q>I.LN_B_HI for c,L,d in terms) for s in range(V+1))
   if closed3:return True
  if not dc or len(x)>depth:
   if self.first is None:self.first=[(str(p),f) for p,f in x]
   return False
  p=max(dc);c=dc[p];maxf=I.ilog(B//(X*(D//p**c)),p)
  for f in range(c,maxf+1):
   if (f%2 and (eu or p%4!=1 or f%4!=1)) or not ok(p,f):continue
   if not self.visit(x+[(p,f)],depth,lim):return False
  return True
