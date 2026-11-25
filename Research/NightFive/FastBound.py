"""Rigorous additional simple obstruction: compute size of newly forced primes before expensive valuation and recursive search. Input U is known to be T-rough, and unknown primes cannot save more than the one Euler exception."""
from Tree import minf
from math import prod
from functools import cache
@cache
def pmin(z,v,eused):
 e=minf(z,v,False);o=None if eused else minf(z,v,True);normal=z**e;save=z**(e-o) if o is not None and o<e else 1;return normal,save

def size(X,U,dc,eu,B):
 full=X*U;discount=1
 for z,v in dc.items():
  a,s=pmin(z,v,eu);full*=a;discount=max(discount,s)
 return full>B*discount
