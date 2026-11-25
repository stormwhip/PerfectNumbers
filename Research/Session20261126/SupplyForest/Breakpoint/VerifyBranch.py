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

def model(p,e,t,f,K,owners,cap):
 k=T.kappa(p);A=sigma(p,e);Sp=sigma(t,f)//(1+f%2);X=p**e*t**f;C=peel(A*Sp,p*t);ban=T.forbidden(p);base=Fr(p**((k+1)*e)*max(1,Fr(t**f,p**(k*a.val(Sp,p)))),blanket(p,e)[0]);U,D=blanket(p,e);Z=X*C*math.prod(owners);kids={q:[] for q in [*K,*owners]};h={q:a.val(C,q) for q in K};C0=C//math.prod(q**j for q,j in h.items());Y=1;Q=1
 for q,z in owners.items():kids[z].append(q)
 @cache
 def props(z,f):
  n=sigma(z,f)//(1+f%2);return a.val(n,p),peel(n,Z),tuple((q,a.val(n,q)) for q in kids[z] if n%q==0)
 def qfree(n):
  if n<Q:return True
  T0=4*Y;b=(n*pow(Q,-1,T0))%T0 or T0;mx=n//Q
  if b>mx:return True
  if mx-b>=16*T0:return False
  return all(n%u for u in range(b,mx+1,T0))
 small=min([1,*[Fr(z,p**(k*a.val(z+1,p))) for z in kids if z%4==1]])
 def layer(mode):
  mass=mode in ('mass','nomassEuler','mix');weighted=mode=='mix';allow=mode in ('mass','high','one','mix')
  @cache
  def node(z,need,loc):
   if loc=='maybe':return min(node(z,need,'under'),node(z,need,'self')) if not weighted and allow and z%4==1 and all((z+1)%b for b in ban) else node(z,need,'under')
   at=loc=='self';under=loc=='under';o=T.multiplicative_order(z,p);t0=a.val(z**o-1,p) if o>1 else 0;j=need+((1-need)%4 if at else need%2);step=4 if at else 2
   if at and mode=='one' and j!=1:return None
   if at and mode=='high' and j==1:j=5
   best=None;cnt=0
   while True:
    powz=z**j;inc=powz**(k-1) if weighted else 1;cheap=Fr(powz,p**(k*t0)*(j+1)**k);lower=inc*max(1,cheap) if weighted else powz if mass else cheap*(small if mode=='one' else 1);mono=z**step*(j+1)**k>=(j+step+1)**k
    if mass and cnt>=cap and (not weighted or mono):return min(lower,best) if best is not None else lower
    if best is not None and lower>=best and (mono or mass and not weighted):return best
    if ready(z,j,ban):
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
 if X*C0*layer('nomassEuler' if f%2 else 'mass')>B:return 'mass'
 if f%2:
  if f==1:assert Fr(p**((k+1)*e)*t*layer('ordinary'),U*p**(k*a.val(Sp,p)))>B
  else:assert base*layer('ordinary')>B*D
  return 'pivot-Euler'
 assert base*layer('high')>B*D,'high';assert base*layer('one')>B,'active Euler';v=base*layer('ordinary');s=next((s for s in range(e+1) if v*max(1,2*p**s-1)<=B*p**(k*s)),e+1)
 if s>e:return 'valuation'
 assert s>0 and p%4==3,'unverified internal A';Y=p**s;Q=2*Y-1;assert all(q%4!=1 or a.val(q+1,p)<s for q in [t,*kids]);assert qfree(peel(Sp,p*t)),'unverified internal pivot sigma'
 assert (X*C0)**(k-1)*base*Fr(Q,Y)**k*layer('mix')>B**k,'mixed';return 'mixed'

def verify(path):
 pack=json.loads(gzip.decompress(Path(path).read_bytes()));assert pack['schema']=='exact-pivot-supply-1';p,e,t=pack['seed'];assert p in (7,11,13,19,31) and e>=2 and e%2==0;A=sigma(p,e);ban=T.forbidden(p);assert A%t==0 and t!=p and all(A%b for b in ban);rows={r['f']:r for r in pack['rows']};assert len(rows)==len(pack['rows']);seen=set();certs=pack['ecpp'];primes={t};cnt={}
 for r in rows.values():primes.update(r['roots']);primes.update(q for q,z in r['owners'])
 for q in primes:
  z=q;assert z>2
  if z>=2**64:
   for level in certs[str(q)]:assert level[0]==z;z=PC.level(*level)
  assert PC.prime64(z)
 c=a.val(A,t);f=c
 while p**e*(A//t**c)*t**f<=B:
  if (f%2==0 or f%4==1 and t%4==1) and ready(t,f,ban):
   S=sigma(t,f);X=p**e*t**f;C=peel(A*(S//(1+f%2)),p*t)
   if X*C<=B and a.val(S,p)<=e and A*S<=2*X:
    assert f in rows,('gap',f);r=rows[f];K=set(r['roots']);P=dict(r['owners']);V=K|set(P);assert len(K)==len(r['roots']) and len(P)==len(r['owners']) and not K.intersection(P) and all(C%z==0 for z in K) and all(X*C%z for z in P);kids={z:[] for z in V}
    for y,z in P.items():kids[z].append(y)
    stack=list(K);visited=set()
    while stack:
     z=stack.pop();assert z not in visited;visited.add(z);stack.extend(kids[z])
    assert visited==V and 1<=r['head']<=512;rule=model(p,e,t,f,K,P,r['head']);cnt[rule]=cnt.get(rule,0)+1;seen.add(f)
  f+=1
 assert set(rows)==seen;return {'p':p,'e':e,'pivot':t,'leaves':len(seen),'tail':f,'rules':cnt}
if __name__=='__main__':
 for f in sys.argv[2:] or sorted(H.glob('Branch*.json.gz')):print(json.dumps(verify(f)),flush=True)
