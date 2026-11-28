from OnePrice import *

def outside(Z,m):
 q=2*m-1
 if q>Z:return True
 k=Z*pow(q,-1,4*m)%(4*m);return Z//q<4*m and (not k or k>Z//q or Z%k)

def square(row):
 s=state(row);blocks=[C.nonsupport(C.sig_odd(z,h),s.X) for z,h in row];D=s.D;left=[]
 for i,v in enumerate(blocks):
  w=v
  for other in blocks[:i]+blocks[i+1:]:w=C.nonsupport(w,other)
  if w==1 or isqrt(w)**2==w:continue
  b=next((k for k in range(3,1001,2) if w%k==0),1001);left.append(b)
 left.sort();return s.base*prod(left if s.fixed_euler else left[:-1])>B

def sevenwin(row,fs):
 s=state(row);X=s.X;D=s.D;a=882-C.valuation(s.S,7);L=loss();U=-(-L.numerator//L.denominator);fs=[z for z in fs if z not in s.rows and D%z==0];F=prod(z**(C.valuation(D,z)%2) for z in fs);em=[C.sig_odd(z,h) for z,h in row];blocks=[C.nonsupport(v,s.X*prod(fs)) for v in em];blocks=[b for b in blocks if b>1];Hh=[z**(C.valuation(D,z)+C.valuation(D,z)%2) for z in fs];
 while blocks:
  v=blocks.pop();other=[b for b in blocks if gcd(b,v)>1];
  if other:
   for b in other:blocks.remove(b);v*=b
   blocks.append(v)
  else:Hh.append(v)
 H0=max(Hh,default=1);miss=[]
 if s.fixed_euler:return [] if priced(row)>B else [('fixed',)]
 for i in range(a+1):
  m=7**i;q=2*m-1;R=7**(2*(a-i));
  if X*q*R>B*U:continue
  # for i>0 root sigma 7^883-1 precludes q=−1 mod7 via reciprocity.
  if not all((n==0 and i>0) or outside(v,m) for n,v in enumerate(em)):miss.append((i,'int'));continue
  if X*D*F*q>B or 4*X**2*D*F*q**4*R>9*B**2*U*H0:continue
  miss.append((i,'em'))
 return miss

def classify(row,t):
 if square(row):return 'square'
 if state(row).fixed_euler and priced(row)>B:return 'price'
 if not sevenwin(row,t.get('roots',[])):return 'win'
 return 'open'
if __name__=='__main__':
 from Holes import count
 for f in map(int,sys.argv[1:]):
  for row,t in count(f):
   tag=classify(row,t);print(f,[h for q,h in row],tag,sevenwin(row,t.get('roots',[]))[:3] if tag=='open' else '')
