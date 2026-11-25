"""Independent integer replay of highest root-5 exponents; same verified input flow bank."""
from math import prod
import json
from LeafCheck import I,ln_low,lower_opt,block,max_ab,proved,sigma,H,Q,check
from DualTree import load_duals

def replay(e,rs,duals,T):
 B=10**2400;P=5**(e+1);X=P//5;A=(P-1)//4;res=A;D={}
 for r in set(rs+I.sieve_primes(T)):
  if not res%r:
   n=0
   while not res%r:res//=r;n+=1
   D[r]=n
 cand=[False, res==1];rows=[];mu_max=max(z.mu for z in duals);ln5=I.log_interval(5)[0];hg=I.ilog(res,T);ab=I.LN2_LO-max_ab(5)-sum(map(max_ab,D))-hg*max_ab(T)
 for z in duals:
  rate=z.lam_p*ln5 if res==1 else min(z.lam_p*ln5,4*ln_low(T));cost={r:lower_opt(r,n,False,rate) for r,n in D.items()};c=ln_low(X*A)+z.const_no_target+z.mu*ab-sum(v for r,v in z.theta_map.items() if A%r==0)-((rate*hg+3)//4)+sum(cost.values());h=min(e,e//2+I.ilog(I.MAX_EXPONENT+1,5),I.ilog(res+1,5)+I.ilog(I.MAX_EXPONENT+1,5));cand[1]|=c+rate*(e-h)>I.LN_B_HI
  vals=[c+rate*e-cost[r]+v for r,n in D.items() if (v:=lower_opt(r,n,True,rate)) is not None];cand[0]|=not vals or min(vals)>I.LN_B_HI;rows.append((c,rate,z,cost))
 if not all(cand):return False
 for s in range(e+1):
  y=5**s;q=max(5,2*y-1);k=e-s; L=ln_low(q);h=max(ln_low(3125),max(0,5*s-5)*ln5)
  def ded(z):return min(z.delta_q,z.mu*max_ab(q)) if q>I.SPECIAL_LIMIT else z.delta_q
  if max(c+rate*k+h-z.delta_q for c,rate,z,cost in rows)<=I.LN_B_HI:return False
  if max(c+rate*k+L-ded(z) for c,rate,z,cost in rows)>I.LN_B_HI:continue
  if s==0:return False
  if 32*X*q**6<243*B:
   if q<=I.MAX_EXPONENT+1:return False
   def hi(n):
    k=max(n.bit_length()-44,0);return I.log_interval((n>>k)+1)[1]+k*I.LN2_HI
   for j in range(1,min(I.ilog(I.MAX_EXPONENT+1,5),k)+1):
    normal=ln_low(q)+5**j*(ln_low(q)+I.log_interval(2,3)[0]);remain=k-j
    # Separate max over duals for each possible location of the emitter.
    def margin(c,rate,z):return c+rate*remain+normal-ded(z)
    if max(margin(c,rate,z)-z.delta_src for c,rate,z,cost in rows)<=I.LN_B_HI:return False
    if res>1 and max(margin(c,rate,z)-hi(res) for c,rate,z,cost in rows)<=I.LN_B_HI:return False
    for r,n in D.items():
     if max(margin(c,rate,z)-cost[r]-n*hi(r) for c,rate,z,cost in rows)<=I.LN_B_HI:return False
  den=max(P,q)*(P//y+4); sh=max(0,den.bit_length()-48);gap=ln_low(q*q*y)-I.log_interval((den>>sh)+1)[1]-sh*I.LN2_HI
  def test(price,r=None,ext=False):return max(c+rate*k+price-ded(z)-(z.delta_src if ext else cost.get(r,0)) for c,rate,z,cost in rows)>I.LN_B_HI
  if not test(2*L+I.log_interval(2,3)[0],ext=True):return False
  if res!=1 and not test(gap):return False
  for r,n in D.items():
   f=n
   while True:
     if f%2==0 and block(r,f):
      a=sigma(r,f);rem=(-a)%(2*y)
      if a>=rem*q:break
     f+=1
   if not test(max(gap,L+(f-n)*ln_low(r)),r=r):return False
 return True
