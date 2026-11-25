"""Independently computed refund; only claim trials guaranteed enumerated in original dual verifier."""
from functools import cache
from DualTree import I

def bind(d,a):
 cost={};income={};cap={}
 for p,f,r,n in a['flows']:
  v=n*(I.SCALE//I.FLOW_SCALE);cost[p,f]=cost.get((p,f),0)+v;income[r]=income.get(r,0)+v;cap[p]=max(cap.get(p,0),f+2)
 @cache
 def allowance(p):
  if p>=5000:return 0
  forb=(19,7,11,31,13,3);m=I.get_f_min(p,forb);upper=max([m,cap.get(p,0),64 if p<=80 else 42 if p<=300 else 0]);rebate=0
  for n in range(m,upper,2):
   if not I.sigma_has_forb(p,n,forb):
    ab=I.log_interval((p**(n+1)-1)//(p-1),p**n)[1] if p<=500 and n<=60 else I.log_interval(p,p-1)[1];j=0;val=n+1
    if p%5==1:
     while val%5==0:j+=1;val//=5
    reduced=n*I.log_interval(p)[0]+cost.get((p,n),0)-income.get(p,0)-d.mu*ab-j*d.lam_p*I.log_interval(5)[1];rebate=max(rebate,-reduced)
  return rebate
 d.refund=allowance;return d
