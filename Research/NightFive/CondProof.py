"""Root-node Euler gap dual conditioned on one forced prime's exact exponent. Discovery version."""
from PaidCheck import *
from PaidSource import paid,lnhi

from functools import cache
# Base gap uses A=sigma(5^e). Do not erroneously apply 4C congruence to r|A' only.
def run(e,ds,cs,secondary,T=100000):
 ps=[r for r in I.sieve_primes(T) if r not in F];P=5**(e+1);pe=P//5;A=(P-1)//4;rs0=[int(v) for v in cs[str(e)]];dc,u=parts(A,rs0,ps);r=max(dc);c=dc[r];del dc[r]; Lmax=I.LN_B_HI
 out=[]
 # Only attempt root with largest known r forced ordinary; handle Euler instead by primary root known/rough outcomes.
 standard=root(e,rs0,ps,T,ds);assert standard['known'] and standard['rough'] and not standard['higher'];alive=[s for lo,hi in standard['one'] for s in range(lo,hi+1)]
 for f in range(2,I.ilog(B//pe,r)+1,2):
  if f<c or not ok(r,f):continue
  x=r**f;sig=(x*r-1)//(r-1);X=pe*x;D=A*sig//math.gcd(A*sig,2*X)
  if math.gcd(D,X*math.prod(F))>1:continue
  extras=[int(n) for n in secondary.get(f'{r}:{f}',[])];assert all(sig%n==0 for n in extras);d2,u2=parts(D,rs0+extras,ps);V=e;ss=sig
  while ss%5==0:ss//=5;V-=1
  if V<0 or X*D>B:continue
  target=I.LN2_LO-abhi(5)-abhi(r)-sum(abhi(z) for z in d2)-I.ilog(u2,T)*abhi(T);terms=[]
  for d in ds:
   L=min(4*lnlo(T),d.lam_p*LP) if u2>1 else d.lam_p*LP; pm={z:point(z,k,False,L) for z,k in d2.items()};gift=(I.ilog(u2,T)*L+3)//4
   base=lnlo(X*D)+d.mu*target+d.const_no_target-sum(w for z,w in d.theta_map.items() if D%z==0 or X%z==0)-gift+sum(pm.values());terms.append((base,L,d,pm))
  failed=[]
  for s in alive:
   if s>V:continue
   y=5**s;Q=2*y-1;lq=lnlo(Q);k=V-s
   # q may be newly in D. q does not divide A in still-open case, so if q|D then q|sig. Skip unless congruence of cofactor proves impossible.
   w=(-sig)%(2*y) if sig%2 else 0
   def has_fixed():
    dv={1:r-1}
    for h in range(2,f+2):
     if (f+1)%h:continue
     a=(r**h-1)//math.prod(v for i,v in dv.items() if h%i==0);dv[h]=a
     if a>=((-a)%(2*y))*Q:return True
    return False
   if sig>=w*Q and has_fixed():failed.append(s);continue
   rows=[]
   for base,L,d,pm in terms:
    dq=d.delta_q if Q<10**18 else min(d.delta_q,d.mu*((S+Q-2)//(Q-1)));rows.append((base+L*k-dq,d,pm))
   if max(b+lq for b,d,pm in rows)>Lmax:continue
   # q external to all fixed/forced blocks; exact r cannot emit. q's emitter may supply 5; price separately.
   if pe*32*Q**6<243*B and not paid(s,V,terms,d2,u2):failed.append(s);continue
   # zero-supply emitter. q | sigma(z^g) implies z^g>2Q/3. For any newly forced z^v with z|sigma(r^f), use the generic r^v budget bound rather than the root gap directly.
   den=max(P,Q)*(P//y+4);joint=lnlo(Q*Q*y)-lnhi(den);generic=2*lq+I.log_interval(2,3)[0];ext=max(b+generic-d.delta_src for b,d,pm in rows)
   if ext<=Lmax:failed.append(s);continue
   # Difference of root c and augmented v: price z^(g-v), not z^(g-c). Extra credit <= sigma(r^f), or its remaining unfactored part.
   unknownsig=parts(sig,rs0+extras,ps)[1];ur=max(b+max(generic-lnhi(u2),joint-lnhi(unknownsig)) for b,d,pm in rows) if u2>1 else 2*Lmax
   if ur<=Lmax:failed.append(s);continue
   for z,v in d2.items():
    g=2*((v+1)//2)
    while True:
     zz=(z**(g+1)-1)//(z-1);w=(-zz)%(2*y)
     if ok(z,g) and zz>=Q*w:break
     g+=2
    cr=dc.get(z,0);price=lq+(g-v)*lnlo(z)
    if cr:price=max(price,joint-lnhi(z**(v-cr)))
    if max(b+price-pm[z] for b,d,pm in rows)<=Lmax:failed.append(s);break
  if failed:out.append([f,min(failed),max(failed),len(failed)])
 return dict(e=e,r=str(r),closed=not out,failed=out)
