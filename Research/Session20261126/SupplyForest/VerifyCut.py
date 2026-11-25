"""Cold replay, no discovery imports, no floating point or external mathematics packages. Use -I -S -B (not -O)."""
import sys,gzip,json,math
from pathlib import Path
from fractions import Fraction as F
from functools import cache
H=Path(__file__).resolve().parent
R=Path(sys.argv[1]).resolve() if len(sys.argv)>1 else next((a for a in H.parents if (a/'TeichmullerValuation/VerifyTeichmullerValuation2400.py').is_file()),None)
if R is None:raise RuntimeError('provide the pinned Research directory as the first argument')
sys.path[:0]=[str(R/'TeichmullerValuation'),str(R/'RootFiveNext')];import VerifyTeichmullerValuation2400 as T,PrimeCheck as PC
B=10**2400
if not __debug__:raise RuntimeError('never run optimized')
def val(n,p):
 v=0
 while n%p==0:v+=1;n//=p
 return v

def floors(n,m,a,b):
 # Standard Euclidean floor-sum, permits signed b.
 out=0
 while True:
  ka,a=divmod(a,m);kb,b=divmod(b,m);out+=ka*n*(n-1)//2+kb*n
  if a*n+b<m:return out
  n,b=divmod(a*n+b,m);m,a=a,m

