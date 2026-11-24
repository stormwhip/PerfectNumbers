"""Independent full-domain review. No NightUniform Python imports. Run with python -B from any cwd. Uses archived Teich blanket lemma and primality verifier only. Successful exits state only what this relaxation excludes."""
import sys,json,math,gzip,argparse,time,collections,random
from pathlib import Path
from fractions import Fraction as F
from functools import cache
import hashlib
D=Path(__file__).resolve().parent; A0=D.parent/'NightUniform'; sys.path.insert(0,str(D.parent/'OrderSupplyNext'))
import VerifyOrderSupply as O
sys.path.insert(0,str(D.parent/'NightMerge'));import LatticeLeaf
pack={};checked=set()
B=10**2400;small=tuple(a for a in range(3,10001,2) if all(a%d for d in range(3,math.isqrt(a)+1,2))); prod=math.prod
@cache
def sig(r,f): return (r**(f+1)-1)//(r-1)
def val(n,p):
 j=0
 while not n%p:n//=p;j+=1
 return j
def logi(n,p):
 if n<1:return -1
 lo,hi=0,n.bit_length()//max(1,p.bit_length()-1)+1
 while hi-lo>1:
  m=(hi+lo)//2
  if p**m<=n:lo=m
  else:hi=m
 return lo
@cache
def root(n,k):
 if k==1 or n<2:return n
 if k==2:return math.isqrt(n)
 if k>=n.bit_length():return 1
 x=1<<((n.bit_length()+k-1)//k)
 while True:
  y=((k-1)*x+n//x**(k-1))//k
  if y>=x:
   assert x**k<=n<(x+1)**k;return x
  x=y
@cache
def phi(p,h):return (p**h-1)//prod(phi(p,j) for j in range(1,h) if h%j==0)
@cache
def certs():return json.load(gzip.open(D.parent/'OrderSupplyNext/OrderPrimeProofs.json.gz','rt'))
def primes(rs,A):
 assert len(set(rs))==len(rs)
 for r in rs:
  assert A%r==0
  O.verify_cert(r,None if r<2**64 else certs()[str(r)])
def chunks(p,e,ss):
 out={};n=e+1;A=sig(p,e);C=A//prod(r**val(A,r) for r in ss);assert math.gcd(C,n)==1
 for h in range(3,n+1,2):
  if n%h==0 and (v:=math.gcd(phi(p,h),C))>1:out[h]=v
 assert prod(out.values())==C and all(math.gcd(v,u)==1 for h,v in out.items() for j,u in out.items() if h<j);return out
def blocks(p,C):
 ans=[];odd=(p-1)//((p-1)&(1-p));H={a for a in range(1,p) if pow(a,odd,p)==1}
 for h,v in C.items():
  ns=v%p not in H; sq=math.isqrt(v)**2==v
  if not ns and sq:continue
  step=2*h;start=10001+(1-10001)%step;end=start+10000*step;L=N=end
  for r in range(start,end,step):
   if v%r==0:
    L=min(L,r)
    if r%p not in H:N=min(N,r)
    if L<end and (not ns or N<end):break
  ans.append([h,1 if sq else L,N if ns else 1]);
 return ans
@cache
def lifts(p,h,b,f):
 # Hensel on X^o-1 (derivative invertible), CRT solve in opposite order from upstream.
 j=val(f+1,p);l=b-j
 if l<=0:return None
 mod=p**l; out=[]
 for a in range(2,p):
  if pow(a,f+1,p)!=1:continue
  x=a;m=p
  while m<mod:
   m2=min(mod,m*m);x=(x-(pow(x,p-1,m2)-1)*pow((p-1)*pow(x,p-2,m2),-1,m2))%m2;m=m2
  t=2*h;g=math.gcd(t,m);T=math.lcm(t,m)
  if (x-1)%g:continue
  z=(1+t*((x-1)//g)*pow(t//g,-1,m//g))%T;out.append((z,T))
 return out
# Lattice points under a line, by transposing positive rows (not upstream's floor implementation).
def fs(n,d,a,b):
 q,a=divmod(a,d);v,b=divmod(b,d);t=q*n*(n-1)//2+v*n
 if n<=0 or a==0:return t
 y=(a*(n-1)+b)//d
 if not y:return t
 return t+n*y-fs(y,a,d,d-b+a-1)
def rect(C,c,z,T,L,H,cap):
 k0=(L-z+T-1)//T;k1=(H-z)//T
 if k1<k0:return False
 w=C*pow(z,-c,T)%T;u0=(C+H**c-1)//H**c;u1=C//L**c;l0=(u0-w+T-1)//T;l1=(u1-w)//T
 if l0>l1:return False
 if l1-l0+1>=T:return True
 x=pow(z,c,T*T);beta=((C%(T*T)-x*w)//T)*pow(x,-1,T)%T;alpha=-c*w*pow(z,-1,T)%T
 def count(a,n):
  d=alpha*a+beta-l0;return fs(n,T,alpha,d)-fs(n,T,alpha,d-(l1-l0+1))
 def test(a,n,nn):
  if not nn:return False
  if nn>cap:return True
  if n==1:return C%(z+a*T)**c==0
  m=n//2;t=count(a,m);return test(a,m,t) or test(a+m,n-m,nn-t)
 n=k1-k0+1;return test(k0,n,count(k0,n))
@cache
def cand(C,c,p,f,L,H,b,h,mode):
 if L>H:return False
 lifts0=lifts(p,h,b,f)
 if lifts0 is None:return True
 for z,T in lifts0:
  r=L+(z-L)%T
  if r>H:continue
  w=C*pow(z,-c,T)%T;u0=(C+H**c-1)//H**c;u1=C//L**c;u=u0+(w-u0)%T
  if (u1-u)//T<8:
   for v in range(u,u1+1,T):
    if C%v:continue
    x=root(C//v,c)
    if x**c*v==C and L<=x<=H and (x-z)%T==0:return True
  elif (H-r)//T<=8:
   if any(C%x**c==0 for x in range(r,H+1,T)):return True
  elif mode<0:return True
  else:
   lo=L
   while lo<=H:
    hi=min(H,2*lo-1)
    if rect(C,c,z,T,lo,hi,mode):
     key=hashlib.sha256('|'.join(map(str,(C,c,z,T,lo,hi))).encode()).hexdigest()
     if key not in pack or not LatticeLeaf.verify(C,c,z,T,lo,hi,pack[key]):return True
     checked.add(key)
    lo=hi+1
 return False
@cache
def price(p,k,r,c):
 # Independently minimize price over ALL even exponents, including forbidden exclusions; rigorous tail from LTE.
 order=next(o for o in range(1,p) if pow(r,o,p)==1);t=val(r**order-1,p) if order>1 and order%2 else 0;best=None
 for f in range(c+(c%2),1000,2):
  H=r**f;Z=sig(r,f)
  if all(Z%v for v in O.tb.forbidden(p)):
   b=val(Z,p);v=F(H,p**(k*b));best=min(best,v) if best is not None else v
  if best is not None and H>=best*p**(k*t)*(f+1)**k and r*r*(f+1)**k>=(f+3)**k:return max(F(1),best)
 raise RuntimeError('tail not proven')
def qfactor(n,Y,Q,hi):
 if hi<Q:return False
 if Y==1:return True
 q=Q+(2*Y-1-Q)%(4*Y)
 if (hi-q)//(4*Y)<4:return any(n%x==0 for x in range(q,hi+1,4*Y))
 lo=(n+hi-1)//hi;v=lo+(-n-lo)%Y
 if (n//Q-v)//Y>=4:return True
 return any(n%x==0 for x in range(v,n//Q+1,Y))
@cache
def hl(p,top,k):
 # overestimate losses by including all odd eligible composites (no PRP oracle); only p=11 used here.
 l=[]
 for a in range(2,p-1):
  o=next(i for i in range(1,p) if pow(a,i,p)==1)
  if o%4==0:continue
  f=next(i for i in range(5,4*o+6,4) if (i+1)%o==0);assert 3**(o*p-1-f)>=p**k
  x=a;m=p
  for t in range(1,top+1):
   y=pow(x,p,m*p)
   if x!=y and x%4==1 and x not in O.tb.forbidden(p) and x**f<m**k and O.tb.may_be_prime(x):l.append((t,F(m**k,x**f)))
   x=y;m*=p
 return l

def run(x,mode):
 p,e=x['p'],x['e'];rs=x['rs'];prof=O.profile(p);k=prof.kap;U=prof.U(e);P=p**(e+1);A=sig(p,e);pe=p**e
 assert p%4==3 and e%2==0 and p**((k+1)*e)>B*U
 if p==11:assert p**((k+1)*e)>B*U*max([F(1),*(v for t,v in hl(p,prof.top,k) if t<=e)])
 else:assert p**(3*e)>B*U*prof.D(e)
 primes(rs,A);ss=set(rs)|{r for r in small if A%r==0};C=chunks(p,e,ss);bs=blocks(p,C);cr={r:val(A,r) for r in ss};jp=[];vp=[]
 for r in rs:
  c=cr[r];f=c+c%2
  while any(sig(r,f)%t==0 for t in O.tb.forbidden(p)):f+=2
  jp.append(r**(f-c));vp.append(price(p,k,r,c));assert vp[-1]==max(1,O.price(p,k,r,c))
 ds=O.G.discounts(p,prof);sp={r for t,x0,d,w in ds for r in w};C2=chunks(p,e,ss|{r for r in sp if A%r==0});bs2=blocks(p,C2)
 base=pe*A*prod(jp);mv=[1,*jp,*[l for h,l,v in bs]];M=base*prod(l for h,l,v in bs);mx=max(mv);vpre=[1,*vp,*[v*v for h,l,v in bs]];K=p**((k+1)*e);Vfull=F(K*prod(vpre),U);V=Vfull/max(vpre);M2=base*prod(l for h,l,v in bs2);mx2=max([1,*jp,*[l for h,l,v in bs2]]);VS=K*prod(v for r,v in zip(rs,vp) if r not in sp)*prod(v*v for h,l,v in bs2)
 ct=collections.Counter();surv=[];post=[];outside=[];ker=[];w={};Ctot=prod(C.values());maxc=logi(Ctot,10001)
 for s in range(e+1):
  Y=p**s;Q=max(5,2*Y-1);den=max(Q,P)*(P//Y+4);budget=B*Y**k
  if Vfull*Q>budget or M*Q>B or (M*Q**2*Y>=B*mx*den and 2*M*Q**2>=3*B):ct['kernel']+=1;continue
  ker.append(s)
  loss=prod(d for t,x0,d,ws in ds if t<=e-s and not any(r%4==3 or r<Q or val(r+1,p)!=s for r in ws))
  if VS*Q>budget*loss or M2*Q>B or (M2*Q**2*Y>=B*mx2*den and 2*M2*Q**2>=3*B):ct['sponsor']+=1;continue
  post.append(s);N=2*V.numerator*Q**2;Z=3*budget*V.denominator;b=0 if N<=Z else (logi((N-1)//Z,p)//(k-1)+1)
  if b>e-s:ct['b']+=1;continue
  if 2*M*Q**2*p**b<=3*B:outside.append(s)
  room=B*mx//(M*Q);need=2*Q*p**b//3;th=Y*Q//den;hit=None
  for r,c in cr.items():
   for f in range(c+c%2,c+logi(room,r)+1,2):
    if r**(f-c)<=th or r**f<=need:continue
    n=sig(r,f)
    if val(n,p)>=b and qfactor(n,Y,Q,min(n,B//(pe*A))):hit=('known',r,c,f,b);break
   if hit:break
  if not hit:
   for g in range(logi(room,10001)+1):
    if g==0 and th>=1:continue
    lo=max(10001,root(th,g)+1) if g else 10001;hi=root(room,g) if g else Ctot
    if lo>hi:continue
    for h,n in C.items():
     for c in range(2-g%2,logi(n,lo)+1,2):
      f=c+g;L=max(lo,root(need,f)+1);H=min(hi,root(n,c));
      if cand(n,c,p,f,L,H,b,h,mode):hit=('unknown',h,c,f,b);break
     if hit:break
    if hit:break
  if hit:surv.append(s);w[s]=hit
  else:ct['inside_empty']+=1
 return dict(p=p,e=e,multipliers=dict(size=[str(i) for i in mv],valuation=[str(i) for i in vpre],sponsor_bases=sorted(sp)),kernel=ker,post_sponsor=post,outside=outside,inside=surv,first=[[s,w[s]] for s in surv[:1]],counts=ct)
if __name__=='__main__':
 a=argparse.ArgumentParser();a.add_argument('--mode',type=int,default=0,help='-1 no rectangles; 0 second-order; >0 exact-test up to this many rectangle hits');a.add_argument('--start',type=int,default=0);a.add_argument('--count',type=int,default=41);a.add_argument('--pack',type=Path);args=a.parse_args();rows=json.loads((D/'input.json').read_text());out=[];t=time.time();sys.setrecursionlimit(30000);pack=(json.loads(gzip.decompress(args.pack.read_bytes())) if args.pack.suffix=='.gz' else json.loads(args.pack.read_bytes())) if args.pack else {};suffix='-pack' if args.pack else ''
 for a in rows[args.start:args.start+args.count]:
  key=(a['p'],a['e']);checked.clear();r=run(a,args.mode);r['lattice_keys']=sorted(checked);out.append(r);print(key,len(r['post_sponsor']),len(r['outside']),len(r['inside']),r['first'],round(time.time()-t,2),flush=True);cand.cache_clear();root.cache_clear()
 (D/f'results-{args.mode}-{args.start}-{args.count}{suffix}.json').write_text(json.dumps(out,separators=(',',':'))+'\n')
