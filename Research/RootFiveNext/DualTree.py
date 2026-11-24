"""Removed-node indicator dual plus the forced-prime exponent/valuation backstop."""
import argparse,json,sys
from functools import cache
from math import gcd
from Tree import H,Tree,B,F,ok,proved,check,PR,SMALL
sys.path.insert(0,str(H.parent/'IndicatorCapacity'))
import VerifyIndicatorCapacity2400 as I
S=I.SCALE; LP=I.log_interval(5)[0]; LIM=10**18-1; J=5 # 5^6>1+floor(log_3 B)
assert 5**(J+1)>I.MAX_EXPONENT+1

def lnlo(n):
 k=max(0,n.bit_length()-20);return k*I.LN2_LO+I.log_interval(n>>k)[0]
@cache
def abhi(r):return (S+r-2)//(r-1) if r>1000 else I.log_interval(r,r-1)[1]

def load_duals():
 c=json.loads((I.CERT_DIR/'DualP5.json').read_text()); ps=I.sieve_primes(c['R_act']);return [I.verify_dual_entry(5,tuple(c['forbidden']),c['R_act'],c['W_max'],d,ps) for d in c['duals']]

def units(r,f):
 if r==5:return 0
 a=f+1;j=0
 while a%5==0:a//=5;j+=1
 if r%5==1:return j
 if r%5==4 and f%2:
  a=r+1
  while a%5==0:a//=5;j+=1
  return j
 return 0

@cache
def point(r,c,odd,L):
 if odd and (r%4!=1 or gcd(r+1,3*7*11*13*19*31)>1):return None
 lim=360; v=I.log_interval(r)[0] if r<10**12 else lnlo(r); u=units(r,1) if odd and r%5==4 else 0
 lo=(max(lim,c)-c)*v - L*(u+J)
 for f in range(max(1,c),lim):
  if (f%4==1 if odd else f%2==0) and ok(r,f):lo=min(lo,(f-c)*v-L*units(r,f))
 return lo

def add_test(duals):
 def extra(self,exact,prod,ss,eu,div,rough,ds):
  # exact plus forced prime blocks purged from external dual. The rough block may share with
  # no exact/known prime; any as-yet-undetected prime of rough exceeds T=2000.
  Y=ss; k=self.e
  while Y%5==0:Y//=5;k-=1
  if k<0:return True
  gone=set(exact)|set(ds); target=I.LN2_LO-sum(abhi(r) for r in gone); capacity=0;u=rough
  while u>2000:u//=2001;capacity+=1
  target-=capacity*abhi(2001); base=lnlo(prod*div)
  # Unknown A_factors: discounted root valuation free in multiplicity c, paid remainder costs >=ln(2001)
  gift=I.ilog(rough,2001**4) if rough>1 else 0
  has_euler=False; ext=False;inside=False
  for d in duals:
   L=min(d.lam_p*LP,lnlo(2001)) if rough>1 else d.lam_p*LP
   decline=0;normal=0
   for r,c in ds.items():
    ve=point(r,c,False,L);normal+=ve
    if not eu:
     vo=point(r,c,True,L)
     if vo is not None:decline=max(decline,ve-vo)
   overlap=sum(th for w,th in d.theta_map.items() if ss%w==0 or prod%w==0)
   common=base + d.mu*target + d.const_no_target-overlap + normal + L*(k-gift)
   if eu:
    if common>I.LN_B_HI:return True
    continue
   if common-decline>I.LN_B_HI:has_euler=True # Euler is known forced prime
   # Euler on unknown rough prime: for odd a either s<=J or q+1 divisible by 5^(s-J).
   # Upper v_q(rough)<=floor(log_q rough), so q^a/q^c >= max(1,q^a/rough).
   if not inside:
    if rough==1:inside=True
    else:
     # If q|rough and contributes s, then log q <= log rough and hence s<= log_5(rough+1)+J.
     h=min(k,I.ilog(rough+1,5)+J); inside=common-L*h>I.LN_B_HI
   # When Euler outside exact/forced blocks, q^a >=5^(s-1) for all s, and the
   # verified global deletion charge d.delta_q covers loss of its flow and abundance.
   if common-d.delta_q+min(0,(LP-L)*k)-LP>I.LN_B_HI:ext=True
   if has_euler and inside and ext:return True
  return False
 return extra

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--depth',type=int,default=8);ap.add_argument('--nodes',type=int,default=1000);ap.add_argument('--output',default='DualAudit.json');ap.add_argument('es',type=int,nargs='*');a=ap.parse_args();duals=load_duals(); Tree.extra=add_test(duals);c=json.loads((H/'Candidates.json').read_text());rows=[]
 for e in a.es or list(map(int,c)):
  rs=sorted({int(r) for r in c[str(e)] if proved(int(r))});A=(5**(e+1)-1)//4;check(all(A%r==0 for r in rs),'wrong factor input'); tr=Tree(e,rs,a.depth,a.nodes);closed=tr.run(); rows.append(dict(e=e,closed=closed,stats=dict(tr.st),example=tr.examples));
  if closed:print('CLOSED',e,dict(tr.st),flush=True)
 (H/a.output).write_text(json.dumps(rows,indent=1)+'\n');print('total',len(rows),'closed',sum(r['closed'] for r in rows))
if __name__=='__main__':main()
