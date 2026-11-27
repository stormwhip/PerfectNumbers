"""Independent interval/polynomial arithmetic for both 19^618 exclusion caps."""
from math import prod,gcd,isqrt
from pathlib import Path
import gzip,json,time,sys
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
A=(19**619-1)//18//2477;F=65537;assert (19**619-1)%(18*2477)==0 and gcd(A,1238*19)==1 and A%619 and all(619%d for d in range(2,isqrt(619)+1)) and all(F%d for d in range(2,isqrt(F)+1));H=Path(__file__).resolve().parents[1]/'Nineteen';s0=time.perf_counter()
def polygcd(a,b):
 a=[v%F for v in a];b=[v%F for v in b];
 while a and not a[-1]:a.pop()
 while b and not b[-1]:b.pop()
 while b:
  if len(a)<len(b):a,b=b,a;continue
  q=a[-1]*pow(b[-1],-1,F)%F;off=len(a)-len(b)
  for i,x in enumerate(b):a[i+off]=(a[i+off]-q*x)%F
  while a and not a[-1]:a.pop()
 return len(a)==1
assert 3**(19**3-1)>10**2400
for d0,nm,deg,expected in [(183,'LatticeCert.json.gz',1,160),(96,'SquareLatticeCert.json.gz',2,264)]:
 m=19**d0;M=1238*m
 roots=[pow(z,19**(d0-1),m) for z in range(2,19) if pow(z,9,19)==1];Rr=[1+1238*(((z-1)*pow(1238,-1,m))%m) for z in roots];assert len(set(Rr))==8 and all(pow(z,9,m)==1 and z%1238==1 for z in Rr)
 if deg==1:Rr+= [A*pow(z,-1,M)%M for z in Rr]
 D=json.loads(gzip.decompress((H/nm).read_bytes()));bs=D['bands'];assert bs[0][1]==isqrt(A) and all(bs[j][0]==bs[j+1][1]+1 for j in range(len(bs)-1)) and all(lo>0 and lo<=hi for lo,hi,k,n in bs) and min(Rr)>=bs[-1][0];seen=set()
 for i,j,cv,dv in D['w']:
  assert (i,j) not in seen;seen.add((i,j));r=Rr[i];assert r>1 and A%r!=0;c=r*pow(M,-1,A)%A;c-=A if c>A//2 else 0;lo,hi,k,n=bs[j];x=(hi-r)//M;assert x>0
  mat=[];px=[1];
  for ell in range(n):
   a=min(ell,deg*k)
   if len(px)<=a:px=[c*px[0],*[c*px[h]+px[h-1] for h in range(1,len(px))],px[-1]]
   off=ell-a;scale=A**(k-a//deg);mat.append([0]*off+[scale*z for z in px]+[0]*(n-ell-1))
  ps=[]
  for v in (cv,dv):
   assert len(v)==n;poly=[sum(a*b for a,b in zip(v,col)) for col in zip(*mat)];L=0
   for h in reversed(poly):L=L*x+abs(h)
   assert L<lo**(deg*k);ps.append(poly)
  assert polygcd(*ps)
 assert seen=={(i,j) for i,r in enumerate(Rr) for j,(_,hi,_,_) in enumerate(bs) if (hi-r)//M>0} and len(seen)==expected
 print('PASS independent lattice exponent',deg,'classes',len(Rr),'pairs',len(seen),flush=True)
print('PASS structural thresholds',185,98,'seconds',round(time.perf_counter()-s0,3))
