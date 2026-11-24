from Replay import *

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
  jp0=dict(zip(rs,jp));vp0=dict(zip(rs,vp));bs0={h:(l,v*v) for h,l,v in bs}
  def min_b(sale):
   # All non-source factors keep their own premiums; blanket U does not rely on sponsor identities.
   v=F(Vfull,sale);n=2*v.numerator*Q*Q;d=3*budget*v.denominator
   return 0 if n<=d else 1+logi((n-1)//d,p)//(k-1)
  def geo(bj):
   z=Y*p**bj;return 2*Q*p**bj//3,z*Q//(max(P,Q)*(P//z+4))
  ext=min_b(1)
  if ext<=e-s and 2*M*Q**2*p**ext<=3*B:outside.append(s)
  hit=None
  for r,c in cr.items():
   bj=min_b(vp0.get(r,1));room=B*jp0.get(r,1)//(M*Q)
   if bj>e-s:continue
   need,th=geo(bj)
   for f in range(c+c%2,c+logi(room,r)+1,2):
    if r**(f-c)<=th or r**f<=need:continue
    n=sig(r,f)
    if val(n,p)>=bj and qfactor(n,Y,Q,min(n,B//(pe*A))):hit=('known',r,c,f,bj);break
   if hit:break
  if not hit:
   for h,n in C.items():
    l,v=bs0.get(h,(1,1));bj=min_b(v)
    if bj>0:bj=min_b(1) # positive b excludes identity with the zero-supply prime in this block
    if bj>e-s:continue
    need,th=geo(bj)
    for g in range(logi(B*l//(M*Q),10001)+1):
     if not g and th>=1:continue
     # c and g have the same parity because f=c+g is even; c even cannot be the odd-multiplicity witness.
     room=B*(l if g%2 else 1)//(M*Q);lo=max(10001,root(th,g)+1) if g else 10001;hi=root(room,g) if g else n
     if lo>hi:continue
     for c in range(2-g%2,logi(n,lo)+1,2):
      f=c+g;L=max(lo,root(need,f)+1);H=min(hi,root(n,c));
      if cand(n,c,p,f,L,H,bj,h,mode):hit=('unknown',h,c,f,bj);break
     if hit:break
    if hit:break
  if hit:surv.append(s);w[s]=hit
  else:ct['inside_empty']+=1
 return dict(p=p,e=e,multipliers=dict(size=[str(i) for i in mv],valuation=[str(i) for i in vpre],sponsor_bases=sorted(sp)),kernel=ker,post_sponsor=post,outside=outside,inside=surv,first=[[s,w[s]] for s in surv[:1]],counts=ct)
