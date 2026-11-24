"""Exact additional forced size/abundance leaf used in wider cold replay."""
from LeafCheck import lower_pow,I
from Tree import PR
from functools import cache
from bisect import bisect_right
from math import prod
@cache
def cardinal(xs,eused):
 vals=[(1,1)];cs=[1];P=1;n=d=1
 for q in PR:
  if q in xs:continue
  P*=q;c=P*P if eused else P*P//q
  if c>10**2400:return cs,vals
  n*=q;d*=q-1;vals.append((n,d));cs.append(c)
 raise ValueError('insufficient prime support')

def leaf(X,sig,dc,u,x,eu):
 B=10**2400;T=100000;prod0=X*u;discount=1
 for p,c in dc.items():
  f=lower_pow(p,c,False);prod0*=p**f;o=None if eu else lower_pow(p,c,True)
  if o is not None and o<f:discount=max(discount,p**(f-o))
 if prod0>B*discount:return True
 n=I.ilog(u,T);num=sig*(T+1)**n*prod(dc);den=X*T**n*prod(p-1 for p in dc);xs=tuple(q for q in PR[:20] if q in dc or any(r==q for r,f in x));cs,vs=cardinal(xs,eu);a,b=vs[bisect_right(cs,B*discount//prod0)-1];return num*a<2*den*b
