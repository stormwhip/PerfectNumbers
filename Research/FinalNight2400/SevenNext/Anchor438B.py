from pathlib import Path
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Seven438Joint import *
def go(h,fs,anc,k):
 X=p**438*t**12*r**h*anc**k;S=C.sigma(p,438)*C.sigma(t,12)*C.sigma(r,h)*C.sigma(anc,k);D=V.strip(S,[p,t,r,anc]); cp=438-V.v(S,p);cr=h-V.v(S,r);assert V.v(S,t)==1 and gcd(3*p,r*(r-1)//2)==1
 blk=[V.strip(b,[p,t,r,anc]) for b in [C.sigma(p,438),C.sigma(t,12),C.sigma(r,h),C.sigma(anc,k)]];assert prod(blk)==D;why=blk[2:]
 while any(gcd(x,y)!=1 for i,x in enumerate(blk) for y in blk[i+1:]):
  a,b=next((a,b) for a,x in enumerate(blk) for b,y in enumerate(blk) if b>a and gcd(x,y)!=1);blk[a]*=blk.pop(b)
 M=max(blk);U=fracprice(p,438,2,(3,))*fracprice(r,71,4,(5,13,65,211,1055,2743));assert (r-1)//2==5*13*211
 ys={y for y in fs if y not in (p,r,t,19) and y!=anc and y>2};assert all(D%y==0 for y in ys);G=prod((credit(y)[0] for y in ys),start=Fraction(1));F=prod(y for y in ys if V.v(D,y)%2);mp=max([0]+[credit(y)[1][0] for y in ys]);mr=max([0]+[credit(y)[1][1] for y in ys]);
 for i in range(cp+1):
  for j in range(cr+1):
   m=T*p**i*r**j;q=2*m-1;K=X*D*q;uk=cr-j;up=cp-i;g=G if not ys or q>max(ys) else prod((credit(y)[0] for y in ys if y%(4*m)!=q),start=Fraction(1))
   if X*q*p**(2*up)*r**(4*uk)*g.numerator*U.denominator>B*g.denominator*U.numerator:continue
   if not all(V.outside(z,m) for z in why):return False,(i,j,'internal')
   if K*F>B:continue
   for v in range(uk+1):
    for first,last,ac in [(0,min(mp,up),v>mr),(mp+1,up,True)]:
     if first>last:continue
     hh=2*X*q*q*r**v; denom=3*M*B; Z=hh*D*(F if ac else 1);lo,hi=first-1,last+1
     while hi-lo>1:
      mid=(hi+lo)//2
      if Z*p**mid>denom:hi=mid
      else:lo=mid
     if lo>=first:
      g2=G if ac else Fraction(1)
      if hh*p**lo*p**(2*(up-lo))*r**(4*(uk-v))*U.denominator*g2.numerator<=3*B*U.numerator*g2.denominator:return False,(i,j,lo,v)
 return True,()

if __name__=='__main__':
 from Find30Factors import get
 from sympy import divisors,isprime,primerange
 from Seven438One import phi
 def factors(y,k):
  out=set()
  for d in divisors(k+1)[1:]:
   n=phi(y,d)
   for w in (get(y,d) or b'').split():
    if w.isdigit() and (q:=int(w))>1 and n%q==0 and isprime(q):
     out.add(q)
     while n%q==0:n//=q
   if n>1 and isprime(n):out.add(n)
  return out
 for h in map(int,sys.argv[1:]):
  fs=factors(r,h)-{7,t,r,19};anc=max(fs);base=[(7,438),(t,12),(r,h)];s=C.State(base);assert anc<2*T-1;v=V.v(s.D,anc);k=v+v%2;left=[]
  while s.base//anc**v*anc**k<=B:
   u=C.State(base+[(anc,k)])
   if not u.conflict and u.base<=B and C.sigma(anc,k)%t:
    ff=(fs|factors(anc,k)|{y for y in primerange(3,5000) if C.sigma(anc,k)%y==0})-set(u.rows);ok,fail=go(h,ff,anc,k);print('k',h,k,ok,fail,flush=True)
    if not ok:left.append(k)
   k+=2
  print('left',h,left,flush=True)
