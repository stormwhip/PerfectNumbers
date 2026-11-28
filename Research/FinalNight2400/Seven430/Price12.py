"""Joint 7,Q cubic price, common cubic order and disjoint remaining length factors."""
from Score import *
qfactor=(3,131,431,21261314101,500153037813072397702273839525601)
@cache
def roots(p,c):
 u=next(y for g in range(2,100) for y in [pow(g,(p-1)//3,p)] if y!=1);m=p;v=[(1,(0,))]
 for i in range(c):v.append((m,(u,m-1-u)));m*=p;u=pow(u,p,m)
 return v
@cache
def joint(a,b):
 assert b<=12 and a<=430 and Q-1==2*math.prod(qfactor) and 3**8000>B
 loss={};
 def add(x,M,h):
  if x<3 or not x%2 or x**h>=M*M:return
  ok=lambda z:z>=3 and z%2 and z not in (7,19,Q) and pow(2,z-1,z)==1
  r=math.isqrt(x)
  if ok(x) or r*r==x and ok(r):loss[x]=max(loss.get(x,1),Fraction(M*M,x**h))
 for v,vv in roots(Q,b):
  inv=1
  for u,uu in roots(7,a):
   m=u*v
   for x in uu:
    for y in vv:add(x+u*((y-x)*inv%v),m,2)
   inv=inv*pow(7,-1,v)%v
 # odd order o>3; reserve 2 powers for p's cubic charge, o-3 for Q. 7-length multiplier coprime to o. Enumerate only primitive residues r<Q^b (o-3≥2).
 orders=[1];
 for s in qfactor:orders +=[k*s for k in orders]
 for o in sorted(orders):
  if o<=3 or o>=8000 or 3**(o-3)>=Q**(2*b):continue
  gen=next(g for g in range(2,400) if all(pow(g,(Q-1)//s,Q)!=1 for s in (2,*qfactor)));v=pow(gen,(Q-1)//o,Q);m=Q
  for j in range(1,b+1):
   x=1;mb=(m*m).bit_length()
   for i in range(1,o):
    x=x*v%m
    if math.gcd(i,o)==1 and x>2 and (x.bit_length()-1)*(o-3)<mb:
     assert x**(o-3)>=m*m or x%2==0,('high loss',o,x)
   m*=Q;v=pow(v,Q,m)
 L=math.prod(loss.values(),start=Fraction(1));return L,len(loss)

def ps(row,special=None):
 # p,T multiplicities for actual remaining ordinary rows / Euler-square atom. A fixed Euler has already supplied its entire output.
 s=C.State(row);c=430-sum(val(sig(x,h),7) for x,h in row);b=s.rows[Q]-sum(val(sig(x,h),Q) for x,h in row);L,n=joint(c,b)
 if special and not s.fixed_euler:
  c-=val(special+1,7);b-=val(special+1,Q)
 return s.X*(special if special and not s.fixed_euler else 1)*7**(2*max(0,c))*Q**(2*max(0,b))*L.denominator//L.numerator
@cache
def netjoint(row):
 row=list(row);s=C.State(row);a=430-sum(val(sig(x,h),7) for x,h in row);b=s.rows[Q]-sum(val(sig(x,h),Q) for x,h in row);loss={};budget=B//s.base;fixed=set(s.rows)
 def add(r,m):
  if r<=2 or not r%2 or r>=m or r*r//math.gcd(r*r,s.D)>budget:return
  def ok(z):return z>=3 and z%2 and z not in (fixed|{19}) and pow(2,z-1,z)==1
  rr=math.isqrt(r)
  if ok(r) or (not s.fixed_euler and rr*rr==r and ok(rr)):loss[r]=max(loss.get(r,1),Fraction(m*m,r*r))
 for b0,bb in roots(Q,b):
  inv=1;nexti=pow(7,-1,b0)
  for a0,aa in roots(7,a):
   m=a0*b0
   for x in aa:
    for y in bb:add(x+a0*((y-x)*inv%b0),m)
   inv=inv*nexti%b0
 return math.prod(loss.values(),start=Fraction(1)),len(loss)
if __name__=='__main__':
 t=json.loads((D/'Even430F12.json').read_bytes());z=max(t['roots']);
 for p in sorted(D.glob('Even430F12J*.json')):
  h=int(p.stem.split('J')[1]);r=root+[(Q,12),(z,h)];a=json.loads(p.read_bytes());V=set(a['roots'])|{v for v,u in a['owners']};lo=min(ps(r,v) for v in V if v%4==1);print(h,floor10(lo),len(V), 'fixed',C.State(r).fixed_euler,flush=True)
