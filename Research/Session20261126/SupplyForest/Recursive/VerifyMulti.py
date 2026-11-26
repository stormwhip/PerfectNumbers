"""Independent finite pivot-exponent domain and per-leaf arithmetic. Imports only archived primality and blanket bounds from sibling VerifyCut.py."""
from pathlib import Path
from importlib.util import spec_from_file_location,module_from_spec
import sys,gzip,json,math
from fractions import Fraction as Fr
from functools import cache
H=Path(__file__).resolve().parent
sp=spec_from_file_location('cut',next(q for q in (H/'VerifyCut.py',H.parent/'VerifyCut.py') if q.is_file()));a=module_from_spec(sp);sp.loader.exec_module(a)
T,B,PC=a.T,a.B,a.PC
if not __debug__:raise RuntimeError('assertions required')
@cache
def sigma(z,h):return (z**(h+1)-1)//(z-1)
def peel(n,S):
 while (d:=math.gcd(n,S))>1:n//=d
 return n
def ready(z,f,ban):return all(((f+1)%b if z%b==1 else pow(z,f+1,b)!=1) for b in ban)
@cache
def blanket(p,e):return a.blanket(p,e,T.kappa(p))

def model(p,e,fixed,K,owners,cap,fixedbudget=False,abundance=False,rock=0,sourceforest=None):
 k=T.kappa(p);t,f=next(((q,j) for q,j in fixed if j%2),fixed[0]);A=sigma(p,e);Sp=math.prod(sigma(q,j)//(1+j%2) for q,j in fixed);X=p**e*math.prod(q**j for q,j in fixed);C=peel(A*Sp,X);ban=T.forbidden(p);U,D=blanket(p,e);rest=math.prod(max(1,Fr(q**j,p**(k*a.val(sigma(q,j),p)))) for q,j in fixed if q!=t);base=Fr(p**((k+1)*e)*rest*max(1,Fr(t**f,p**(k*a.val(sigma(t,f),p)))),U);Z=X*C*math.prod(owners);kids={q:[] for q in [*K,*owners]};h={q:a.val(C,q) for q in K};C0=C//math.prod(q**j for q,j in h.items());Y=1;Q=1
 assert type(abundance)==bool
 if abundance:
  sigmafixed=A*math.prod(sigma(z,j) for z,j in fixed);reg=Fr(sigmafixed,X);savings=Fr(1)
  for z,j in h.items():
   j0=j+(j%2);term=Fr(sigma(z,j0),z**j0);reg*=term
   if not any(u%2 for _,u in fixed) and z%4==1:
    j1=j+((1-j)%4);savings=min(savings,Fr(sigma(z,j1),z**j1)/term)
  if reg*savings>2:return 'abundance'
 mods=[q**(j-a.val(A*Sp,q)+1) for q,j in [(p,e),*fixed]] if fixedbudget else [];assert type(fixedbudget)==bool
 for q,z in owners.items():kids[z].append(q)
 @cache
 def props(z,f):
  n=sigma(z,f)//(1+f%2);return a.val(n,p),peel(n,Z),tuple((q,a.val(n,q)) for q in kids[z] if n%q==0)
 def qfree(n,limit=16):
  if n<Q:return True
  T0=4*Y;b=(n*pow(Q,-1,T0))%T0 or T0;mx=n//Q
  if b>mx:return True
  if (mx-b)//T0>=limit:return False
  ok=all(n%u for u in range(b,mx+1,T0))
  if ok and limit>16 and (mx-b)//T0>=16:print('extended_exact_cofactor',p,e,fixed,'s',s,'first',b,'step',T0,'upper',mx,'count',(mx-b)//T0+1,flush=True)
  return ok
 small=min([1,*[Fr(z,p**(k*a.val(z+1,p))) for z in kids if z%4==1]])
 def layer(mode):
  mass=mode in ('mass','nomassEuler','mix');weighted=mode=='mix';allow=mode in ('mass','high','one','mix')
  @cache
  def node(z,need,loc):
   if loc=='maybe':return min(node(z,need,'under'),node(z,need,'self')) if not weighted and allow and z%4==1 and all((z+1)%b for b in ban) else node(z,need,'under')
   at=loc=='self';under=loc=='under';o=T.multiplicative_order(z,p);t0=a.val(z**o-1,p) if o>1 else 0;j=need+((1-need)%4 if at else need%2);step=4 if at else 2
   if at and (mode=='one' and j!=1 or fixedbudget and any(((z+1)//2)%m==0 for m in mods)):return None # sigma(z) divides every odd-exponent sigma
   if at and mode=='high' and j==1:j=5
   best=None;cnt=0
   while True:
    powz=z**j;inc=powz**(k-1) if weighted else 1;cheap=Fr(powz,p**(k*t0)*(j+1)**k);lower=inc*max(1,cheap) if weighted else powz if mass else cheap*(small if mode=='one' else 1);mono=z**step*(j+1)**k>=(j+step+1)**k
    if mass and cnt>=cap and (not weighted or mono):return min(lower,best) if best is not None else lower
    if best is not None and lower>=best and (mono or mass and not weighted):return best
    if fixedbudget and best is None and lower>10**12000 and (mono or mass and not weighted):return 10**12000 # conservative truncation, including a forbidden whole parity class
    if ready(z,j,ban) and all((sigma(z,j)//(1+j%2))%m for m in mods):
     b,rem,ch=props(z,j);premium=max(1,Fr(powz,p**(k*b)));value=(powz*rem)**(k-1)*premium if weighted else powz*rem if mass else Fr(powz,p**(k*b)) if at and mode=='one' else premium;disc=Fr(1)
     if weighted and under and not qfree(rem):disc=Fr(rem*pow(Q,-1,4*Y)%(4*Y) or 4*Y,rem)**(k-1)
     for y,n in ch:
      u=node(y,n,'no');value*=u
      if under:
       v=maybe(y,n);disc=min(disc,Fr(v,u))
     v=value*disc;best=v if best is None else min(v,best);cnt+=1
    if at and mode=='one':return best
    j+=step
  def maybe(z,n):
   under=node(z,n,'under')
   if weighted or not allow or z%4!=1 or any((z+1)%b==0 for b in ban):return under
   x=node(z,n,'self');return min(under,x) if x is not None else under
  rs={z:node(z,j,'no') for z,j in h.items()};v=math.prod(rs.values());d=min([Fr(1),*[Fr(maybe(z,j),rs[z]) for z,j in h.items()]]) if allow else 1;node.cache_clear();return v*d
 if rock:
  asp=spec_from_file_location('br',H/'RoughVerify.py');br=module_from_spec(asp);asp.loader.exec_module(br);mplus,vplus,mone,vone=br.ledger(p,e,fixed,C0,rock)
 else:mplus=vplus=mone=vone=1
 if X*C0*(mplus if f%2 else mone)*layer('nomassEuler' if f%2 else 'mass')>B:return 'mass'
 if f%2:
  if f==1:assert Fr(vplus*p**((k+1)*e)*rest*t*layer('ordinary'),U*p**(k*a.val(sigma(t,f),p)))>B
  else:assert vplus*base*layer('ordinary')>B*D
  return 'pivot-Euler'
 assert vone*base*layer('high')>B*D,'high';assert vplus*base*layer('one')>B,'active Euler';v=vone*base*layer('ordinary');s=next((s for s in range(e+1) if v*max(1,2*p**s-1)<=B*p**(k*s)),e+1)
 if s>e:return 'valuation'
 assert s>0 and p%4==3,'unverified internal A';Y=p**s;Q=2*Y-1;assert all(q%4!=1 or a.val(q+1,p)<s for q in [*[z for z,j in fixed],*kids]);
 if sourceforest is None:assert all(qfree(peel(sigma(z,j),X),33) for z,j in fixed),('unverified internal pivot sigma',fixed,s)
 else:
  sys.path.insert(0,str(a.R/'NightMerge'));import LatticeLeaf as ll
  assert len(sourceforest)==len(fixed)
  for (z,j),rows in zip(fixed,sourceforest):
   N=peel(sigma(z,j),X);T0=4*Y;lo=Q;hi=N//(N*pow(Q,-1,T0)%T0)
   for l,upper,w in rows:
    assert l==lo and l<=upper<=hi and ll.verify(N,1,Q,T0,l,upper,w);lo=upper+1
   assert lo>hi,'incomplete internal emitter cofactor intervals'
 assert (X*C0*mplus)**(k-1)*vplus*base*Fr(Q,Y)**k*layer('mix')>B**k,'mixed';return 'mixed'
