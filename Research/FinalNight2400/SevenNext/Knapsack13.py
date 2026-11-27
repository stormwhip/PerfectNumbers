"""Exact 173^13 via a deficit knapsack and conditional paid children, with Euler already fixed."""
from pathlib import Path
import sys,math
from functools import cache
from fractions import Fraction
from math import prod
H=Path(__file__).resolve().parent;sys.path.insert(0,str(H));import Odd42 as O
from Odd42 import C,B,Q,R,val
X=7**12*Q**42*R**13;parent=[3,29,43,3144079,8576317,26654680037077];fixed={7,Q,R}
child={23:[102219917850387811990824636930475340357519336809223],29:[52990215639704354810299474687300887696772792277],43:[19825223972382274003506149120708429799166030881820329892377241],83:[2336135433502794653513996041185660622750750046472050110617216725345196956032001],47:[1291,5595019993],109:[10321,1030577145377926171],14627:[38959],4428761511619:[21101059589],326542598030513:[172140869]}
@cache
def net(r,w):
 best=None;rf=r*r;h=2
 while X*rf<=B:
  sig=(rf*r-1)//(r-1);vv=val(sig,R);uu=val(sig,Q)
  if vv<=12 and uu<=41 and sig%19!=0:
   n=Fraction(rf,R**(w*vv)*Q**(2*uu));best=n if best is None else min(best,n)
  h+=2;rf*=r*r
 assert best is not None;return best

def test(w):
 from KnapsackLoss import losses
 uc=losses(Q,41,2);ur=losses(R,12,w);childset={q for ys in child.values() for q in ys};allr=set(ur)|set(parent)|set(child)
 assert len(childset)==sum(map(len,child.values())) and not allr&childset and not fixed&(allr|childset)
 UQ=prod((v for r,v in uc.items() if r not in allr),start=Fraction(1));D=[None]*13;D[0]=Fraction(1)
 for r in allr:
  # Enumerate full even exponent domain. For each valuation at 173, retain minimum exact cost relative to target prices. Optional base may be absent.
  opts={} if r in parent else {0:Fraction(1)};h=2;m=r*r
  while X*m<=B:
   sig=(r*m-1)//(r-1);j=val(sig,R);i=val(sig,Q)
   if j<=12 and i<=41 and sig%19:
    # Cost of credited children, only when forced by actual emission. Every such child lies outside all handled parent bases.
    G=prod((net(y,w) for y in child.get(r,[]) if sig%y==0),start=Fraction(1));v=Fraction(m,Q**(2*i)*R**(w*j))*G;opts[j]=min(v,opts.get(j,v))
   m*=r*r;h+=2
  dst=[None]*13
  for i,d in enumerate(D):
   if d is None:continue
   for j,v in opts.items():
    if i+j<=12:
     k=d*v;dst[i+j]=k if dst[i+j] is None else min(dst[i+j],k)
  D=dst
 # Child net includes their whole Q and R supply; do not remove their UQ losses in the fallback for paths where child is unforced.
 G=min(v for v in D if v is not None);N=X*Q**82*R**(12*w)*G/UQ
 return N
if __name__=='__main__':
 import json
 assert __debug__ and C.pc.prime64(Q) and C.pc.prime64(R) and C.sigma(7,12)==Q and R-1==4*43 and Q>5100 and (Q-1)%R!=0
 s=C.State([(7,12),(Q,42),(R,13)]);assert s.X==X and not s.conflict and s.fixed_euler and val(s.S,Q)==val(s.S,R)==1
 assert not fixed.intersection(parent) and len(parent)==len(set(parent)) and all(C.pc.prime64(r) and s.D%r==0 for r in parent)
 zset={q for ys in child.values() for q in ys};bank={rows[0][0]:rows for rows in json.loads((H/'Child13.json').read_bytes())};assert set(bank)=={q for q in zset if q>=2**64}
 for q in zset:
  y=q
  for row in bank.get(q,[]):assert y==row[0];y=C.pc.level(*row)
  assert C.pc.prime64(y)
 n=test(40);assert n>B;print('PASS 173^13: joint priced lower/B in millionths =',n.numerator*1000000//(n.denominator*B),flush=True)
