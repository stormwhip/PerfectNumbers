"""Exact accelerated sieve: one gcd per prime block, only recomputed for a newly fixed sigma factor; U remains rigorously T-rough."""
from functools import cache
from math import gcd,prod,isqrt
@cache
def primegroups(T):
 b=bytearray([1])*(T+1);b[:2]=b'\0\0'
 for p in range(2,isqrt(T)+1):
  if b[p]:b[p*p::p]=bytes(1+(T-p*p)//p)
 ps=[p for p in range(2,T+1) if b[p]];return [(prod(ps[i:i+48]),tuple(ps[i:i+48])) for i in range(0,len(ps),48)]
@cache
def mentioned(n,T):
 ans=[]
 for product,group in primegroups(T):
  g=gcd(n,product)
  if g>1:
   for p in group:
    if g%p==0:ans.append(p);g//=p
    if g==1:break
 return tuple(ans)
