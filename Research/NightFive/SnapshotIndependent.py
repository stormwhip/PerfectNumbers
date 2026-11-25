"""Independent conditioned arithmetic; no search/cache. Root gap lemma from merged proof."""
from PaidCheck import I,F,B,root,parts
from LeafCheck import ln_low as lo,lower_opt as opt,max_ab,block,sigma
from math import prod,gcd

def hi(x):
 j=max(0,x.bit_length()-52);return j*I.LN2_HI+I.log_interval((x>>j)+1)[1]
def lower_source(z,g,y,Q):
 if g%2:return False
 a=sigma(z,g);w=(-a)%y
 if w%2==0:w+=y
 return a>=Q*w

def replay(e,ds,roots,sec,depth=3,limit=800):
 T=100000;ps=I.sieve_primes(T);P=5**(e+1);A=sigma(5,e);pr=list(map(int,roots[str(e)]));initial=root(e,pr,[z for z in ps if z not in F],T,ds);assert initial['known'] and initial['rough'] and not initial['higher'];initials=[s for lo0,hi0 in initial['one'] for s in range(lo0,hi0+1)];threshold=I.LN_B_HI;count=0
 def visit(exact,ss):
  nonlocal count
  count+=1
  if count>limit:return False
  bank=[A];X=5**e;V=e;extras=[];subblocks=[]
  for pivot,f in exact:
   X*=pivot**f;h=sigma(pivot,f);bank.append(h);tmp=h
   while tmp%5==0:tmp//=5;V-=1
   qs=list(map(int,sec.get(f'{pivot}:{f}',[])));assert all(h%z==0 for z in qs);extras.extend(qs);geo=[(1,pivot-1)]
   for m in range(2,f+2):
    if (f+1)%m==0:geo.append((m,(pivot**m-1)//prod(t for j,t in geo if m%j==0)))
   assert prod(t for _,t in geo[1:])==h;subblocks.append((h,[t for _,t in geo[1:]]))
  S=prod(bank);D=S//gcd(2*X,S)
  if X*D>B or gcd(D,X*prod(F))>1:return True
  def strip(v):
   m={}
   for z in set(pr+extras+ps):
    if v%z==0:
     t=0
     while v%z==0:v//=z;t+=1
     m[z]=t
   return m,v
  mult,U=strip(D);origins=[gcd(U,z) for z in bank];separated=prod(origins)==U and all(gcd(v,w)==1 for i,v in enumerate(origins) for w in origins[i+1:]);n=I.ilog(U,T);target=I.LN2_LO-sum(map(max_ab,[5,*[z for z,f in exact],*mult]))-n*max_ab(T)
  if V<0:return True
  rows=[]
  for d in ds:
   L=d.lam_p*lo(5);L=min(L,4*lo(T)) if U!=1 else L;prices={z:opt(z,v,False,L) for z,v in mult.items()};common=sum(d.refund(z) for z in set(mult)|{p for p,f in exact})+lo(X*D)+d.const_no_target+d.mu*target-sum(x for z,x in d.theta_map.items() if (X*D)%z==0)+sum(prices.values())-(n*L+3)//4;rows.append((d,L,common,prices))
  def single(s):
   if s>V:return True
   y=5**s;Q=2*y-1;k=V-s;qq=lo(Q)
   def permits(a):
    w=(-a)%y
    if w%2==0:w+=y
    return a>=w*Q
   if any(permits(h) and any(permits(t) for t in ts) for h,ts in subblocks):return False
   def score(row,j=0):
    d,L,b,pr=row;loss=d.delta_q if Q<=I.SPECIAL_LIMIT else min(d.delta_q,d.mu*max_ab(Q));return b+(k-j)*L-loss
   if max(score(row)+qq for row in rows)>threshold:return True
   if 32*5**e*Q**6<243*B:
    if Q<=I.MAX_EXPONENT+1:return False
    for j in range(1,min(k,I.ilog(I.MAX_EXPONENT+1,5))+1):
     fee=qq+5**j*(qq+I.log_interval(2,3)[0]);bb=[score(row,j)+fee for row in rows]
     if max(b-row[0].delta_src for b,row in zip(bb,rows))<=threshold:return False
     if U!=1 and max(bb)-hi(U)<=threshold:return False
     if any(max(b-row[3][z] for b,row in zip(bb,rows))-hi(z)*v<=threshold for z,v in mult.items()):return False
   bare=2*qq+I.log_interval(2,3)[0];gap=lo(Q*Q*y)-hi(max(P,Q)*(P//y+4));bs=[score(row) for row in rows]
   if max(b+bare-row[0].delta_src for b,row in zip(bs,rows))<=threshold:return False
   if separated:
    for i,v in enumerate(origins):
     if v==1:continue
     cost=bare-hi(v)
     if i==0:cost=max(cost,gap)
     if max(bs)+cost<=threshold:return False
   elif U!=1 and max(bs)+bare-hi(U)<=threshold:return False
   for z,v in mult.items():
    u=0;tmp=A
    while tmp%z==0:u+=1;tmp//=z
    g=v
    while not (block(z,g) and lower_source(z,g,y,Q)):g+=1
    price=qq+(g-v)*lo(z)
    if u:price=max(price,gap-hi(z)*(v-u))
    if max(b-row[3][z] for b,row in zip(bs,rows))+price<=threshold:return False
   return True
  unresolved=[s for s in ss if not single(s)]
  if not unresolved:return True
  if len(exact)>=depth or not mult:return False
  pivot=max(mult);v=mult[pivot];b=B//(X*(D//pivot**v));f=2
  pv=pivot+1;j=0
  while pv%5==0:j+=1;pv//=5
  if A%pivot and pivot%4==1 and j in unresolved:return False
  while pivot**f<=b:
   if f>=v and block(pivot,f) and not visit(exact+[(pivot,f)],unresolved):return False
   f+=2
  return True
 ans=visit([],initials);return ans,count
