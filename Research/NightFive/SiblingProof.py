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
  # Any single fixed prime z among forced W can incur an excess globally paid exponent. For a given z^f, SHIFT only its stored point, keep the existing unknown-block and fixed-size ledger; no new sigma arithmetic.
  # Precompute ordinary/euler allowed lower costs for sibling pruning. Unknown Euler and external Euler remain separate when z is assigned even.
  sibling_cache={}
  def sibling(z,f):
   rr=f%2;v=dc[z];uf=0;tmp=(z**(f+1)-1)//(z-1)
   while tmp%5==0:tmp//=5;uf+=1
   if uf>V:return True
   a=b=False;bb=[]
   for common,L,d in terms:
    vp=point(z,v,False,L); cb=common-vp+(f-v)*lnlo(z)-L*uf
    if eu or rr:
     if cb>I.LN_B_HI:return True
    else:
     delta=[point(p,c,True,L)-point(p,c,False,L) for p,c in dc.items() if p!=z and point(p,c,True,L) is not None];a|=not delta or cb+min(delta)>I.LN_B_HI
     b|=u==1 or cb-L*min(V-uf,I.ilog(u+1,5)+5)>I.LN_B_HI;bb.append((cb,L,d))
   if not (eu or rr) and a and b:
    if all(any(cb-L*t+max(0,t-1)*LP-d.delta_q>I.LN_B_HI for cb,L,d in bb) for t in range(V-uf+1)):return True
   return False
  # Child size exact: sigma(r^f) > r^f, after gcd with exact product Y=X*r^f. New mandatory cost X*r^f*D_child >= X*r^f*D* sigma(r^f)/(D*r^c*2X...), standard global bound only. For improved parent prefilter retain actual gcd, not a heuristic divisor.
  # New D divides the multiplicative sigma; before exploring any candidate factors we may already reject from gcd consistency or raw size.
  def direct(z,f):
   t=z**f;hh=(z*t-1)//(z-1);child=X*t;SS=sig*hh;g=math.gcd(SS,2*child);dsub=SS//g
   return child*dsub>B or math.gcd(dsub,child*math.prod(F))>1
  if not dc or len(x)>depth:
   if self.first is None:self.first=[(str(p),f) for p,f in x]
   return False
  p=max(dc);c=dc[p];maxf=I.ilog(B//(X*(D//p**c)),p)
  for f in range(c,maxf+1):
   if (f%2 and (eu or p%4!=1 or f%4!=1)) or not ok(p,f):continue
   if direct(p,f) or sibling(p,f):continue
   if not self.visit(x+[(p,f)],depth,lim):return False
  return True
