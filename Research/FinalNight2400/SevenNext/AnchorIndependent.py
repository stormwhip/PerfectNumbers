"""Companion to Audit618.py --anchor. Exact all-s, all-u arithmetic, without binary log relaxations."""
from pathlib import Path
import sys,json
from math import gcd,prod
from functools import cache
from fractions import Fraction
from Audit618 import p,t,B,strip,geom

def outside(Z,m):
 q=2*m-1
 if Z<q:return True
 k=Z*pow(q,-1,4*m)%(4*m);return Z//q<4*m and not(0<k<=Z//q and Z%k==0)
@cache
def net(r):
 h=2;u=0;cost=[];R=r*r
 while R<=B:
  if r%p==1:j=strip(h+1,p)[1]
  else:j=strip(pow(r,h+1,p**619)-1,p)[1] if pow(r,h+1,p)==1 else 0
  u=max(u,j);cost.append(Fraction(R,p**(2*j)));R*=r*r;h+=2
 return min(cost),u

def run_anchor(Qlim,Slim,A):
 Hdir=Path(__file__).resolve().parent;sys.path.insert(0,str(Hdir.parents[1]/'RootFiveNext'));import PrimeCheck as pc
 pack=json.loads((Hdir.parent/'Nineteen/Anchor618.json').read_bytes());assert set(pack['low'])=={'18','20'}
 for mode,table in pack.items():
  for index,values in table.items():
   rest=geom(t,int(index)) if mode=='low' else geom(int(index),2)
   for label,chain in values.items():
    r=y=int(label);rest,j=strip(rest,r);assert j>0
    for row in chain:assert row[0]==y;y=pc.level(*row)
    assert pc.prime64(y)
   assert rest==1
 for sf,zs in pack['low'].items():
  f=int(sf);zs=set(map(int,zs))-{p};z=max(zs);C0,j0=strip(geom(t,f),p);T=t**(f-1);X0=p**618*t**f
  assert gcd(A,C0)==gcd(X0,A*C0)==1 and strip(C0,z)[1]==1 and outside(C0,T)
  h=0;direct=[];total=0;strong=0
  while X0*A*C0*z**(h+1)<=B:
   h+=2;X=X0*z**h;E,j=strip(geom(z,h),p);c=618-j0-j
   if E%t==0 or c<0:continue
   H=C0//z*E;D=A*H
   if X*D>B:continue
   direct.append(h);Y=zs-{z}
   if h==2:Y|=set(map(int,pack['emit'][str(z)]))-{p,t,z}
   assert all(D%r==0 for r in Y)
   safe={r for r in Y if r in zs or (r+1)%(2*T)!=0 or r%(4*T)!=2*T-1}
   F=prod(r for r in Y if strip(D,r)[1]%2);G=prod((net(r)[0] for r in Y),start=Fraction(1));G0=prod((net(r)[0] for r in safe),start=Fraction(1)); mg=max(net(r)[1] for r in Y); cop=gcd(A,H)==1;M=max(A,H) if cop else D
   assert X%G.denominator==X%G0.denominator==0;XG=X//G.denominator*G.numerator;XG0=X//G0.denominator*G0.numerator
   for s in range(c+1):
    q=2*T*p**s-1;K=X*D*q
    if XG0*q>Qlim[c-s]:continue
    assert s>0
    if X0*A*C0*q>B:continue
    assert outside(E,T*p**s)
    if K*F>B or XG*q>Qlim[c-s]:continue
    a=2*q;v=2*X*q*q;vg=2*XG*q*q
    for u in range(c-s+1):
     kr=K*(F if u>mg else 1);vv=vg if u>mg else v
     if vv<=Slim[c-s-u] and kr*a<=3*M*B:
      assert cop and u>=206 and kr*kr*a>3*B*B and kr*a>3*H*B,(f,h,s,u);strong+=1
     a*=p;v*=p;vg*=p;total+=1
  print('Anchor',f,'h',direct,'supplier allocations',total,'square required',strong,flush=True)
  assert direct==list(range(2,16 if f==18 else 12,2))
