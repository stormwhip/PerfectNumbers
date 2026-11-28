"""19th-century sigma identity + two sealed lattice caps: at s=453 at least three distinct prime factors in Phi907(7)."""
from pathlib import Path
from fractions import Fraction as F
from math import isqrt
import sys
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Gain906 as Z;from RepeatedMid906 import run
run(150);X,A,B,U=Z.X,Z.A,Z.B,Z.U;W=7*X;survive=[];external=[];highE=[];distinct=[]
for s in range(1,711):
 Y=7**s;Q=2*Y-1;bal=max(1,F(Y*Q,max(W,Q)*(W//Y+4)));can=ext=he=de=False
 for high in [False,True]:
  lower,upper=(154,258) if high else (0,153);u=max(lower,min(upper,906-s-5));K=10**7*7**(u-4) if high else 1;v=max(0,906-s-5-u);B0=X*A*Q*K
  if B0*7**(2*v)>B*U:continue
  if 2*B0*Q*7**v<=3*B*U:ext=True
  if not high:
   can=True;continue
  if B0*bal*7**(2*v)<=B*U:de=True;can=True
  for uu in range(154,259):
   v=max(0,906-s-5-uu);K=max(10**7*7**(uu-4),isqrt((2*Q*7**uu+2)//3))
   if X*A*Q*K*7**(2*v)<=B*U:he=True;can=True;break
 if can:survive.append(s)
 if he:highE.append(s)
 if de:distinct.append(s)
 if ext:external.append(s)
assert not external and not highE and 453 not in survive;print('PASS <=2 A primes: necessary s range',min(survive),max(survive),'count',len(survive),'high-A-source range',min(distinct),max(distinct),'s453 impossible with ANY q-emitter')