def internal(C,T0):
 t=4*T0;a=2*T0-1;b=C*pow(a,-1,t)%t;assert b and math.gcd(C,t)==1
 # q=a+ti and u=b+tj: b*i + a*j == (C-a*b)/t mod t.
 m=-b*pow(a,-1,t)%t;v=((C-a*b)//t)*pow(a,-1,t)%t;lo=a;top=C//b;num=0
 while lo<=top:
  hi=min(top,4*lo);i=(lo-a+t-1)//t;I=(hi-a)//t;j=((C+hi-1)//hi-b+t-1)//t;J=(C//lo-b)//t;n=I-i+1
  if n>0 and J>=j:
   # Number of j in [j,J] congruent to m*i+v summed over i.
   ct=floors(n,t,-m,J-v-m*i)-floors(n,t,-m,j-1-v-m*i)
   assert ct==0,('internal bin unresolved',lo,hi,ct)
  num+=1;lo=hi+1
 return num

def blanket(p,e,k):
 pr=T.Profile(p,e);assert T.check_lemmas(p);U=pr.U(e);D=pr.D(e)
 if k==2:return U,D
 assert p==11 and k==4
 # At order 1, or order 2 (f>=5), q^f >= p^(4k_q). At other orders use Hensel digit-by-digit and include even composite odd candidates for a conservative D.
 D=F(1)
 for a in range(2,p-1):
  o=T.multiplicative_order(a,p)
  if o%4==0:continue
  fm=T.fmin_euler(o);assert 3**(o*p-1-fm)>=p**k
  x=a;w=p
  for t0 in range(1,e+1):
   y=x+w*((-((pow(x,o,w*p)-1)//w)*pow(o*pow(x,o-1,p),-1,p))%p)
   if x!=y and x%4==1 and x not in T.forbidden(p):D=max(D,F(w**k,x**fm))
   x=y;w*=p
 return U,D

def verify(path):
 d=json.loads(gzip.decompress(path.read_bytes()));assert d['schema']=='teich-cut-1';r=d['row'];p,e=r['p'],r['e'];assert p in (7,11,13,19,31) and e%2==0 and e>0;k=T.kappa(p);A=T.sigma(p,e);pe=p**e;ban=T.forbidden(p);K=set(r['roots']);edges=r['owners'];par=dict(edges);V=set(par)|K;assert len(K)==len(r['roots']) and len(par)==len(edges) and not K.intersection(par) and all(A%q==0 for q in K) and all(p*A%q for q in par)
 for z in V:
  assert z>2 and z!=p
  cur=z
  if z>=2**64:
   for row in d['ecpp'][str(z)]:assert row[0]==cur;cur=PC.level(*row)
  assert PC.prime64(cur)
 ch={z:[] for z in V};seen=set();stk=list(K)
 for y,z in edges:ch[z].append(y)
 while stk:
  z=stk.pop();assert z not in seen;seen.add(z);stk.extend(ch[z])
 assert seen==V
 c={z:val(A,z) for z in K};C=A//math.prod(z**c[z] for z in K);Z=p*A*math.prod(par);cut=r['cut'];s0=r['small'];assert 1<=s0<=cut<=e;Q=2*p**cut-1;Y=p**cut;cap=r['head'];assert 1<=cap<=512
 U,D=blanket(p,e,k);budget=pe**(k+1);weighted=r.get('weighted',False);assert type(weighted)==bool;power=k if weighted else 1;wt=power-1 if weighted else 1
 @cache
 def options(z,f,mass):
  n=T.sigma(z,f);b=val(n,p);rem=n//(2 if f%2 else 1);ac=tuple((y,val(rem,y)) for y in ch[z] if rem%y==0)
  if mass:
   while (g:=math.gcd(rem,Z))!=1:rem//=g
  return b,rem,ac
 def emitter(rem):
  # If q>=Q and q == 2Y-1 mod 4Y then the positive cofactor must lie in this class.
  if rem<Q:return False
  t=4*Y;v=rem*pow(Q,-1,t)%t or t;M=rem//Q
  if v>M:return False
  if M-v<16*t:return any(rem%h==0 for h in range(v,M+1,t))
  return True
 def combine(pairs,lost=None):
  a=math.prod(x for x,y in pairs);w=min([F(1),*[F(y,x) for x,y in pairs],*([lost] if lost else [])]);return a,a*w
 @cache
 def solve(z,h,mass):
  # Pair: ordinary; with zero or one allowed exceptional location. No separate choice of location is assumed in the same subtree twice.
  o=T.multiplicative_order(z,p);t=val(z**o-1,p) if o>1 else 0;res=[None,None]
  for odd in ([False,True] if not mass and z%4==1 and all((z+1)%b for b in ban) else [False]):
   f=h+((1-h)%4 if odd else h%2);step=4 if odd else 2;n=0
   while True:
    low=z**f if mass else F(z**f,p**(k*t)*(f+1)**k)
    mono=z**step*(f+1)**k>=(f+step+1)**k
    if mass and weighted:low=(z**f)**wt*max(1,F(z**f,p**(k*t)*(f+1)**k))
    if mass and n>=cap and (not weighted or mono):
     res=[min(v,low) if v is not None else low for v in res];break
    relevant=res[1:] if odd else res
    if not (odd and f==1) and all(v is not None and low>=v for v in relevant) and ((mass and not weighted) or mono):break
    if all(((f+1)%b if z%b==1 else pow(z,f+1,b)!=1) for b in ban):
     b,rem,sub=options(z,f,mass);n+=1
     if mass:
       unit=(z**f*rem)**wt*(max(1,F(z**f,p**(k*b))) if weighted else 1)
       ref=(rem*pow(Q,-1,4*Y)%(4*Y) or 4*Y) if weighted else 1
       loss=F(ref,rem)**wt if emitter(rem) else None
     else:unit=1 if odd and f==1 else max(1,F(z**f,p**(k*b)));loss=None
     a,w=combine([solve(y,h1,mass) for y,h1 in sub],loss)
     if odd:res[1]=unit*a if res[1] is None else min(res[1],unit*a)
     else:
      for j,v in enumerate((a,w)):res[j]=unit*v if res[j] is None else min(res[j],unit*v)
    f+=step
  return tuple(res)
 v,vv=combine([solve(z,c[z],False) for z in K]);assert budget*vv>B*U*D,'high Euler'
 for s in range(cut):
  w=vv if s<s0 else v;assert budget*w*max(1,2*p**s-1)>B*U*p**(k*s),('small exponent',s)
 assert all(z%4!=1 or val(z+1,p)<s0 for z in V),'Euler possibly inside active tree'
 bins=0
 if 'leaves' in r:
  sys.path.insert(0,str(R/'NightMerge'));import LatticeLeaf
  n=e+1;assert p%4==1 and PC.prime64(n) and math.gcd(C,4*Y*n)==1 and math.gcd(n,4*Y)==1
  mod=4*Y*n;z=Q+4*Y*((1-Q)*pow(4*Y,-1,n)%n);lo=z;hi=C//(C*pow(z,-1,mod)%mod)
  for l,h,w in r['leaves']:
   assert l==lo and l<=h<=hi and LatticeLeaf.verify(C,1,z,mod,l,h,w),'bad internal Euler lattice leaf';lo=h+1;bins+=1
  assert lo==hi+1,'missing part of lattice interval'
 elif p%4==1:bins=internal(C,Y)
 else:assert p%4==3 # quadratic reciprocity excludes q|A when s>0
 extra=1
 if 'rough' in r:
  L=r['rough'];n=e+1;assert type(L)==int and L>=3 and PC.prime64(n) and math.gcd(C,n)==1 and C>1
  # Each odd prime dividing C has ord_r(p)=n (n prime, r!=n), hence r=1 mod 2n.
  assert all(C%d for d in range(2*n+1,L,2*n)), 'claimed roughness incorrect'
  if math.isqrt(C)**2!=C:extra*=L**wt
  oddpart=(p-1)//((p-1)&(1-p))
  if weighted and pow(C,oddpart,p)!=1:extra*=L**2
 _,mw=combine([solve(z,c[z],True) for z in K]);floor=extra*(pe*C)**wt*mw*(F(pe**(k+1),U)*F(Q,Y)**k if weighted else Q);assert floor>B**power,'large exponent';m=0
 while floor>=10**((m+1)*power):m+=1
 return {'actual':[p,e],'labels':len(V),'lower_log10_floor_large_s':m,'s0':s0,'cut':cut,'internal_bins':bins}
if __name__=='__main__':
 files=[Path(f) for f in sys.argv[2:]] or sorted(H.glob('Cut*.json.gz'))
 for path in files:print(json.dumps(verify(path)),flush=True)
