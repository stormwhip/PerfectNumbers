"""Joint fifth/p-specific cubic network: use p=11 and the secondary R only, disjoint p-order 5 from R-1 odd and both base-prime factors."""
from Joint import *
Z=309862619201513446309679813467;zf=(3,7,13,37,661,82261,41131,787477,8709079)
@cache
def rloss(z,cap):
 assert z==Z and z-1==2*prod(zf) and gcd(z*prod(zf),55)==1;L={};O=[1]
 for q in zf:O+=[a*q for a in O]
 gen=next(v for v in range(2,300) if all(pow(v,(z-1)//r,z)!=1 for r in (2,*zf)))
 for o in O:
  if o<=1 or o>8000 or 3**(o-1)>=z**(2*cap):continue
  g=pow(gen,(z-1)//o,z);m=z
  for v in range(1,cap+1):
   a=1;goal=m*m;bits=goal.bit_length()
   for j in range(1,o):
    a=a*g%m
    if a>2 and a%2 and gcd(j,o)==1 and (a.bit_length()-1)*(o-1)<bits and a**(o-1)<goal:
     y=isqrt(a);ok=lambda x:x>=3 and x%2 and x not in (7,19,11,Z,82261) and pow(2,x-1,x)==1
     if ok(a) or y*y==a and ok(y):L[a]=max(L.get(a,1),Fraction(goal,a**(o-1)))
   m*=z;g=pow(g,z,m)
 return prod(L.values(),start=Fraction(1))

def gtest(row,rs):
 s=C.State(row);X=s.X;D=s.D;cap=s.rows[Z]-val(s.S,Z);a=e-val(s.S,p);L=loss()*rloss(Z,cap);U=-(-L.numerator//L.denominator);R=p**(4*a)*Z**(2*cap)
 if s.fixed_euler:return [] if X*R>B*U else [-1]
 fs=[r for r in rs if r not in s.rows and D%r==0];F=prod(z**(val(D,z)%2)for z in fs);em=[C.sig_odd(z,h)for z,h in row];blocks=[C.nonsupport(v,X*prod(fs)) for v in em];hs=[r**(val(D,r)+val(D,r)%2) for r in fs];
 while blocks:
  z=blocks.pop();sames=[r for r in blocks if gcd(r,z)>1]
  if sames:
   for r in sames:blocks.remove(r);z*=r
   blocks.append(z)
  else:hs.append(z)
 Hh=max(hs,default=1);miss=[]
 for j in range(cap+1):
  m=Z**j;C0=p**(4*a)*Z**(2*(cap-j))
  for i in range(a+1):
   q=2*m-1
   if X*q*C0<=B*U:
    if not all(k==0 and i or external(z,m)for k,z in enumerate(em)):miss.append((i,j,'int'))
    elif X*D*F*q<=B:
     # Enumerate remaining Z units to sharpen y-cancellation cap at each v.
     for v in range(cap-j+1):
      b=Z**v;A=B*U*Hh//(X*D*F*q*b*b);hi=min(p**(a-i),isqrt(isqrt(A)),3*B*Hh//(2*X*D*F*q*q*b));
      if hi and 2*X*q*q*C0<=3*B*U*b*hi**3:miss.append((i,j,'em'));break
   m*=p;C0//=p**4
 return miss
if __name__=='__main__':
 from Report import rem
 for row,n in rem():
  if row[1][1]==6:
   m=gtest(row,n['roots']);print([h for z,h in row],len(m),m[:2],flush=True)
