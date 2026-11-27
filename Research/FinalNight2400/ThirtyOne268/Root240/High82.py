from Kernel import *
B72=366204586019;B4=71
SPECS={B72:(1,[83,11743,187861],70),B4:(1,[5,7],4)}
@cache
def sloss(z,c):
 a,fs,w=SPECS[z];assert z-1==2**a*prod(fs) and all(C.pc.prime64(q) for q in fs);O=[1]
 for q in fs:O+=[j*q for j in O]
 gen=next(g for g in range(2,200)if all(pow(g,(z-1)//a,z)!=1 for a in [2]+fs));loss={}
 for o in O:
  if o<=1 or o>8000 or 3**(o-1)>=z**(c*w):continue
  g=pow(gen,(z-1)//o,z);m=z
  for l in range(c):
   x=1;goal=m**w
   for j in range(1,o):
    x=x*g%m
    if x<=2 or not x%2 or gcd(j,o)!=1 or (x.bit_length()-1)*(o-1)>=goal.bit_length():continue
    if x**(o-1)<goal:loss[x]=max(loss.get(x,1),Fraction(goal,x**(o-1)))
   m*=z;g=pow(g,z,m)
 assert 3**(z-1)>=z**w if z<8000 else True
 return prod(loss.values(),start=Fraction(1))

def side(row,z):
 s=C.State(row);c=s.rows[z]-val(s.S,z);w=SPECS[z][2];U=sloss(z,c);L=-(-U.numerator//U.denominator);X=s.X;D=s.D
 if s.fixed_euler:return [] if X*z**(w*c)>B*L else [(-1,)]
 # Exact targets q+1 large force Euler external to D by applying CRT q-admissible cofactor divisions separately to each sigma.
 em=[C.sig_odd(p,h)for p,h in row];bad=[]
 for j in range(c+1):
  m=z**j;q=2*m-1;rest=z**(w*(c-j));
  if X*q*rest>B*L:continue
  if not all(outside(v,m)for v in em):bad.append(j);continue
  if X*D*q>B:continue
  # Any q external so unique ordinary emitter size >2qz^u/3; use price of the others and its own cost exactly over u.
  blocks=[C.nonsupport(v,X) for v in em];hh=1
  while blocks:
   a=blocks.pop();eq=[b for b in blocks if gcd(a,b)>1]
   if eq:
    for b in eq:blocks.remove(b);a*=b
    blocks.append(a)
   else:hh=max(hh,a)
  for u in range(c-j+1):
   y=z**u
   if 2*X*D*q*q*y>3*B*hh or X*D*q*y**w>B*hh*L or 2*X*q*q*rest>3*B*L*y**(w-1):continue
   bad.append(j);break
 return bad
if __name__=='__main__':
 r=P+[(t,82),(B72,36)];print('open',side(r,B72),flush=True)
