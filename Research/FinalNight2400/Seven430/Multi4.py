"""Fractional joint cubic price with the extra order-five demand target W."""
from Win12 import *
W=62619225867394162638521;wf=(5,43,83,653,671719527428359)
@cache
def wloss(c):
 assert W-1==8*prod(wf);L={};orders=[1]
 for z in wf:orders += [s*z for s in orders]
 gen=next(z for z in range(2,150) if all(pow(z,(W-1)//p,W)!=1 for p in (2,*wf)));assert len([z for z in qfactor if z in wf])==0 and 7 not in wf and Q not in wf
 for o in orders:
  if o<=1 or o>=8000 or 3**(o-1)>=W**(4*c):continue
  v=pow(gen,(W-1)//o,W);m=W
  for i in range(1,c+1):
   r=1;bits=(m**4).bit_length()
   for j in range(1,o):
    r=r*v%m
    if r<=2 or not r%2 or gcd(j,o)>1 or (r.bit_length()-1)*(o-1)>=bits:continue
    n=r**(o-1)
    if n<m**4:
     y=math.isqrt(r);ok=lambda x:x>=3 and x%2 and x not in (7,19,Q,W) and pow(2,x-1,x)==1
     if ok(r) or y*y==r and ok(y):L[r]=max(L.get(r,1),Fraction(m**4,n))
   m*=W;v=pow(v,W,m)
 return prod(L.values(),start=Fraction(1))
@cache
def seed(row):
 s=C.State(row);a=s.rows[7]-sum(val(sig(z,h),7) for z,h in row);b=s.rows[Q]-sum(val(sig(z,h),Q) for z,h in row);c=s.rows[W]-sum(val(sig(z,h),W) for z,h in row);L=netjoint(row)[0]*wloss(c);U=-(-L.numerator//L.denominator);return a,b,c,U

def multi(row,fac,one=None):
 row=tuple(row);s=C.State(row);a,b,c,U=seed(row);X=s.X
 if s.fixed_euler:return [] if X*(7**a*Q**b*W**(2*c))**2>B*U else [('fixed',)]
 fs={z for z in fac if s.D%z==0 and z not in s.rows};em=[sig(z,h) for z,h in row];F=prod(z**(val(s.D,z)%2) for z in fs);hh=max([maxover(row,fs)]+[z**(val(s.D,z)+val(s.D,z)%2) for z in fs]);miss=[]
 for k in range(c+1):
  for j in range(b+1):
   for i in range(a+1):
    m=7**i*Q**j*W**k;q=2*m-1;R=(7**(a-i)*Q**(b-j)*W**(2*(c-k)))**2
    if X*q*R>B*U:continue
    if one is not None and (val(one+1,7),val(one+1,Q),val(one+1,W))!=(i,j,k):continue
    if not all(ext(v,m) for v in em):miss.append((i,j,k,'int'));continue
    if X*s.D*F*q>B:continue
    # supplier shares y7,yQ with squared price, but W component has cost weight4; cancellation leaves 2 extra W powers.
    if 4*X**2*s.D*F*q**4*R>9*B**2*U*hh*W**(2*(c-k)):continue
    miss.append((i,j,k,'em'))
 return miss
if __name__=='__main__':
 raw=json.loads((H/'New4any.json').read_bytes());res={};
 for jj,t in sorted(raw.items(),key=lambda e:-int(e[0])):
  j=int(jj);r=root+[(Q,4),(W,j)];m=multi(r,t['roots']);res[j]=m;(H/'Win4W.json').write_text(json.dumps(res));print(j,len(m),m[:2],flush=True)
