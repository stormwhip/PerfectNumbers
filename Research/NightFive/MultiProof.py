"""Experimental recursive conditioned source with separate origin blocks, aggregate installed exponent accounting."""
from CondProof import *
from collections import Counter
from itertools import chain
class Scan:
 def __init__(self,e,ds,roots,sec,T=100000):
  self.e=e;self.ds=ds;self.ps=[p for p in I.sieve_primes(T) if p not in F];self.T=T;self.P=5**(e+1);self.A=(self.P-1)//4;self.root=list(map(int,roots[str(e)]));self.sec=sec;self.cache={};self.stats=Counter();self.first=[];self.used=set();self.seen={}
 def decomp(self,v,known):
  # Always trial-divide full prime list so any unrecognized source >T.
  return parts(v,known,self.ps)
 def visit(self,assigned,Vin,lev,lim):
  self.stats['nodes']+=1
  if self.stats['nodes']>lim:return False
  e=self.e;T=self.T;P=self.P;A=self.A;X=5**e;sig=A;bank=[A];known=self.root.copy();V=e;blocks=[]
  for r,f in assigned:
   self.used.add((r,f));x=r**f;w=(r*x-1)//(r-1);X*=x;sig*=w;bank.append(w);known +=list(map(int,self.sec.get(f'{r}:{f}',[])));tmp=w
   while tmp%5==0:V-=1;tmp//=5
   fac={1:r-1}
   for h in range(2,f+2):
    if (f+1)%h==0:fac[h]=(r**h-1)//math.prod(m for j,m in fac.items() if h%j==0)
   blocks.append((w,list(fac.values())[1:]))
  D=sig//math.gcd(sig,2*X)
  if X*D>B or math.gcd(D,X*math.prod(F))>1 or V<0:return True
  dc,u=self.decomp(D,known);Uroots=[math.gcd(u,w) for w in bank];split=math.prod(Uroots)==u and all(math.gcd(v,w)==1 for i,v in enumerate(Uroots) for w in Uroots[i+1:]);
  if not split:Uroots=[u]
  target=I.LN2_LO-abhi(5)-sum(abhi(z) for z,f in assigned)-sum(abhi(z) for z in dc)-I.ilog(u,T)*abhi(T);terms=[]
  for d in self.ds:
   L=min(4*lnlo(T),d.lam_p*LP) if u>1 else d.lam_p*LP;pm={z:point(z,k,False,L) for z,k in dc.items()};gift=(I.ilog(u,T)*L+3)//4;base=lnlo(X*D)+d.mu*target+d.const_no_target-sum(w for z,w in d.theta_map.items() if D%z==0 or X%z==0)-gift+sum(pm.values());terms.append((base,L,d,pm))
  failed=[]
  for s in Vin:
   if s>V:continue
   y=5**s;Q=2*y-1;lq=lnlo(Q);k=V-s
   if any(w>=((-w)%(2*y))*Q and any(z>=((-z)%(2*y))*Q for z in fac) for w,fac in blocks):failed.append(s);continue
   rows=[(b+L*k-(d.delta_q if Q<10**18 else min(d.delta_q,d.mu*((S+Q-2)//(Q-1)))),d,pm) for b,L,d,pm in terms]
   best=max(b for b,d,pm in rows)
   if best+lq>I.LN_B_HI:continue
   if 32*5**e*Q**6<243*B and not paid(s,V,terms,dc,u):failed.append(s);continue
   generic=2*lq+I.log_interval(2,3)[0];joint=lnlo(Q*Q*y)-lnhi(max(P,Q)*(P//y+4))
   if max(b+generic-d.delta_src for b,d,pm in rows)<=I.LN_B_HI:failed.append(s);continue
   if split:
    if any(z>1 and best+(max(joint,generic-lnhi(z)) if i==0 else generic-lnhi(z))<=I.LN_B_HI for i,z in enumerate(Uroots)):failed.append(s);continue
   elif u>1 and best+generic-lnhi(u)<=I.LN_B_HI:failed.append(s);continue
   for z,v in dc.items():
    g=2*((v+1)//2)
    while True:
     zz=(z**(g+1)-1)//(z-1);w=(-zz)%(2*y)
     if ok(z,g) and zz>=Q*w:break
     g+=2
    cr=0;tmp=A
    while tmp%z==0:cr+=1;tmp//=z
    price=lq+(g-v)*lnlo(z)
    if cr:price=max(price,joint-lnhi(z**(v-cr)))
    if max(b+price-pm[z] for b,d,pm in rows)<=I.LN_B_HI:failed.append(s);break
  if not failed:return True
  if not dc or len(assigned)>=lev:
   self.first.append([[(str(p),f) for p,f in assigned],min(failed),max(failed)]);return False
  r=max(dc);c=dc[r];u0=Uroots[:];self.stats['split']+=1
  # A secondary pivot could be the odd Euler prime unless ruled out at each still-live s.
  if A%r and r%4==1 and any(r>=2*5**s-1 and (r+1)%5**s==0 and (r+1)%5**(s+1)!=0 for s in failed):return False
  for f in range(2,I.ilog(B//(X*D//r**c),r)+1,2):
   if f<c or not ok(r,f):continue
   tag=f'{r}:{f}'
   if not self.visit(assigned+[(r,f)],failed,lev,lim):return False
  return True
 def run(self,lev,lim):
  standard=root(self.e,self.root,self.ps,self.T,self.ds)
  if not (standard['known'] and standard['rough'] and not standard['higher']):return False
  s=[s for lo,hi in standard['one'] for s in range(lo,hi+1)]
  return self.visit([],s,lev,lim)
