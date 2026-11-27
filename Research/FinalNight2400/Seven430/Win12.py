from Price12 import *
from math import prod,gcd
@cache
def ext(Z,m):
 q=2*m-1
 if q>Z:return True
 k=Z*pow(q,-1,4*m)%(4*m);return Z//q<4*m and (not k or k>Z//q or Z%k)

def maxover(row,fs):
 s=C.State(row);S=[C.sig_odd(z,h) for z,h in row];blocks=[C.nonsupport(v,prod(s.rows)*prod(fs)) for v in S];b=[v for v in blocks if v>1];gs=[]
 # create single overlap upper bound; merge blocks sharing hidden primes
 while b:
  x=b.pop();shared=[v for v in b if gcd(x,v)>1]
  if shared:
   for v in shared:b.remove(v);x*=v
   b.append(x)
  else:gs.append(x)
 return max(gs,default=1)

def win(row,fac):
 s=C.State(row);a=430-sum(val(sig(z,h),7) for z,h in row);b=s.rows[Q]-sum(val(sig(z,h),Q) for z,h in row); L,k=netjoint(tuple(row));U=-(-L.numerator//L.denominator);X=s.X;D0=s.D;c=7**a*Q**b;
 if s.fixed_euler:return [] if X*c*c>B*U else [('fixed',)]
 fs={z for z in fac if z not in s.rows and s.D%z==0};H0=maxover(row,fs);em=[sig(z,h) for z,h in row];mm=[]
 for i in range(a+1):
  for j in range(b+1):
   m=7**i*Q**j;q=2*m-1;R=(c//m)**2
   if X*q*R>B*U:continue
   if not all(ext(v,m) for v in em):mm.append((i,j,'interior'));continue
   F=prod(z**(val(D0,z)%2) for z in fs);  # q external => all fs ordinary
   if X*D0*F*q>B:continue
   # Independent size and subset price: if supplier known, use its full multiplicity cost from D·F as overlap, else at most H0.
   hh=max([H0]+[z**(val(D0,z)+val(D0,z)%2) for z in fs]);
   if 4*X**2*D0*F*q**4*R>9*B**2*U*hh:continue
   mm.append((i,j,'emitter'))
 return mm
if __name__=='__main__':
 f=int(sys.argv[1]);d=json.loads((D/f'Even430F{f}.json').read_bytes());z=max(d['roots']);res={};
 for h0 in json.loads((H/f'New{f}any.json').read_bytes()):
  h=int(h0);row=root+[(Q,f),(z,h)];a=json.loads((D/f'Even430F{f}J{h}.json').read_bytes());mm=win(row,a['roots']);res[h]=mm;print(h,len(mm),mm[:4],flush=True);(H/f'Win{f}.json').write_text(json.dumps(res))
