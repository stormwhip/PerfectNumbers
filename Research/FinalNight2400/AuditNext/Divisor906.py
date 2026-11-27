"""Cold verification of a simple-divisor inverse CRT cap for the canonical 7^906 block."""
from math import prod,gcd,isqrt
from pathlib import Path
import gzip,json,time,sys
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
from itertools import combinations
A=(7**907-1)//6;F=65537;H=Path(__file__).resolve().parent;assert all(F%i for i in range(2,isqrt(F)+1)) and all(907%i for i in range(2,isqrt(907)+1)) and A%907 and gcd(A,7*1814)==1
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
def run(depth,discovery=False):
 name=f'Candidate{depth}.json.gz' if discovery else 'Divisor906.json.gz';D=json.load(gzip.open(H/name));assert D['u']==depth and 3**(7**5-1)>10**2400; m=7;rs=[2,4]
 for _ in range(1,depth):
  rs=[r+m*((-((r*r+r+1)//m)*pow(2*r+1,-1,7))%7) for r in rs];m*=7
 M=1814*m;rr=[r+m*((1-r)*pow(m,-1,1814)%1814) for r in rs];rr+=[A*pow(r,-1,M)%M for r in rr];assert len(set(rr))==4 and all(r>1 and A%r for r in rr)
 bs=D['bands'];assert bs[0][1]==isqrt(A) and all(x[0]==y[1]+1 for x,y in zip(bs,bs[1:])) and all(0<lo<=hi for lo,hi,k,n in bs) and min(rr)>=bs[-1][0];seen=set();out=[]
 for item in D['w']:
  i,j=item[:2];r=rr[i];lo,hi,k,n=bs[j];x=(hi-r)//M;assert x>0 and (i,j) not in seen;seen.add((i,j));vv=item[2] if discovery else item[2:];c=r*pow(M,-1,A)%A;c-=A if c>A//2 else 0;rows=[];px=[1];pairs=[]
  for l in range(n):
   d=min(l,k)
   if len(px)<=d:px=[c*px[0],*[c*px[h]+px[h-1] for h in range(1,len(px))],px[-1]]
   rows.append([0]*(l-d)+[y*A**(k-d) for y in px]+[0]*(n-l-1))
  for v in vv:
   assert len(v)==n;poly=[sum(a*b for a,b in zip(v,col)) for col in zip(*rows)];sz=0
   for y in reversed(poly):sz=sz*x+abs(y)
   if sz<lo**k:pairs.append((v,poly))
  pair=next(((a,b) for (a,f),(b,g) in combinations(pairs,2) if polygcd(f,g)),None);assert pair,(i,j)
  out.append([i,j,*pair])
 assert seen=={(i,j) for i,r in enumerate(rr) for j,(_,hi,_,_) in enumerate(bs) if (hi-r)//M>0}
 if discovery:(H/'Divisor906.json.gz').write_bytes(gzip.compress(json.dumps({'u':depth,'bands':bs,'w':out}).encode(),mtime=0))
 print('PASS depth',depth,'supply threshold',depth+4,'classes',len(rr),'pairs',len(seen),'complete bounds, no lattice oracle in replay')
if __name__=='__main__':run(int(sys.argv[1]) if len(sys.argv)>1 else 255,len(sys.argv)>2 and sys.argv[2]=='seal')
