"""Independent 7^906 two-prime companion CRT/square/cofactor/remnant-window audit."""
from pathlib import Path
from fractions import Fraction
from math import gcd,isqrt
from itertools import product
import sys,json,gzip,time
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));from Divisor906 import polygcd
A=(7**907-1)//6;X=7**906;B=10**2400;W=7*X;m=7**140;M=1814*m;s0=time.perf_counter()
d=json.load(gzip.open(H.parent/'Nineteen/Sparse906.json.gz'));ws={(j,i,b):(c,v) for j,i,b,c,v in d['w']};used=set();admitted=[]
for j in range(2,110):
 if j%7==0:assert all(pow(a,3*j,49)!=A**3%49 for a in range(1,49) if a%7);continue
 # Choose residue mod7 then lift by trying all seven digits (no derivative or inherited Hensel formula).
 rr=[a for a in range(1,7) if pow(a,3*j,7)==1 and A*pow(a,-j,7)%7 in (2,4)];mod=7
 for _ in range(1,140):
  rr=[a+k*mod for a in rr for k in range(7) if pow(a+k*mod,3*j,7*mod)==pow(A,3,7*mod)];mod*=7
 rs=[z+m*((1-z)*pow(m,-1,1814)%1814) for z in rr];active=[(i,r) for i,r in enumerate(rs) if r**j<=A]
 if not active:continue
 admitted.append(j);bands=d['bands'][str(j)];h=bands[0][1];assert h**j<=A<(h+1)**j and min(r for i,r in active)>=bands[-1][0] and all(x[0]==y[1]+1 for x,y in zip(bands,bands[1:]))
 for i,r in active:
  assert r>1 and A%r;c=r*pow(M,-1,A)%A;c-=A if 2*c>A else 0
  for b,(lo,hi,k,n) in enumerate(bands):
   assert 0<lo<=hi and 0<k<n;xx=(hi-r)//M
   if xx<=0:continue
   used.add((j,i,b));basis=[];power=[1]
   for l in range(n):
    e=min(l,j*k)
    if len(power)<=e:power=[c*power[0],*[c*power[t]+power[t-1] for t in range(1,len(power))],power[-1]]
    basis.append([0]*(l-e)+[v*A**(k-e//j) for v in power]+[0]*(n-l-1))
   ps=[]
   for v in ws[j,i,b]:
    z=[sum(a*b for a,b in zip(v,col)) for col in zip(*basis)];nn=0
    for coef in z[::-1]:nn=nn*xx+abs(coef)
    assert nn<lo**(j*k);ps.append(z)
   assert polygcd(*ps)
assert admitted==[2,4,5] and used==set(ws) and len(ws)==164 and 10**770>A
# Use monotonicity in u: find the first threshold for each s by binary search, then reconstruct counts.
rows={};U=579125
for s in range(1,711):
 Y=7**s;Q=2*Y-1;F=max(1,Fraction(Y*Q,max(W,Q)*(W//Y+4)));a0=-1;b0=144
 while b0-a0>1:
  mid=(a0+b0)//2
  if X*A*Q*F*7**(2*max(0,901-s-mid))<=B*U:b0=mid
  else:a0=mid
 if b0<144:rows[s]=b0
assert list(rows)==list(range(482,666)) and min(rows.values())==82 and sum(144-v for v in rows.values())==5735;print('PASS independent composite repeated-power certificate, 164 pairs; 5735 remaining sparse (s,u), elapsed',round(time.perf_counter()-s0,3))
