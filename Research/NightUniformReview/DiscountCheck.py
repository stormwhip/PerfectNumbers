"""Audit the sponsor generator as a mathematical ledger, without assuming its decisions valid."""
from Replay import *
for p in (7,11,19,31):
 prof=O.profile(p);k=prof.kap;ds=O.G.discounts(p,prof);dep={(t,x):(d,ws) for t,x,d,ws in ds};used={x for t,x,o in prof.non_euler};paid=set();nskip=0
 assert len(dep)==len(ds);assert len(used)==len(prof.non_euler)
 for t,x,o in prof.non_euler:
  delta=F(p**(k*t),x**(o-1));assert delta>1
  assert o%2 and pow(x,o,p**t)==1 and pow(x,o,p**(t+1))!=1;d,ws=dep.get((t,x),(None,()))
  if d is not None:assert d==delta
  if d is None or ws:
   # f+1 = odd multiple of o. Costs once past the first multiple, even allowing LTE increment j>=1.
   assert x**(3*o-1)>=p**(k*t) and x**(o*(p-3))>=p**k
   if d is None:assert any(sig(x,o-1)%z==0 for z in O.tb.forbidden(p));nskip+=1
   for w in ws:
    assert w not in used and w not in paid and w!=p and w not in O.tb.forbidden(p);O.verify_cert(w,None);assert sig(x,o-1)%w==0
    assert price(p,k,w,1)>=delta;paid.add(w)
 print(p,'deficits',len(used),'sponsor reservations',len(paid),'forbidden suppressions',nskip)
