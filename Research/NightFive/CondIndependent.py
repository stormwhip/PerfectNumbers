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

def replay(e,ds,roots,sec):
 T=10**5;ps=I.sieve_primes(T);A=sigma(5,e);pr=list(map(int,roots[str(e)]));pivot=max(pr);c=0;tmp=A
 while tmp%pivot==0:c+=1;tmp//=pivot
 initial=root(e,pr,[z for z in ps if z not in F],T,ds);assert initial['known'] and initial['rough'] and not initial['higher'];ss=[s for lo0,hi0 in initial['one'] for s in range(lo0,hi0+1)];threshold=I.LN_B_HI
 for f in range(2,I.ilog(B//5**e,pivot)+1,2):
  if f<c or not block(pivot,f):continue
  X=5**e*pivot**f;P=5**(e+1);h=sigma(pivot,f);S=A*h;D=S//gcd(2*X,S)
  if X*D>B or gcd(D,X*prod(F))>1:continue
  extras=list(map(int,sec.get(f'{pivot}:{f}',[])));assert all(h%z==0 for z in extras)
  def strip(v):
   m={}
   for z in set(pr+extras+ps):
    if v%z==0:
     t=0
     while v%z==0:v//=z;t+=1
     m[z]=t
   return m,v
  mult,U=strip(D);irreduc=strip(h)[1];n=I.ilog(U,T);target=I.LN2_LO-sum(map(max_ab,[5,pivot,*mult]))-n*max_ab(T);V=e;tmp=h
  while tmp%5==0:V-=1;tmp//=5
  if V<0:continue
  rows=[]
  for d in ds:
   L=d.lam_p*lo(5);L=min(L,4*lo(T)) if U!=1 else L;prices={z:opt(z,v,False,L) for z,v in mult.items()};common=lo(X*D)+d.const_no_target+d.mu*target-sum(x for z,x in d.theta_map.items() if (X*D)%z==0)+sum(prices.values())-(n*L+3)//4;rows.append((d,L,common,prices))
  for s in ss:
   if s>V:continue
   y=5**s;Q=2*y-1;k=V-s;qq=lo(Q);geo=[(1,pivot-1)]
   for m in range(2,f+2):
    if (f+1)%m==0:geo.append((m,(pivot**m-1)//prod(t for j,t in geo if m%j==0)))
   def permits(a):
    w=(-a)%y
    if w%2==0:w+=y
    return a>=w*Q
   if permits(h) and any(permits(t) for j,t in geo[1:]):return False
   def score(row,j=0):
    d,L,b,pr=row;loss=d.delta_q if Q<=I.SPECIAL_LIMIT else min(d.delta_q,d.mu*max_ab(Q));return b+(k-j)*L-loss
   if max(score(row)+qq for row in rows)>threshold:continue
   if 32*5**e*Q**6<243*B:
    if Q<=I.MAX_EXPONENT+1:return False
    for j in range(1,min(k,I.ilog(I.MAX_EXPONENT+1,5))+1):
     fee=qq+5**j*(qq+I.log_interval(2,3)[0]);bb=[score(row,j)+fee for row in rows]
     if max(b-row[0].delta_src for b,row in zip(bb,rows))<=threshold:return False
     if U!=1 and max(bb)-hi(U)<=threshold:return False
     if any(max(b-row[3][z] for b,row in zip(bb,rows))-hi(z)*v<=threshold for z,v in mult.items()):return False
   bare=2*qq+I.log_interval(2,3)[0];gap=lo(Q*Q*y)-hi(max(P,Q)*(P//y+4));bs=[score(row) for row in rows]
   if max(b+bare-row[0].delta_src for b,row in zip(bs,rows))<=threshold:return False
   if U!=1 and max(bs)+max(bare-hi(U),gap-hi(irreduc))<=threshold:return False
   for z,v in mult.items():
    u=0;tmp=A
    while tmp%z==0:u+=1;tmp//=z
    g=v
    while not (block(z,g) and lower_source(z,g,y,Q)):g+=1
    price=qq+(g-v)*lo(z)
    if u:price=max(price,gap-hi(z)*(v-u))
    if max(b-row[3][z] for b,row in zip(bs,rows))+price<=threshold:return False
 return True
